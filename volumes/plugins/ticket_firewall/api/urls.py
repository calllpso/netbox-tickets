from netbox.api.routers import NetBoxRouter
from . import views

app_name = 'ticket_firewall'

router = NetBoxRouter()
router.register('tickets', views.TicketViewSet)   #tickets задано в url.py
router.register('rules', views.RuleViewSet)
# router.register('protocols', views.RuleViewSet)

urlpatterns = router.urls