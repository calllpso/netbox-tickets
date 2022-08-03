import django_tables2 as tables

from netbox.tables import NetBoxTable, ChoiceFieldColumn
from .models import TicketList, AccessListRule

# pk and actions columns render the checkbox selectors and dropdown menus
class TicketListTable(NetBoxTable):

    class Meta(NetBoxTable.Meta):
        model = TicketList
        fields = ('pk', 'id', 'name', 'rule_count', 'status', 'id_directum', 'actions')
        default_columns = ('name', 'rule_count', 'status')
        name = tables.Column(
            linkify=True
        )
        status = ChoiceFieldColumn()


class AccessListRuleTable(NetBoxTable):
    ticket_list = tables.Column(
        linkify=True
    )
    ticket_id = tables.Column()
    index = tables.Column(
        linkify=True
    )
    protocol = ChoiceFieldColumn()
    action = ChoiceFieldColumn()

    class Meta(NetBoxTable.Meta):
        model = AccessListRule
        fields = (
            'pk', 'id', 'ticket_list', 'ticket_id', 'index', 'source_prefix', 'source_ports', 'destination_prefix',
            'destination_ports', 'protocol', 'action', 'description', 'opened', 'closed', 'actions',
        )
        default_columns = (
            'ticket_list', 'ticket_id', 'index', 'source_prefix', 'source_ports', 'destination_prefix',
            'destination_ports', 'protocol', 'action', 'opened', 'closed', 'actions',
        )