import subprocess, sys, os, time
from datetime import datetime
import pandas as pd
import os, sys
import logging
import datetime as dt
import time

username = os.environ['USERNAME']
path = 'C:/Users/'+username+'/Sicredi/Equipe BI - Desenvolvimento Power BI - General/SCRIPTS/PYTHON/conecta_odbc'
sys.path.insert(1, path)
import conecta_odbc as db
path = 'C:/Users/app_0737_equipebi/OneDrive - Sicredi/Documents/Scripts/portal'
sys.path.insert(1, path)
username = os.environ['USERNAME']
import update_portal as up #type: ignore


def run_file(title, script_file, time, linguagem):
        con = db.conecta_sqlite()
        cursor = con.cursor()
        logger = logging.getLogger()
        data_execucao_str = dt.datetime.now().strftime("%d-%m-%Y %H:%M")
        data_execucao = dt.date.today()        
        ret_db = []
        path_padrao = 'C:/Users/'+username+'/Sicredi/Equipe BI - Desenvolvimento Power BI - General/'
        file_path = (path_padrao+script_file)
        ret_db.append([title, linguagem ,file_path]) 
        df = pd.DataFrame(ret_db, columns=["Processo", "Linguagem", "Path"])
        for _, row in df.iterrows():
            if row['Linguagem'] == 'R':                         
                try:                  
                    print('Running the process, '+title+' at '+ str(time))
                    start_time = dt.datetime.now()
                    process = subprocess.Popen(["Rscript","--vanilla", file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    output, error = process.communicate()
                    end_time = dt.datetime.now()
                    execution_time = (end_time - start_time).total_seconds()
                    if process.returncode == 0:   
                    
                        log_execucao_r = f" Atualizado com sucesso, data execução: {data_execucao_str}, tempo de execução do script: {execution_time:.2f} segundos"

                        sql = 'update monitor_atualizado set Log_Execucao =?, Ultima_Atualizacao = ?, Atualizado_Vigente = ? where processo = ?'
                        cursor.execute(sql, (log_execucao_r, data_execucao, True, row["Processo"]))
                        con.commit()
                        con.close()
                        res = ('Process '+ title + ' was finished at '+str(time)+' STATUS: SUCCESS')
                        return(res)
                    else:
                        log_text_r = f"Erro ao executar script, data execução: {data_execucao_str} \n  \n {row['Processo']} - {error.decode('utf-8')}"
                        logger.error(log_text_r)
                        sql = 'update monitor_atualizado set Log_Execucao =?, Ultima_Atualizacao = ?, Atualizado_Vigente = ? where processo = ?'
                        cursor.execute(sql, (log_text_r, data_execucao, False, row["Processo"]))
                        con.commit()
                        con.close()
                        res = ('Process '+ title + ' was finished at '+str(time)+' STATUS: FAILED')
                        return res

                except Exception as e:
                        log_text_script_att = logger.error(f"Erro inesperado ao executar script de atualização: {row['Processo']} - {e}")
                        logger.error(log_text_script_att)
                        sql = 'update monitor_atualizado set Log_Execucao =?, Ultima_Atualizacao = ?, Atualizado_Vigente = ? where processo = ?'
                        cursor.execute(sql, (log_text_script_att, data_execucao, False, row["Processo"]))
                        con.commit()
                        con.close()

            elif row['Linguagem'] == 'Python':
                try:
                    print('Running the process, '+title+' at '+ str(time))
                    start_time = dt.datetime.now()
                    process = subprocess.Popen(["python", file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    output, error = process.communicate()
                    end_time = dt.datetime.now()
                    execution_time = (end_time - start_time).total_seconds()
                    if process.returncode == 0:        
                        log_execucao_p = f"Atualizado com sucesso, data execução: {data_execucao_str}, tempo de execução do script: {execution_time:.2f} segundos"
                        sql = 'update monitor_atualizado set Log_Execucao =?, Ultima_Atualizacao = ?, Atualizado_Vigente =? where processo = ?'
                        cursor.execute(sql, (log_execucao_p, data_execucao,True, row["Processo"]))
                        con.commit()
                        con.close()
                        res = ('Process '+ title + ' was finished at '+str(time)+' STATUS: SUCCESS')
                        return(res)
                    
                    else:
                        log_text_p = f"Erro ao executar script, data execução: {data_execucao_str} \n  \n {row['Processo']} - {error.decode('utf-8')}"
                        logger.error(log_text_p)
                        sql = 'update monitor_atualizado set Log_Execucao =?, Ultima_Atualizacao = ?, Atualizado_Vigente = ? where processo = ?'
                        cursor.execute(sql, (log_text_p, data_execucao, False, row["Processo"]))
                        con.commit()
                        con.close()
                        res = ('Process '+ title + ' was finished at '+str(time)+' STATUS: FAILED')
                        return res

                except Exception as e:
                        log_text_script_att = f"Erro inesperado ao executar o script de atualização: {file_path} - {e}"
                        logger.error(log_text_script_att)
                        sql = 'update monitor_atualizado set Log_Execucao =?, Ultima_Atualizacao = ?, Atualizado_Vigente = ? where processo = ?'
                        cursor.execute(sql, (log_text_script_att, data_execucao, False, row["Processo"]))
                        con.commit()
                        con.close()

while True:    
    con = db.conecta_sqlite()
    cursor = con.cursor()
    sql = ('SELECT  p.Processo, p.Script_File, a.Horario, p.Linguagem FROM Cadastro_Agendamento a INNER JOIN Cadastro_Processo p ON a.Processo = p.Processo')
    cursor.execute(sql)
    rows = cursor.fetchall()
    ls = [(row[0], row[1], row[2], row[3]) for row in rows]
    for i in ls:
        now_dt = datetime.now().strftime("%d-%m-%Y")
        now = datetime.now().strftime("%H:%M:%S")
        weekday = datetime.today().strftime('%A')
        if i[2] == now:
            exec = run_file(i[0],i[1],i[2],i[3])
            time.sleep(60)
            print(exec)

