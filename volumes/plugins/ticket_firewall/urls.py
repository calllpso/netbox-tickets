from django.urls import path
from . import models, views
from netbox.views.generic import ObjectChangeLogView,ObjectJournalView

urlpatterns = (
    # Ticket lists
    path('tickets/', views.TicketListView.as_view(), name='ticket_list'),
    path('tickets/add/', views.TicketCreateView.as_view(), name='ticket_add'),
    path('tickets/<int:pk>/', views.TicketView.as_view(), name='ticket'),           # Этот ticket указывается в get_absolute_url в models
    path('tickets/<int:pk>/edit/', views.TicketEditView.as_view(), name='ticket_edit'),
    path('tickets/<int:pk>/delete/', views.TicketDeleteView.as_view(), name='ticket_delete'),
    path('tickets/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='ticket_changelog', kwargs={
        'model': models.Ticket
    }),
    path('tickets/import/', views.TicketBulkImportView.as_view(), name='ticket_import'),

    #для журнала необходимо добавить WritableNestedSerializer  
    path('ticket/<int:pk>/journal/', ObjectJournalView.as_view(), name='ticket_journal', kwargs={'model': models.Ticket}),
    path('rules/', views.RuleListView.as_view(), name='rule_list'),
    path('rules/add/', views.RuleCreateView.as_view(), name='rule_add'),
    path('rules/<int:pk>/', views.RuleView.as_view(), name='rule'),             
    path('rules/<int:pk>/edit/', views.RuleEditView.as_view(), name='rule_edit'),
    path('rules/<int:pk>/delete/', views.RuleDeleteView.as_view(), name='rule_delete'),

    path('rules/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='rule_changelog', kwargs={
        'model': models.Rule
    }),
    path('rules/import/', views.RuleBulkImportView.as_view(), name='rule_import'),


    path('attachfile/add/', views.AttachFileEditView.as_view(), name='attachfile_add'),
    path('attachfile/<int:pk>/edit/', views.AttachFileEditView.as_view(), name='attachfile_edit'),
    path('attachfile/<int:pk>/delete/', views.AttachFileDeleteView.as_view(), name='attachfile_delete'),

    path('prefix/add/', views.PrefixRuleViewEdit.as_view(), name='prefix_add'),
    

)