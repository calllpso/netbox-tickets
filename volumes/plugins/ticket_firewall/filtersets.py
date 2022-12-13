from netbox.filtersets import NetBoxModelFilterSet
from .models import Rule, Ticket, Protocol

from django.db.models import Q


from utilities.filters import MultiValueCharFilter,MultiValueNumberFilter

class RuleFilterSet(NetBoxModelFilterSet):
    source_prefix = MultiValueCharFilter()
    destination_prefix =  MultiValueCharFilter()

    index = MultiValueNumberFilter()

    class Meta:
        model = Rule
        fields = ('ticket_id', 'protocol', 'index', 'source_prefix', 'destination_prefix','closed', 'action', 'opened',
        )
    def search(self, queryset, name, value):
        # если добавить Q(tags=value), то будет ошибка. это только для тегов. qs без contains работает 
        qs_filter = Q(ticket_id__ticket_id__contains=value) | Q(index__contains=value) | Q(action__contains=value) | Q(opened__icontains=value) | Q(closed__contains=value) | Q(source_prefix__contains=value) | Q(destination_prefix__contains=value)
        return queryset.filter(qs_filter) 



class TicketFilterSet(NetBoxModelFilterSet):
    status =  MultiValueCharFilter()    #для фильтра (не для quick search)
    class Meta:
        model = Ticket
        fields = ('ticket_id','id_directum', 'status')
    def search(self, queryset, name, value):
        qs_filter = Q(ticket_id__contains=value) | Q(id_directum__contains=value) | Q(status__contains=value)
        return queryset.filter(qs_filter)

