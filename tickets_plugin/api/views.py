from netbox.api.viewsets import NetBoxModelViewSet

from .. import filtersets, models
from .serializers import TicketListSerializer, RuleSerializer

from django.db.models import Count

class TicketListViewSet(NetBoxModelViewSet):
    queryset = models.TicketList.objects.prefetch_related('tags').annotate(
        rule_count=Count('rules')
    )
    serializer_class = TicketListSerializer

class RuleViewSet(NetBoxModelViewSet):
    queryset = models.Rule.objects.prefetch_related(
        'ticket_id', 'tags'
    )
    serializer_class = RuleSerializer
    filterset_class = filtersets.RuleFilterSet