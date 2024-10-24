# -*- coding: utf-8 -*-
"""Aula2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1kmNec7HURU7u8O3Yd_IiEEy-WLlp45f9

### Preparando o ambiente
"""

# Montando o Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/drive/MyDrive/pasta

import os
print(os.getcwd())

!ls

"""# Passo a Passo da Análise de Dados Completa

Para esta análise completa, vamos usar a base de dados "Heart Disease UCI" do Kaggle, que contém dados relacionados a fatores de risco e ocorrências de doenças cardíacas. O objetivo é demonstrar como realizar uma análise de dados desde a extração, limpeza, tratamento e análise estatística, incluindo testes de hipótese.

Link para o dataset: Heart Disease UCI Dataset

## 1. Extração dos Dados

Vamos começar baixando a base de dados do Kaggle e carregando os dados em um DataFrame do pandas.

### Importando bibliotecas
"""

import kagglehub
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

"""### Extraindo os dados"""

# Download latest version
path = kagglehub.dataset_download("ketangangal/heart-disease-dataset-uci")

print("Path to dataset files:", path)

# Carregando a base de clientes
dados = pd.read_csv('/root/.cache/kagglehub/datasets/ketangangal/heart-disease-dataset-uci/versions/1/HeartDiseaseTrain-Test.csv')

# Visualizar os primeiros registros
dados.head()

"""## 2. Limpeza e Tratamento dos Dados"""

# Verificar se há valores ausentes
print(dados.isnull().sum())

# Verificar valores duplicados
print(f"Valores duplicados: {dados.duplicated().sum()}")

# Remover valores duplicados, se existirem
dados.drop_duplicates(inplace=True)

# Resumo estatístico dos dados
dados.describe()

"""## 3. Entendimento das Variáveis

Vamos examinar algumas variáveis importantes e entender como elas se relacionam com a ocorrência de doenças cardíacas (variável target).
"""

# Plotar a distribuição de idade dos pacientes
plt.figure(figsize=(8,5))
sns.histplot(dados['age'], kde=True, bins=30)
plt.title('Distribuição de Idade dos Pacientes')
plt.show()

# Análise da variável alvo (target)
sns.countplot(x='target', data=dados)
plt.title('Distribuição da Doença Cardíaca')
plt.show()

# Matriz de correlação
plt.figure(figsize=(10,8))
# Select only numeric columns for correlation calculation
numeric_data = dados.select_dtypes(include=np.number)
sns.heatmap(numeric_data.corr(), annot=True, fmt='.2f', cmap='coolwarm')
plt.title('Matriz de Correlação')
plt.show()

"""## 4. Pré-processamento dos Dados

Aqui vamos realizar uma transformação em algumas variáveis que precisam ser ajustadas para a análise. Além disso, vamos normalizar colunas que possuem valores em diferentes escalas.
"""

# Normalizar as colunas com diferentes escalas (como idade e colesterol)
from sklearn.preprocessing import StandardScaler

# Normalizar colunas que estão em diferentes escalas
scaler = StandardScaler()

dados[[ 'cholestoral', 'resting_blood_pressure', 'Max_heart_rate']] = scaler.fit_transform(dados[['cholestoral', 'resting_blood_pressure', 'Max_heart_rate']])

# Verificar os dados após a normalização
dados.head()





"""## Passo 5: Análise Estatística: Teste de Hipóteses e Probabilidade"""

from scipy import stats

"""Teste de Hipótese 1: Frequência Cardíaca Máxima (Max_heart_rate)




"""

# Separar os grupos
thalach_com_doenca = dados[dados['target'] == 1]['Max_heart_rate']
thalach_sem_doenca = dados[dados['target'] == 0]['Max_heart_rate']

# Teste T de duas amostras
t_stat, p_value = stats.ttest_ind(thalach_com_doenca, thalach_sem_doenca)

# Interpretação
if p_value < 0.05:
    print("Rejeitamos a hipótese nula: Há uma diferença significativa na frequência cardíaca máxima.")
else:
    print("Não rejeitamos a hipótese nula: Não há diferença significativa na frequência cardíaca máxima.")

"""Teste de Hipótese 2: Níveis de Colesterol (chol)

"""

# Separar os grupos
chol_com_doenca = dados[dados['target'] == 1]['cholestoral']
chol_sem_doenca = dados[dados['target'] == 0]['cholestoral']

# Teste T de duas amostras
t_stat, p_value = stats.ttest_ind(chol_com_doenca, chol_sem_doenca)

print(f"Estatística T: {t_stat}")

# Interpretação
if p_value < 0.05:
    print("Rejeitamos a hipótese nula: Há uma diferença significativa nos níveis de colesterol.")
else:
    print("Não rejeitamos a hipótese nula: Não há diferença significativa nos níveis de colesterol.")

"""## Passo 6: Probabilidade e Distribuições"""

