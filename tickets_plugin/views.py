from netbox.views import generic
from . import forms, models, tables
from django.db.models import Count

from . import filtersets, forms, models, tables

class TicketListView(generic.ObjectView):
    queryset = models.TicketList.objects.all()

    #счетчик rules
    def get_extra_context(self, request, instance):
        table = tables.AccessListRuleTable(instance.rules.all())
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
class AccessListRuleView(generic.ObjectView):
    queryset = models.AccessListRule.objects.all()

#many
class AccessListRuleListView(generic.ObjectListView):
    queryset = models.AccessListRule.objects.all()
    table = tables.AccessListRuleTable ###
    filterset = filtersets.AccessListRuleFilterSet
    filterset_form = forms.AccessListRuleFilterForm
    

class AccessListRuleEditView(generic.ObjectEditView):
    queryset = models.AccessListRule.objects.all()
    form = forms.AccessListRuleForm


class AccessListRuleDeleteView(generic.ObjectDeleteView):
    queryset = models.AccessListRule.objects.all()
