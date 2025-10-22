import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from imblearn.over_sampling import SMOTE

# Carregar dados de treinamento
df_train = pd.read_csv("dados_tratados_com_tags_cbk.csv", encoding='latin1')

# Corrigir codificação da coluna CBK
df_train['CBK'] = df_train['CBK'].astype(str).str.encode('latin1').str.decode('utf-8', errors='ignore')
df_train['CBK'] = df_train['CBK'].str.strip().str.lower().replace({
    'não': 'nao', 'nã£o': 'nao', 'nãâ£o': 'nao', 'sim': 'sim'
})

# Criar variável alvo binária
df_train['CBK_flag'] = (df_train['CBK'] == 'sim').astype(int)

# Selecionar variáveis preditoras
features = [
    'Valor', 'Hora_H', 'Risco_Horario_Alto', 'Risco_Valor_Alto',
    'Risco_Cartao_Recorrente', 'Risco_BIN_Alto', 'Risco_Combinado'
]
X = df_train[features]
y = df_train['CBK_flag']

# Aplicar SMOTE para balanceamento
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

# Treinar modelo Random Forest
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_resampled, y_resampled)

# Carregar nova planilha para previsão
df_new = pd.read_csv("dados_tratados_com_tags_ajustado_2.csv", encoding='latin1')

# Prever CBK futuro
X_new = df_new[features]
df_new['CBK_Previsto'] = rf_model.predict(X_new)

# Salvar resultados
df_new.to_csv("planilha_2_com_previsao_cbk.csv", index=False)
print("Arquivo com previsões salvo como 'planilha_2_com_previsao_cbk.csv'")