# Generated by Django 4.0.7 on 2022-10-04 08:21

import django.contrib.postgres.fields
import django.core.files.storage
import django.core.serializers.json
from django.db import migrations, models
import django.db.models.deletion
import ipam.fields
import taggit.managers
import ticket_firewall.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('extras', '0077_customlink_extend_text_and_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder)),
                ('ticket_id', models.CharField(max_length=100, unique=True)),
                ('status', models.CharField(default='inactive', max_length=30)),
                ('id_directum', models.CharField(blank=True, max_length=100)),
                ('description', models.CharField(blank=True, max_length=500)),
                ('comments', models.TextField(blank=True)),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'ordering': ('ticket_id',),
            },
        ),
        migrations.CreateModel(
            name='AttachFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder)),
                ('file', models.FileField(storage=django.core.files.storage.FileSystemStorage(location='./media/ticket_attachments'), upload_to='')),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
                ('ticket_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='file', to='ticket_firewall.ticket')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder)),
                ('index', models.PositiveIntegerField(unique=True)),
                ('source_prefix', ipam.fields.IPAddressField(blank=True, default=None, null=True)),
                ('source_ports', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, size=None)),
                ('destination_prefix', ipam.fields.IPAddressField(blank=True, default=None, null=True)),
                ('destination_ports', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, size=None)),
                ('protocol', ticket_firewall.models.ChoiceArrayField(base_field=models.CharField(blank=True, max_length=4), size=None)),
                ('action', models.CharField(blank=True, default='permit', max_length=30)),
                ('description', models.CharField(blank=True, max_length=500)),
                ('opened', models.DateField(blank=True, null=True)),
                ('closed', models.DateField(blank=True, null=True)),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
                ('ticket_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rules', to='ticket_firewall.ticket')),
            ],
            options={
                'ordering': ('ticket_id', 'index'),
                'unique_together': {('ticket_id', 'index')},
            },
        ),
    ]