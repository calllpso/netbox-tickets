from utilities.choices import ChoiceSet
from django.contrib.postgres.fields import ArrayField
from django.db import models
from netbox.models import NetBoxModel
from django.urls import reverse

class TicketList_Action(ChoiceSet):
    key = 'TicketList.status'
    CHOICES = [
        ('active', 'Active', 'green'),
        ('inactive', 'Inactive', 'red'),
        ('staged', 'Staged', 'orange'),
    ]

class AccessListRule_Action(ChoiceSet):
    key = 'AccessListRule.action'
    CHOICES = [
        ('permit', 'Permit', 'green'),
        ('drop', 'Drop', 'red'),
    ]

class AccessListRule_Protocol(ChoiceSet):
    CHOICES = [
        ('ip', 'IP', 'green'),
        ('tcp', 'TCP', 'blue'),
        ('udp', 'UDP', 'orange'),
        ('icmp', 'ICMP', 'purple'),
    ]

class TicketList(NetBoxModel):
    name = models.CharField(
        max_length=100
    )
    status = models.CharField(
        max_length=30,
        choices=TicketList_Action
    )
    id_directum = models.CharField(
        max_length=100
    )
    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
    
    def get_default_action_color(self):
        return TicketList_Action.colors.get(self.status)
    
    def get_absolute_url(self):
        return reverse('plugins:tickets_plugin:ticketlist', args=[self.pk])

class AccessListRule(NetBoxModel):
    ticket_list = models.ForeignKey(
        to=TicketList,
        on_delete=models.CASCADE,
        related_name='rules'
    )
    ticket_id = models.CharField(
        max_length=30,
    )
    index = models.PositiveIntegerField()
    
    source_prefix = models.CharField(
        max_length=30,
    )
    source_ports = ArrayField(
        base_field=models.PositiveIntegerField(),
    )
    destination_prefix = models.CharField(
        max_length=30,
    )
    destination_ports = ArrayField(
        base_field=models.PositiveIntegerField(),
    )
    protocol = models.CharField(
        max_length=30,
        choices=AccessListRule_Protocol,
        blank=True
    )
    action = models.CharField(
        max_length=30,
        choices=AccessListRule_Action
    )

    description = models.CharField(
        max_length=500,
        blank=True
    )

    opened = models.CharField(
        max_length=30
    )
    closed = models.CharField(
        max_length=30
    )

    class Meta:
        ordering = ('ticket_list', 'index')
        unique_together = ('ticket_list', 'index')

    def __str__(self):
        return f'{self.ticket_list}: Rule {self.index}'

    def get_protocol_color(self):
        return AccessListRule_Protocol.colors.get(self.protocol)

    def get_action_color(self):
        return AccessListRule_Action.colors.get(self.action)

    def get_absolute_url(self):
        return reverse('plugins:tickets_plugin:accesslistrule', args=[self.pk])