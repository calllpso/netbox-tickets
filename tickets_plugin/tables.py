import django_tables2 as tables

from netbox.tables import NetBoxTable, ChoiceFieldColumn
from .models import TicketList, Rule
from django.utils.safestring import mark_safe

# pk and actions columns render the checkbox selectors and dropdown menus
class TicketListTable(NetBoxTable):
    ticket_id = tables.Column(
        linkify=True
    )
    status = ChoiceFieldColumn()
    rule_count = tables.Column()

    class Meta(NetBoxTable.Meta):
        model = TicketList
        fields = ('pk', 'id', 'ticket_id', 'rule_count', 'status', 'id_directum', 'actions', 'description', 'comments')
        default_columns = ('ticket_id', 'rule_count', 'status', 'description')
        ticket_id = tables.Column(
            linkify=True
        )
        status = ChoiceFieldColumn()

        


class ChoiceFieldArrayColumn(tables.Column):
    # def render(self, record, bound_column, value):
    def render(self, value):
        mark_str = ''
        colors = {'ip':'green',
            'tcp': 'blue',
            'udp': 'orange',
            'icmp': 'purple'}
        for i in value:
            mark_str = mark_str + f'<span class="badge bg-{colors[i]}">{i}</span>'
        return mark_safe(mark_str)

    def value(self, value):
        return value



class RuleTable(NetBoxTable):
    ticket_id = tables.Column(
        linkify=True
    )
    index = tables.Column(
        linkify=True
    )
    protocol = ChoiceFieldArrayColumn()
    
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
