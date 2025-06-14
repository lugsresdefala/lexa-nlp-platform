"""Streamlit authentication component for LEXA - Development Version"""

import streamlit as st

def render_auth() -> None:
    """Render a simplified authentication widget for development."""
    st.sidebar.subheader("Modo Desenvolvimento")
    st.sidebar.info("Autenticação desativada para desenvolvimento")
    
    # Set default session state for development
    if 'user' not in st.session_state:
        st.session_state.user = {
            'email': 'dev@example.com',
            'plan': 'enterprise',
            'char_usage': 0,
            'char_limit': 1000000
        }
    
    # Display mock user info
    st.sidebar.success(f"Logado como: {st.session_state.user['email']}")
    st.sidebar.info(f"Plano: {st.session_state.user['plan'].title()}")
    
    # Display usage information
    char_limit = st.session_state.user['char_limit']
    char_usage = st.session_state.user['char_usage']
    usage_percent = (char_usage / char_limit) * 100 if char_limit > 0 else 0
    
    st.sidebar.info(f"Uso: {char_usage:,}/{char_limit:,} caracteres ({usage_percent:.1f}%)")
    st.sidebar.progress(min(usage_percent / 100, 1.0))
