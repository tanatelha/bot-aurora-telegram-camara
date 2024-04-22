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
sheet_inscritos = planilha.worksheet('inscritos')
sheet_raspagem = planilha.worksheet('raspagem')
sheet_mensagens = planilha.worksheet('mensagens')
sheet_enviadas = planilha.worksheet('enviadas')
sheet_descadastrados = planilha.worksheet('descadastrados')


# Criação do site
app = Flask(__name__)


@app.route("/")
def index():
  return "Esse é o site da Aurora da Câmara dos Deputados"


@app.route("/bot-aurora-telegram", methods=["POST"]) # método utilizado para enviar dados para o servidor
def telegram_bot():
  mensagens = []
  inscricoes = []
  descadastrados = []
  
  update = request.json 

  ### dados da mensagem
  update_id = update['update_id']
  first_name = update['message']['from']['first_name']
  chat_id = update['message']['chat']['id']
  date = datetime.fromtimestamp(update['message']['date']).date().strftime('%d/%m/%Y')
 
  # calcular horário / converter fuso
  timestamp = update['message']['date']  
  fuso_sao_paulo = pytz.timezone('America/Sao_Paulo') # converter para o fuso horário 'America/Sao_Paulo'
  saopaulo_time = datetime.fromtimestamp(timestamp, fuso_sao_paulo)
  time = saopaulo_time.strftime('%H:%M:%S')

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


  
  ### definição da mensagem a ser enviada a partir da mensagem recebida
  inscritos = sheet_inscritos.col_values(6)
  print(inscritos)
  
  if message == "/start":
        if str(chat_id) in inscritos:
            print(chat_id)
            texto_resposta = f'Hmmm... \U0001F914 \n \nPelas minhas anotações, <b>você já está inscrita</b> para receber as pautas das da Sessão Deliberativa da Câmara dos Deputados! \n \nO envio é feito a partir das 10h da manhã. Caso a pauta do dia não esteja disponível nesse horário, eu faço uma nova conferência durante o almoço. \n \nMas, ó, não precisa se preocupar! Eu cuido disso para você! \N{winking face} \n \nCaso queira acessar um comando específico, clique em "menu" aqui do lado esquerdo da tela \n \n \U00002B07'
            nova_mensagem = {"chat_id": chat_id, "text": texto_resposta, "parse_mode": 'html'}
            resposta = requests.post(f"https://api.telegram.org./bot{TELEGRAM_TOKEN}/sendMessage", data = nova_mensagem)
            mensagens.append([str(date), str(time), "recebida", first_name, last_name, username,chat_id, message])
            mensagens.append([str(date), str(time), "enviada", first_name, last_name, username, chat_id, texto_resposta])

        else:
            texto_resposta = f'Olá, humane! \n \nEu sou o <b>Aurora da Câmara dos Deputados</b>, mas você pode me chamar de <b>Aurora da Câmara</b>! \U0001F916 \n \nSou um bot criado para enviar diariamente, por meio do Telegram, as prévias das pautas de discussões da Sessão Deliberativa na Câmara dos Deputados. \n \nPor enquanto, eu estou em atualização, mas vou voltar em breve. Já guardei aqui o seu contato. \N{winking face} '
            nova_mensagem = {"chat_id": chat_id, "text": texto_resposta, "parse_mode": 'html'}
            resposta = requests.post(f"https://api.telegram.org./bot{TELEGRAM_TOKEN}/sendMessage", data = nova_mensagem)
            inscricoes.append([str(date), str(time), first_name, last_name, username, chat_id, message])
            mensagens.append([str(date), str(time), "enviada", first_name, last_name, username, chat_id, texto_resposta])
            
            
  elif message == "/exit":
    data = sheet_inscritos.get_all_values()
    id_procurado = str(chat_id)  # é o mesmo valor que o chat_id calculado lá em cima

    def processo_de_descadrastamento():
        linha_encontrada = None

        for i, row in enumerate(data):
          if row[5] == id_procurado:
            linha_encontrada = i+1    # índice da linha no sheet começa com 0, então adiciona-se 1 ao índice da lista

        if linha_encontrada:
          sheet_inscritos.delete_row(linha_encontrada)
        
        texto = f'Você foi descadastrado e não irá mais receber as minhas mensagens! Que pena, humana! \U0001F622 \n \nCaso deseje voltar a receber os meus trabalhos, basta me mandar "/start" que eu te reinscrevo. \n \nNos vemos por aí \U0001F916'

        return texto
    
    texto_resposta = processo_de_descadrastamento()
    nova_mensagem = {"chat_id": id_procurado, "text": texto_resposta, "parse_mode": 'html'}
    resposta = requests.post(f"https://api.telegram.org./bot{TELEGRAM_TOKEN}/sendMessage", data = nova_mensagem)
    descadastrados.append([str(date), str(time), "descadastrado", first_name, last_name, username, chat_id, texto_resposta])

    
  else:
    texto_resposta = f'Olá, humana! \n \nVocê já se inscreveu para receber as prévias das pautas da <i>Câmara dos Deputados</i>. Agora é só esperar os envios das mensagens, de segunda a sexta, a partir das 10h \U0001F609 \n \nPor enquanto, eu estou em atualização, mas vou voltar em breve. Já guardei aqui o seu contato. \n \nCaso queira acessar um comando específico, clique em "menu" aqui do lado esquerdo da tela'
    nova_mensagem = {"chat_id": chat_id, "text": texto_resposta, "parse_mode": 'html'}
    resposta = requests.post(f"https://api.telegram.org./bot{TELEGRAM_TOKEN}/sendMessage", data = nova_mensagem)
    mensagens.append([str(date), str(time), "recebida", first_name, last_name, username, chat_id, message])
    mensagens.append([str(date), str(time), "enviada", first_name, last_name, username, chat_id, texto_resposta])
    
 
 
  ### Atualizando a planilha sheets ss mensagens enviadas
  sheet_inscritos.append_rows(inscricoes)
  sheet_mensagens.append_rows(mensagens)
  sheet_descadastrados.append_rows(descadastrados)
    
  print(message)
  print(resposta.text)
  return "ok"
    
    
