from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer
from ..models import TicketList, Rule


from netbox.api.serializers import WritableNestedSerializer


class NestedTicketListSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:tickets_plugin-api:ticketlist-detail'
    )



    class Meta:
        model = TicketList
        fields = ('id', 'url', 'display', 'ticket_id')
        # fields = ('id', 'url', 'display', 'name')

class NestedRuleSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:tickets_plugin-api:rule-detail'
    )

    class Meta:
        model = Rule
        fields = ('id', 'url', 'display', 'index')







class TicketListSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:tickets_plugin-api:ticketlist-detail'
    )
    rule_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = TicketList
        fields = (
            'id', 'display', 'ticket_id', 'status', 'id_directum', 'tags', 'custom_fields', 'created',
            'last_updated', 'url', 'rule_count', 'description'
        )
   

class RuleSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:tickets_plugin-api:rule-detail'
    )
    ticket_id = NestedTicketListSerializer()


    class Meta:
        model = Rule
        fields = (
            'id', 'url', 'display', 'ticket_id', 'index', 'protocol', 'source_prefix', 'source_ports',
            'destination_prefix', 'destination_ports', 'action', 'tags', 'custom_fields', 'created',
            'last_updated', 'opened', 'closed'
        )
        