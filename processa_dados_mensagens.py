# importar bibliotecas que já vêm com python
import os # biblioteca para ver chaves em ambiente virtual


# importar bibliotecas externas: import em ordem alfética e depois froms em ordem alfabética
import gspread
import pytz
import requests
from flask import Flask, request
from bs4 import BeautifulSoup
from datetime import date, datetime, time, timedelta
from oauth2client.service_account import ServiceAccountCredentials 

from data_funcao import data_hoje, data_final_abertura, dia_da_semana_extenso
from api_funcoes import proxima_pagina, todos_eventos, id_sessao_deliberativa, pautas_sessao_deliberativa, mensagem_telegram
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






# Função que processa as mensagens recebida no Telegram dá um retorno

def processa_update(dados):
  inscricoes = []
  mensagens = []
  descadastrados = []
  enviadas = []
  
  
  # Coletando informações de cada mensagem
  update = dados
  update_id = update['update_id']
  first_name = update['message']['from']['first_name']
  user_name = update['message']['from']['username']
  sender_id = update['message']['from']['id']
  chat_id = update['message']['chat']['id']
  date = datetime.fromtimestamp(update['message']['date']).date().strftime('%d/%m/%Y')

  ## calcular o horário com fuso para Brasil
  timestamp = update['message']['date']
  fuso_sao_paulo= pytz.timezone('America/Sao_Paulo')  # converter para o fuso horário 'America/Sao_Paulo'
  saopaulo_time = datetime.fromtimestamp(timestamp, fuso_sao_paulo)
  time = saopaulo_time.strftime('%H:%M:%S')
  
  ## Lidando com informações que podem estar ausentes nas contas dos usuários
  if 'text' not in update['message']:
    message = 'A mensagem é um conteúdo textual que não é possível compreender.'
  else:
    message = update['message']['text'].lower().strip()

  if "username" in update['message']['from']:
    username = f"@{update['message']['from']['username']}"
  else:
    username = f'@ indisponível'

  if 'last_name' not in update['message']['from']['last_name']:
    last_name = update['message']['from']['last_name']
  else:
    last_name = 'Sem last name disponível'
  
  
  # Lista dos usuários inscritos
  inscritos = sheet_inscritos.col_values(6)
  
  
  # Definindo as mensagens
  if message == "/start":
    if str(chat_id) in inscritos:
      texto_resposta = f'Hmmm... \U0001F914 \n \nPelas minhas anotações, <b>você já está inscrita</b> para receber as pautas das da Sessão Deliberativa da Câmara dos Deputados! \n \nO envio é feito a partir das 10h da manhã. Caso a pauta do dia não esteja disponível nesse horário, eu faço uma nova conferência durante o almoço. \n \nMas, ó, não precisa se preocupar! Eu cuido disso para você! \N{winking face} \n \nCaso queira acessar um comando específico, clique em "menu" aqui do lado esquerdo da tela \n \n \U00002B07'
      mensagens.append([str(date), str(time), "recebida", user_name, first_name, last_name, chat_id, message])
      mensagens.append([str(date), str(time), "enviada", user_name, first_name, last_name, chat_id, texto_resposta])
    else:
      texto_resposta = 'Olá, humane! \n \nEu sou o <b>Aurora da Câmara dos Deputados</b>, mas você pode me chamar de <b>Aurora da Câmara</b>! \U0001F916 \n \nPara ter acesso às pautas de discussões da Sessão Deliberativa de hoje, basta digitar /manda que eu te envio. \n \n Seja bem-vinde! \N{winking face}'
      inscricoes.append([str(date), str(time), first_name, last_name, username, sender_id, chat_id, message])
 
  elif message == '/exit':
    todos_inscritos = sheet_inscritos.get_all_values()
    id_procurado = str(chat_id) # é o mesmo valor que o chat_id calculado lá em cima, mas como string, pois é assim que o sheet entende
    texto_resposta = processo_de_descadrastamento()
    descadastrados.append([str(date), str(time), "descadastrado", username, first_name, last_name, chat_id, texto_resposta])
 
  else:
    texto_resposta = f'Olá, humane! \n \nVocê já se inscreveu para receber os destaques do Executivo publicados no <i>Diário Oficial da União</i>. Agora é só esperar os envios das mensagens todo dia de manhã a partir das 7h \U0001F609 \n \nCaso queira acessar um comando específico, clique em "menu" aqui do lado esquerdo da tela'

  nova_mensagem = {"chat_id": chat_id, "text": texto_resposta, "parse_mode": 'html'}
  resposta = requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data = nova_mensagem)

  sheet_inscritos.append_rows(inscricoes)
  sheet_mensagens.append_rows(mensagens)
  sheet_descadastrados.append_rows(descadastrados)
  
  
  
  
  
  
  
  
  
  
