# importar bibliotecas que já vêm com python
import os # biblioteca para ver chaves em ambiente virtual


# importar bibliotecas externas: import em ordem alfética e depois froms em ordem alfabética
import gspread
import pytz
import requests
from flask import Flask, request
from datetime import date, datetime, time, timedelta
from oauth2client.service_account import ServiceAccountCredentials 

from data_funcao import hora_hoje, data_hoje, data_final_abertura, dia_da_semana_extenso
from api_funcoes import proxima_pagina, todos_eventos, id_sessao_deliberativa, pautas_sessao_deliberativa, mensagem_telegram, mensagem_telegram_2
from processa_dados_mensagens import processa_update
from descadrastamento import processo_de_descadrastamento


# variáveis de ambiente
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_ADMIN_ID = os.environ["TELEGRAM_ADMIN_ID"]

GOOGLE_SHEETS_KEY = os.environ["GOOGLE_SHEETS_KEY"] 

GOOGLE_SHEETS_CREDENTIALS = os.environ['GOOGLE_SHEETS_CREDENTIALS']
with open("credenciais.json", mode="w") as arquivo:
    arquivo.write(GOOGLE_SHEETS_CREDENTIALS)
conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")

api = gspread.authorize(conta)
planilha = api.open_by_key(f'{GOOGLE_SHEETS_KEY}') 
sheet_mensagens = planilha.worksheet('mensagens')
sheet_enviadas = planilha.worksheet('enviadas')
sheet_inscritos = planilha.worksheet('inscritos')
sheet_descadastrados = planilha.worksheet('descadastrados')


# Criação do site
app = Flask(__name__)


@app.route("/")
def index():
  return "Esse é o site da Aurora da Câmara dos Deputados"


@app.route("/bot-aurora-telegram", methods=["POST"]) # método utilizado para enviar dados para o servidor
def telegram_bot():
  update = request.json
  processa_update()
  return f'{processa_update()}'
  
  
@app.route("/bot-aurora-telegram-envio")
def telegram_bot_envio():
    data = data_hoje()
    hora = hora_hoje()
    inscritos = sheet_inscritos.col_values(6)
    tamanho_mensagem = len(mensagem_telegram())
    if tamanho_mensagem <= 4096:
        texto_resposta = mensagem_telegram()
    else:
        texto_resposta = mensagem_telegram_2()
    

    enviadas = []
    for id in inscritos:
        nova_mensagem = {"chat_id": id,
                         "text": texto_resposta,
                         "parse_mode": 'html'}
        resposta_2 = requests.post(f"https://api.telegram.org./bot{TELEGRAM_TOKEN}/sendMessage", data=nova_mensagem)
        enviadas.append([str(data), str(hora), "enviada", id, texto_resposta])
    
    sheet_enviadas.append_rows(enviadas)

    print(resposta_2.text) 
    return f'{(resposta_2.text)}'
  
