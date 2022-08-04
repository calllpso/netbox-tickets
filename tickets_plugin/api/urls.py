from netbox.api.routers import NetBoxRouter
from . import views

app_name = 'tickets_plugin'

router = NetBoxRouter()
router.register('ticket-list', views.TicketListViewSet)
router.register('rules', views.AccessListRuleViewSet)

urlpatterns = router.urls