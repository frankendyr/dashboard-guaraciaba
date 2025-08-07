import streamlit as st
import pandas as pd
import plotly.express as px

# Título do Painel
st.set_page_config(layout="wide")
st.title("📊 Painel das Escolas - Guaraciaba do Norte")

# Carregamento do CSV
df = pd.read_csv("dashboard_escolas_guaraciaba.csv")

# Verifica colunas disponíveis
colunas = df.columns.tolist()

# Filtrar apenas escolas municipais
df_municipal = df[df["dependencia_administrativa"] == "Municipal"]

# KPIs - Indicadores
total_escolas = len(df_municipal)
total_escolas_geral = len(df)
porcentagem_municipais = round((total_escolas / total_escolas_geral) * 100, 2)
media_matriculas = int(df_municipal["qtd_matricula"].mean())

col1, col2, col3 = st.columns(3)
col1.metric("🏫 Total de Escolas Municipais", total_escolas)
col2.metric("📈 % Municipal", f"{porcentagem_municipais}%")
col3.metric("👩‍🎓 Média de Matrículas", media_matriculas)

st.markdown("---")

# 📊 Gráfico 1: Porte das Escolas
st.subheader("Distribuição por Porte das Escolas")
porte_counts = df_municipal["porte"].value_counts().reset_index()
porte_counts.columns = ["Porte", "Quantidade"]
fig1 = px.bar(porte_counts, x="Porte", y="Quantidade", color="Porte", text="Quantidade")
fig1.update_layout(xaxis_title="Porte", yaxis_title="Número de Escolas")
st.plotly_chart(fig1, use_container_width=True)

# 📊 Gráfico 2: Quantidade de Matrículas por Escola
st.subheader("Quantidade de Matrículas por Escola")
fig2 = px.histogram(df_municipal, x="qtd_matricula", nbins=20, title="Distribuição de Matrículas")
fig2.update_layout(xaxis_title="Quantidade de Matrículas", yaxis_title="Número de Escolas")
st.plotly_chart(fig2, use_container_width=True)

# 📊 Gráfico 3: Modalidade de Ensino
st.subheader("Distribuição por Modalidade de Ensino")
modalidade_counts = df_municipal["modalidade_ensino"].value_counts().reset_index()
modalidade_counts.columns = ["Modalidade", "Quantidade"]
fig3 = px.pie(modalidade_counts, names="Modalidade", values="Quantidade", hole=0.4)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# 📋 Tabela Final
st.subheader("📋 Lista das Escolas Municipais")
st.dataframe(df_municipal.sort_values(by="nome_escola"), use_container_width=True)
