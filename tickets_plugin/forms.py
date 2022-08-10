from netbox.forms import NetBoxModelForm
from utilities.forms.fields import CommentField, DynamicModelChoiceField
from .models import TicketList, Rule

from netbox.forms import NetBoxModelFilterSetForm
from django import forms
from .models import Rule_Action, Rule_Protocol


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

    
    class Meta:
        model = Rule
        fields = (
            'ticket_id', 'index', 'source_prefix', 'source_ports', 'destination_prefix',
            'destination_ports', 'protocol', 'action', 'description', 'opened', 'closed', 'tags',
        )


class RuleFilterForm(NetBoxModelFilterSetForm):
    model = Rule

    ###из названия ниже берет создает поле в форме создания
    ticket_id = forms.ModelMultipleChoiceField(
        queryset=TicketList.objects.all(),
        required=False
        )

    index = forms.IntegerField(
        required=False
    )

    protocol = forms.MultipleChoiceField(
        choices=Rule_Protocol,
        required=False
    )
    action = forms.MultipleChoiceField(
        choices=Rule_Action,
        required=False
    )

    opened = forms.CharField(
        required=False
    )

    closed = forms.CharField(
        required=False
    )

    source_prefix = forms.GenericIPAddressField(
        required=False
    )

    destination_prefix = forms.GenericIPAddressField(
        required=False
    )

    description = forms.CharField(
        required=False
    )




class TicketListFilterForm(NetBoxModelFilterSetForm):
    model = TicketList

    name = forms.CharField(
        required=False
    )

    id_directum = forms.CharField(
        required=False
    )

    description = forms.CharField(
        required=False
    )

