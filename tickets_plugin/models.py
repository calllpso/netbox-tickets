from utilities.choices import ChoiceSet
from django.contrib.postgres.fields import ArrayField
from django.db import models
from netbox.models import NetBoxModel
from django.urls import reverse

from ipam.fields import IPAddressField

from dcim.models import Device


from django import forms

class ChoiceArrayField(ArrayField):

    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.MultipleChoiceField,
            'choices': self.base_field.choices,
        }
        defaults.update(kwargs)
        return super(ArrayField, self).formfield(**defaults)


class TicketList_status(ChoiceSet):
    key = 'TicketList.status'
    active = 'active'
    inactive = 'inactive'
    staged = 'staged'
    CHOICES = [
        (active, 'Active', 'green'),
        (inactive, 'Inactive', 'red'),
        (staged, 'Staged', 'orange'),
    ]

class Rule_Action(ChoiceSet):
    key = 'Rule.action'
    CHOICES = [
        ('permit', 'Permit', 'green'),
        ('drop', 'Drop', 'red'),
    ]

class Rule_Protocol(ChoiceSet):  #это должно остаться и для массива выбора
    key = 'Rule.protocol'
    CHOICES = [
        ('ip', 'IP', 'green'),
        ('tcp', 'TCP', 'blue'),
        ('udp', 'UDP', 'orange'),
        ('icmp', 'ICMP', 'purple'),
    ]

class TicketList(NetBoxModel):
    ticket_id = models.CharField(
        max_length=100
    )
    status = models.CharField(
        max_length=30,
        choices=TicketList_status,
        default=TicketList_status.inactive
        # blank=True
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

    class Meta:
        ordering = ('ticket_id',)

    def __str__(self):
        return self.ticket_id
    
    def get_status_color(self):
        return TicketList_status.colors.get(self.status)
    
    def get_absolute_url(self):
        return reverse('plugins:tickets_plugin:ticketlist', args=[self.pk])

class Rule(NetBoxModel):

    ticket_id = models.ForeignKey(
        to=TicketList,
        on_delete=models.CASCADE,
        related_name='rules'
    )
    # blank=True,
    device = models.ForeignKey(to="dcim.Device", on_delete=models.PROTECT)

    index = models.PositiveIntegerField()
    
    source_prefix = IPAddressField(
        help_text='IPv4 or IPv6 address (with mask)',
        blank=True, null=True, default=None
    )
    source_ports = ArrayField(
        base_field=models.CharField(max_length=50),
        blank=True
    )
    destination_prefix = IPAddressField(
        help_text='IPv4 or IPv6 address (with mask)',
        blank=True, null=True, default=None
    )
    destination_ports = ArrayField(
        base_field=models.CharField(max_length=50),
        blank=True
    )

    protocol = ChoiceArrayField(models.CharField(max_length=4, choices=Rule_Protocol, blank=True))


    action = models.CharField(
        max_length=30,
        choices=Rule_Action,
        blank=True
    )

    description = models.CharField(
        max_length=500,
        blank=True
    )

    opened = models.CharField(
        max_length=30,
        blank=True
    )
    closed = models.CharField(
        max_length=30,
        blank=True
    )

    class Meta:
        ordering = ('ticket_id', 'index')
        unique_together = ('ticket_id', 'index')

    def __str__(self):
        return f'{self.ticket_id}: Rule {self.index}'

    # def get_protocol_color(self):
    #     return Rule_Protocol.colors.get(self.protocol)

    def get_action_color(self):
        return Rule_Action.colors.get(self.action)

    def get_absolute_url(self):
        return reverse('plugins:tickets_plugin:rule', args=[self.pk])