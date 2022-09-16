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


class Ticket_status(ChoiceSet):
    key = 'Ticket.status'
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
        ('', '----', 'white'),
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


# from netbox.models.features import WebhooksMixin
# from netbox.models import ChangeLoggedModel
# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType
# from utilities.querysets import RestrictedQuerySet


# class FileAttachment(WebhooksMixin, ChangeLoggedModel):
#     """
#     An uploaded image which is associated with an object.
#     """
#     content_type = models.ForeignKey(
#         to=ContentType,
#         on_delete=models.CASCADE
#     )
#     object_id = models.PositiveBigIntegerField()
#     parent = GenericForeignKey(
#         ct_field='content_type',
#         fk_field='object_id'
#     )
#     file = models.FileField(
#         upload_to=file_upload,
#     )
#     name = models.CharField(
#         max_length=50,
#         blank=True
#     )


#     def __str__(self):
#         if self.name:
#             return self.name
#         filename = self.file.name.rsplit('/', 1)[-1]
#         return filename.split('_', 2)[2]

#     @property
#     def size(self):
#         """
#         Wrapper around `image.size` to suppress an OSError in case the file is inaccessible. Also opportunistically
#         catch other exceptions that we know other storage back-ends to throw.
#         """
#         expected_exceptions = [OSError]

#         try:
#             from botocore.exceptions import ClientError
#             expected_exceptions.append(ClientError)
#         except ImportError:
#             pass

#         try:
#             return self.file.size
#         except tuple(expected_exceptions):
#             return None





class Ticket(NetBoxModel):
    ticket_id = models.CharField(
        max_length=100,
        unique=True
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

    class Meta:
        ordering = ('ticket_id',)

    def __str__(self):
        return self.ticket_id
    
    def get_status_color(self):
        return Ticket_status.colors.get(self.status)
    
    def get_absolute_url(self):
        return reverse('plugins:ticket_firewall:ticket', args=[self.pk])


from django.core.files.storage import FileSystemStorage
fs = FileSystemStorage(location='./static')

class AttachFile(NetBoxModel):
    ticket_id = models.ForeignKey(
        to=Ticket,
        on_delete=models.CASCADE,
        related_name='file'
    )
    file = models.FileField(storage=fs) 
    # class Meta:
    #     ordering = ('ticket_id',)
    #     unique_together = ('ticket_id',)




class Rule(NetBoxModel):
    ticket_id = models.ForeignKey(
        to=Ticket,
        on_delete=models.CASCADE,
        related_name='rules'
        # doesn't work: help_text='select corresponding ticket'
    )
    device = models.ForeignKey(to="dcim.Device", on_delete=models.SET_NULL, null=True, blank=True)

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

    class Meta:
        ordering = ('ticket_id', 'index')
        unique_together = ('ticket_id', 'index')

       

    def __str__(self):
        return f'{self.ticket_id}: Rule {self.index}'

    def get_action_color(self):
        return Rule_Action.colors.get(self.action)

    def get_absolute_url(self):
        return reverse('plugins:ticket_firewall:rule', args=[self.pk])