# Importando as bibliotecas
import gspread
from oauth2client.service_account import ServiceAccountCredentials 


# Definindo as variáveis de ambiente
GOOGLE_SHEETS_KEY = os.environ["GOOGLE_SHEETS_KEY"] 

GOOGLE_SHEETS_CREDENTIALS = os.environ['GOOGLE_SHEETS_CREDENTIALS']
with open("credenciais.json", mode="w") as arquivo:
    arquivo.write(GOOGLE_SHEETS_CREDENTIALS)
conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")

api = gspread.authorize(conta)
planilha = api.open_by_key(f'{GOOGLE_SHEETS_KEY}') 
sheet_inscritos = planilha.worksheet('inscritos')


# Função para realizar o descadrastamento do usuário
def processo_de_descadrastamento():
  linha_encontrada = None

  for i, row in enumerate(todos_inscritos):
    if row[5] == id_procurado:  # id está na sexta coluna (índice 5)
      linha_encontrada = i+1  # índice da linha no sheet começa com 0, então adiciona-se 1 ao índice da lista

    if linha_encontrada:
      sheet_inscritos.delete_row(linha_encontrada)

  texto = f'Você foi descadastrado e não irá mais receber as minhas mensagens! Que pena, humane! \U0001F622 \n \nCaso deseje voltar a receber os meus trabalhos, basta me mandar "/start" que eu te reinscrevo. \n \nNos vemos por aí \U0001F916'
  return texto
