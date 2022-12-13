from pyexpat import model
from utilities.choices import ChoiceSet
from django.contrib.postgres.fields import ArrayField
from django.db import models
from netbox.models import NetBoxModel
from django.urls import reverse
from ipam.fields import IPAddressField
from django import forms
from django.core.files.storage import FileSystemStorage
from django.dispatch import receiver
import os

class ChoiceArrayField(ArrayField):
    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.MultipleChoiceField,
            'choices': self.base_field.choices,
        }
        defaults.update(kwargs)
        return super(ArrayField, self).formfield(**defaults)


class Ticket_status(ChoiceSet):
    key = 'Ticket.status'
    active = 'active'
    inactive = 'inactive'
    staged = 'staged'
    CHOICES = [
        (active, 'active', 'green'),
        (inactive, 'inactive', 'red'),
        (staged, 'Staged', 'orange'),
    ]

class Rule_Action(ChoiceSet):
    key = 'Rule.action'
    CHOICES = [
        ('', '----', 'white'),
        ('permit', 'permit', 'green'),
        ('drop', 'drop', 'red'),
    ]

class Protocol_colors(ChoiceSet):
    key = 'Protocol.name'
    ip = 'ip'
    tcp = 'tcp'
    icmp = 'icmp'
    CHOICES = [
        (ip, 'ip', 'green'),
        (tcp, 'tcp', 'red'),
        (icmp, 'icmp', 'orange'),
    ]

class Ticket(NetBoxModel):
    ticket_id = models.PositiveIntegerField(
        unique=True
    )

    ticket_name = models.CharField(
        max_length=100,
        unique=True,
        blank=True
    )

    status = models.CharField(
        max_length=30,
        choices=Ticket_status,
        default=Ticket_status.inactive
    )
    id_directum = models.CharField(
        max_length=100,
        blank=True
    )
    description = models.CharField(
        max_length=500,
        blank=True
    )
    comments = models.TextField(
        blank=True
    )

    clone_fields = (
        'ticket_id', 'ticket_name', 'status', 'id_directum', 'description', 'comments'
    )

    class Meta:
        ordering = ('ticket_id',)
    # возвращает для RuleTable
    def __str__(self):
        return str(self.ticket_id)
    def get_status_color(self):
        return Ticket_status.colors.get(self.status)
    def get_absolute_url(self):
        return reverse('plugins:ticket_firewall:ticket', args=[self.pk])


fs = FileSystemStorage(location='./media/ticket_attachments')
class AttachFile(NetBoxModel):
    ticket_id = models.ForeignKey(
        to=Ticket,
        on_delete= models.CASCADE,
        related_name='file'
    )
    file = models.FileField(storage=fs)
    def __str__(self):
        return f'{self.ticket_id.id}: {self.file.name}'
    def get_absolute_url(self):
        return reverse('plugins:ticket_firewall:ticket', args=[self.ticket_id.id])

    @property
    def size(self):
        """
        Wrapper around `image.size` to suppress an OSError in case the file is inaccessible. Also opportunistically
        catch other exceptions that we know other storage back-ends to throw.
        """
        expected_exceptions = [OSError]
        try:
            from botocore.exceptions import ClientError
            expected_exceptions.append(ClientError)
        except ImportError:
            pass
        try:
            return self.file.size
        except tuple(expected_exceptions):
            return None



class Protocol(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('plugins:ticket_firewall:protocol', args=[self.pk])
    def get_status_color(self):
        return Protocol_colors.colors.get(self.status)



class Rule(NetBoxModel):
    ticket_id = models.ForeignKey(
        to=Ticket,
        on_delete=models.CASCADE,
        related_name='rules'
        # doesn't work: help_text='select corresponding ticket'
    )

    index = models.PositiveIntegerField(unique=True) #!! not blank=True

    source_prefix = IPAddressField(
        help_text='IPv4 or IPv6 address (with mask)',
        blank=True, null=True, default=None
    )

    source_ports = ArrayField(
        help_text='Left field blank for ANY ports',
        base_field=models.CharField(max_length=50),
        blank=True
    )
    destination_prefix = IPAddressField(
        help_text='IPv4 or IPv6 address (with mask)',
        blank=True, null=True, default=None
    )
    destination_ports = ArrayField(
        help_text='[port], [port1,port2], [any], [port1-port100]',
        base_field=models.CharField(max_length=50),
        blank=True
    )

    protocol = models.ManyToManyField(Protocol, blank=True, related_name="+")

    action = models.CharField(
        max_length=30,
        choices=Rule_Action,
        blank=True,
        default='permit'
    )

    description = models.CharField(
        max_length=500,
        blank=True
    )

    opened = models.DateField(
        blank=True,
        null=True,
        verbose_name='Opening date'
    )

    closed = models.DateField(
        blank=True,
        null=True,
        verbose_name='Closing date'
    )

    clone_fields = (
        'ticket_id', 'source_ports', 'destination_ports', 'protocol', 'action', 'description', 'opened', 'closed','source_prefix', 'destination_prefix'
    )

    class Meta:
        ordering = ('ticket_id', 'index')
        unique_together = ('ticket_id', 'index')

    def __str__(self):
        return f'Ticket {self.ticket_id}: Rule {self.index}'

    def get_action_color(self):
        return Rule_Action.colors.get(self.action)

    def get_absolute_url(self):
        return reverse('plugins:ticket_firewall:rule', args=[self.pk])

    def __unicode__(self): #?
        return self






# эти ресиверы мутят удаление файла из файловой системы. Без них будет удаляться запись только из Базы Данных
# их не объединить потому что разные сигналы post_delete и pre_save
@receiver(models.signals.post_delete, sender=AttachFile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
            reverse('plugins:ticket_firewall:ticket', args=[instance.pk])


@receiver(models.signals.pre_save, sender=AttachFile)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).file
    except sender.DoesNotExist:
        return False

    new_file = instance.file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
