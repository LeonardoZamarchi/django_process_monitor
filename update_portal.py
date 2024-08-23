import os, sys
import datetime
from datetime import timedelta
import pandas as pd
import sqlite3
import sensitive_data
import conecta_odbc as db # type: ignore


#funcao para retorna ro tamnho do arquivo em bytes
def get_file_size(file_path):
    # Get the file size
    size = os.path.getsize(file_path)
    return size

#Funcao para pegar a data da ultima modificacao em str
def get_file_last_modif(file_path):
    # Get the last modification time
    last_modified_timestamp = os.path.getmtime(file_path)
    last_modified_datetime = datetime.datetime.fromtimestamp(last_modified_timestamp).strftime('%Y-%m-%d')
    return last_modified_datetime

# Funcao onde diminui a data atual menos a data da ultima modificacao do arquivo para obter o o valor para fazer a comparacao e verfificar se a atualizacao e diaria semanal ou mensal
def get_file_vigente(atualizacao,file_path):
    last_modified_timestamp = os.path.getmtime(file_path)
    last_modified_datetime = datetime.datetime.fromtimestamp(last_modified_timestamp)
    diferenca = datetime.date.today() - last_modified_datetime.date()
    if atualizacao == 'Diário':
        return int(diferenca <= timedelta(days=0))
    elif atualizacao == 'Semanal':
        return int(diferenca <= timedelta(days=8))
    elif atualizacao == 'Mensal':
        return int(diferenca <= timedelta(days=32))
    elif atualizacao == 'Anual':
        return int(diferenca <= timedelta(days=370))
    elif atualizacao == 'Sob Demanda':
        return 1
    elif atualizacao == 'Inativado':
        return 1
    else:
        return 0
    #return is_modified_today
 
# Funcao para fazer o update no portal
 
def run_update_portal():
    con = db.conecta_sqlite()
    cursor = con.cursor()
    rows = cursor.execute(sensitive_data.query).fetchall()
    df = pd.DataFrame(rows,columns=['processo', 'file_path', 'atualizacao'])
    # Apply the function to each file path in the DataFrame
    df['file_path'] = sensitive_data.default_path
    df['size'] = df['file_path'].apply(get_file_size)
    df['last_modified'] = df['file_path'].apply(get_file_last_modif)
    #df['is_modified_today'] = df['file_path'].apply(get_file_vigente)
    df['atualizado'] = df.apply(lambda row: get_file_vigente(row['atualizacao'],row['file_path']), axis=1)
    con.commit()


    processos = cursor.execute('SELECT PROCESSO FROM MONITOR_ATUALIZADO').fetchall()
    
    processos = [processo[0] for processo in processos]

    for _, row in  df.iterrows():
        if row['processo'] in processos:           
            sql = 'update monitor_atualizado set ultima_atualizacao =?, atualizado_vigente =?, tamanho_arquivo =? where processo =?'
            cursor.execute(sql, (row['last_modified'], row['atualizado'], row['size'], row['processo']))
        else:
            sql = 'insert into monitor_atualizado (ULTIMA_ATUALIZACAO, ATUALIZADO_VIGENTE, TAMANHO_ARQUIVO, PROCESSO, Log_Execucao) values(?,?,?,?,?)'
            cursor.execute(sql, (row['last_modified'], row['atualizado'], row['size'], row['processo'],''))
        
        con.commit()
    con.close()
run_update_portal()


