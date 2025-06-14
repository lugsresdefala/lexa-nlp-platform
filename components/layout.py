import streamlit as st
from config import APP_TITLE, APP_SUBTITLE

def render_header(title: str = APP_TITLE, subtitle: str = APP_SUBTITLE) -> str:
    """Render application header and return the HTML used."""
    html = f"""
    <div class="header">
        <div class="header-container" style="text-align: center; margin-bottom: 3rem; padding: 2rem 0;">
            <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 1.5rem;">
                <h1 style="
                    font-size: 3.5rem; 
                    font-weight: 900; 
                    margin: 0;
                    background: linear-gradient(135deg, #06b6d4, #22d3ee, #f59e0b);
                    background-size: 200% 200%;
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                    animation: gradient-shift 4s ease-in-out infinite;
                    letter-spacing: -0.02em;
                    font-family: 'Inter', sans-serif;
                ">
                    {title}
                </h1>
            </div>
            <p style="
                font-size: 1.3rem; 
                color: #cbd5e1; 
                margin: 0;
                font-weight: 500;
                opacity: 0.9;
            ">
                {subtitle}
            </p>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
    return html

def render_footer() -> str:
    """Render the application footer and return the HTML used."""
    html = (
        "<div class='footer'>"
        "<p>LEXA - Linguística Exploratória e Análise Textual Avançada © 2023</p>"
        "</div>"
    )
    st.markdown(html, unsafe_allow_html=True)
    return html
