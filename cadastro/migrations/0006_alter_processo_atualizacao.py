# Generated by Django 5.0.3 on 2024-06-06 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro', '0005_rename_path_csv_final_processo_path_arquivo_saida_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processo',
            name='Atualizacao',
            field=models.CharField(choices=[('Diário', 'Diário'), ('Mensal', 'Mensal'), ('Semanal', 'Semanal'), ('Anual', 'Anual'), ('Sob Demanda', 'Sob Demanda'), ('Inativado', 'Inativado')], default='Mensal', max_length=13),
        ),
    ]
