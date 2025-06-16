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

# Features Grid with enhanced styling
st.markdown("""
<div class="section-header hover-scale">
    <h2>🚀 Recursos Principais</h2>
</div>
""", unsafe_allow_html=True)
st.write("")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card hover-lift">
        <div class="feature-icon">🔍</div>
        <h3>Análise Multidimensional</h3>
        <p>Avaliação através de oito dimensões linguísticas fundamentais para textos acadêmicos e científicos.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card hover-lift">
        <div class="feature-icon">📊</div>
        <h3>Visualizações Avançadas</h3>
        <p>Dashboards interativos e gráficos tridimensionais para interpretação detalhada dos resultados.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card hover-lift">
        <div class="feature-icon">💡</div>
        <h3>Recomendações Precisas</h3>
        <p>Sugestões específicas para aprimoramento textual baseadas em análise computacional rigorosa.</p>
    </div>
    """, unsafe_allow_html=True)

# Enhanced CTA Section
st.markdown("""
<div class="cta-section hover-lift">
    <div class="cta-content">
        <h2 class="cta-title">✨ Inicie sua Análise</h2>
        <p class="cta-text">Acesse a plataforma principal para começar a análise de seus textos acadêmicos.</p>
        <div class="cta-animation">
            <span class="pulse-dot"></span>
            <span class="pulse-ring"></span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar with authentication and settings
render_auth()
language, domain, genre, audience = render_sidebar()

# Navigation button
if st.button("Acessar Plataforma de Análise", type="primary"):
    st.switch_page("pages/LEXA_Analysis.py")

# Footer
render_footer()
