from django.contrib import admin
import subprocess
from .models import Atualizado
import logging
from datetime import datetime
import datetime

import os, sys
import pandas as pd
import sensitive_data
import conecta_odbc as db # type: ignore


def atualizar_painel_at(modeladmin, request, queryset):
    subprocess.call(['python', './update_portal.py'])

atualizar_painel_at.short_description = "Atualizar Painel Atualizações"


def atualizar_processo(modeladmin, request, queryset):
    con = db.conecta_sqlite()
    cursor = con.cursor()
    ret_db = []
    logger = logging.getLogger()
    
    for obj in queryset:
        print(obj)
        rows = cursor.execute(f'SELECT processo, script_file, linguagem from cadastro_processo where processo = "{obj}"').fetchall()
        ret_db.append(rows)    
    ret_db = [item for sublist in ret_db for item in sublist]
    df = pd.DataFrame(ret_db, columns=["Processo", "Path", "Linguagem"])
    print(df)
    for _, row in df.iterrows():

        data_execucao_str = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
        data_execucao = datetime.date.today()

        if row['Linguagem'] == 'R':
            file_path = sensitive_data.default_path + row['Path']             
            try:
                process = subprocess.Popen(["Rscript","--vanilla", file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output, error = process.communicate()

                if process.returncode == 0:
                    log_execucao = f" Atualizado com sucesso, data execução: {data_execucao_str}"
                    sql = 'update monitor_atualizado set Log_Execucao =?, Ultima_Atualizacao = ?, Atualizado_Vigente = ? where processo = ?'
                    cursor.execute(sql, (log_execucao, data_execucao, True, row["Processo"]))
                    con.commit()
                    con.close()

                else:

                    log_text = f"Erro ao executar script, data execução: {data_execucao_str} \n  \n {row['Processo']} - {error.decode('utf-8')}"
                    logger.error(log_text)
                    sql = 'update monitor_atualizado set Log_Execucao =? where processo = ?'
                    cursor.execute(sql, (log_text, row["Processo"]))
                    con.commit()
                    con.close()

            except Exception as e:
                    logger.error(f"Erro inesperado ao executar script: {row['Processo']} - {e}")

        elif row['Linguagem'] == 'Python':
            file_path = sensitive_data.default_path + row['Path'] 

            try:
                process = subprocess.Popen(["python", file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output, error = process.communicate()

                if process.returncode == 0:        
                    log_execucao = f" Atualizado com sucesso, data execução: {data_execucao_str}"
                    sql = 'update monitor_atualizado set Log_Execucao =?, Ultima_Atualizacao = ?, Atualizado_Vigente =? where processo = ?'
                    cursor.execute(sql, (log_execucao, data_execucao,True, row["Processo"]))
                    con.commit()
                    con.close()

                else:
                    log_text = f"Erro ao executar script, data execução: {data_execucao_str} \n  \n {row['Processo']} - {error.decode('utf-8')}"
                    logger.error(log_text)
                    sql = 'update monitor_atualizado set Log_Execucao =? where processo = ?'
                    cursor.execute(sql, (log_text, row["Processo"]))
                    con.commit()
                    con.close()

            except Exception as e:
                    logger.error(f"Erro inesperado ao executar script: {file_path} - {e}")


atualizar_processo.short_description = "Atualizar Processos"


class AtualizadoAdmin(admin.ModelAdmin):
    model = Atualizado
    list_display = ['Processo','Ultima_Atualizacao','Log_Execucao', 'Atualizado_Vigente']
    list_filter = ['Atualizado_Vigente']
    search_fields = ['Processo']
    actions = [atualizar_painel_at, atualizar_processo]

admin.site.register(Atualizado, AtualizadoAdmin)
