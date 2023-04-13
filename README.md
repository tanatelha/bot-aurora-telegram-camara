# Aurora da Câmara dos Deputados 🤖 🗂️ 🗳️
A bot Aurora da Câmara dos Deputados ou Aurora da Câmara é o projeto final da primeira parte da especialização do Master em Jornalismo de Dados, Automação e Data Storytelling do Insper. A robô nasceu a partir de uma demanda pessoal de ter mais conhecimento do que estava sendo discutido na Casa Legislativa que representada o povo. Além desse contato, era exigido também uma maior praticidade para ter acesso a atualizações diárias com pouco gasto de tempo para ir até a informação.

Os códigos aqui apresentados executam as funcionalidades aprendidadas durante a especialização:
* Acesso e coleta de dados por API,
* Análise de dados com a biblioteca *pandas*,
* Recebimento e envio de mensagens pela API de robôs do Telegram usando a biblioteca *requests* e o método webhook (site com Flask),
* Leitura e escrita de dados em planilhas do Google Sheets usando a biblioteca *gspread*,
* Criação de site dinâmicos em Python usando *Flask*

Para conhecer a Aurora, acesse a sua [página oficial no Telegram](https://t.me/Aurora_da_Camara_bot) ou busque por **@Aurora_da_Camara_bot**.

## Funcionalidades
A Aurora está em *constante atualização*. Atualmente, ela se encontra na sua versão beta 1.0, sendo capaz de realizar as seguintes funções:
1. Inscrição de usuários para receber mensagens diárias
2. Indentificação de usuários já inscrito e barragem de inscrições duplas
3. Desinscrição de usuários para receber mensagens diárias
3. Envio diário das prévias das pautas de discussões na Câmara dos Deputados (função realizada de segunda a sexta)


## Composição
Para utilizar esse robô, você irá precisar de alguns processos:
* **BotFather:** é uma ferramenta do Telegram para criação de bot. Para dar continuidade, é só acessar o site e seguir as orientações. Quando o robô for criado, o Telegram irá te enviar um token. É necessário salvar esse código, pois é com ele que você irá acessar a API do Telegram para enviar os comandos para o seu bot | [Acesso](https://t.me/botfather)
* **Google Sheets:** Para usar o sheets, é necessário pedir acesso ao Google, que pode ser feito [neste link](https://console.cloud.google.com/). O resultado final será dois conteúdos: um e-mail genérico do Google, que será usado para você compartilhar a planilha do sheets com ele, e uma chave de acesso, enviada por meio de um arquivo .json. Dica: além de ativar o Google Sheets, você deve ativar também o Google Drive
* **Render:** é uma plataforma de nuvem, em que podemos usar para rodar o código e automatizar seu funcionamento. No Ben, essa foi a ferramenta utilizada, mas você pode escolher a de sua preferência

## Arquivos
* **app.py:** contém o site criado no Flask para automatização juntamente com as aplicações do robô no Telegram.
* **data_funcao.py:** contém todas funções que se relacionam com a produção de resultados voltados para data e hora. É composto por quatro funções.
* **api_funcoes.py:** contém todas as funções construídas para acessar as APIs da Câmara dos Deputados e coletar informações sobre as sessões e suas respectivas pautas. É nesse arquivo também que as mensagens diárias são produzidas. É composta por 6 funções.
* **descadrastamento.py:** contém a função que descadrasta o usuário para não receber mais as mensagens da Aurora
* **processa_dados_mensagens.py:** contém as funções responsáveis por processar as mensagens recebidas no Telegram e gerar respostas automatizadas. É composta por 1 função.
* **requirements.txt:** é um arquivo de texto que possui todas as bibliotecas que precisam ser instaladas para rodar o código dentro da nuvem

*Descrição de cada uma das funções podem ser encontradas dentro dos respectivos arquivos.*

## setWebhook
É um método disponível na API do Telegram que permite a configuração de uma URL para receber atualizações do bot de forma assíncrona, em vez de usar o método getUpdates que faz com que o bot precise verificar periodicamente se há atualizações. Quando você configura um webhook, o Telegram enviará uma solicitação HTTP POST para a URL que você especificou sempre que houver uma atualização para o seu bot.

Para fazer essa configuração, você precisa rodar o seguinte código:
```
import getpass            
import requests

token = getpass.getpass()

dados = {"url": "https://seu-site-do-render.onrender.com"}  # colocar aqui o site do Web Service criado no Render
resposta = requests.post(f"https://api.telegram.org/bot{token}/setWebhook", data = dados)
print(resposta.text)
```

A biblioteca getpass é uma biblioteca que permite com que você use dados pessoais em um código. Ao rodar, irá aparecer um espaço, onde você irá adicionar o token do seu robô no Telegram. 

## Contato
Em caso de dúvidas, a [API do Telegram](https://core.telegram.org/api) documenta de forma acessível os passo a passo para você desenvolver as suas ideias. Para outras dúvidas e sugestões, envie um e-mail para tanatelha.dados@gmail.com ;)

## Agradecimentos
Gostaria de agradecer os professores Eduardo Cuducos, Guilherme Felitti e Álvaro Justen que ministraram as aulas no Master em Jornalismo de Dados, Automação e Data Storytelling do Insper, cujos aprendizados e ensinamentos foram fundamentais para a criação da Aurora.
