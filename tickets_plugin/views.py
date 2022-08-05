from netbox.views import generic
from . import forms, models, tables
from django.db.models import Count

from . import filtersets, forms, models, tables

class TicketListView(generic.ObjectView):
    queryset = models.TicketList.objects.all()

    #счетчик rules
    def get_extra_context(self, request, instance):
        table = tables.RuleTable(instance.rules.all())
        table.configure(request)

        return {
            'rules_table': table,
        }



class TicketListListView(generic.ObjectListView):
    queryset = models.TicketList.objects.annotate(
        rule_count=Count('rules')
    )
    table = tables.TicketListTable
    ############
    filterset = filtersets.TicketListFilterSet
    filterset_form = forms.TicketListFilterForm

class TicketListEditView(generic.ObjectEditView):
    queryset = models.TicketList.objects.all()
    form = forms.TicketListForm

class TicketListDeleteView(generic.ObjectDeleteView):
    queryset = models.TicketList.objects.all()




#one
class RuleView(generic.ObjectView):
    queryset = models.Rule.objects.all()

#many
class RuleListView(generic.ObjectListView):
    queryset = models.Rule.objects.all()
    table = tables.RuleTable ###
    filterset = filtersets.RuleFilterSet
    filterset_form = forms.RuleFilterForm
    

class RuleEditView(generic.ObjectEditView):
    queryset = models.Rule.objects.all()
    form = forms.RuleForm


class RuleDeleteView(generic.ObjectDeleteView):
    queryset = models.Rule.objects.all()
