from netbox.forms import NetBoxModelForm
from utilities.forms.fields import CommentField, DynamicModelChoiceField
from .models import TicketList, AccessListRule

from netbox.forms import NetBoxModelFilterSetForm
from django import forms
from .models import AccessListRule_Action, AccessListRule_Protocol

class TicketListForm(NetBoxModelForm):
    comments = CommentField()

    class Meta:
        model = TicketList
        fields = ('name', 'status', 'id_directum', 'tags')

class AccessListRuleForm(NetBoxModelForm):
    
    
    access_list = DynamicModelChoiceField(
        queryset=TicketList.objects.all()
    )

    class Meta:
        model = AccessListRule
        fields = (
            'ticket_list', 'ticket_id', 'index', 'source_prefix', 'source_ports', 'destination_prefix',
            'destination_ports', 'protocol', 'action', 'description', 'opened', 'closed', 'tags',
        )



class AccessListRuleFilterForm(NetBoxModelFilterSetForm):
    model = AccessListRule

    access_list = forms.ModelMultipleChoiceField(
        queryset=TicketList.objects.all(),
        required=False
        )

    index = forms.IntegerField(
        required=False
    )

    protocol = forms.MultipleChoiceField(
        choices=AccessListRule_Protocol,
        required=False
    )
    action = forms.MultipleChoiceField(
        choices=AccessListRule_Action,
        required=False
    )
    

