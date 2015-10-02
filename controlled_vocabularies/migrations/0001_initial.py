# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('property_name', models.CharField(help_text=b'The name of the added property. E.g. Description', max_length=50, verbose_name=b'Property Type', choices=[(b'definition', b'Definition'), (b'description', b'Description'), (b'note', b'Note'), (b'system', b'System')])),
                ('label', models.TextField(help_text=b'The value for the added property')),
            ],
            options={
                'ordering': ['property_name'],
                'verbose_name_plural': 'Properties',
            },
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'The name or key that uniquely identify the term within the vocabulary', max_length=50)),
                ('label', models.CharField(help_text=b'The human readable name of the term', max_length=255)),
                ('order', models.IntegerField(help_text=b'The preferred order of viewing the term in the Vocabulary', null=True, blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'Terms',
            },
        ),
        migrations.CreateModel(
            name='Vocabulary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'The name or key that uniquely identify the vocabulary', unique=True, max_length=50)),
                ('label', models.CharField(help_text=b'The human readable name of the vocabulary', max_length=255)),
                ('order', models.CharField(help_text=b'The preferred order of viewing the UNTL list of controled Vocabularies', max_length=10, choices=[(b'name', b'name'), (b'label', b'label'), (b'order', b'order')])),
                ('maintainer', models.CharField(help_text=b'The person responsible for creating and updating the vocabulary', max_length=50)),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('maintainerEmail', models.CharField(help_text=b'E-mail address of maintainer', max_length=50, verbose_name=b'Maintainer E-mail')),
                ('definition', models.TextField(help_text=b'A brief statement of the meaning of the vocabulary', blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'Vocabularies',
            },
        ),
        migrations.AddField(
            model_name='term',
            name='vocab_list',
            field=models.ForeignKey(verbose_name=b'Vocabulary', to='controlled_vocabularies.Vocabulary', help_text=b'The vocabulary that the term needs to be added'),
        ),
        migrations.AddField(
            model_name='property',
            name='term_key',
            field=models.ForeignKey(verbose_name=b'Term', to='controlled_vocabularies.Term'),
        ),
        migrations.AlterUniqueTogether(
            name='term',
            unique_together=set([('name', 'vocab_list')]),
        ),
    ]
