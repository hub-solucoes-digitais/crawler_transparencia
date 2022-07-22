from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from dotenv import load_dotenv
from datetime import date
import smtplib
import ssl
import os

load_dotenv()

data_consulta = date.today()

ctx = ssl.create_default_context()
password = os.getenv("PASSWORD")    # Your app password goes here
sender = os.getenv("SENDER")    # Your e-mail address
receiver = os.getenv("RECEIVER") # Recipient's address

with smtplib.SMTP_SSL("smtp.gmail.com", port="465", context=ctx) as server:
    server.login(sender, password)
    
    corpo = f"Segue o arquivo de log com o resultado das buscas realizadas utilizando a api da transparência, disponível em https://sorsdn.sistemaindustria.com.br/swagger/index.html. \nAs buscas foram realizadas no dia {data_consulta}. \nAtt,"
    
    #montando e-mail 
    email_msg = MIMEMultipart()
    email_msg['From'] = sender
    email_msg['To'] = receiver
    email_msg['Subject'] = f"Relatório atualização da base de dados - Dia {data_consulta}"
    email_msg.attach(MIMEText(corpo,'html'))

    #Abrimos o arquivo em modo leitura e binary 
    cam_arquivo = f"log\\arquivo_log_{data_consulta}.txt"
    attchment = open(cam_arquivo,'rb')

    #Lemos o arquivo no modo binario e jogamos codificado em base 64 (que é o que o e-mail precisa )
    att = MIMEBase('application', 'octet-stream')
    att.set_payload(attchment.read())
    encoders.encode_base64(att)

    #ADCIONAMOS o cabeçalho no tipo anexo de email 
    att.add_header('Content-Disposition', f'attachment; filename=arquivo_log_{data_consulta}.txt')
    #fechamos o arquivo 
    attchment.close()

    #colocamos o anexo no corpo do e-mail 
    email_msg.attach(att)
    #3- ENVIAR o EMAIL tipo MIME no SERVIDOR SMTP 
    server.sendmail(email_msg['From'],email_msg['To'],email_msg.as_string())
    server.quit()