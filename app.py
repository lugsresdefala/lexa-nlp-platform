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
st.markdown("""
<div class="overview-section">
    <h2>Sistema Avançado de Análise Linguística</h2>
    <p class="overview-text">
        O LEXA oferece análise multidimensional de qualidade textual através de métricas computacionais 
        sofisticadas, desenvolvido especificamente para contextos acadêmicos e de pesquisa científica.
    </p>
</div>
""", unsafe_allow_html=True)

# Features Grid
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon icon-primary">
            <div style="width: 20px; height: 20px; border: 3px solid white; border-radius: 50%;"></div>
        </div>
        <h3>Análise Multidimensional</h3>
        <p class="feature-text">
            Avaliação através de oito dimensões linguísticas fundamentais para textos acadêmicos e científicos.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon icon-secondary">
            <div style="width: 24px; height: 16px; border: 2px solid white; border-radius: 4px; position: relative;">
                <div style="position: absolute; top: 4px; left: 4px; right: 4px; height: 2px; background: white; border-radius: 1px;"></div>
                <div style="position: absolute; bottom: 4px; left: 4px; right: 8px; height: 2px; background: white; border-radius: 1px;"></div>
            </div>
        </div>
        <h3>Visualizações Avançadas</h3>
        <p class="feature-text">
            Dashboards interativos e gráficos tridimensionais para interpretação detalhada dos resultados.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon icon-tertiary">
            <div style="width: 24px; height: 24px; border: 2px solid white; border-radius: 12px; position: relative;">
                <div style="position: absolute; top: 6px; left: 6px; width: 8px; height: 8px; background: white; border-radius: 4px;"></div>
            </div>
        </div>
        <h3>Recomendações Precisas</h3>
        <p class="feature-text">
            Sugestões específicas para aprimoramento textual baseadas em análise computacional rigorosa.
        </p>
    </div>
    """, unsafe_allow_html=True)

# CTA Section
st.markdown("""
<div class="cta-section">
    <h3 class="cta-title">Inicie sua Análise</h3>
    <p class="cta-text">
        Acesse a plataforma principal para começar a análise de seus textos acadêmicos.
    </p>
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
