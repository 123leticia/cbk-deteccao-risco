import streamlit as st
import pandas as pd
import plotly.express as px

# Exibir logo na barra lateral
st.sidebar.image("assets/imagem.png", width=9)

# Menu de navegação
opcao = st.sidebar.radio("Escolha uma seção:", [
    "Objetivo da análise",
    "Análise do comportamento transacional",
    "Perfil das transações com chargeback",
    "Modelo preditivo e resultados",
    "Regras de negócio e impacto estimado"
])

# Título principal
st.title("Case de Detecção de Comportamento de Risco em Transações com Chargeback")

# Variáveis globais para a aba "Regras de negócio e impacto estimado"
df_modelo = pd.read_csv("planilha_2_com_previsao_cbk.csv")
cbk_predicted = df_modelo[df_modelo['CBK_Previsto'] == 1].copy()

risk_tags = ['Risco_Horario_Alto', 'Risco_Valor_Alto', 'Risco_Cartao_Recorrente', 'Risco_BIN_Alto', 'Risco_Combinado']
cbk_predicted['Num_TAGs'] = cbk_predicted[risk_tags].sum(axis=1)
tag_distribution = cbk_predicted['Num_TAGs'].value_counts().sort_index()

risk_tags_filtered = ['Risco_Horario_Alto', 'Risco_Valor_Alto', 'Risco_Cartao_Recorrente', 'Risco_BIN_Alto']
tag_type_counts_filtered = cbk_predicted[risk_tags_filtered].sum().sort_values(ascending=False)

if opcao == "Objetivo da análise":
    st.write(
        "Esta análise tem como objetivo identificar comportamentos transacionais suspeitos que possam indicar risco de chargeback. "
        "Através da exploração de dados históricos, foi buscado padrões e variáveis relevantes para apoiar a construção de modelos preditivos "
        "e a definição de regras de negócio voltadas à prevenção de fraudes."
    )

elif opcao == "Análise do comportamento transacional":
    df = pd.read_csv("dados_tratados_com_tags_ajustado.csv")
    df['DataHora'] = pd.to_datetime(df['DataHora'])
    df['DiaFormatada'] = df['DataHora'].dt.strftime('%d/%m')
    df['Hora'] = df['DataHora'].dt.hour
    df['Risco_Horario_Alto'] = df['Hora'] < 6

    st.write("Nesta seção, foi analisado o comportamento das transações ao longo do tempo, identificando tendências e sazonalidades.")

    colunas_risco = ['Risco_Horario_Alto', 'Risco_Valor_Alto', 'Risco_Cartao_Recorrente', 'Risco_BIN_Alto']
    volumetria = {coluna: df[coluna].sum() for coluna in colunas_risco}
    volumetria_df = pd.DataFrame(list(volumetria.items()), columns=['TAG', 'Quantidade'])
    fig = px.bar(volumetria_df, x='TAG', y='Quantidade', text='Quantidade',
                 title='Volumetria dos Tipos de Comportamento de Risco')
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig)

    tabela_tags = pd.DataFrame({
        "TAG": colunas_risco,
        "Descrição": [
            "Transações realizadas entre 00h e 06h são consideradas de alto risco.",
            "Transações com valor acima do percentil 90 (top 10%) são consideradas de alto risco.",
            "Cartões com mais de 10 transações em um único dia são considerados recorrentes.",
            "BINs mais frequentes no conjunto de dados são considerados de alto risco."
        ]
    })
    st.markdown("**Regras utilizadas para definição das TAGs de risco:**")
    st.dataframe(tabela_tags)

    transacoes_madrugada = df[df['Hora'] < 6]
    volumetria_madrugada = transacoes_madrugada.groupby('DiaFormatada').size().reset_index(name='Quantidade')
    fig1 = px.bar(volumetria_madrugada, x='DiaFormatada', y='Quantidade', text='Quantidade',
                  title='Volumetria de Transações entre 00h e 06h')
    fig1.update_traces(textposition='outside')
    st.plotly_chart(fig1)

    st.markdown("**TAG utilizada: Risco_Horario_Alto**")
    st.write("Este gráfico mostra a quantidade de transações realizadas entre 00h e 06h, consideradas de alto risco.")

    valor_alto_df = df[df['Risco_Valor_Alto'] == True]
    volumetria_valor_alto = valor_alto_df.groupby('DiaFormatada').size().reset_index(name='Quantidade')
    fig2 = px.bar(volumetria_valor_alto, x='DiaFormatada', y='Quantidade', text='Quantidade',
                  title='Volumetria por Dia - Risco Valor Alto')
    fig2.update_traces(textposition='outside')
    st.plotly_chart(fig2)

    st.markdown("**TAG utilizada: Risco_Valor_Alto**")
    st.write("Transações com valor acima do percentil 90 (top 10%) são consideradas de alto risco de valor.")

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

    bin_table = df['BIN'].value_counts().reset_index()
    bin_table.columns = ['BIN', 'Quantidade']
    st.subheader("Top 10 BINs por Quantidade de Transações")
    st.dataframe(bin_table.head(10))

    st.markdown("**TAG utilizada: Risco_BIN_Alto**")
    st.write("BINs mais frequentes no conjunto de dados são considerados de alto risco.")

