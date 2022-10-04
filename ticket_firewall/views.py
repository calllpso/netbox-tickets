from netbox.views import generic
from . import forms, models, tables
from django.db.models import Count
from . import forms, models, tables, filtersets
# from django.shortcuts import render

class AttachFileEditView(generic.ObjectEditView):
    queryset = models.AttachFile.objects.all()
    form = forms.AttachFileForm

class AttachFileDeleteView(generic.ObjectDeleteView):
    queryset = models.AttachFile.objects.all()
    

class TicketView(generic.ObjectView):
    queryset = models.Ticket.objects.all()
    def get_extra_context(self, request, instance):
        table = tables.RuleTable(instance.rules.all())
        table.configure(request)
        files = models.AttachFile.objects.filter(ticket_id = instance)

        return {
            'files':    files,
            'rules_table': table,
        }

#ListList
class TicketListView(generic.ObjectListView):
    queryset = models.Ticket.objects.annotate(
        rule_count=Count('rules')
    )
    table = tables.TicketTable
    filterset = filtersets.TicketFilterSet
    filterset_form = forms.TicketFilterForm

class TicketEditView(generic.ObjectEditView):
    queryset = models.Ticket.objects.all()
    form = forms.TicketForm

class TicketDeleteView(generic.ObjectDeleteView):
    queryset = models.Ticket.objects.all()

#one
class RuleView(generic.ObjectView):
    queryset = models.Rule.objects.all()

#many
class RuleListView(generic.ObjectListView):
    queryset = models.Rule.objects.all()
    table = tables.RuleTable ###
    filterset = filtersets.RuleFilterSet
    filterset_form = forms.RuleFilterForm
    

class RuleCreateView(generic.ObjectEditView):
    queryset = models.Rule.objects.all()
    form = forms.RuleFormCreate

class RuleEditView(generic.ObjectEditView):
    queryset = models.Rule.objects.all()
    form = forms.RuleFormEdit



class RuleDeleteView(generic.ObjectDeleteView):
    queryset = models.Rule.objects.all()
