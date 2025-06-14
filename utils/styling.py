"""
LEXA Styling System - Clean CSS management
Professional styling without force methods or redundancies
"""

import streamlit as st
from pathlib import Path

def load_css() -> None:
    """Load the consolidated CSS file for professional styling."""
    css_file = Path("assets/styles.css")
    
    if css_file.exists():
        with open(css_file) as f:
            css_content = f.read()
            st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
            
            # Force immediate application
            st.markdown("""
            <script>
            // Force CSS application
            document.documentElement.classList.add('lexa-loaded');
            </script>
            """, unsafe_allow_html=True)
    else:
        st.error("CSS file not found")

def inject_hero_section(title: str, subtitle: str, logo_path: str = "") -> None:
    """Inject a professional hero section with logo."""
    logo_html = ""
    if logo_path and Path(logo_path).exists():
        import base64
        try:
            with open(logo_path, "rb") as img_file:
                logo_b64 = base64.b64encode(img_file.read()).decode()
                logo_html = f"""
                <img src="data:image/png;base64,{logo_b64}" 
                     class="hero-logo" 
                     alt="LEXA Logo" />
                """
        except Exception:
            logo_html = ""
    
    st.markdown(f"""
    <div class="hero-section">
        <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 2rem;">
            {logo_html}
            <div style="text-align: left;">
                <h1>{title}</h1>
                <p style="font-size: 1.5rem; color: #cbd5e1; margin: 0.5rem 0; font-weight: 500;">{subtitle}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_metric_card(title: str, value: str, subtitle: str = "") -> None:
    """Create a professional metric card."""
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{value}</div>
        <div class="metric-label">{title}</div>
        {f'<p style="margin-top: 0.5rem; color: #cbd5e1; font-size: 0.875rem;">{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)