elif opcao == "Perfil das transações com chargeback":
    st.write("Aqui foi explorado as características das transações que resultaram em chargeback, buscando entender os fatores que contribuem para esse tipo de ocorrência.")

    cbk_df = pd.read_csv("dados_tratados_com_tags_cbk.csv")
    cbk_df['DataHora'] = pd.to_datetime(cbk_df['DataHora'])
    cbk_df['DiaFormatada'] = cbk_df['DataHora'].dt.strftime('%d/%m')
    cbk_df['CBK'] = cbk_df['CBK'].astype(str).str.strip().str.lower()
    cbk_sim = cbk_df[cbk_df['CBK'] == 'sim']

    tags_cbk = ['CBK_Horario_Alto', 'CBK_Valor_Alto', 'CBK_BIN_Frequente', 'CBK_Cartao_Recorrente']
    volumetria_cbk = {tag: cbk_sim[tag].sum() for tag in tags_cbk}
    volumetria_cbk_df = pd.DataFrame(list(volumetria_cbk.items()), columns=['TAG_CBK', 'Quantidade'])

    fig_cbk = px.bar(volumetria_cbk_df, x='TAG_CBK', y='Quantidade', text='Quantidade',
                     title='Volumetria por TAG de CBK')
    fig_cbk.update_traces(textposition='outside')
    st.plotly_chart(fig_cbk)

    resumo_tags = pd.DataFrame({
        'TAG_CBK': tags_cbk,
        'Descrição': [
            'Transações com chargeback realizadas entre 00h e 06h.',
            'Transações com chargeback com valor acima do percentil 90.',
            'Transações com chargeback de BINs mais frequentes.',
            'Transações com chargeback de cartões com mais de 10 transações no mesmo dia.'
        ]
    })
    st.markdown("**Resumo das TAGs de CBK:**")
    st.dataframe(resumo_tags)

    # Gráfico 1: CBK Horário de Risco por Dia
    cbk_horario = cbk_sim[cbk_sim['CBK_Horario_Alto'] == True]
    vol_cbk_horario = cbk_horario.groupby('DiaFormatada').size().reset_index(name='Quantidade')
    fig1 = px.bar(vol_cbk_horario, x='DiaFormatada', y='Quantidade', text='Quantidade',
                  title='Volumetria de CBK - Horário de Risco por Dia')
    fig1.update_traces(textposition='outside')
    st.plotly_chart(fig1)

    # Gráfico 2: CBK Valor Alto por Dia (Valor total)
    cbk_valor = cbk_sim[cbk_sim['CBK_Valor_Alto'] == True]
    vol_cbk_valor = cbk_valor.groupby('DiaFormatada').size().reset_index(name='Quantidade')
    fig2 = px.bar(vol_cbk_valor, x='DiaFormatada', y='Quantidade', text='Quantidade',
                  title='Quantidade de CBK - Valor Alto por Dia')
    fig2.update_traces(textposition='outside')
    st.plotly_chart(fig2)

    # Gráfico 3: CBK Cartão Recorrente por Dia (Quantidade de transações)
    cbk_cartao = cbk_sim[cbk_sim['CBK_Cartao_Recorrente'] == True]
    vol_cbk_cartao = cbk_cartao.groupby('DiaFormatada').size().reset_index(name='Quantidade')
    fig3 = px.bar(vol_cbk_cartao, x='DiaFormatada', y='Quantidade', text='Quantidade',
                  title='Quantidade de Cartões Únicos com CBK - Cartão Recorrente por Dia')
    fig3.update_traces(textposition='outside')
    st.plotly_chart(fig3)

    # Tabela de BINs frequentes
    bin_freq = cbk_sim[cbk_sim['CBK_BIN_Frequente'] == True]
    bin_table = bin_freq['BIN'].value_counts().reset_index()
    bin_table.columns = ['BIN', 'Quantidade']
    st.subheader("Top 10 BINs frequentes entre transações com CBK")
    st.dataframe(bin_table.head(10))

