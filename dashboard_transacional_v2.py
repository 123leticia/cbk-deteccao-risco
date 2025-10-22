import pandas as pd
import streamlit as st
import plotly.express as px
from lightgbm import LGBMClassifier

# Carregar os dados
df = pd.read_csv("C:/Users/Z550647/OneDrive - Claro SA/Documentos/dadoscbk/dados_tratados.csv")
df2 = pd.read_csv("C:/Users/Z550647/OneDrive - Claro SA/Documentos/dadoscbk/predicoes_cbk_com_risco.csv")

# Pré-processamento comum
df['Dia'] = pd.to_datetime(df['Dia'], errors='coerce')
df['Hora'] = pd.to_datetime(df['Hora'], errors='coerce')
df['BIN'] = df['Cartão'].astype(str).str[:6]
df['HoraNum'] = df['Hora'].dt.hour

# Segmentação por faixa de valor
faixas = [0, 50, 100, 200, float('inf')]
labels = ['Até 50', '51-100', '101-200', 'Acima de 200']
df['Faixa_Valor'] = pd.cut(df['Valor'], bins=faixas, labels=labels, include_lowest=True)
distribuicao_faixas = df['Faixa_Valor'].value_counts().sort_index().reset_index()
distribuicao_faixas.columns = ['Faixa de Valor', 'Quantidade de Transações']

# Filtrar transações com CBK
df_cbk = df[df['CBK'].astype(str).str.upper() == 'SIM']
df_cbk['Faixa_Valor'] = pd.cut(df_cbk['Valor'], bins=faixas, labels=labels, include_lowest=True)

# Estatísticas CBK
volume_cbk = len(df_cbk)
media_cbk = df_cbk['Valor'].mean()
mediana_cbk = df_cbk['Valor'].median()
desvio_cbk = df_cbk['Valor'].std()

# Frequências CBK
horas_cbk = df_cbk['HoraNum'].value_counts().sort_index()
horas_cbk_formatadas = [f"{h:02d}h" for h in horas_cbk.index]
bins_cbk = df_cbk['BIN'].value_counts().head(10).reset_index()
bins_cbk.columns = ['BIN', 'Quantidade de CBKs']
faixas_cbk = df_cbk['Faixa_Valor'].value_counts().sort_index().reset_index()
faixas_cbk.columns = ['Faixa de Valor', 'Quantidade de CBKs']

# Interface Streamlit
st.title("Case de Chargebacks - Ecommerce")
st.subheader("Comportamento Transacional")

st.markdown("""
Comportamento transacional dos clientes, identificando padrões de valor, 
frequência, horário e recorrência de cartões e BINs.
""")

# Resumo estatístico geral
st.subheader("Resumo Estatístico")
st.markdown(f"**Volume total de transações:** {len(df)}")
st.markdown(f"**Média dos valores:** R${df['Valor'].mean():.2f}")
st.markdown(f"**Mediana dos valores:** R${df['Valor'].median():.2f}")
st.markdown(f"**Desvio padrão:** R${df['Valor'].std():.2f}")

# Gráficos e tabelas
st.subheader("Volume de Transações por Dia")
dias_freq = df['Dia'].dt.date.value_counts().sort_values(ascending=False)
fig_dias = px.bar(x=dias_freq.index, y=dias_freq.values,
                  labels={'x': 'Data', 'y': 'Número de Transações'},
                  text=dias_freq.values)
fig_dias.update_traces(textposition="outside")
st.plotly_chart(fig_dias)

st.subheader("Top 10 Cartões mais Recorrentes")
cartoes_freq = df['Cartão'].value_counts().head(10)
fig_cartoes = px.bar(x=cartoes_freq.index, y=cartoes_freq.values,
                     labels={'x': 'Cartão', 'y': 'Número de Transações'},
                     text=cartoes_freq.values)
fig_cartoes.update_traces(textposition='outside')
st.plotly_chart(fig_cartoes)

st.subheader("Volumetria por Horários")
horas_freq = df['HoraNum'].value_counts().sort_index()
horas_formatadas = [f"{h:02d}h" for h in horas_freq.index]
fig_horas = px.bar(x=horas_formatadas, y=horas_freq.values,
                   labels={'x': 'Hora do Dia', 'y': 'Número de Transações'},
                   text=horas_freq.values)
fig_horas.update_traces(textposition='outside')
st.plotly_chart(fig_horas)

st.subheader("Tabela Interativa de BINs Mais Recorrentes")
bin_freq = df['BIN'].value_counts().reset_index()
bin_freq.columns = ['BIN', 'Quantidade de Transações']
st.dataframe(bin_freq.head(10))

st.subheader("Distribuição de Transações por Faixa de Valor")
st.dataframe(distribuicao_faixas)

# Perfil CBK
st.subheader("Perfil das Transações que Retornaram Chargeback")
st.markdown(f"**Volume total de transações com CBK:** {volume_cbk}")
st.markdown(f"**Média dos valores:** R${media_cbk:.2f}")
st.markdown(f"**Mediana dos valores:** R${mediana_cbk:.2f}")
st.markdown(f"**Desvio padrão:** R${desvio_cbk:.2f}")

st.subheader("Horários mais recorrentes com CBK")
fig_cbk_horas = px.bar(x=horas_cbk_formatadas, y=horas_cbk.values,
                       labels={'x': 'Hora do Dia', 'y': 'CBKs'},
                       text=horas_cbk.values)
fig_cbk_horas.update_traces(textposition='outside')
st.plotly_chart(fig_cbk_horas)

st.subheader("BINs mais recorrentes com CBK")
st.dataframe(bins_cbk)

st.subheader("Distribuição por Faixa de Valor com CBK")
fig_cbk_faixas = px.bar(faixas_cbk, x='Faixa de Valor', y='Quantidade de CBKs',
                        text='Quantidade de CBKs',
                        labels={'Faixa de Valor': 'Faixa de Valor', 'Quantidade de CBKs': 'CBKs'})
fig_cbk_faixas.update_traces(textposition='outside')
st.plotly_chart(fig_cbk_faixas)

# 🔮 Método preditivo aplicado à Aba 2
st.subheader("Predição de Chargebacks em Transações Futuras (Aba 2)")

# Pré-processamento Aba 2
df2['BIN'] = df2['Cartão'].astype(str).str[:6]
df2['BIN_cod'] = df2['BIN'].astype('category').cat.codes
df2['Cartao_cod'] = df2['Cartão'].astype('category').cat.codes
df2['HoraNum'] = pd.to_datetime(df2['Hora'], errors='coerce').dt.hour

# Distribuição por faixa
contagem_risco = df2['Faixa_Risco'].value_counts().reset_index()
contagem_risco.columns = ['Faixa de Risco', 'Quantidade']

# Gráfico
fig_risco = px.bar(contagem_risco, x='Faixa de Risco', y='Quantidade', color='Faixa de Risco',
                   title='Distribuição das Transações Futuras por Faixa de Risco',
                   text='Quantidade')
fig_risco.update_traces(textposition='outside')
st.plotly_chart(fig_risco)

# Tabela de transações de alto risco
st.subheader("Transações Futuras com Alto Risco de Chargeback")
st.dataframe(df2[df2['Faixa_Risco'] == 'Alto'][['Dia', 'Hora', 'Valor', 'Cartão', 'CBK_prob']].head(10))