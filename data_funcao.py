from datetime import date, time, datetime, timedelta


# Função para descobrir a data do dia em questão (resultado no formato necessário para parâmetro da api da Câmara)
def data_hoje():
  data = date.today()
  dia = data.day
  if dia < 10: 
    dia = str(dia)
    dia = '0'+dia
  else:
    dia = str(dia)

  mes = data.month
  if mes < 10:
    mes = str(mes)
    mes = '0'+mes
  else:
    mes = str(mes)

  ano = data.year
  ano = str(ano)

  data_final = (ano)+'-'+(mes)+'-'+(dia)

  return data_final


# Função para coletar a data do dia em um formato legível para o texto de abertura
def data_final_abertura():
  data = datetime.strptime(data_hoje(), '%Y-%m-%d').date()
  dia_2 = str(data.day)
  mes_2 = data.month
  ano_2 = str(data.year)

  if mes_2 == 1:
    mes_2 = ' de Janeiro de '
  elif mes_2 == 2:
    mes_2 = ' de Fevereiro de '
  elif mes_2 == 3:
    mes_2 = ' de Março de '
  elif mes_2 == 4:
    mes_2 = ' de Abril de '
  elif mes_2 == 5:
    mes_2 = ' de Maio de '
  elif mes_2 == 6:
    mes_2 = ' de Junho de '
  elif mes_2 == 7:
    mes_2 = ' de Julho de '
  elif mes_2 == 8:
    mes_2 = ' de Agosto de '
  elif mes_2 == 9:
    mes_2 = ' de Setembro de '
  elif mes_2 == 10:
    mes_2 = ' de Outubro de '
  elif mes_2 == 11:
    mes_2 = ' de Novembro de '
  elif mes_2 == 12:
    mes_2 = ' de Dezembro de '

  dia_final = dia_2 + mes_2 + ano_2

  return dia_final


# Função para descobrir o dia da semana
def dia_da_semana_extenso():
  DIAS = ['segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira', 'sábado', 'domingo']
  data = datetime.strptime(data_hoje(), '%Y-%m-%d').date()
  indice_da_semana = data.weekday()
  dia_da_semana = DIAS[indice_da_semana]

  return dia_da_semana
