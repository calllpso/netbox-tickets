from netbox.api.viewsets import NetBoxModelViewSet

from .. import filtersets, models
from .serializers import TicketListSerializer, RuleSerializer

from django.db.models import Count

class TicketListViewSet(NetBoxModelViewSet):
    # queryset = models.TicketList.objects.all()
    queryset = models.TicketList.objects.prefetch_related('tags').annotate(
        rule_count=Count('rules')
    )
    serializer_class = TicketListSerializer
    filterset_class = filtersets.TicketListFilterSet
    

class RuleViewSet(NetBoxModelViewSet):
    # queryset = models.Rule.objects.prefetch_related(
    #     'ticket_id', 'tags'
    # )
    queryset = models.Rule.objects.all()
    serializer_class = RuleSerializer
    filterset_class = filtersets.RuleFilterSet