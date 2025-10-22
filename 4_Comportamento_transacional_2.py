import pandas as pd

# Carregar o arquivo com codificação e separador correto
df = pd.read_csv("dados_tratados_2_com_datahora.csv", encoding='latin1', sep=',')

# Normalizar nomes de colunas
df.columns = [col.strip().replace('ç', 'c').replace('ã', 'a').replace('Ã', 'A').replace('Ã£', 'a') for col in df.columns]

# Tratar o campo 'Valor'
df['Valor'] = df['Valor'].astype(str).str.replace('R$', '', regex=False).str.replace(' ', '').str.replace('.', '').str.replace(',', '.')
df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')

# Criar coluna 'DataHora' a partir de Dia + Hora
df['DataHora'] = pd.to_datetime(df['Dia'] + ' ' + df['Hora'], errors='coerce', dayfirst=True)

# Extrair hora
df['Hora_H'] = df['DataHora'].dt.hour

# TAG 1: Risco_Horario_Alto (00h–06h)
df['Risco_Horario_Alto'] = df['Hora_H'].between(0, 6)

# TAG 2: Risco_Valor_Alto (top 10% dos valores)
limite_valor = df['Valor'].quantile(0.90)
df['Risco_Valor_Alto'] = df['Valor'] > limite_valor

# TAG 3: Risco_Cartao_Recorrente (mais de 10 transações por cartão em um único dia)
df['Dia'] = pd.to_datetime(df['Dia'], errors='coerce', dayfirst=True)
transacoes_por_cartao_dia = df.groupby(['Cartao', df['Dia'].dt.date]).size()
cartoes_risco = transacoes_por_cartao_dia[transacoes_por_cartao_dia > 10].reset_index()[['Cartao', 'Dia']]
cartoes_risco['Risco'] = True

df = df.merge(cartoes_risco, how='left', left_on=['Cartao', df['Dia'].dt.date], right_on=['Cartao', 'Dia'])
df['Risco_Cartao_Recorrente'] = df['Risco'].fillna(False)
df.drop(columns=['Dia_y', 'Risco'], inplace=True)
df.rename(columns={'Dia_x': 'Dia'}, inplace=True)

# TAG 4: Risco_BIN_Alto (BINs mais frequentes)
df['BIN'] = df['Cartao'].astype(str).str[:6]
bin_freq = df['BIN'].value_counts().head(10)
df['Risco_BIN_Alto'] = df['BIN'].isin(bin_freq.index)

# TAG 5: Risco_Combinado
df['Risco_Combinado'] = (
    df['Risco_BIN_Alto'] &
    df['Risco_Valor_Alto'] &
    df['Risco_Cartao_Recorrente']
)

# Salvar o arquivo ajustado
df.to_csv("dados_tratados_com_tags_ajustado_2.csv", index=False)

print("Arquivo tratado com TAGs ajustadas salvo como 'dados_tratados_com_tags_ajustado_2.csv'")