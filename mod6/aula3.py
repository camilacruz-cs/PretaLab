# -*- coding: utf-8 -*-
"""aula3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1XPPjZ2596EvNYCFbthFzQX-czop8oplv

### Preparando o ambiente
"""

# Montando o Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/drive/MyDrive/Cic

import os
print(os.getcwd())

!ls



"""# Análise de dados do Mundo Real

Para esta aula vamos realizar uma análise completa com base de dados de saúde mental na indústria de tecnologia, começaremos com a extração dos dados utilizando o KaggleHub. Faremos o download da base, organizaremos e armazenaremos os dados em um banco de dados SQLite, e finalmente realizaremos as etapas de análise, desde a limpeza até a aplicação de testes de hipóteses, probabilidade e visualizações.

Conjunto de dados: [Saude Mental](https://https://www.kaggle.com/datasets/anth7310/mental-health-in-the-tech-industry)

## Extração dos Dados
"""

import kagglehub

# Download do dataset da saúde mental na indústria de tecnologia
path = kagglehub.dataset_download("anth7310/mental-health-in-the-tech-industry")

print("Path to dataset files:", path)

/root/.cache/kagglehub/datasets/anth7310/mental-health-in-the-tech-industry/versions/7

"""## Abrir e Manipular o Banco de Dados SQLite

Depois de baixar o dataset, que já está no formato SQLite, podemos abrir o banco de dados e copiar suas tabelas para um novo banco de dados local.
"""

import sqlite3
import os

# Caminho do banco de dados baixado
db_path = os.path.join(path, "mental_health.sqlite")

# Conectar ao banco de dados baixado
conn_original = sqlite3.connect(db_path)
cursor_original = conn_original.cursor()

# Exibir as tabelas disponíveis no banco de dados
cursor_original.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor_original.fetchall()
print(f"Tabelas disponíveis: {tables}")

"""## Consultas e Cruzamentos no Banco de Dados

Nesta etapa, faremos consultas no banco de dados para obter informações sobre idade, gênero, e tratamento de saúde mental. Estamos interessados em observar como esses fatores interagem.
"""

# Consultar a estrutura das tabelas
cursor_original.execute("PRAGMA table_info('Answer')")
print(cursor_original.fetchall())

cursor.execute("PRAGMA table_info('Question')")
print(cursor.fetchall())

cursor.execute("PRAGMA table_info('Survey')")
print(cursor.fetchall())

# Consultar dados de respostas sobre gênero, idade e saúde mental
query = '''
    SELECT s.survey_date, q.question_text, a.answer_text
    FROM Answer a
    JOIN Question q ON a.question_id = q.id
    JOIN Survey s ON a.survey_id = s.id
    WHERE q.question_text IN ('Age', 'Gender', 'Do you seek treatment for mental health?');
'''

df_answers = pd.read_sql_query(query, conn)
df_answers.head()

df_answers = pd.read_sql_query(query, conn)
df_answers.head()

"""## Análise Estátistica

Vamos filtrar os dados para analisar separadamente aqueles que procuram tratamento de saúde mental e segmentar os dados por gênero e idade
"""

# Filtrando apenas aqueles que procuraram tratamento
df_treatment_yes = df_answers[df_answers['answer_text'] == 'Yes']

# Filtrando apenas aqueles que não procuraram tratamento
df_treatment_no = df_answers[df_answers['answer_text'] == 'No']

df_treatment_yes.head()

df_treatment_no.head()

"""Estatísticas Descritivas com Média, Mediana e Contagem"""

# Agrupando por gênero para calcular a média e mediana de idade para aqueles que buscaram tratamento
media_idade_tratamento_sim = df_treatment_yes.groupby('Gender')['Age'].mean()
mediana_idade_tratamento_sim = df_treatment_yes.groupby('Gender')['Age'].median()

# Agrupando por gênero para calcular a média e mediana de idade para aqueles que não buscaram tratamento
media_idade_tratamento_nao = df_treatment_no.groupby('Gender')['Age'].mean()
mediana_idade_tratamento_nao = df_treatment_no.groupby('Gender')['Age'].median()

print("Média de idade (procuraram tratamento):")
print(media_idade_tratamento_sim)
print("\nMediana de idade (procuraram tratamento):")
print(mediana_idade_tratamento_sim)

print("\nMédia de idade (não procuraram tratamento):")
print(media_idade_tratamento_nao)
print("\nMediana de idade (não procuraram tratamento):")
print(mediana_idade_tratamento_nao)

"""Contagem de Pessoas por Gênero"""

# Contagem de pessoas por gênero que procuraram tratamento
contagem_tratamento_sim = df_treatment_yes['Gender'].value_counts()

# Contagem de pessoas por gênero que não procuraram tratamento
contagem_tratamento_nao = df_treatment_no['Gender'].value_counts()

print("\nContagem de pessoas que procuraram tratamento:")
print(contagem_tratamento_sim)

print("\nContagem de pessoas que não procuraram tratamento:")
print(contagem_tratamento_nao)

"""Visualizando a Distribuição de Idades"""

import seaborn as sns
import matplotlib.pyplot as plt

# Visualizando a distribuição de idades para quem procurou e quem não procurou tratamento
plt.figure(figsize=(12, 6))
sns.histplot(df_treatment_yes['Age'], color='green', kde=True, label='Procuraram Tratamento')
sns.histplot(df_treatment_no['Age'], color='red', kde=True, label='Não Procuraram Tratamento')

plt.title('Distribuição de Idades por Busca de Tratamento de Saúde Mental')
plt.xlabel('Idade')
plt.ylabel('Frequência')
plt.legend()
plt.show()

"""Cálculo de Probabilidade"""

# Calcular a probabilidade de uma pessoa procurar tratamento com base no gênero
prob_tratamento_genero = df_treatment_yes['Gender'].value_counts() / df_answers['Gender'].value_counts()
print(f'Probabilidade de procurar tratamento por gênero:\n{prob_tratamento_genero}')

# Definir faixas etárias para análise
bins = [18, 25, 35, 45, 55, 65, 100]
labels = ['18-25', '26-35', '36-45', '46-55', '56-65', '65+']

df_answers['faixa_etaria'] = pd.cut(df_answers['Age'], bins=bins, labels=labels, right=False)

# Calcular a probabilidade de procurar tratamento por faixa etária
prob_tratamento_faixa = df_answers[df_answers['answer_text'] == 'Yes']['faixa_etaria'].value_counts() / df_answers['faixa_etaria'].value_counts()
print(f'Probabilidade de procurar tratamento por faixa etária:\n{prob_tratamento_faixa}')

"""Testes de Hipóteses (ANOVA)"""

from scipy import stats

# Realizar ANOVA para comparar a idade média entre diferentes gêneros
anova_result = stats.f_oneway(
    df_treatment_yes[df_treatment_yes['Gender'] == 'Male']['Age'],
    df_treatment_yes[df_treatment_yes['Gender'] == 'Female']['Age'],
    df_treatment_yes[df_treatment_yes['Gender'] == 'Other']['Age']
)

print(f'Resultado ANOVA: {anova_result}')