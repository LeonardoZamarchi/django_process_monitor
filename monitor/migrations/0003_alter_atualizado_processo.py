# Generated by Django 5.0.3 on 2024-03-26 19:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro', '0001_initial'),
        ('monitor', '0002_atualizado_tamanho_arquivo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atualizado',
            name='Processo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastro.processo'),
        ),
    ]
