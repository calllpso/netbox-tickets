from netbox.forms import NetBoxModelForm,NetBoxModelFilterSetForm
from utilities.forms.fields import CommentField, DynamicModelChoiceField,TagFilterField, DynamicModelMultipleChoiceField
from utilities.forms import DatePicker,widgets
from .models import Ticket, Rule, Rule_Action, Ticket_status,Rule_Protocol, AttachFile
from django import forms
# from ipam.models import Prefix
from django.db.models import Max


class AttachFileForm(NetBoxModelForm):
    file = forms.FileField()
    ticket_id = DynamicModelChoiceField(
        queryset=Ticket.objects.all()
    )
    def __init__(self, *args, **kwargs):
        super(AttachFileForm,self).__init__(*args, **kwargs)

        if 'ticket_id' in kwargs:
            ticket_id = kwargs.pop('ticket_id')
            self.fields['ticket_id'].initial = ticket_id
    
    class Meta:
        model = AttachFile
        fields = ('ticket_id','file',)

class TicketForm(NetBoxModelForm):

    comments = CommentField()
    class Meta:
        model = Ticket
        fields = ('ticket_id', 'status', 'id_directum', 'tags', 'description', 'comments')



class RuleFormEdit(NetBoxModelForm):
    ###из названия ниже берет создает поле в форме создания
    ticket_id = DynamicModelChoiceField(
        queryset=Ticket.objects.all()
    )

    protocol = forms.MultipleChoiceField(
        widget = widgets.StaticSelectMultiple, 
        choices=Rule_Protocol,
        required=False
    )
    #нужно index д.б. всегда required=True: это ж ссылка из тикета 
    class Meta:
        model = Rule
        fields = (
        'ticket_id', 'index', 'source_prefix', 'source_ports', 'destination_prefix',
        'destination_ports', 'protocol', 'action', 'description', 'opened', 'closed', 'tags',
        )
        widgets = {
            'opened': DatePicker(),
            'closed': DatePicker()
        }

class RuleFormCreate(NetBoxModelForm):
    ###из названия ниже берет создает поле в форме создания
    ticket_id = DynamicModelChoiceField(
        queryset=Ticket.objects.all()
    )

    protocol = forms.MultipleChoiceField(
        widget = widgets.StaticSelectMultiple, 
        choices=Rule_Protocol,
        required=False
    )
    #нужно index д.б. всегда required=True: это ж ссылка из тикета 
    def __init__(self, *args, **kwargs):
        super(RuleFormCreate,self).__init__(*args, **kwargs)
        if 'ticket_id' in kwargs:
            ticket_id = kwargs.pop('ticket_id')
            self.fields['ticket_id'].initial = ticket_id

        try:
            max_index=Rule.objects.filter().aggregate(max_index=Max('index'))
            index = max_index['max_index'] + 1
            self.initial['index'] = index
        except:
            pass

    class Meta:
        model = Rule
        fields = (
           'ticket_id', 'index', 'source_prefix', 'source_ports', 'destination_prefix',
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

    index = forms.ModelMultipleChoiceField(
        widget = widgets.StaticSelectMultiple, 
        queryset=Rule.objects.values_list('index', flat =True),
        required=False
    )
    
    action = forms.ChoiceField(
        choices=Rule_Action,
        widget = widgets.StaticSelect,
        required=False
    )
    
    # queryset_model_prefix=Prefix.objects.values_list('prefix', flat =True).exclude(prefix=None)
    # queryset_source_prefix=Rule.objects.values_list('source_prefix', flat =True).exclude(source_prefix=None)
    # queryset = queryset_model_prefix.union(queryset_source_prefix),

    source_prefix = forms.ModelChoiceField(
        widget = widgets.StaticSelect, 
        queryset = Rule.objects.values_list('source_prefix', flat =True).exclude(source_prefix=None),
        required=False
    )
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
        widget = widgets.StaticSelectMultiple, 
        choices=Ticket_status,
        required=False
    )


from netbox.forms import NetBoxModelCSVForm

class TicketCSVForm(NetBoxModelCSVForm):
    class Meta:
        model = Ticket
        fields = ('ticket_id', 'status', 'id_directum', 'description', 'comments',)
    def __init__(self, data=None, *args, **kwargs):
        super().__init__(data, *args, **kwargs)


class RuleCSVForm(NetBoxModelCSVForm):
    from django.db import models
    # source_prefix=models.CharField(max_length=50)
    # destination_prefix=models.CharField(max_length=50)
    # source_ports = models.Array
    from taggit.models import Tag
    taggg = Tag.objects.all()

    class Meta:
        model = Rule
        fields = ('ticket_id', 'index', 'source_ports', 'destination_ports', 'action', 'opened', 'closed', 'protocol', 'source_prefix',)
        # fields = ('source_prefix', 'destination_prefix','tags')
    def __init__(self, data=None, *args, **kwargs):
        super().__init__(data, *args, **kwargs)


