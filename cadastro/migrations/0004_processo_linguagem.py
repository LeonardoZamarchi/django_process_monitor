# Generated by Django 5.0.3 on 2024-05-28 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro', '0003_rename_pasta_processo_path_csv_final_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='processo',
            name='Linguagem',
            field=models.CharField(choices=[('Python', 'Python'), ('R', 'R')], default='Python', max_length=10),
        ),
    ]
