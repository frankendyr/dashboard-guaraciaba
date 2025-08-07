import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuração da página
st.set_page_config(page_title="Painel Educacional - Guaraciaba do Norte", layout="wide")

# Carregamento dos dados
@st.cache_data
def carregar_dados():
    df = pd.read_csv("dashboard_escolas_guaraciaba.csv")
    df.columns = df.columns.str.lower()  # padronizar nomes das colunas
    return df

df = carregar_dados()

# Filtrar escolas municipais
municipais = df[df['dependencia_administrativa'].str.upper() == 'MUNICIPAL']

# Indicadores principais
total_escolas = len(df)
total_municipais = len(municipais)
perc_municipais = (total_municipais / total_escolas) * 100

perc_urbana_municipais = (municipais['localizacao'].str.upper() == 'URBANA').mean() * 100
perc_rural_municipais = (municipais['localizacao'].str.upper() == 'RURAL').mean() * 100

st.title("📊 Painel Educacional - Guaraciaba do Norte (CE)")
st.markdown("### 🎯 Foco: Escolas Municipais")

col1, col2, col3 = st.columns(3)
col1.metric("Total de Escolas", total_escolas)
col2.metric("Qtd Municipais", total_municipais)
col3.metric("% Municipais", f"{perc_municipais:.1f}%")

col4, col5 = st.columns(2)
col4.metric("% Municipais Urbanas", f"{perc_urbana_municipais:.1f}%")
col5.metric("% Municipais Rurais", f"{perc_rural_municipais:.1f}%")


st.divider()
st.subheader("📌 Gráficos Simples")

# Gráfico 1 - Dependência Administrativa
st.markdown("#### Número de Escolas por Dependência Administrativa")
fig1, ax1 = plt.subplots()
df['dependencia_administrativa'].value_counts().plot(kind='bar', ax=ax1, color='skyblue')
ax1.set_ylabel("Número de Escolas")
st.pyplot(fig1)

# Gráfico 2 - Localização
st.markdown("#### Número de Escolas por Localização (Urbana/Rural)")
fig2, ax2 = plt.subplots()
df['localizacao'].value_counts().plot(kind='bar', ax=ax2, color='lightgreen')
ax2.set_ylabel("Número de Escolas")
st.pyplot(fig2)

# Gráfico 3 - Porte das Escolas
st.markdown("#### Número de Escolas por Porte")
fig3, ax3 = plt.subplots()
df['porte'].value_counts().plot(kind='bar_
