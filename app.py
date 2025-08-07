import streamlit as st
import pandas as pd
import plotly.express as px

# Carregando o CSV
df = pd.read_csv("dashboard_escolas_guaraciaba.csv")

# Configuração do app
st.set_page_config(page_title="Painel Educacional — Guaraciaba do Norte", layout="wide")
st.title("🏫 Painel Educacional — Guaraciaba do Norte (CE)")

# Filtro base
df_municipal = df[df["dependencia_administrativa"].str.lower() == "municipal"]

# Filtros na barra lateral
with st.sidebar:
    st.header("🔍 Filtros")
    categoria = st.selectbox("Categoria Administrativa", options=["Todas"] + sorted(df["categoria_administrativa"].dropna().unique()))
    zona = st.selectbox("Zona", options=["Todas"] + sorted(df["localizacao"].dropna().unique()))
    porte = st.selectbox("Porte", options=["Todas"] + sorted(df["porte"].dropna().unique()))

# Aplicar filtros
df_filtrado = df.copy()
if categoria != "Todas":
    df_filtrado = df_filtrado[df_filtrado["categoria_administrativa"] == categoria]
if zona != "Todas":
    df_filtrado = df_filtrado[df_filtrado["localizacao"] == zona]
if porte != "Todas":
    df_filtrado = df_filtrado[df_filtrado["porte"] == porte]

# Métricas principais
col1, col2, col3 = st.columns(3)
col1.metric("Total de Escolas", len(df_filtrado))
col2.metric("Escolas Municipais", f"{len(df_municipal)} ({len(df_municipal)/len(df)*100:.1f}%)")
col3.metric("Escolas Urbanas", f"{(df[df['localizacao'] == 'Urbana'].shape[0] / len(df)) * 100:.1f}%")

# Gráfico 1: Categoria Administrativa
st.subheader("📊 Distribuição por Categoria Administrativa")
fig1 = px.pie(df_filtrado, names='categoria_administrativa', title='Categorias das Escolas', hole=0.4)
st.plotly_chart(fig1, use_container_width=True)

# Gráfico 2: Localização das Escolas
st.subheader("📊 Localização (Urbana/Rural) por Dependência")
fig2 = px.histogram(df_filtrado, x='localizacao', color='dependencia_administrativa', barmode='group')
st.plotly_chart(fig2, use_container_width=True)

# Gráfico 3: Porte das Escolas
st.subheader("📊 Porte das Escolas")
fig3 = px.bar(df_filtrado['porte'].value_counts().reset_index(),
              x='index', y='porte',
              labels={'index': 'Porte', 'porte': 'Quantidade'})
st.plotly_chart(fig3, use_container_width=True)

# Gráfico 4: Zona das Escolas Municipais
st.subheader("📊 Localização das Escolas Municipais")
fig4 = px.pie(df_municipal, names='localizacao', title='Escolas Municipais por Zona', hole=0.3)
st.plotly_chart(fig4, use_container_width=True)

# Tabela com dados
st.subheader("📄 Lista de Escolas")
st.dataframe(df_filtrado.reset_index(drop=True))