elif opcao == "Modelo preditivo e resultados":
    
    st.write("Para prever transações com risco de chargeback, foram testados três algoritmos de classificação:")

    st.markdown("""
    - **Random Forest**
    - **Logistic Regression**
    - **XGBoost**
    """)

    st.subheader("Desempenho inicial (sem balanceamento)")
    st.write("Apesar da alta acurácia geral (acima de 95%), os modelos apresentaram baixa capacidade de identificar transações com chargeback:")

    st.dataframe({
        "Modelo": ["Random Forest", "Logistic Regression", "XGBoost"],
        "Acurácia": ["96,2%", "95,2%", "95,8%"],
        "Recall (Chargeback)": ["46%", "6%", "33%"]
    })

    st.subheader("Após balanceamento das classes")
    st.write("Para melhorar a detecção da classe minoritária (chargeback), foram aplicadas técnicas de balanceamento:")

    st.markdown("""
    - **SMOTE** para Random Forest e XGBoost  
    - **class_weight='balanced'** para Logistic Regression
    """)

    st.write("Os resultados mostraram melhora significativa na sensibilidade dos modelos:")

    st.dataframe({
        "Modelo": [
            "Random Forest com SMOTE",
            "Logistic Regression com peso",
            "XGBoost com SMOTE"
        ],
        "Acurácia": ["90,6%", "66,1%", "89,2%"],
        "Recall (Chargeback)": ["93%", "81%", "93%"]
    })

    st.subheader("Comparativo visual de desempenho")
    st.image("comparativo_modelos_recall.png", caption="Recall por modelo antes e depois do balanceamento")

    # Informações gerais do modelo preditivo
    st.subheader("Resumo das Previsões do Modelo")
    st.write("Total de transações analisadas: 11.820")
    st.write("Transações previstas como chargeback: 1.333")
    st.write("Porcentagem prevista como chargeback: 11,28%")

    # Tabela de volumetria por número de TAGs de risco
    st.subheader("Volumetria das transações previstas como chargeback por número de TAGs de risco")
    tabela_volumetria = pd.DataFrame({
        'Número de TAGs de risco': [0, 1, 2, 3],
        'Quantidade de transações': [871, 391, 64, 7]
    })
    st.dataframe(tabela_volumetria)

    # Interpretação dos resultados
    st.subheader("Interpretação")
    st.markdown("""
    - **871 transações** não possuem nenhuma TAG de risco, mas ainda assim foram previstas como chargeback pelo modelo.  
    - **462 transações** possuem pelo menos uma TAG de risco (**391 com 1**, **64 com 2**, **7 com 3**).  
    - A presença de múltiplas TAGs (2 ou 3) indica **acúmulo de fatores de risco**, o que pode aumentar a probabilidade de fraude.
    """)

