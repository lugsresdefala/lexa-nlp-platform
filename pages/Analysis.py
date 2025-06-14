import streamlit as st
import time
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import base64

from config import APP_TITLE, PLANS
from database import SessionLocal, init_db
from models.text import Text, save_text
from models.user import User as DBUser
from utils.processing import process_text, ensure_nltk_data
from utils.metrics import calculate_metrics
from utils.recommendations import generate_recommendations
from utils.user import User as GuestUser
from components.auth import render_auth
from components.sidebar import render_sidebar
from components.text_analysis import render_text_input
from components.metrics_dashboard import render_metrics_dashboard
from components.recommendations import render_recommendations
from components.text_annotation import render_text_annotation

# Page configuration
st.set_page_config(
    page_title="LEXA - Análise Textual", 
    page_icon="🔬", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional styling
st.markdown("""
<style>
/* Force application background */
.stApp, 
[data-testid="stAppViewContainer"],
[data-testid="stHeader"],
section[data-testid="stSidebar"] {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%) !important;
}

/* Main container styling */
.main .block-container {
    background: rgba(15, 23, 42, 0.95) !important;
    backdrop-filter: blur(20px) !important;
    border-radius: 24px !important;
    border: 1px solid rgba(6, 182, 212, 0.3) !important;
    padding: 3rem !important;
    margin: 2rem auto !important;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.8) !important;
    max-width: 1400px !important;
}

/* Sidebar styling */
.css-1d391kg, .css-k1vhr4, section[data-testid="stSidebar"] > div {
    background: linear-gradient(180deg, rgba(15, 23, 42, 0.98), rgba(30, 41, 59, 0.95)) !important;
    backdrop-filter: blur(20px) !important;
    border-right: 2px solid rgba(6, 182, 212, 0.3) !important;
}

/* Typography */
h1 {
    background: linear-gradient(135deg, #06b6d4, #22d3ee, #f59e0b) !important;
    background-size: 200% 200% !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    font-size: 3.5rem !important;
    font-weight: 900 !important;
    text-align: center !important;
    margin-bottom: 3rem !important;
    animation: gradient-shift 4s ease-in-out infinite !important;
}

@keyframes gradient-shift {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

/* Button styling */
.stButton > button {
    background: linear-gradient(135deg, #06b6d4, #0891b2) !important;
    color: white !important;
    border: none !important;
    border-radius: 16px !important;
    padding: 1rem 2.5rem !important;
    font-weight: 700 !important;
    transition: all 0.4s ease !important;
    box-shadow: 0 8px 25px rgba(6, 182, 212, 0.3) !important;
}

.stButton > button:hover {
    transform: translateY(-4px) scale(1.05) !important;
    box-shadow: 0 20px 40px rgba(6, 182, 212, 0.4) !important;
}

/* Tabs styling */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(30, 41, 59, 0.9) !important;
    border-radius: 20px !important;
    padding: 1rem !important;
    margin-bottom: 3rem !important;
    border: 1px solid rgba(6, 182, 212, 0.3) !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #06b6d4, #0891b2) !important;
    color: white !important;
    box-shadow: 0 8px 25px rgba(6, 182, 212, 0.4) !important;
    transform: translateY(-3px) !important;
}

/* Form inputs */
.stTextArea textarea, .stTextInput input {
    background: rgba(30, 41, 59, 0.9) !important;
    border: 2px solid rgba(6, 182, 212, 0.3) !important;
    border-radius: 16px !important;
    color: #f1f5f9 !important;
    backdrop-filter: blur(15px) !important;
    padding: 1.5rem !important;
}

.stSelectbox > div > div {
    background: rgba(30, 41, 59, 0.9) !important;
    border: 2px solid rgba(6, 182, 212, 0.3) !important;
    border-radius: 16px !important;
    backdrop-filter: blur(15px) !important;
}

/* Metric cards */
.metric-card {
    background: rgba(30, 41, 59, 0.9) !important;
    backdrop-filter: blur(15px) !important;
    border: 1px solid rgba(6, 182, 212, 0.3) !important;
    border-radius: 20px !important;
    padding: 2rem !important;
    margin: 1rem !important;
    transition: all 0.3s ease !important;
    text-align: center !important;
}

.metric-card:hover {
    transform: translateY(-5px) !important;
    border-color: rgba(6, 182, 212, 0.6) !important;
    box-shadow: 0 20px 40px rgba(6, 182, 212, 0.2) !important;
}

/* Text colors */
.stApp *, p, span, div, label, .stMarkdown {
    color: #f1f5f9 !important;
}

h2, h3, h4, h5, h6 {
    color: #f1f5f9 !important;
}

/* Force visibility */
* {
    visibility: visible !important;
}
</style>
""", unsafe_allow_html=True)

# Helper functions
def _check_quota(user, text_len: int) -> bool:
    """Check if user has remaining quota for text_len characters."""
    if hasattr(user, "has_quota"):
        return user.has_quota(text_len)
    limit = PLANS.get(getattr(user, "plan", "free"), 0)
    return False if limit and (user.char_usage + text_len) > limit else True

def _persist_user(user: DBUser) -> None:
    """Persist updated user statistics to the database."""
    db = SessionLocal()
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    finally:
        db.close()

def _persist_text(content: str, language: str, domain: str) -> None:
    """Create and save a Text record."""
    text_record = Text.create(content=content, language=language, domain=domain)
    save_text(text_record)

# Initialize database and NLTK
init_db()
ensure_nltk_data()

# Initialize session state
st.session_state.setdefault("analyzed_text", None)
st.session_state.setdefault("analysis_results", None)
st.session_state.setdefault("metrics", None)
st.session_state.setdefault("recommendations", None)
st.session_state.setdefault("active_tab", "text_input")
st.session_state.setdefault("user", GuestUser())

# Load logo
logo_path = "attached_assets/Sem nome (Ícone para YouTube).png"
logo_html = ""
if Path(logo_path).exists():
    try:
        with open(logo_path, "rb") as img_file:
            logo_b64 = base64.b64encode(img_file.read()).decode()
            logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="width: 80px; height: 80px; border-radius: 15px; margin-bottom: 1rem;" alt="LEXA Logo" />'
    except Exception:
        logo_html = ""

# Header with logo
st.markdown(f"""
<div style="text-align: center; margin-bottom: 3rem;">
    {logo_html}
    <h1>{APP_TITLE}</h1>
    <p style="font-size: 1.2rem; color: #cbd5e1; margin-bottom: 2rem;">Plataforma de Análise Linguística</p>
</div>
""", unsafe_allow_html=True)

# Sidebar components
render_auth()
language, domain, genre, audience = render_sidebar()

# Main tabs
tab_titles = [
    "📝 Entrada de Texto",
    "📊 Métricas de Qualidade", 
    "🏷️ Anotações Textuais",
    "💡 Recomendações"
]
tabs = st.tabs(tab_titles)

# Tab 1: Text Input & Analysis
with tabs[0]:
    st.session_state.active_tab = "text_input"
    text, analyze_pressed = render_text_input()
    
    if analyze_pressed and text:
        user = st.session_state.user
        char_count = len(text)
        
        if not _check_quota(user, char_count):
            st.warning("⚠️ Limite de caracteres do plano atingido.")
        else:
            with st.spinner("🔍 Processando análise linguística..."):
                # NLP processing
                doc = process_text(text, language)
                
                # Update user quota
                user.char_usage += char_count
                if isinstance(user, DBUser):
                    _persist_user(user)
                
                # Calculate metrics
                t0 = time.perf_counter()
                metrics = calculate_metrics(
                    doc, domain=domain, genre=genre or "Acadêmico", audience=audience
                )
                metrics_time = time.perf_counter() - t0
                
                # Generate recommendations
                t0 = time.perf_counter()
                recommendations = generate_recommendations(
                    doc, metrics, domain=domain, genre=genre or "Acadêmico"
                )
                rec_time = time.perf_counter() - t0
                
                # Store results
                st.session_state.update({
                    "analyzed_text": text,
                    "analysis_results": {
                        "doc": doc,
                        "metrics": metrics,
                        "recommendations": recommendations,
                        "processing_time": {
                            "metrics": metrics_time,
                            "recommendations": rec_time,
                        },
                    },
                })
                
                # Save text record
                _persist_text(text, language, domain)
                
                st.success(f"✅ Análise concluída! Tempo de processamento: {metrics_time:.2f}s")

# Tab 2: Metrics Dashboard
with tabs[1]:
    st.session_state.active_tab = "metrics"
    if st.session_state.metrics:
        metrics = st.session_state.metrics
        
        # Advanced metrics cards grid
        st.markdown("### 📊 Métricas Principais")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            coesao_score = metrics.get('coesao', {}).get('score', 0)
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #06b6d4;">Coesão</h3>
                <div style="font-size: 2.5rem; font-weight: 900; color: #22d3ee; margin: 1rem 0;">
                    {coesao_score:.1f}
                </div>
                <p style="color: #cbd5e1; font-size: 0.9rem;">Conectividade textual</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            coerencia_score = metrics.get('coerencia', {}).get('score', 0)
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #22d3ee;">Coerência</h3>
                <div style="font-size: 2.5rem; font-weight: 900; color: #06b6d4; margin: 1rem 0;">
                    {coerencia_score:.1f}
                </div>
                <p style="color: #cbd5e1; font-size: 0.9rem;">Lógica e organização</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            adequacao_score = metrics.get('adequacao', {}).get('score', 0)
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #f59e0b;">Adequação</h3>
                <div style="font-size: 2.5rem; font-weight: 900; color: #fbbf24; margin: 1rem 0;">
                    {adequacao_score:.1f}
                </div>
                <p style="color: #cbd5e1; font-size: 0.9rem;">Conformidade de gênero</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            complexidade_score = metrics.get('complexidade', {}).get('score', 0)
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #8b5cf6;">Complexidade</h3>
                <div style="font-size: 2.5rem; font-weight: 900; color: #a78bfa; margin: 1rem 0;">
                    {complexidade_score:.1f}
                </div>
                <p style="color: #cbd5e1; font-size: 0.9rem;">Sofisticação linguística</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Interactive visualization
        st.markdown("### 📈 Visualização Interativa")
        
        # Create radar chart
        dimensions = ['Coesão', 'Coerência', 'Adequação', 'Complexidade', 'Clareza', 'Precisão', 'Variação', 'Densidade']
        scores = [
            metrics.get('coesao', {}).get('score', 0),
            metrics.get('coerencia', {}).get('score', 0),
            metrics.get('adequacao', {}).get('score', 0),
            metrics.get('complexidade', {}).get('score', 0),
            metrics.get('clareza', {}).get('score', 0),
            metrics.get('precisao', {}).get('score', 0),
            metrics.get('variacao', {}).get('score', 0),
            metrics.get('densidade', {}).get('score', 0)
        ]
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=scores,
            theta=dimensions,
            fill='toself',
            name='Análise Atual',
            line_color='#06b6d4',
            fillcolor='rgba(6, 182, 212, 0.2)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10],
                    tickfont=dict(color='#f1f5f9'),
                    gridcolor='rgba(6, 182, 212, 0.3)'
                ),
                angularaxis=dict(
                    tickfont=dict(color='#f1f5f9', size=12),
                    gridcolor='rgba(6, 182, 212, 0.3)'
                )
            ),
            showlegend=True,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#f1f5f9')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed metrics breakdown
        render_metrics_dashboard(metrics)
    else:
        st.info("📄 Realize uma análise na aba 'Entrada de Texto' para visualizar as métricas.")

# Tab 3: Text Annotation
with tabs[2]:
    st.session_state.active_tab = "annotations"
    if st.session_state.analysis_results:
        st.markdown("### 🏷️ Anotações do Texto")
        render_text_annotation(
            st.session_state.analyzed_text,
            st.session_state.analysis_results
        )
    else:
        st.info("📄 Realize uma análise na aba 'Entrada de Texto' para visualizar as anotações.")

# Tab 4: Recommendations
with tabs[3]:
    st.session_state.active_tab = "recommendations"
    if st.session_state.recommendations:
        st.markdown("### 💡 Recomendações de Melhoria")
        render_recommendations(st.session_state.recommendations)
    else:
        st.info("📄 Realize uma análise na aba 'Entrada de Texto' para gerar recomendações.")

# Navigation button back to home
if st.button("🏠 Voltar à Página Inicial", type="secondary"):
    st.switch_page("app.py")