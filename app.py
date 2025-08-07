import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Carregar o CSV
df = pd.read_csv("dashboard_escolas_guaraciaba.csv")

# Configuração inicial
st.set_page_config(page_title="Painel Educacional — Guaraciaba do Norte (CE)", layout="wide")
st.title("🏫 Painel Educacional — Guaraciaba do Norte (CE)")

# Foco nas escolas municipais
df_municipal = df[df["dependencia_administrativa"].str.lower() == "municipal"]

# Filtros
with st.sidebar:
    st.header("🔎 Filtros")
    categoria = st.selectbox("Categoria Administrativa", options=["Todas"] + sorted(df["categoria_administrativa"].dropna().unique()))
    localizacao = st.selectbox("Localização", options=["Todas"] + sorted(df["localizacao"].dropna().unique()))
    porte = st.selectbox("Porte", options=["Todas"] + sorted(df["porte"].dropna().unique()))

# Aplicar filtros
df_filtrado = df.copy()
if categoria != "Todas":
    df_filtrado = df_filtrado[df_filtrado["categoria_administrativa"] == categoria]
if localizacao != "Todas":
    df_filtrado = df_filtrado[df_filtrado["localizacao"] == localizacao]
if porte != "Todas":
    df_filtrado = df_filtrado[df_filtrado["porte"] == porte]

# Métricas principais
col1, col2, col3 = st.columns(3)
col1.metric("🏫 Total de Escolas", len(df_filtrado))
col2.metric("🏫 % Municipais", f"{(len(df_municipal) / len(df) * 100):.1f}%")
col3.metric("🏙️ % Urbanas", f"{(len(df[df['localizacao'] == 'Urbana']) / len(df) * 100):.1f}%")

# Gráfico: Categoria Administrativa
st.subheader("📊 Distribuição por Categoria Administrativa")
fig1 = px.pie(df_filtrado, names='categoria_administrativa', title='Categorias Administrativas', hole=0.4)
st.plotly_chart(fig1, use_container_width=True)

# Gráfico: Localização Urbana vs Rural
st.subheader("📊 Localização das Escolas")
fig2 = px.histogram(df_filtrado, x='localizacao', color='dependencia_administrativa', barmode='group')
st.plotly_chart(fig2, use_container_width=True)

# Gráfico: Distribuição por Porte
st.subheader("📊 Distribuição por Porte das Escolas")
fig3 = px.bar(df_filtrado['porte'].value_counts().reset_index(), x='index', y='porte', labels={'index': 'Porte', 'porte': 'Quantidade'})
st.plotly_chart(fig3, use_container_width=True)

# Tabela final
st.subheader("📄 Lista de Escolas")
st.dataframe(df_filtrado.reset_index(drop=True))
