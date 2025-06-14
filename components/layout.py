import streamlit as st
from config import APP_TITLE, APP_SUBTITLE

def render_header(title: str = APP_TITLE, subtitle: str = APP_SUBTITLE) -> None:
    """Render application header."""
    try:
        st.image("assets/images/logo.png", width=100)
    except:
        st.warning("Logo não encontrado")
    
    st.title(title)
    st.subheader(subtitle)
    st.markdown("---")

def render_footer() -> None:
    """Render the application footer."""
    st.markdown("---")
    st.caption("LEXA - Linguística Exploratória e Análise Textual Avançada © 2023")