# Probabilidade de doença cardíaca em pacientes acima de 50 anos
idade_acima_50 = dados[dados['age'] > 50]
prob_doenca_acima_50 = idade_acima_50['target'].mean()

print(f"Probabilidade de ter doença cardíaca em pacientes acima de 50 anos: {prob_doenca_acima_50:.2%}")

"""## Passo 7: Conclusão e Storytelling

***Introdução ao Contexto:***

Nosso objetivo é entender os fatores que influenciam o diagnóstico de doenças cardíacas, identificando quais variáveis são mais indicativas de risco e quais podem ser usadas para prever essa condição.

Para isso, analisamos dados de pacientes com diversas informações clínicas e comportamentais, como idade, níveis de colesterol, frequência cardíaca máxima, entre outros.

***1. Teste de Hipóteses: Avaliação dos Fatores Clínicos***

Através dos testes de hipóteses, pudemos investigar a relevância de diferentes variáveis no diagnóstico de doenças cardíacas. Vamos apresentar os principais achados:

  - Frequência Cardíaca Máxima: Um Indicador Importante A análise mostrou que existe uma diferença estatisticamente significativa na frequência cardíaca máxima alcançada entre pacientes com e sem doença cardíaca. Isso sugere que a frequência cardíaca máxima é um fator relevante na identificação de risco cardíaco.
  
  Para ilustrar, vamos observar o gráfico abaixo:
"""

plt.figure(figsize=(10, 6))
sns.boxplot(x='target', y='Max_heart_rate', data=dados)
plt.title('Distribuição da Frequência Cardíaca Máxima entre Grupos com e sem Doença Cardíaca')
plt.xlabel('Diagnóstico de Doença Cardíaca (0 = Não, 1 = Sim)')
plt.ylabel('Frequência Cardíaca Máxima')
plt.show()

"""O gráfico de boxplot acima revela que os pacientes com diagnóstico positivo para doença cardíaca tendem a ter uma frequência cardíaca máxima mais baixa em comparação com aqueles sem a condição. Isso sugere que a limitação na capacidade de aumentar a frequência cardíaca durante o esforço pode ser um indicador de doença cardíaca.

***2. Análise de Probabilidade: Idade como Fator Crítico***

A análise probabilística indica que a idade desempenha um papel crucial no risco de desenvolver doenças cardíacas. Pacientes acima de 50 anos apresentam uma probabilidade consideravelmente maior de diagnóstico positivo para a condição. A idade surge, então, como um fator determinante, o que reforça a importância de iniciativas preventivas voltadas para essa faixa etária.

  - Gráfico de Distribuição por Faixa Etária Para visualizarmos melhor essa correlação, a distribuição de pacientes com doença cardíaca por faixa etária é apresentada a seguir:
"""

plt.figure(figsize=(10, 6))
sns.histplot(data=dados[dados['target'] == 1], x='age', bins=10, kde=True)
plt.title('Distribuição de Pacientes com Doença Cardíaca por Faixa Etária')
plt.xlabel('Idade')
plt.ylabel('Frequência')
plt.show()

"""O gráfico de distribuição mostra uma concentração mais alta de casos de doença cardíaca em pacientes com mais de 50 anos, enfatizando que a idade é um fator de risco importante.

### Storytelling: De Dados a Decisões

***1. Cenário Atual:***

As doenças cardíacas são uma das principais causas de mortalidade, e entender os fatores de risco pode ajudar a salvar vidas. Nossa análise focou em variáveis como idade, colesterol e frequência cardíaca para identificar padrões e fatores preditivos.

***2. Exploração dos Dados:***

Analisamos os dados de pacientes com e sem diagnóstico de doença cardíaca para identificar quais variáveis se mostravam mais relevantes. Nossos testes de hipóteses foram aplicados para validar essas variáveis estatisticamente.

***3. Principais Descobertas:***

 - A frequência cardíaca máxima mostrou-se significativamente diferente entre os grupos, sugerindo que limitações na capacidade de aumentar a frequência cardíaca podem indicar maior risco cardíaco.

 - Os níveis de colesterol, embora considerados comumente um fator de risco, não apresentaram diferença significativa entre os grupos analisados.

- Pacientes acima de 50 anos apresentam uma maior probabilidade de desenvolver a condição, destacando a idade como um fator importante.

***4.Implicações para o Futuro:***

 - Programas de rastreamento mais rigorosos para pessoas acima de 50 anos podem ajudar a detectar a doença mais cedo.

- Monitoramento contínuo da frequência cardíaca máxima durante avaliações de saúde pode ser utilizado como parte de um protocolo preventivo.

- A inclusão de outros fatores e comportamentos no modelo de análise pode melhorar ainda mais a precisão do diagnóstico.

***5. Próximos Passos:***

Com base nos resultados, recomendamos ajustes nas políticas de saúde e prevenção, além de maior ênfase no monitoramento dos fatores críticos identificados, visando à redução do risco de doenças cardíacas na população.
"""





