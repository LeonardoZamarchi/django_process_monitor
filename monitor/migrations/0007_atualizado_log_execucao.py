# Generated by Django 5.0.3 on 2024-06-11 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0006_alter_atualizado_ultima_atualizacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='atualizado',
            name='Log_Execucao',
            field=models.TextField(blank=True),
        ),
    ]
