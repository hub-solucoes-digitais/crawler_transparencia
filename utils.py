from datetime import date
import shutil
import os

data_consulta = date.today()
mes_consulta = date.today().month

def define_periodo(mes_consulta):
    if (mes_consulta == 1):
        periodo = "Jan-Dez"
        ano = str(date.today().year-1)
    elif (mes_consulta == 2):
        periodo = "Janeiro"
        ano = str(date.today().year)
    elif (mes_consulta == 3):
        periodo = "Jan-Fev"
        ano = str(date.today().year)
    elif (mes_consulta == 4):
        periodo = "Jan-Mar"
        ano = str(date.today().year)
    elif (mes_consulta == 5):
        periodo = "Jan-Abr"
        ano = str(date.today().year)
    elif (mes_consulta == 6):
        periodo = "Jan-Mai"
        ano = str(date.today().year)
    elif (mes_consulta == 7):
        periodo = "Jan-Jun"
        ano = str(date.today().year)
    elif (mes_consulta == 8):
        periodo = "Jan-Jul"
        ano = str(date.today().year)
    elif (mes_consulta == 9):
        periodo = "Jan-Ago"
        ano = str(date.today().year)
    elif (mes_consulta == 10):
        periodo = "Jan-Set"
        ano = str(date.today().year)
    elif (mes_consulta == 11):
        periodo = "Jan-Out"
        ano = str(date.today().year)
    elif (mes_consulta == 12):
        periodo = "Jan-Nov"
        ano = str(date.today().year)
        
    return periodo,ano

def move_arquivos(fonte, destino):
    source = f'./{fonte}'
    for diretorio, subpastas, arquivos in os.walk(source):
        for arquivo in arquivos:
            file_name_in_source = os.path.join(os.path.realpath(diretorio), arquivo)
            file_name_in_destination = file_name_in_source.replace(f"\{fonte}",f"\{destino}")
            shutil.move(file_name_in_source,file_name_in_destination)