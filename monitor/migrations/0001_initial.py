# Generated by Django 5.0.3 on 2024-03-26 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Atualizado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Processo', models.CharField(max_length=200)),
                ('Ultima_Atualizacao', models.DateTimeField(verbose_name='last update')),
                ('Atualizado_Hoje', models.BooleanField(default=False)),
            ],
        ),
    ]
