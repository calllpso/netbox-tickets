from netbox.forms import NetBoxModelForm,NetBoxModelFilterSetForm
from utilities.forms.fields import CommentField, DynamicModelChoiceField,TagFilterField, DynamicModelMultipleChoiceField
from utilities.forms import DatePicker,widgets
from .models import Ticket, Rule, Rule_Action, Ticket_status,Rule_Protocol
from django import forms
from dcim.models import Device
from ipam.models import Prefix

class TicketForm(NetBoxModelForm):
    comments = CommentField()
    class Meta:
        model = Ticket
        fields = ('ticket_id', 'status', 'id_directum', 'tags', 'comments')

class RuleForm(NetBoxModelForm):
    ###из названия ниже берет создает поле в форме создания
    ticket_id = DynamicModelChoiceField(
        queryset=Ticket.objects.all()
    )
    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False
    )
    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False
    )
    
    #!!!!!!!
    protocol = forms.MultipleChoiceField(
        choices=Rule_Protocol,
        required=False
    )
    #нужно всегда задавать: это ж ссылка из тикета 
    # index = forms.CharField(
    #     required=False
    # )
    
    # queryset_model_prefix=Prefix.objects.values_list('prefix', flat =True).exclude(prefix=None)
    # queryset_source_prefix=Rule.objects.values_list('source_prefix', flat =True).exclude(source_prefix=None)
    # queryset = queryset_model_prefix.union(queryset_source_prefix),    
    # source_prefix = forms.ModelChoiceField(
    #     widget = widgets.StaticSelect, 
    #     queryset = queryset_model_prefix.union(queryset_source_prefix),
    #     required=False
    # )

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
        queryset=Ticket.objects.all(),
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
    
    queryset_model_prefix=Prefix.objects.values_list('prefix', flat =True).exclude(prefix=None)
    queryset_source_prefix=Rule.objects.values_list('source_prefix', flat =True).exclude(source_prefix=None)
    queryset = queryset_model_prefix.union(queryset_source_prefix),

    source_prefix = forms.ModelChoiceField(
        widget = widgets.StaticSelect, 
        queryset = Rule.objects.values_list('source_prefix', flat =True).exclude(source_prefix=None),
        required=False
    )
    # source_prefix = forms.ModelChoiceField(
    #     widget = widgets.StaticSelect, 
    #     queryset=Rule.objects.values_list('source_prefix', flat =True).exclude(source_prefix=None),
    #     required=False
    # )
    destination_prefix = forms.ModelChoiceField(
        widget = widgets.StaticSelect,
        queryset=Rule.objects.values_list('destination_prefix', flat =True).exclude(destination_prefix=None),
        required=False
    )

    opened = forms.ModelMultipleChoiceField(
        widget = widgets.StaticSelectMultiple,
        queryset=Rule.objects.values_list('opened', flat =True).exclude(opened=None),
        required=False
    )

    closed = forms.ModelMultipleChoiceField(
        widget = widgets.StaticSelectMultiple,
        queryset=Rule.objects.values_list('closed', flat =True).exclude(closed=None),
        required=False
    )

class TicketFilterForm(NetBoxModelFilterSetForm):
    model = Ticket
    tag = TagFilterField(model)
    ticket_id = forms.ModelMultipleChoiceField(
        widget = widgets.StaticSelectMultiple, 
        queryset=Ticket.objects.values_list('ticket_id', flat =True),
        required=False
        )

    id_directum = forms.ModelMultipleChoiceField(
        widget = widgets.StaticSelectMultiple, 
        queryset=Ticket.objects.values_list('id_directum', flat =True),
        required=False
        )

    status = forms.MultipleChoiceField(
        choices=Ticket_status,
        required=False
    )