from random import choices
from rest_framework import serializers
from netbox.api.serializers import NetBoxModelSerializer
from ..models import Ticket, Rule,AttachFile, Protocol, PrefixRule
from netbox.api.serializers import WritableNestedSerializer

class NestedTicketSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:ticket_firewall-api:ticket-detail'
    )
    class Meta:
        model = Ticket
        fields = ('id', 'url', 'display', 'ticket_id', 'ticket_name')

class TicketSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:ticket_firewall-api:ticket-detail'
    )
    rule_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Ticket
        fields = (
            'id', 'display', 'ticket_id', 'ticket_name',  'status', 'id_directum', 'tags', 'custom_fields', 'created',
            'last_updated', 'url', 'rule_count', 'description'
        )

class AttachFileSerializer(NetBoxModelSerializer):
    ticket_id = NestedTicketSerializer()
    class Meta:
        model = AttachFile
        fields = (
            'ticket_id', 'file'
        )

class ProtocolSerializer(NetBoxModelSerializer):
    class Meta:
        model = Protocol
        fields = [
            'name'
        ]
class PrefixRuleSerializer(NetBoxModelSerializer):
    class Meta:
        model = PrefixRule
        fields = [
            'prefix'
        ]

class RuleSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:ticket_firewall-api:rule-detail'
    )
    ticket_id = NestedTicketSerializer()
    protocol = ProtocolSerializer(many=True, read_only=True)
    class Meta:
        model = Rule 
        fields = (
            'id', 'url', 'display', 'ticket_id', 'index', 'protocol', 'source_prefix', 'source_ports',
            'destination_prefix', 'destination_ports', 'action', 'tags', 'custom_fields', 'created',
            'last_updated', 'opened', 'closed'
        )