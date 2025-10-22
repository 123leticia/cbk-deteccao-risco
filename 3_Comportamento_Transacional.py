import streamlit as st
import pandas as pd
import plotly.express as px

# Exibir logo na barra lateral
st.sidebar.image("C:/Users/Z550647/OneDrive - Claro SA/Documentos/dadoscbk/image.png", width=90)

# Menu de navegação
opcao = st.sidebar.radio("Escolha uma seção:", [
    "Objetivo da análise",
    "Análise do comportamento transacional",
    "Perfil das transações com chargeback",
    "Modelo preditivo e resultados",
    "Regras de negócio e impacto estimado",
    "Conclusão e recomendações"
])

# Título principal
st.title("Case de Detecção de Comportamento de Risco em Transações com Chargeback")

# Carregar os dados
df = pd.read_csv("C:/Users/Z550647/OneDrive - Claro SA/Documentos/dadoscbk/dados_tratados_com_tags_ajustado.csv")
df['DataHora'] = pd.to_datetime(df['DataHora'])
df['DiaFormatada'] = df['DataHora'].dt.strftime('%d/%m')

if opcao == "Objetivo da análise":
    st.write(
        "Esta análise tem como objetivo identificar comportamentos transacionais suspeitos que possam indicar risco de chargeback. "
        "Através da exploração de dados históricos, buscamos padrões e variáveis relevantes para apoiar a construção de modelos preditivos "
        "e a definição de regras de negócio voltadas à prevenção de fraudes."
    )

elif opcao == "Análise do comportamento transacional":
    st.write("Nesta seção, analisamos o comportamento das transações ao longo do tempo, identificando tendências e sazonalidades.")

    # Volumetria dos tipos de comportamento de risco
    colunas_risco = [
        'Risco_Horario_Alto',
        'Risco_Valor_Alto',
        'Risco_Cartao_Recorrente',
        'Risco_BIN_Alto'
    ]
    volumetria = {col: df[col].sum() for col in colunas_risco}
    volumetria_df = pd.DataFrame(list(volumetria.items()), columns=['Tipo de Risco', 'Quantidade'])
    fig = px.bar(volumetria_df, x='Tipo de Risco', y='Quantidade', text='Quantidade',
                 title='Volumetria dos Tipos de Comportamento de Risco')
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig)

    # Volumetria por horário
    volumetria_horario = df.groupby('Hora_H').size().reset_index(name='Quantidade')
    volumetria_horario['HoraFormatada'] = volumetria_horario['Hora_H'].astype(str) + 'h'
    fig1 = px.bar(volumetria_horario, x='HoraFormatada', y='Quantidade', text='Quantidade',
                  title='Volumetria por Horário')
    fig1.update_traces(textposition='outside')
    st.plotly_chart(fig1)

    st.markdown("**TAG utilizada: Risco_Horario_Alto**")
    st.write("Transações realizadas entre 00h e 06h são consideradas de alto risco de horário.")

    # Volumetria por dia - Risco Valor Alto
    valor_alto_df = df[df['Risco_Valor_Alto'] == True]
    volumetria_valor_alto = valor_alto_df.groupby('DiaFormatada').size().reset_index(name='Quantidade')
    fig2 = px.bar(volumetria_valor_alto, x='DiaFormatada', y='Quantidade', text='Quantidade',
                  title='Volumetria por Dia - Risco Valor Alto')
    fig2.update_traces(textposition='outside')
    st.plotly_chart(fig2)

    st.markdown("**TAG utilizada: Risco_Valor_Alto**")
    st.write("Transações com valor acima do percentil 90 (top 10%) são consideradas de alto risco de valor.")

    # Volumetria por dia - Cartão Recorrente
    cartao_recorrente_df = df[df['Risco_Cartao_Recorrente'] == True]
    volumetria_cartao = cartao_recorrente_df.groupby('DiaFormatada').size().reset_index(name='Quantidade')

    todos_os_dias = pd.DataFrame({'DiaFormatada': df['DiaFormatada'].unique()})
    volumetria_cartao = todos_os_dias.merge(volumetria_cartao, on='DiaFormatada', how='left').fillna(0)

    fig3 = px.bar(volumetria_cartao, x='DiaFormatada', y='Quantidade', text='Quantidade',
                  title='Volumetria por Dia - Cartão Recorrente')
    fig3.update_traces(textposition='outside')
    st.plotly_chart(fig3)

    st.markdown("**TAG utilizada: Risco_Cartao_Recorrente**")
    st.write("Cartões com mais de 10 transações em um único dia são considerados recorrentes.")

    # Tabela de BIN por quantidade
    bin_table = df['BIN'].value_counts().reset_index()
    bin_table.columns = ['BIN', 'Quantidade']
    st.subheader("Top 10 BINs por Quantidade de Transações")
    st.dataframe(bin_table.head(10))

    st.markdown("**TAG utilizada: Risco_BIN_Alto**")
    st.write("BINs mais frequentes no conjunto de dados são considerados de alto risco.")

elif opcao == "Perfil das transações com chargeback":
    st.header("Perfil das transações com chargeback")
    st.write("Aqui exploramos as características das transações que resultaram em chargeback, buscando entender os fatores que contribuem para esse tipo de ocorrência.")

elif opcao == "Modelo preditivo e resultados":
    st.header("Modelo preditivo e resultados")
    st.write("Apresentamos os resultados do modelo preditivo desenvolvido para antecipar transações com risco de chargeback.")

elif opcao == "Regras de negócio e impacto estimado":
    st.header("Regras de negócio e impacto estimado")
    st.write("Discussão sobre as regras de negócio propostas com base na análise e os impactos esperados na operação.")

elif opcao == "Conclusão e recomendações":
    st.header("Conclusão e recomendações")
    st.write("Resumo dos principais achados da análise e recomendações para mitigação de riscos e melhoria dos processos.")