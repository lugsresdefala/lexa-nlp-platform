import streamlit as st
from config import APP_TITLE, APP_SUBTITLE
from components.auth import render_auth
from components.sidebar import render_sidebar
from components.layout import render_header, render_footer
from utils.styling import load_css

# Page configuration
st.set_page_config(
    page_title="LEXA - Plataforma Acadêmica", 
    page_icon="🎓", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load consolidated CSS styling
load_css()

# Hero Section
render_header()

# Overview Section
st.title("Sistema Avançado de Análise Linguística")
st.write("""
O LEXA oferece análise multidimensional de qualidade textual através de métricas computacionais 
sofisticadas, desenvolvido especificamente para contextos acadêmicos e de pesquisa científica.
""")

# Add some spacing
st.write("")
st.write("")

# Features Grid
st.subheader("🚀 Recursos Principais")
st.write("")  # Add spacing after subheader
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🔍 Análise Multidimensional")
    st.write("Avaliação através de oito dimensões linguísticas fundamentais para textos acadêmicos e científicos.")

with col2:
    st.markdown("### 📊 Visualizações Avançadas")
    st.write("Dashboards interativos e gráficos tridimensionais para interpretação detalhada dos resultados.")

with col3:
    st.markdown("### 💡 Recomendações Precisas")
    st.write("Sugestões específicas para aprimoramento textual baseadas em análise computacional rigorosa.")

# CTA Section
st.markdown("---")
st.header("Inicie sua Análise")
st.write("Acesse a plataforma principal para começar a análise de seus textos acadêmicos.")

# Sidebar with authentication and settings
render_auth()
language, domain, genre, audience = render_sidebar()

# Navigation button
if st.button("Acessar Plataforma de Análise", type="primary"):
    st.switch_page("pages/LEXA_Analysis.py")

# Footer
render_footer()