@app.route("/bot-aurora-telegram-raspagem")  
def telegram_bot_raspagem():
    raspagem = []
    data = data_hoje()
    hora = hora_hoje()
    texto = mensagem_telegram()
    raspagem.append([str(data), str(hora), texto])
    sheet_raspagem.append_rows(raspagem)
    return f'Raspagem feita às {hora} do dia {data}'
  
@app.route("/bot-aurora-telegram-envio")
def telegram_bot_envio():
    # Coletando a raspagem no sheet
    data_procurada = data_hoje()  # definindo a data que você quer buscar
    linha = sheet_raspagem.find(data_procurada).row # Procurando a linha na qual a data está localizada
    raspagem_do_dia = sheet_raspagem.cell(linha,3).value # Acessando a célula da terceira coluna na linha encontrada e obtendo o valor
    
    # Definindo qual mensagem será enviada
    tamanho_mensagem = len(raspagem_do_dia)
    if tamanho_mensagem <= 4096:    # O Telegram só envia mensagens de até 4.096 caracteres
        texto_resposta = raspagem_do_dia
    else:
        texto_resposta = mensagem_telegram_2()
    
    # Envio das mensagens
    data = data_hoje()
    hora = hora_hoje()
    
    enviadas = []  
    inscritos = sheet_inscritos.col_values(6)
    for id in inscritos:
        nova_mensagem = {"chat_id": id,
                         "text": texto_resposta,
                         "parse_mode": 'html'}
        resposta_2 = requests.post(f"https://api.telegram.org./bot{TELEGRAM_TOKEN}/sendMessage", data=nova_mensagem)
        enviadas.append([str(data), str(hora), "enviada", id, texto_resposta])
    
    sheet_enviadas.append_rows(enviadas)

    print(resposta_2.text) 
    return f'{(resposta_2.text)}'
  
