# Generated by Django 5.0.3 on 2024-05-28 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro', '0002_alter_processo_atualizacao'),
    ]

    operations = [
        migrations.RenameField(
            model_name='processo',
            old_name='Pasta',
            new_name='Path_CSV_Final',
        ),
        migrations.AddField(
            model_name='processo',
            name='Script_File',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
