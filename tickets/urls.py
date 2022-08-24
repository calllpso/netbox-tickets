from django.urls import path
from . import models, views
from netbox.views.generic import ObjectChangeLogView,ObjectJournalView

urlpatterns = (
    # Ticket lists
    path('ticket-list/', views.TicketListListView.as_view(), name='ticketlist_list'),
    path('ticket-list/add/', views.TicketListEditView.as_view(), name='ticketlist_add'),
    path('ticket-list/<int:pk>/', views.TicketListView.as_view(), name='ticketlist'),
    path('ticket-list/<int:pk>/edit/', views.TicketListEditView.as_view(), name='ticketlist_edit'),
    path('ticket-list/<int:pk>/delete/', views.TicketListDeleteView.as_view(), name='ticketlist_delete'),
    path('ticket-list/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='ticketlist_changelog', kwargs={
        'model': models.TicketList
    }),

    #для журнала необходимо добавить WritableNestedSerializer  
    path('ticket-list/<int:pk>/journal/', ObjectJournalView.as_view(), name='ticketlist_journal', kwargs={'model': models.TicketList}),

    # Access list rules
    path('rules/', views.RuleListView.as_view(), name='rule_list'),
    path('rules/add/', views.RuleEditView.as_view(), name='rule_add'),
    path('rules/<int:pk>/', views.RuleView.as_view(), name='rule'),
    path('rules/<int:pk>/edit/', views.RuleEditView.as_view(), name='rule_edit'),
    path('rules/<int:pk>/delete/', views.RuleDeleteView.as_view(), name='rule_delete'),

    path('rules/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='rule_changelog', kwargs={
        'model': models.Rule
    }),
)