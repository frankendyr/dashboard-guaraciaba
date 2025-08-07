import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar os dados
df = pd.read_csv("dashboard_escolas_guaraciaba.csv")

# Tratamento de nomes de colunas
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

# Título
st.set_page_config(page_title="Painel das Escolas - Guaraciaba do Norte", layout="wide")
st.title("📊 Painel das Escolas - Guaraciaba do Norte")

# Filtros
anos = sorted(df['ano_censo'].unique())
ano_sel = st.selectbox("Selecione o ano", anos)

redes = df['rede'].unique()
rede_sel = st.selectbox("Selecione a rede", redes)

# Filtro do DataFrame
df_filtrado = df[(df['ano_censo'] == ano_sel) & (df['rede'] == rede_sel)]

# Indicadores principais
total_escolas = df_filtrado.shape[0]
municipais = df_filtrado[df_filtrado['dependencia_adm'] == 'Municipal'].shape[0]
estaduais = df_filtrado[df_filtrado['dependencia_adm'] == 'Estadual'].shape[0]
privadas = df_filtrado[df_filtrado['dependencia_adm'] == 'Privada'].shape[0]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Escolas", total_escolas)
col2.metric("Municipais", f"{municipais} ({municipais/total_escolas:.0%})")
col3.metric("Estaduais", f"{estaduais} ({estaduais/total_escolas:.0%})")
col4.metric("Privadas", f"{privadas} ({privadas/total_escolas:.0%})")

st.markdown("---")

# Gráfico 1: Porte das Escolas
st.subheader("📐 Distribuição por Porte das Escolas")
porte_data = df_filtrado['porte'].value_counts().reset_index()
porte_data.columns = ['Porte', 'Quantidade']
fig1 = px.bar(porte_data, x='Porte', y='Quantidade', color='Porte', text='Quantidade')
st.plotly_chart(fig1, use_container_width=True)

# Gráfico 2: Etapas de Ensino Ofertadas
st.subheader("📚 Etapas de Ensino Ofertadas")
etapas_cols = [
    'educacao_infantil_creche', 'educacao_infantil_pre_escola',
    'ensino_fundamental_anos_iniciais', 'ensino_fundamental_anos_finais',
    'ensino_medio'
]
etapas_labels = {
    'educacao_infantil_creche': 'Creche',
    'educacao_infantil_pre_escola': 'Pré-escola',
    'ensino_fundamental_anos_iniciais': 'EF Anos Iniciais',
    'ensino_fundamental_anos_finais': 'EF Anos Finais',
    'ensino_medio': 'Ensino Médio'
}
etapas_qtd = {
    etapas_labels[col]: df_filtrado[col].sum() for col in etapas_cols
}
etapas_df = pd.DataFrame(etapas_qtd.items(), columns=['Etapa', 'Quantidade'])
fig2 = px.pie(etapas_df, names='Etapa', values='Quantidade', title="Distribuição das Etapas de Ensino")
st.plotly_chart(fig2, use_container_width=True)

# Gráfico 3: Localização das Escolas
st.subheader("📍 Localização das Escolas")
local_data = df_filtrado['localizacao'].value_counts().reset_index()
local_data.columns = ['Localização', 'Quantidade']
fig3 = px.bar(local_data, x='Localização', y='Quantidade', color='Localização', text='Quantidade')
st.plotly_chart(fig3, use_container_width=True)

# Lista das Escolas
st.markdown("---")
st.subheader("📋 Lista de Escolas")
st.dataframe(df_filtrado[['nome_escola', 'dependencia_adm', 'localizacao', 'bairro']], use_container_width=True)
