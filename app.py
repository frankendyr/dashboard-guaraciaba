import streamlit as st
import pandas as pd
import plotly.express as px

# Título do Painel
st.set_page_config(page_title="Painel de Escolas - Guaraciaba", layout="wide")
st.title("📊 Painel de Escolas - Guaraciaba do Norte/CE")

# Carregamento do CSV
@st.cache_data
def carregar_dados():
    df = pd.read_csv("dashboard_escolas_guaraciaba.csv")
    return df

df = carregar_dados()

# Filtro para escolas municipais
df_municipal = df[df['dependencia_administrativa'] == 'Municipal']

# Exibição de métrica
col1, col2 = st.columns(2)
col1.metric("Total de Escolas", len(df))
col2.metric("Escolas Municipais", len(df_municipal))

st.divider()

# Tabela de todas as escolas
st.subheader("📋 Lista de Escolas")
st.dataframe(df[['nome', 'dependencia_administrativa', 'categoria_administrativa', 'porte', 'etapas_modalidades_oferecidas']], use_container_width=True)

st.divider()

# Gráfico: Dependência Administrativa
st.subheader("🏛️ Dependência Administrativa")
fig1 = px.pie(df, names='dependencia_administrativa', title='Distribuição por Dependência')
st.plotly_chart(fig1, use_container_width=True)

# Gráfico: Porte das Escolas (Municipais)
st.subheader("🏫 Porte das Escolas Municipais")
df_municipal_porte = df_municipal['porte'].value_counts().reset_index()
df_municipal_porte.columns = ['Porte', 'Quantidade']
fig2 = px.bar(df_municipal_porte, x='Porte', y='Quantidade', text='Quantidade', title='Distribuição por Porte - Escolas Municipais')
st.plotly_chart(fig2, use_container_width=True)

# Gráfico: Categorias Administrativas
st.subheader("📂 Categoria Administrativa")
fig3 = px.histogram(df, x='categoria_administrativa', color='dependencia_administrativa', barmode='group')
st.plotly_chart(fig3, use_container_width=True)

# Gráfico: Etapas e Modalidades
st.subheader("📚 Etapas / Modalidades Oferecidas")
df_etapas = df['etapas_modalidades_oferecidas'].dropna().value_counts().reset_index()
df_etapas.columns = ['Etapas/Modalidades', 'Quantidade']
fig4 = px.bar(df_etapas, y='Etapas/Modalidades', x='Quantidade', orientation='h', text='Quantidade')
st.plotly_chart(fig4, use_container_width=True)

# Rodapé
st.markdown("---")
st.caption("Dados fornecidos por Kennedy | Desenvolvido com ❤️ usando Streamlit")
