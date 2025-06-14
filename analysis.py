"""LEXA – Streamlit main application entrypoint.
Resolves merge‑conflict artefacts and harmonises callbacks.
"""

from __future__ import annotations

import streamlit as st

# ---------------------------------------------------------------------------
# Streamlit page configuration (must be first Streamlit command)
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="LEXA - Plataforma de Análise",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

import time
from pathlib import Path

import pandas as pd  # noqa: F401 – used by downstream components

from config import (
    APP_TITLE,
    AUDIENCE_LEVELS,  # noqa: F401 – future use
    PLANS,
)
from database import SessionLocal, init_db
from models.text import Text, save_text
from models.user import User as DBUser
from utils.processing import process_text, ensure_nltk_data
from utils.metrics import calculate_metrics
from utils.recommendations import generate_recommendations
from utils.user import User as GuestUser
from utils.visualization import (
    create_bar_chart,  # noqa: F401 – future use
    create_radar_chart,  # noqa: F401 – future use
)

# UI components --------------------------------------------------------------
from components.auth import render_auth
from components.layout import render_footer, render_header
from components.metrics_dashboard import render_metrics_dashboard
from components.recommendations import render_recommendations
from components.sidebar import render_sidebar
from components.text_analysis import render_text_input
from components.text_annotation import render_text_annotation
from components.advanced_ui import (
    inject_advanced_css, render_hero_section, render_advanced_metrics_card,
    render_interactive_tabs, render_analysis_progress, render_3d_metrics_chart,
    render_floating_action_menu
)
from utils.styling import load_css

# Load consolidated CSS styling
load_css()


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def _check_quota(user: GuestUser | DBUser, text_len: int) -> bool:
    """Return ``True`` if user has remaining quota for *text_len* characters."""
    if hasattr(user, "has_quota"):
        return user.has_quota(text_len)
    limit = PLANS.get(getattr(user, "plan", "free"), 0)
    return False if limit and (user.char_usage + text_len) > limit else True


def _persist_user(user: DBUser) -> None:
    """Persist updated *user* statistics to the database."""
    db = SessionLocal()
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    finally:
        db.close()


def _persist_text(content: str, language: str, domain: str) -> None:
    """Create and save a :class:`~models.text.Text` record."""
    text_record = Text.create(content=content, language=language, domain=domain)
    save_text(text_record)


def _js_switch_tab(index: int) -> None:
    """Inject JS to switch Streamlit tab programmatically."""
    import streamlit.components.v1 as components
    components.html(
        f"""
        <script>
            const tabs = window.parent.document.querySelectorAll('.stTabs button');
            if (tabs && tabs[{index}]) {{ tabs[{index}].click(); }}
        </script>
        """,
        height=0,
    )


# ---------------------------------------------------------------------------
# Main application
# ---------------------------------------------------------------------------


