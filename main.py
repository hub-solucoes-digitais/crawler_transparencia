from pandas import json_normalize
from utils import define_periodo
from utils import move_arquivos
from datetime import date, datetime
import pandas as pd
import requests
import json

fonte = "csv"
destino = "log\old_csv"
move_arquivos(fonte,destino)

DATA_CONSULTA = date.today()
ANO = date.today().year
URL = "https://sorsdn.sistemaindustria.com.br/api/Transparencia"
payload = ""

UF_LIST = ["cn","ct","al","ba","se","pe","pb","rn","ce","pi","ma","ac","ap","am","pa","rr","ro","to","ms","mt","go","df","dn","rj","sp","es","mg","rs","pr","sc"]
ENTIDADES_LIST = ["sesi","senai"]

for ENTIDADE in ENTIDADES_LIST:
    for UF in UF_LIST:
        querystring = {"entidade":ENTIDADE,
                    "regional":UF,
                    "ano":ANO}
        response = requests.request("GET", URL, data=payload, params=querystring)

        if not ((ENTIDADE == "senai" and UF == "cn") or (ENTIDADE == "sesi" and UF == "ct")) and len(response.text) > 962:
            print(UF,ENTIDADE)
            data = json.loads(response.text)
            df_receitas = json_normalize(data[0]["Contas"])
            df_despesas = json_normalize(data[1]["Contas"])
            df_despesas_finalidade = json_normalize(data[2]["Contas"])
            
            df_receitas["Tipo"] = data[0]["Tipo"]
            df_despesas["Tipo"] = data[1]["Tipo"]
            df_despesas_finalidade["Tipo"] = data[2]["Tipo"]
            df_receitas["DataPublicacao"] = datetime.strptime(data[0]["DataPublicacao"], "%d/%m/%Y %H:%M")
            df_despesas["DataPublicacao"] = datetime.strptime(data[1]["DataPublicacao"], "%d/%m/%Y %H:%M")
            df_despesas_finalidade["DataPublicacao"] = datetime.strptime(data[2]["DataPublicacao"], "%d/%m/%Y %H:%M")
            
            df = pd.concat([df_receitas,df_despesas,df_despesas_finalidade])
            df["Uf"] = UF.upper()
            df["etl_versao"] = 2
            df["etl_dt_inicio"] = "1900-01-01 00:00:00.0000000"
            df["etl_dt_fim"] = "2200-01-01 00:00:00.0000000"
            df["nr_ano"] = df["DataPublicacao"].apply(lambda x: x.year)
            df["dsc_periodo"] = df["DataPublicacao"].apply(lambda x: define_periodo(x.month))
            df["dsc_unidade"] = ENTIDADE.upper()
            path = f'csv/df_{UF}_{ENTIDADE}_{DATA_CONSULTA}.csv'
            df.to_csv(path, index=False)
            
            with open(f"log/arquivo_log_{DATA_CONSULTA}.txt", "a", encoding="utf-8") as arquivo_log:
                arquivo_log.write(f"Status: Sucesso, Entidade: {ENTIDADE}, UF: {UF}, Data Consulta: {DATA_CONSULTA}, Caminho Arquivo: {path}\n")
        
        else:
            if not (ENTIDADE == "senai" and UF == "cn") or not (ENTIDADE == "sesi" and UF == "ct"):
                with open(f"log/arquivo_log_{DATA_CONSULTA}.txt", "a", encoding="utf-8") as arquivo_log:
                    arquivo_log.write(f"Status: Falha, Entidade: {ENTIDADE}, UF: {UF}, Data Consulta: {DATA_CONSULTA}\n")