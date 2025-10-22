import pandas as pd

# Carregar o arquivo com codificação e separador correto
df = pd.read_csv("Planilha_1.csv", encoding='latin1', sep=';')

# Normalizar nomes de colunas
df.columns = [col.strip().replace('ç', 'c').replace('ã', 'a').replace('Ã', 'A').replace('Ã£', 'a') for col in df.columns]

# Tratar o campo 'Valor'
def limpar_valor(valor):
    try:
        valor = str(valor)
        if 'R$' in valor:
            valor = valor.replace('R$', '').replace(' ', '').replace('.', '').replace(',', '.')
        return float(valor)
    except:
        return None

df['Valor'] = df['Valor'].apply(limpar_valor)

# Tratar o campo 'Hora'
df['Hora'] = df['Hora'].astype(str).str.split('.').str[0]

# Criar coluna 'DataHora' como string formatada
df['DataHora'] = pd.to_datetime(df['Dia'] + ' ' + df['Hora'], errors='coerce', dayfirst=True)
df['DataHora'] = df['DataHora'].dt.strftime('%Y-%m-%d %H:%M:%S')  # formato padrão ISO

# Criar nova coluna 'CBK_BIN'
cbk_map = {'NÃ£o': 0, 'Não': 0, 'Sim': 1, 'sim': 1}
df['CBK_BIN'] = df['CBK'].map(cbk_map)

# Salvar o arquivo tratado
df.to_csv("dados_tratados_com_datahora.csv", index=False)

print("Arquivo tratado salvo como 'dados_tratados_com_datahora.csv'")