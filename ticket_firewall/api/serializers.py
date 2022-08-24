from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer
from ..models import Ticket, Rule


from netbox.api.serializers import WritableNestedSerializer


class NestedTicketSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:ticket_firewall-api:ticket-detail'
        # view_name='plugins-api:ticket_firewall-api:ticketlist-detail'
    )
    class Meta:
        model = Ticket
        fields = ('id', 'url', 'display', 'ticket_id')

class NestedRuleSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:ticket_firewall-api:rule-detail'
    )

    class Meta:
        model = Rule
        fields = ('id', 'url', 'display', 'index')







class TicketSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:ticket_firewall-api:ticket-detail'
    )
    rule_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Ticket
        fields = (
            'id', 'display', 'ticket_id', 'status', 'id_directum', 'tags', 'custom_fields', 'created',
            'last_updated', 'url', 'rule_count', 'description'
        )
   

class RuleSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:ticket_firewall-api:rule-detail'
    )
    ticket_id = NestedTicketSerializer()

    # device = NestedTicketSerializer()

    class Meta:
        model = Rule
        fields = (
            'id', 'url', 'display', 'device', 'ticket_id', 'index', 'protocol', 'source_prefix', 'source_ports',
            'destination_prefix', 'destination_ports', 'action', 'tags', 'custom_fields', 'created',
            'last_updated', 'opened', 'closed'
        )
        