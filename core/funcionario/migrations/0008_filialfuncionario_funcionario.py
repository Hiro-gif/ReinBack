# Generated by Django 5.0.3 on 2025-03-19 22:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funcionario', '0007_remove_filialfuncionario_funcionario_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='filialfuncionario',
            name='funcionario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
