from pandas import json_normalize
from datetime import date
import pandas as pd
import requests
import shutil
import json
import os

source = './csv'
for diretorio, subpastas, arquivos in os.walk(source):
    for arquivo in arquivos:
        file_name_in_source = os.path.join(os.path.realpath(diretorio), arquivo)
        file_name_in_destination = file_name_in_source.replace("\csv","\log\old_csv")
        shutil.move(file_name_in_source,file_name_in_destination)

data_consulta = date.today()
url = "https://sorsdn.sistemaindustria.com.br/api/Transparencia"
payload = ""

uf_list = ["cn","ct","al","ba","se","pe","pb","rn","ce","pi","ma","ac","ap","am","pa","rr","ro","to","ms","mt","go","df","dn","rj","sp","es","mg","rs","pr","sc"]
entidades = ["sesi","senai"]
ano = "2022"

for entidade in entidades:
    for uf in uf_list:
        querystring = {"entidade":entidade,
                    "regional":uf,
                    "ano":ano}
        response = requests.request("GET", url, data=payload, params=querystring)

        if len(response.text) > 962:
            data = json.loads(response.text)
            df_receitas = json_normalize(data[0]["Contas"])
            df_despesas = json_normalize(data[1]["Contas"])
            df_despesas_finalidade = json_normalize(data[2]["Contas"])
            
            df_receitas["Tipo"] = data[0]["Tipo"]
            df_despesas["Tipo"] = data[1]["Tipo"]
            df_despesas_finalidade["Tipo"] = data[2]["Tipo"]
            
            df = pd.concat([df_receitas,df_despesas,df_despesas_finalidade])
            df["Uf"] = uf.upper()
            df["nr_ano"] = ano
            df["etl_versao"] = 2
            df["etl_dt_inicio"] = "1900-01-01 00:00:00.0000000"
            df["etl_dt_fim"] = "2200-01-01 00:00:00.0000000"
            df["dsc_periodo"] = "Jan-Jun"
            df["dsc_unidade"] = entidade.upper()
            path = f'csv/df_{uf}_{entidade}_{data_consulta}.csv'
            df.to_csv(path, index=False)
            
            with open(f"log/arquivo_log_{data_consulta}.txt", "a", encoding="utf-8") as arquivo_log:
                arquivo_log.write(f"Status: Sucesso, Entidade: {entidade}, UF: {uf}, Data Consulta: {data_consulta}, Caminho Arquivo: {path}\n")
        
        else:
            if not (entidade == "senai" and uf == "cn") or not (entidade == "sesi" and uf == "ct"):
                with open(f"log/arquivo_log_{data_consulta}.txt", "a", encoding="utf-8") as arquivo_log:
                    arquivo_log.write(f"Status: Falha, Entidade: {entidade}, UF: {uf}, Data Consulta: {data_consulta}\n")