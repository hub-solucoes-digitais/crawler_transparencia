from datetime import date
import shutil
import os

data_consulta = date.today()
mes_consulta = date.today().month

def define_periodo(mes_consulta):
    if (mes_consulta == 1):
        periodo = "Janeiro"
    elif (mes_consulta == 2):
        periodo = "Jan-Fev"
    elif (mes_consulta == 3):
        periodo = "Jan-Mar"
    elif (mes_consulta == 4):
        periodo = "Jan-Abr"
    elif (mes_consulta == 5):
        periodo = "Jan-Mai"
    elif (mes_consulta == 6):
        periodo = "Jan-Jun"
    elif (mes_consulta == 7):
        periodo = "Jan-Jul"
    elif (mes_consulta == 8):
        periodo = "Jan-Ago"
    elif (mes_consulta == 9):
        periodo = "Jan-Set"
    elif (mes_consulta == 10):
        periodo = "Jan-Out"
    elif (mes_consulta == 11):
        periodo = "Jan-Nov"
    elif (mes_consulta == 12):
        periodo = "Jan-Dez"
    else:
        periodo = "Não informado"
        
    return periodo

def move_arquivos(fonte, destino):
    source = f'./{fonte}'
    for diretorio, subpastas, arquivos in os.walk(source):
        for arquivo in arquivos:
            file_name_in_source = os.path.join(os.path.realpath(diretorio), arquivo)
            file_name_in_destination = file_name_in_source.replace(f"\{fonte}",f"\{destino}")
            shutil.move(file_name_in_source,file_name_in_destination)