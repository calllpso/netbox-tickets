from netbox.filtersets import NetBoxModelFilterSet
from .models import Rule, TicketList


from utilities.filters import MultiValueCharFilter #,MultipleChoiceFilter

class RuleFilterSet(NetBoxModelFilterSet):
    source_prefix = MultiValueCharFilter()
    destination_prefix = MultiValueCharFilter()

    # protocol = MultiValueCharFilter()

    class Meta:
        model = Rule
        fields = ('id','ticket_id','index',
            'protocol','action','description',
            'opened','closed', 'source_prefix','destination_prefix'
        ) 


class TicketListFilterSet(NetBoxModelFilterSet):
    id_directum = MultiValueCharFilter() 
    class Meta:
        model = TicketList

        fields = ('id','ticket_id','status','id_directum',
            'description'
        ) 

