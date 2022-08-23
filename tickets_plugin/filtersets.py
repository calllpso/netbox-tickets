from netbox.filtersets import NetBoxModelFilterSet
from .models import Rule, TicketList

from django.db.models import Q

# from django_filters import CharFilter

from utilities.filters import MultiValueCharFilter,MultiValueNumberFilter

class RuleFilterSet(NetBoxModelFilterSet):

    """
    не фильтрует Ticket id
    """


    source_prefix = MultiValueCharFilter()
    destination_prefix =  MultiValueCharFilter()

    device = MultiValueCharFilter()
    index = MultiValueNumberFilter()

    class Meta:
        model = Rule
        fields = ('ticket_id', 'device', 'index', 'source_prefix', 'destination_prefix','closed', 'action', 'opened',
        ) 

    def search(self, queryset, name, value):
        qs_filter = Q(tags=value) | Q(ticket_id__ticket_id__contains=value) | Q(action__contains=value) | \
            Q(source_prefix__contains=value) | Q(destination_prefix__contains=value) | Q(index__contains=value) | Q(opened__icontains=value) | Q(closed__contains=value)
        return queryset.filter(qs_filter)



class TicketListFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = TicketList
        fields = ('ticket_id','id_directum')
    def search(self, queryset, name, value):
        qs_filter = Q(ticket_id__contains=value) | Q(id_directum__contains=value)
        return queryset.filter(qs_filter)









"""
 Choices are: action, custom_field_data, description, destination_ports,  
 id, index, opened, protocol, source_ports, tagged_items, tags, ticket_id, ticket_id_id

"""