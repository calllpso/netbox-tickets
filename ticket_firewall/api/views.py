from netbox.api.viewsets import NetBoxModelViewSet

from .. import filtersets, models
from .serializers import TicketSerializer, RuleSerializer

# from django.db.models import Count

class TicketViewSet(NetBoxModelViewSet):
    queryset = models.Ticket.objects.all()
    # queryset = models.Ticket.objects.prefetch_related('tags').annotate(
    #     rule_count=Count('rules')
    # )
    serializer_class = TicketSerializer
    filterset_class = filtersets.TicketFilterSet
    

class RuleViewSet(NetBoxModelViewSet):
    queryset = models.Rule.objects.all()
    serializer_class = RuleSerializer
    filterset_class = filtersets.RuleFilterSet
