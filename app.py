import pandas as pd
import plotly.express as px
import streamlit as st

# Título do painel
st.set_page_config(page_title="Painel das Escolas de Guaraciaba", layout="wide")
st.title("📊 Painel das Escolas - Guaraciaba do Norte")

# Carregando o CSV
df = pd.read_csv("dashboard_escolas_guaraciaba.csv")

# Filtro apenas para escolas MUNICIPAIS
df_municipal = df[df['dependencia_adm'] == 'Municipal']

# Indicadores principais
total_escolas = len(df_municipal)
total_zona_urbana = len(df_municipal[df_municipal['zona'] == 'Urbana'])
total_zona_rural = len(df_municipal[df_municipal['zona'] == 'Rural'])

col1, col2, col3 = st.columns(3)
col1.metric("Total de Escolas Municipais", total_escolas)
col2.metric("Escolas na Zona Urbana", total_zona_urbana, f"{(total_zona_urbana/total_escolas)*100:.1f}%")
col3.metric("Escolas na Zona Rural", total_zona_rural, f"{(total_zona_rural/total_escolas)*100:.1f}%")

st.markdown("---")

# Gráfico 1: Distribuição por Etapa de Ensino
fig1 = px.bar(
    df_municipal['etapas_ensino'].value_counts().reset_index(),
    x='index', y='etapas_ensino',
    labels={'index': 'Etapa de Ensino', 'etapas_ensino': 'Quantidade'},
    title="Distribuição de Escolas por Etapa de Ensino"
)
st.plotly_chart(fig1, use_container_width=True)

# Gráfico 2: Porte das Escolas
fig2 = px.pie(
    df_municipal, names='porte',
    title="Distribuição de Porte das Escolas Municipais",
    hole=0.4
)
st.plotly_chart(fig2, use_container_width=True)

# Gráfico 3: Quantidade de Escolas por Zona
fig3 = px.bar(
    df_municipal['zona'].value_counts().reset_index(),
    x='index', y='zona',
    labels={'index': 'Zona', 'zona': 'Quantidade'},
    title="Quantidade de Escolas por Zona"
)
st.plotly_chart(fig3, use_container_width=True)

# Gráfico 4: Tipo de Localização
if 'local_func_predio' in df_municipal.columns:
    fig4 = px.histogram(
        df_municipal, x='local_func_predio',
        title="Localização das Escolas Municipais"
    )
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# Tabela final com a lista de escolas
st.subheader("📋 Lista de Escolas Municipais")
st.dataframe(df_municipal[['nome_escola', 'zona', 'etapas_ensino', 'porte']].sort_values(by='nome_escola'))
