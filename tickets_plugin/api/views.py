from netbox.api.viewsets import NetBoxModelViewSet

from .. import filtersets, models
from .serializers import TicketListSerializer, AccessListRuleSerializer

from django.db.models import Count

class TicketListViewSet(NetBoxModelViewSet):
    queryset = models.TicketList.objects.prefetch_related('tags').annotate(
        rule_count=Count('rules')
    )
    serializer_class = TicketListSerializer

class AccessListRuleViewSet(NetBoxModelViewSet):
    queryset = models.AccessListRule.objects.prefetch_related(
        'ticket_list', 'tags'
    )
    #  'source_prefix', 'destination_prefix',
    serializer_class = AccessListRuleSerializer
    filterset_class = filtersets.AccessListRuleFilterSet