import imp
from netbox.forms import NetBoxModelForm
from utilities.forms.fields import CommentField, DynamicModelChoiceField,TagFilterField, DynamicModelMultipleChoiceField
from .models import TicketList, Rule

from netbox.forms import NetBoxModelFilterSetForm
from django import forms
from .models import Rule_Action, Rule_Protocol

from dcim.models import Device

from utilities.forms import DatePicker


# from dcim.forms import DeviceFilterForm
from django.forms.widgets import  SelectMultiple #, StaticSelectMultiple
from utilities.forms import widgets
from django.forms.widgets import Select as sel

class TicketListForm(NetBoxModelForm):
    comments = CommentField()

    class Meta:
        model = TicketList
        fields = ('ticket_id', 'status', 'id_directum', 'tags', 'comments')

class RuleForm(NetBoxModelForm):
    ###из названия ниже берет создает поле в форме создания
    ticket_id = DynamicModelChoiceField(
        queryset=TicketList.objects.all()
    )

    device = DynamicModelChoiceField(
        queryset=Device.objects.all()
    )

    class Meta:
        model = Rule
        fields = (
           'ticket_id', 'device', 'index', 'source_prefix', 'source_ports', 'destination_prefix',
           'destination_ports', 'protocol', 'action', 'description', 'opened', 'closed', 'tags',
        )

        widgets = {
            'opened': DatePicker(),
            'closed': DatePicker()
        }


class RuleFilterForm(NetBoxModelFilterSetForm):
    model = Rule

    tag = TagFilterField(model)

    ticket_id = DynamicModelChoiceField(
        queryset=TicketList.objects.all(),
        required=False
    )

    device = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False
    ) 

    index = forms.ModelMultipleChoiceField(
        widget = widgets.StaticSelectMultiple, 
        queryset=Rule.objects.values_list('index', flat =True),
        required=False
        )
    
    action = forms.MultipleChoiceField(
        choices=Rule_Action,
        required=False
    )
    # action = forms.ChoiceField(
    #     widget = sel,
    #     # widget = widgets.StaticSelect,
    #     choices=Rule_Action,
    #     required=False
    # )

    # source_prefix = forms.GenericIPAddressField(
    # source_prefix = forms.ModelMultipleChoiceField(
    source_prefix = forms.ModelChoiceField(
        #если делать multi, то поле фильтра всегда активно, даже, если ничего в нем нет
        # widget = widgets.StaticSelectMultiple, 
        widget = widgets.StaticSelect, 
        queryset=Rule.objects.values_list('source_prefix', flat =True).exclude(source_prefix=None),
        required=False
    )
    destination_prefix = forms.ModelChoiceField(
        widget = widgets.StaticSelect,
        queryset=Rule.objects.values_list('destination_prefix', flat =True).exclude(destination_prefix=None),
        required=False
    )

    opened = forms.ModelMultipleChoiceField(
        # widget=DatePicker,
        widget = widgets.StaticSelectMultiple,
        queryset=Rule.objects.values_list('opened', flat =True).exclude(opened=None),
        required=False
    )

    closed = forms.ModelMultipleChoiceField(
        widget = widgets.StaticSelectMultiple,
        queryset=Rule.objects.values_list('closed', flat =True).exclude(closed=None),
        required=False
    )

   





class TicketListFilterForm(NetBoxModelFilterSetForm):
    model = TicketList

    tag = TagFilterField(model)

    ticket_id = forms.CharField(
        required=False
    )
    id_directum = forms.CharField(
        required=False
    )
    status = forms.CharField(
        required=False
    )

    