import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, accuracy_score

# Carregar os dados
df = pd.read_csv("dados_tratados_com_tags_cbk.csv", encoding='latin1')

# Corrigir codificação da coluna CBK
df['CBK'] = df['CBK'].astype(str).str.encode('latin1').str.decode('utf-8', errors='ignore')
df['CBK'] = df['CBK'].str.strip().str.lower().replace({
    'não': 'nao', 'nã£o': 'nao', 'nãâ£o': 'nao', 'sim': 'sim'
})

# Criar variável alvo binária
df['CBK_flag'] = (df['CBK'] == 'sim').astype(int)

# Selecionar variáveis preditoras
features = [
    'Valor', 'Hora_H', 'Risco_Horario_Alto', 'Risco_Valor_Alto',
    'Risco_Cartao_Recorrente', 'Risco_BIN_Alto', 'Risco_Combinado'
]
X = df[features]
y = df['CBK_flag']

# Dividir em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Random Forest
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train, y_train)
rf_preds = rf_model.predict(X_test)
print("Random Forest Accuracy:", accuracy_score(y_test, rf_preds))
print("Random Forest Report:\n", classification_report(y_test, rf_preds))

# Logistic Regression
lr_model = LogisticRegression(max_iter=1000, random_state=42)
lr_model.fit(X_train, y_train)
lr_preds = lr_model.predict(X_test)
print("Logistic Regression Accuracy:", accuracy_score(y_test, lr_preds))
print("Logistic Regression Report:\n", classification_report(y_test, lr_preds))

# XGBoost
xgb_model = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
xgb_model.fit(X_train, y_train)
xgb_preds = xgb_model.predict(X_test)
print("XGBoost Accuracy:", accuracy_score(y_test, xgb_preds))
print("XGBoost Report:\n", classification_report(y_test, xgb_preds))