import streamlit as st
from components.auth import render_auth
from components.sidebar import render_sidebar
from components.layout import render_header, render_footer

# Page configuration
st.set_page_config(
    page_title="LEXA - Análise de Texto",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header
render_header("Análise de Texto", "Plataforma de Análise Linguística")

# Sidebar
render_auth()
language, domain, genre, audience = render_sidebar()

# Main content
st.markdown("""
<div class="overview-section">
    <h2>Análise de Texto</h2>
    <p class="overview-text">
        Cole seu texto abaixo para iniciar a análise linguística multidimensional.
    </p>
</div>
""", unsafe_allow_html=True)

# Text input
text_input = st.text_area(
    "Texto para análise",
    height=300,
    placeholder="Cole aqui o texto que você deseja analisar...",
    help="O texto deve ter pelo menos 100 caracteres para uma análise adequada."
)

# Analysis options
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>Opções de Análise</h3>
        <div style="margin-top: 1rem;">
    """, unsafe_allow_html=True)
    
    analyze_cohesion = st.checkbox("Coesão Textual", value=True)
    analyze_coherence = st.checkbox("Coerência", value=True)
    analyze_adequacy = st.checkbox("Adequação ao Gênero", value=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>Métricas Avançadas</h3>
        <div style="margin-top: 1rem;">
    """, unsafe_allow_html=True)
    
    analyze_complexity = st.checkbox("Complexidade Linguística", value=True)
    analyze_style = st.checkbox("Estilo e Registro", value=True)
    analyze_intertextuality = st.checkbox("Intertextualidade", value=False)
    
    st.markdown("</div></div>", unsafe_allow_html=True)

# Analysis button
if st.button("Iniciar Análise", type="primary"):
    if not text_input or len(text_input.strip()) < 100:
        st.error("Por favor, insira um texto com pelo menos 100 caracteres.")
    else:
        with st.spinner("Analisando texto..."):
            # Placeholder for actual analysis
            st.info("Modo de desenvolvimento: Análise simulada")
            
            # Sample metrics display
            metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
            
            with metrics_col1:
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-value">85%</div>
                    <div class="metric-label">Coesão Textual</div>
                </div>
                """, unsafe_allow_html=True)
            
            with metrics_col2:
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-value">78%</div>
                    <div class="metric-label">Coerência</div>
                </div>
                """, unsafe_allow_html=True)
            
            with metrics_col3:
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-value">92%</div>
                    <div class="metric-label">Adequação</div>
                </div>
                """, unsafe_allow_html=True)

# Footer
render_footer()
