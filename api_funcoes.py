# importando bibliotecas necessárias
from bs4 import BeautifulSoup


# Caminho para coletar as informações necessárias para a producao da mensagem final

## 1 | Acessando a API/eventos da Câmara dos Deputados
def proxima_pagina(dados):  # Função para coletar as informações de todas as páginas da API (válidos para outras API da Câmara)
  for link in dados['links']:
    if link['rel'] == 'next':
      return link['href']
    
def todos_eventos():
  eventos = []
  url = f'https://dadosabertos.camara.leg.br/api/v2/eventos?dataInicio={data_hoje()}&dataFim={data_hoje()}'
 
  while url:
    resp = requests.get(url)
    dados = resp.json()
    eventos.extend(dados['dados'])
    url = proxima_pagina(dados)
  
  return eventos


## 2 | Acessando a API/eventos/{id}/pauta da Câmara dos Deputados

# Função para identificar a id da sessão
def id_sessao_deliberativa():
  id = 0
  for item in todos_eventos():

    if item['descricaoTipo'] == 'Sessão Deliberativa':
      id = item['id']   

  resultado = id          
  return resultado

# Função para captar as pautas
def pautas_sessao_deliberativa():

  if id_sessao_deliberativa() == 0:
    pautas = ''

  else:  
    response_api_2 = requests.get(f'https://dadosabertos.camara.leg.br/api/v2/eventos/{id_sessao_deliberativa()}/pauta')
    response_api_2 = response_api_2.json()
    response_api_2

    if response_api_2['dados'] == []:
      pautas = f'<b>\N{card index dividers} Pautas</b> \n \n<i>As prévias das pautas ainda não foram definidas.</i> Às 13h, vou buscar saber se tivemos novas atualizações. Em caso afirmativo, eu te mando aqui. Não precisa se preocupar \N{relieved face} \n \nEnquanto isso, confira mais informações no site <a href="https://www.camara.leg.br/agenda">Câmara dos Deputados</a>'

    else:
      pautas_gerais = []
      pautas = f"<b>\N{card index dividers} Pautas para discussão:</b> \n \n"

      ordem = 0
      for item in response_api_2['dados']:
        if item['topico'] == 'Discussão':
          titulo = item['titulo']
          id_proposicao = item['proposicao_']['id']
          ementa = item['proposicao_']['ementa']
          ordem += 1

          pautas += f'<b>{ordem} | {titulo}</b> \n<b>Ementa:</b> {ementa} \n \n'
      
      pautas_finais = f'{pautas} \n \nÉ importante lembrar que essa é uma prévia do que será discutido. Os deputados podem fazer alterações durante a sessão'
    return pautas
  
  
  ## 3 | União final de todas as raspagens para construir a mensagem final do Telegram
  
  def mensagem_telegram():
    
    # bloco das datas
    data_hoje()
    data_final_abertura()
    dia_da_semana_extenso()

    # coletar todos os eventos
    todos_eventos()

    # buscar se tem sessão deliberativa
    teve_sessao_deliberativa = False
    abertura = f'<b>Bom dia, humana! \U0001F31E \N{hot beverage}</b> \nVamos lá para as informações dessa {dia_da_semana_extenso()} \n \n\U0001F4C6 <b>{data_final_abertura()}</b> \n \n \n'

    #### se tiver sessão deliberativa
    for item in todos_eventos():
      if item['descricaoTipo'] == 'Sessão Deliberativa':
        teve_sessao_deliberativa = True
        id = item['id']             
        descricao_geral = item['descricaoTipo']
        descricao_detalhada = item['descricao']
        local = item['localCamara']['nome']
        link = str(item['urlRegistro'])
        horario = item['dataHoraInicio'][11:16]

        abertura += f"<b>{horario} | {descricao_geral}</b> \n{descricao_detalhada} \n{local} \n \n"

        id_sessao_deliberativa()
        pautas_sessao_deliberativa()

        abertura += f'{pautas_sessao_deliberativa()}'


    #### se não tiver sessão deliberativa
    if not teve_sessao_deliberativa:
      abertura += f"Não tem Sessão Deliberativa marcada para o dia de hoje! \n \n<i>Pode descansar e fazer outra coisa, humana! \U0001F973</i>"
  
    return abertura
  
  
  
