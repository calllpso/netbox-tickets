from netbox.filtersets import NetBoxModelFilterSet
from .models import AccessListRule, TicketList


from utilities.filters import MultiValueCharFilter

class AccessListRuleFilterSet(NetBoxModelFilterSet):
    source_prefix = MultiValueCharFilter()
    destination_prefix = MultiValueCharFilter()

    class Meta:
        model = AccessListRule
        fields = ('id','ticket_list','ticket_id','index',
            'protocol','action','description',
            'opened','closed', 'source_prefix','destination_prefix'
        ) 


class TicketListFilterSet(NetBoxModelFilterSet):
    id_directum = MultiValueCharFilter()
    class Meta:
        model = TicketList

        fields = ('id','name','status','id_directum',
            'description'
        ) 


    
