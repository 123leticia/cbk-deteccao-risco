import pandas as pd

# 1. Carregar o arquivo com previsões
df = pd.read_csv("predicoes_cbk.csv")

# 2. Função para classificar risco
def classificar_risco(prob):
    if prob >= 0.8:
        return 'Alto'
    elif prob >= 0.5:
        return 'Moderado'
    else:
        return 'Baixo'

# 3. Adicionar coluna Faixa_Risco
df['Faixa_Risco'] = df['CBK_prob'].apply(classificar_risco)

# 4. Gerar distribuição das faixas de risco
distribuicao = df['Faixa_Risco'].value_counts().reset_index()
distribuicao.columns = ['Faixa de Risco', 'Quantidade']
print(distribuicao)

# 5. Salvar novo arquivo com Faixa_Risco
df.to_csv("predicoes_cbk_com_risco.csv", index=False)
print("Arquivo 'predicoes_cbk_com_risco.csv' gerado com sucesso.")