def main() -> None:  # noqa: D401
    """LEXA Streamlit application entrypoint."""

    # Professional styling system
    inject_advanced_css()
    
    # Ensure database schema is present
    init_db()

    # Ensure required NLTK resources are available
    ensure_nltk_data()

    # ---------------------------------------------------------------------
    # Initialise Streamlit session state
    # ---------------------------------------------------------------------
    st.session_state.setdefault("analyzed_text", None)
    st.session_state.setdefault("analysis_results", None)
    st.session_state.setdefault("metrics", None)
    st.session_state.setdefault("recommendations", None)
    st.session_state.setdefault("active_tab", "text_input")
    st.session_state.setdefault("user", GuestUser())

    # ---------------------------------------------------------------------
    # Revolutionary Hero Section
    # ---------------------------------------------------------------------
    render_hero_section()

    # ---------------------------------------------------------------------
    # Advanced Authentication and Navigation
    # ---------------------------------------------------------------------
    render_auth()
    language, domain, genre, audience = render_sidebar()

    # ---------------------------------------------------------------------
    # Define main tabs
    # ---------------------------------------------------------------------
    tab_titles = [
        "Entrada de Texto",
        "Métricas de Qualidade",
        "Anotações Textuais",
        "Recomendações",
    ]
    tabs = st.tabs(tab_titles)

    # ------------------------------------------------------------------
    # Tab 0 – Text Input & Analysis
    # ------------------------------------------------------------------
    with tabs[0]:
        st.session_state.active_tab = "text_input"
        text, analyze_pressed = render_text_input()

        if analyze_pressed and text:
            user = st.session_state.user
            char_count = len(text)

            if not _check_quota(user, char_count):
                st.warning("Limite de caracteres do plano atingido.")
            else:
                with st.spinner("Processando análise linguística…"):
                    # NLP processing --------------------------------------------------
                    doc = process_text(text, language)

                    # Update user quota --------------------------------------------
                    user.char_usage += char_count
                    if isinstance(user, DBUser):
                        _persist_user(user)

                    # Metrics -------------------------------------------------------
                    t0 = time.perf_counter()
                    metrics = calculate_metrics(
                        doc, domain=domain, genre=genre or "Acadêmico", audience=audience
                    )
                    metrics_time = time.perf_counter() - t0

                    # Recommendations ---------------------------------------------
                    t0 = time.perf_counter()
                    recommendations = generate_recommendations(
                        doc, metrics, domain=domain, genre=genre or "Acadêmico"
                    )
                    rec_time = time.perf_counter() - t0

                    # Persist text and update session ------------------------------
                    _persist_text(text, language, domain)

                    st.session_state.update(
                        analyzed_text=text,
                        metrics=metrics,
                        recommendations=recommendations,
                        analysis_results={
                            "doc": doc,
                            "metrics": metrics,
                            "recommendations": recommendations,
                            "processing_time": {
                                "metrics": metrics_time,
                                "recommendations": rec_time,
                            },
                        },
                    )

                    # Auto‑switch to metrics tab
                    _js_switch_tab(1)

    # ------------------------------------------------------------------
    # Tab 1 – Advanced Metrics Dashboard
    # ------------------------------------------------------------------
    with tabs[1]:
        st.session_state.active_tab = "metrics"
        if st.session_state.metrics:
            metrics = st.session_state.metrics
            
            # Advanced metrics cards grid
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                render_advanced_metrics_card(
                    "Coesão",
                    f"{metrics.get('coesao', {}).get('score', 0):.1f}",
                    "Conectividade textual",
                    "#06b6d4"
                )
            
            with col2:
                render_advanced_metrics_card(
                    "Coerência", 
                    f"{metrics.get('coerencia', {}).get('score', 0):.1f}",
                    "Lógica e organização",
                    "#22d3ee"
                )
            
            with col3:
                render_advanced_metrics_card(
                    "Adequação",
                    f"{metrics.get('adequacao', {}).get('score', 0):.1f}",
                    "Conformidade de gênero",
                    "#f59e0b"
                )
            
            with col4:
                render_advanced_metrics_card(
                    "Complexidade",
                    f"{metrics.get('complexidade', {}).get('score', 0):.1f}",
                    "Sofisticação linguística",
                    "#fbbf24"
                )
            
            # 3D visualization
            metrics_data = {
                "Coesão": metrics.get('coesao', {}).get('score', 0),
                "Coerência": metrics.get('coerencia', {}).get('score', 0),
                "Adequação": metrics.get('adequacao', {}).get('score', 0),
                "Complexidade": metrics.get('complexidade', {}).get('score', 0),
                "Precisão": metrics.get('precisao', {}).get('score', 0)
            }
            
            render_3d_metrics_chart(metrics_data, "Análise Multidimensional")
            
            # Traditional dashboard
            render_metrics_dashboard(metrics)
        else:
            st.markdown("""
            <div class="empty-state glass animate-slide-up">
                <div class="empty-indicator" style="width: 60px; height: 60px; border-radius: 50%; background: linear-gradient(135deg, #06b6d4, #0891b2); margin: 0 auto 1rem; display: flex; align-items: center; justify-content: center;">
                    <div style="width: 20px; height: 20px; border: 3px solid white; border-radius: 50%; border-top-color: transparent; animation: spin 1s linear infinite;"></div>
                </div>
                <h3 style="color: #f1f5f9; margin-bottom: 1rem;">Análise Pendente</h3>
                <p style="color: #cbd5e1; opacity: 0.8;">Envie um texto para análise e visualize métricas avançadas de qualidade linguística.</p>
            </div>
            <style>
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            .empty-state {
                text-align: center;
                padding: 4rem 2rem;
                border-radius: 16px;
                margin: 2rem 0;
                background: rgba(30, 41, 59, 0.8);
                backdrop-filter: blur(15px);
                border: 1px solid rgba(6, 182, 212, 0.2);
            }
            </style>
            """, unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # Tab 2 – Text Annotation
    # ------------------------------------------------------------------
    with tabs[2]:
        st.session_state.active_tab = "annotations"
        if st.session_state.analysis_results:
            render_text_annotation(
                st.session_state.analyzed_text,
                st.session_state.analysis_results,
            )
        else:
            st.info("Realize uma análise para visualizar anotações.")

    # ------------------------------------------------------------------
    # Tab 3 – Recommendations
    # ------------------------------------------------------------------
    with tabs[3]:
        st.session_state.active_tab = "recommendations"
        if st.session_state.recommendations:
            render_recommendations(st.session_state.recommendations)
        else:
            st.info("Realize uma análise para visualizar recomendações.")

    # Revolutionary Floating Action Menu
    render_floating_action_menu()

    # Footer --------------------------------------------------------------
    render_footer()


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()
