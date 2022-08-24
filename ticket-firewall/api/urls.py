from netbox.api.routers import NetBoxRouter
from . import views

#tickets - name of plugin
app_name = 'ticket_firewall'

router = NetBoxRouter()
router.register('ticket-list', views.TicketListViewSet)
router.register('rules', views.RuleViewSet)

urlpatterns = router.urls