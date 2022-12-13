from netbox.forms import NetBoxModelForm,NetBoxModelFilterSetForm
from utilities.forms.fields import CommentField, DynamicModelChoiceField,TagFilterField, DynamicModelMultipleChoiceField
from utilities.forms import DatePicker,widgets
from .models import Ticket, Rule, Rule_Action, Ticket_status, AttachFile, Protocol
from django import forms
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

class TicketFormCreate(NetBoxModelForm):
    comments = CommentField()
    class Meta:
        model = Ticket
        fields = ('ticket_id', 'ticket_name', 'status', 'id_directum', 'tags', 'description', 'comments')

    #нужно index д.б. всегда required=True: это ж ссылка из тикета 
    def __init__(self, *args, **kwargs):
        super(TicketFormCreate,self).__init__(*args, **kwargs)
        try:
            max_index=Ticket.objects.filter().aggregate(max_index=Max('ticket_id'))
            ticket_id = max_index['max_index'] + 1
            ticket_id = int(max_index['max_index']) + 1
            self.initial['ticket_id'] = ticket_id
        except:
            pass

class TicketFormEdit(NetBoxModelForm):
    comments = CommentField()
    class Meta:
        model = Ticket
        fields = ('ticket_id', 'ticket_name', 'status', 'id_directum', 'tags', 'description', 'comments')


class RuleFormEdit(NetBoxModelForm):
    ###из названия ниже берет создает поле в форме создания
    ticket_id = DynamicModelChoiceField(
        queryset=Ticket.objects.all()
    )

    protocol = forms.ModelMultipleChoiceField(
        widget = widgets.StaticSelectMultiple, 
        queryset = Protocol.objects.all(),
        required=False
    )
    
    #нужно index д.б. всегда required=True: это ж ссылка из тикета 
    class Meta:
        model = Rule
        fields = (
            'ticket_id', 'index', 'source_ports', 'destination_ports', 'protocol', 'action', 
            'description', 'opened', 'closed', 'tags', 'source_prefix', 'destination_prefix',
        )
        widgets = {
            'opened': DatePicker(),
            'closed': DatePicker()
        }

# class HelpDynamicModelChoiceField(DynamicModelChoiceField):


class RuleFormCreate(NetBoxModelForm):
    ###из названия ниже берет создает поле в форме создания
    ticket_id = DynamicModelChoiceField(
        queryset=Ticket.objects.all()
    )
    
    #it works. 
    # but: django.urls.exceptions.NoReverseMatch: Reverse for 'protocol-list' not found. 'protocol-list' is not a valid view function or pattern name.
    # protocol = DynamicModelChoiceField(
    #     queryset=Protocol.objects.all()
    # )

    protocol = forms.ModelMultipleChoiceField(
        widget = widgets.StaticSelectMultiple, 
        queryset = Protocol.objects.all(),
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
            'ticket_id', 'index', 'source_ports', 'source_prefix', 'destination_prefix',
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
    
    index = forms.ModelChoiceField(
        widget = widgets.StaticSelect, 
        queryset = Rule.objects.values_list('index', flat =True),
        required=False
    )

    action = forms.ChoiceField(
        choices=Rule_Action,
        widget = widgets.StaticSelect,
        required=False
    )

    protocol = forms.ModelMultipleChoiceField(
        widget = widgets.StaticSelectMultiple, 
        queryset = Protocol.objects.all(),
        required=False
    )

    source_prefix = forms.ModelChoiceField(
        widget = widgets.StaticSelect, 
        queryset = Rule.objects.values_list('source_prefix', flat =True).exclude(source_prefix=None),
        required=False
    )
    destination_prefix = forms.ModelMultipleChoiceField (
        widget = widgets.StaticSelectMultiple,
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

    ticket_name = forms.ModelMultipleChoiceField(
        widget = widgets.StaticSelectMultiple, 
        queryset=Ticket.objects.values_list('ticket_name', flat =True),
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



















#CSV

from netbox.forms import NetBoxModelCSVForm

class TicketCSVForm(NetBoxModelCSVForm):
    class Meta:
        model = Ticket
        fields = ('ticket_id', 'status', 'id_directum', 'description', 'comments',)
    def __init__(self, data=None, *args, **kwargs):
        super().__init__(data, *args, **kwargs)


class RuleCSVForm(NetBoxModelCSVForm):
    from taggit.models import Tag
    taggg = Tag.objects.all()

    class Meta:
        model = Rule
        fields = ('ticket_id', 'index', 'source_prefix', 'source_ports', 'destination_prefix', 'destination_ports', 'action', 'opened', 'closed', 'protocol', 'tags',)
    def __init__(self, data=None, *args, **kwargs):
        super().__init__(data, *args, **kwargs)



