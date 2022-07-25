from pandas import json_normalize
from utils import define_periodo
from utils import move_arquivos
from datetime import date
import pandas as pd
import requests
import shutil
import json
import os

fonte = "csv"
destino = "log\old_csv"
move_arquivos(fonte,destino)

data_consulta = date.today()
mes_consulta = date.today().month
url = "https://sorsdn.sistemaindustria.com.br/api/Transparencia"
payload = ""

uf_list = ["cn","ct","al","ba","se","pe","pb","rn","ce","pi","ma","ac","ap","am","pa","rr","ro","to","ms","mt","go","df","dn","rj","sp","es","mg","rs","pr","sc"]
entidades = ["sesi","senai"]
periodo = define_periodo(mes_consulta)[0]
ano = define_periodo(mes_consulta)[1]

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
            df["dsc_periodo"] = periodo
            df["dsc_unidade"] = entidade.upper()
            path = f'csv/df_{uf}_{entidade}_{data_consulta}.csv'
            df.to_csv(path, index=False)
            
            with open(f"log/arquivo_log_{data_consulta}.txt", "a", encoding="utf-8") as arquivo_log:
                arquivo_log.write(f"Status: Sucesso, Entidade: {entidade}, UF: {uf}, Data Consulta: {data_consulta}, Caminho Arquivo: {path}\n")
        
        else:
            if not (entidade == "senai" and uf == "cn") or not (entidade == "sesi" and uf == "ct"):
                with open(f"log/arquivo_log_{data_consulta}.txt", "a", encoding="utf-8") as arquivo_log:
                    arquivo_log.write(f"Status: Falha, Entidade: {entidade}, UF: {uf}, Data Consulta: {data_consulta}\n")