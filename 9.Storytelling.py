import pandas as pd
import plotly.express as px

# Carregar a planilha com previsões
df = pd.read_csv("planilha_2_com_previsao_cbk.csv", encoding='latin1')

# Filtrar apenas transações previstas como CBK
df_cbk = df[df['CBK_Previsto'] == 1]

# Contar quantas dessas transações possuem cada risco ativado
resumo_riscos = {
    'Risco_Horario_Alto': df_cbk['Risco_Horario_Alto'].sum(),
    'Risco_Valor_Alto': df_cbk['Risco_Valor_Alto'].sum(),
    'Risco_Cartao_Recorrente': df_cbk['Risco_Cartao_Recorrente'].sum(),
    'Risco_BIN_Alto': df_cbk['Risco_BIN_Alto'].sum(),
    'Risco_Combinado': df_cbk['Risco_Combinado'].sum()
}

# Criar gráfico de storytelling
fig = px.bar(
    x=list(resumo_riscos.keys()),
    y=list(resumo_riscos.values()),
    labels={'x': 'Fator de Risco', 'y': 'Transações CBK com Risco'},
    title='Principais Fatores de Risco nas Transações Previstas como CBK'
)

# Exibir gráfico
fig.show()