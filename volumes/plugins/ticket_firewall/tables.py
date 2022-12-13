import django_tables2 as tables

from netbox.tables import NetBoxTable, ChoiceFieldColumn
from .models import Ticket, Rule, Protocol
from django.utils.safestring import mark_safe

# pk and actions columns render the checkbox selectors and dropdown menus
class TicketTable(NetBoxTable):
    ticket_id = tables.Column(
        linkify=True
    )
    status = ChoiceFieldColumn()
    rule_count = tables.Column()

    class Meta(NetBoxTable.Meta):
        model = Ticket
        fields = ('pk', 'id', 'ticket_id', 'ticket_name', 'rule_count', 'status', 'id_directum', 'actions', 'description', 'comments')
        default_columns = ('ticket_id', 'ticket_name', 'id_directum', 'rule_count', 'status', 'description')
        ticket_id = tables.Column(
            linkify=True
        )
        status = ChoiceFieldColumn()


class RuleTable(NetBoxTable):
    ticket_id = tables.Column(
        linkify=True
    )

    index = tables.Column(
        linkify=True
    )

    ### цвет
    action = ChoiceFieldColumn()

    class Meta(NetBoxTable.Meta):
        model = Rule
        fields = (
            'pk', 'id', 'ticket_id', 'index', 'source_prefix', 'source_ports', 'destination_prefix',
            'destination_ports', 'protocol', 'action', 'description', 'opened', 'closed', 'actions', 
        )
        default_columns = (
            'ticket_id', 'index', 'source_prefix', 'source_ports', 'destination_prefix',
            'destination_ports', 'protocol', 'action', 'opened', 'closed', 'actions',
        )