elif opcao == "Regras de negócio e impacto estimado":
    st.subheader("Resumo dos Resultados")

    st.markdown(f"""
    - **{tag_distribution.get(0, 0)}** transações previstas como CBK **não possuem nenhuma TAG de risco**.
    - **{cbk_predicted.shape[0] - tag_distribution.get(0, 0)}** transações possuem **pelo menos uma TAG de risco**:
        - **{tag_distribution.get(1, 0)}** com **1 TAG**
        - **{tag_distribution.get(2, 0)}** com **2 TAGs**
        - **{tag_distribution.get(3, 0)}** com **3 TAGs**
    """)

    st.subheader("Distribuição das Combinações de TAGs de Risco")
    tag_comb_table = cbk_predicted[['Risco_Horario_Alto', 'Risco_Valor_Alto', 'Risco_Cartao_Recorrente', 'Risco_BIN_Alto']].apply(
        lambda row: ', '.join([tag for tag in ['Risco_Horario_Alto', 'Risco_Valor_Alto', 'Risco_Cartao_Recorrente', 'Risco_BIN_Alto'] if row[tag]]),
        axis=1
    ).replace('', 'Sem TAG').value_counts().reset_index()
    tag_comb_table.columns = ['Combinação de TAGs', 'Quantidade de Transações']
    st.dataframe(tag_comb_table)

    st.subheader("Regras de Negócio por Tipo de TAG")
    st.markdown("""
    | Tipo de TAG | Ação recomendada |
    |-------------|------------------|
    | **Risco_Horario_Alto** | Monitorar horários críticos com maior incidência de fraude. Aplicar limites ou bloqueios. |
    | **Risco_Valor_Alto** | Solicitar autenticação adicional para valores altos. Implementar alertas em tempo real. |
    | **Risco_Cartao_Recorrente** | Verificar padrão de uso do cartão. Aplicar bloqueio temporário ou validação manual. |
    | **Risco_BIN_Alto** | Reforçar validações para BINs com histórico de fraude. Aplicar regras específicas por emissor. |
    """)

    st.subheader("Regras por Quantidade de TAGs")
    st.markdown("""
    - **1 TAG**: Aplicar alerta leve ou autenticação adicional.
    - **2 TAGs**: Aplicar bloqueio temporário ou exigir validação manual.
    - **3 TAGs ou mais**: Tratar como fraude potencial. Encaminhar para equipe de prevenção ou aplicar bloqueio automático.
    """)

    st.subheader("Sugestão de Regra de Negócio para Transações sem TAG")
    st.markdown(f"""
    Para as **{tag_distribution.get(0, 0)}** transações sem nenhuma TAG de risco, mas previstas como CBK:
    - Verificação biométrica (facial ou digital).
    - Autenticação multifator (MFA).
    - Monitoramento comportamental em tempo real.
    """)

    st.subheader("Impacto Estimado Financeiro das Transações CBK")

    impacto_df = cbk_predicted.copy()
    impacto_df['Qtd_TAGs'] = impacto_df[['Risco_Horario_Alto', 'Risco_Valor_Alto', 'Risco_Cartao_Recorrente', 'Risco_BIN_Alto']].sum(axis=1)

    impacto_financeiro = impacto_df.groupby('Qtd_TAGs').agg(
    Transacoes=('Valor', 'count'),
    Valor_Total=('Valor', 'sum')
    ).reset_index()

    valor_total_cbk = impacto_financeiro['Valor_Total'].sum()
    impacto_financeiro['% do Total'] = (impacto_financeiro['Valor_Total'] / valor_total_cbk * 100).round(2)

    impacto_financeiro['Categoria'] = impacto_financeiro['Qtd_TAGs'].map({
    0: 'CBK sem TAG',
    1: 'CBK com 1 TAG',
    2: 'CBK com 2 TAGs',
    3: 'CBK com 3 TAGs'
    }).fillna('CBK com 4+ TAGs')

    linha_total = pd.DataFrame({
    'Categoria': ['Total CBK'],
    'Transacoes': [impacto_financeiro['Transacoes'].sum()],
    'Valor_Total': [valor_total_cbk],
    '% do Total': [100.0]
    })

    impacto_financeiro = pd.concat([impacto_financeiro[['Categoria', 'Transacoes', 'Valor_Total', '% do Total']], linha_total], ignore_index=True)

    impacto_financeiro['Valor_Total'] = impacto_financeiro['Valor_Total'].apply(lambda x: f"{int(round(x)):,}".replace(",", "."))

    st.dataframe(impacto_financeiro)

    st.markdown("""
    ### Interpretação Estratégica com Percentuais

    - A maior parte do impacto financeiro está concentrada em transações **sem TAGs**, representando **84,65%** do total — indicando risco residual não capturado pelas regras atuais.
    - Transações com **1 TAG** representam apenas **2,36%**, sugerindo que regras leves podem ser suficientes.
    - Transações com **2 ou mais TAGs** somam cerca de **13%**, sendo casos prioritários para **bloqueio ou encaminhamento à equipe de prevenção**.
    - A análise reforça a importância de aplicar **regras escalonadas** conforme a quantidade de TAGs e **reforçar mecanismos adicionais** para transações sem TAGs (como biometria, MFA e monitoramento comportamental).

    """)

