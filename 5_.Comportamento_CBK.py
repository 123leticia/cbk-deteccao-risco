import pandas as pd

# Carregar o arquivo
df = pd.read_csv("dados_tratados_com_tags_ajustado.csv", encoding='latin1')

# Corrigir possíveis problemas de codificação na coluna CBK
df['CBK'] = df['CBK'].str.strip().str.lower().replace({'nÃ£o': 'nao', 'sim': 'sim'})

# Calcular limite de valor alto (top 10%)
limite_valor = df['Valor'].quantile(0.90)

# TAG CBK_Horario_Alto: transações CBK entre 00h–06h
df['CBK_Horario_Alto'] = (df['CBK'] == 'sim') & df['Hora_H'].between(0, 6)

# TAG CBK_Valor_Alto: transações CBK acima do limite de valor
df['CBK_Valor_Alto'] = (df['CBK'] == 'sim') & (df['Valor'] > limite_valor)

# TAG CBK_BIN_Frequente: transações CBK com BINs mais frequentes
bin_freq = df['BIN'].value_counts().head(10).index
df['CBK_BIN_Frequente'] = (df['CBK'] == 'sim') & df['BIN'].isin(bin_freq)

# TAG CBK_Cartao_Recorrente: transações CBK com cartões recorrentes
df['CBK_Cartao_Recorrente'] = (df['CBK'] == 'sim') & df['Risco_Cartao_Recorrente']

# TAG CBK_Risco_Combinado: todas as condições acima verdadeiras
df['CBK_Risco_Combinado'] = df[
    ['CBK_Horario_Alto', 'CBK_Valor_Alto', 'CBK_BIN_Frequente', 'CBK_Cartao_Recorrente']
].all(axis=1)

# Salvar o novo arquivo
df.to_csv("dados_tratados_com_tags_cbk.csv", index=False)
print("Arquivo com TAGs CBK salvo como 'dados_tratados_com_tags_cbk.csv'")