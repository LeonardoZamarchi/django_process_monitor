# Generated by Django 5.0.3 on 2024-05-29 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro', '0004_processo_linguagem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='processo',
            old_name='Path_CSV_Final',
            new_name='Path_Arquivo_Saida',
        ),
        migrations.AlterField(
            model_name='processo',
            name='Atualizacao',
            field=models.CharField(choices=[('Diário', 'Diário'), ('Mensal', 'Mensal'), ('Semanal', 'Semanal'), ('Anual', 'Anual'), ('Sob Demanda', 'Sob Demanda')], default='Mensal', max_length=13),
        ),
    ]
