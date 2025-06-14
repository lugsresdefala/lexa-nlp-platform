"""
Advanced UI Components for LEXA
Sophisticated, modern interface elements with animations and interactions
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Any, Optional
import json


def render_hero_section():
    """Render sophisticated hero section with animated elements"""
    st.markdown("""
    <div class="hero-container animate-slide-up">
        <div class="hero-content">
            <div class="logo-section animate-float">
                <div class="lexa-logo-advanced">
                    <div class="logo-ring pulse"></div>
                    <div class="logo-center glow">
                        <span class="logo-text text-gradient">LEXA</span>
                    </div>
                </div>
            </div>
            <h1 class="hero-title text-gradient">
                Análise Linguística Inteligente
            </h1>
            <p class="hero-subtitle">
                Transforme texto em insights profundos com IA avançada
            </p>
            <div class="hero-features">
                <div class="feature-item glass">
                    <div class="feature-icon">🧠</div>
                    <span>IA Avançada</span>
                </div>
                <div class="feature-item glass">
                    <div class="feature-icon">📊</div>
                    <span>Métricas Precisas</span>
                </div>
                <div class="feature-item glass">
                    <div class="feature-icon">⚡</div>
                    <span>Análise Rápida</span>
                </div>
            </div>
        </div>
    </div>
    
    <style>
    .hero-container {
        text-align: center;
        padding: 4rem 2rem;
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.8) 100%);
        border-radius: 24px;
        margin-bottom: 3rem;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .hero-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(from 0deg, transparent, rgba(6, 182, 212, 0.1), transparent);
        animation: rotate 20s linear infinite;
        z-index: -1;
    }
    
    .lexa-logo-advanced {
        position: relative;
        width: 120px;
        height: 120px;
        margin: 0 auto 2rem;
    }
    
    .logo-ring {
        position: absolute;
        width: 100%;
        height: 100%;
        border: 3px solid;
        border-color: #06b6d4 transparent #f59e0b transparent;
        border-radius: 50%;
        animation: spin 3s linear infinite;
    }
    
    .logo-center {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, #06b6d4, #f59e0b);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 30px rgba(6, 182, 212, 0.5);
    }
    
    .logo-text {
        font-size: 1.5rem;
        font-weight: 900;
        color: white;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 900;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #ffffff 0%, #67e8f9 50%, #fcd34d 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: #f1f5f9;
        margin-bottom: 3rem;
        opacity: 0.9;
    }
    
    .hero-features {
        display: flex;
        justify-content: center;
        gap: 2rem;
        flex-wrap: wrap;
    }
    
    .feature-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 1rem 1.5rem;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .feature-item:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(6, 182, 212, 0.2);
        background: rgba(255, 255, 255, 0.15);
    }
    
    .feature-icon {
        font-size: 1.5rem;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        .hero-features {
            flex-direction: column;
            align-items: center;
        }
    }
    </style>
    """, unsafe_allow_html=True)


def render_advanced_metrics_card(title: str, value: Any, subtitle: str = "", 
                                 color: str = "#06b6d4", icon: str = ""):
    """Render sophisticated metrics card with animations"""
    st.markdown(f"""
    <div class="advanced-metric-card glass glow-border">
        <div class="metric-header">
            <div class="metric-indicator" style="background: {color}; width: 4px; height: 40px; border-radius: 2px; margin-right: 1rem;"></div>
            <h3 class="metric-title">{title}</h3>
        </div>
        <div class="metric-content">
            <div class="metric-value text-gradient" style="--gradient-color: {color};">
                {value}
            </div>
            {f'<div class="metric-subtitle">{subtitle}</div>' if subtitle else ''}
        </div>
        <div class="metric-indicator">
            <div class="indicator-bar" style="background: {color};"></div>
        </div>
    </div>
    
    <style>
    .advanced-metric-card {{
        padding: 1.5rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        margin-bottom: 1rem;
    }}
    
    .advanced-metric-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1), 0 0 30px rgba(6, 182, 212, 0.2);
    }}
    
    .metric-header {{
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
    }}
    
    .metric-icon {{
        font-size: 1.5rem;
        filter: drop-shadow(0 0 8px currentColor);
    }}
    
    .metric-title {{
        color: #f1f5f9;
        font-size: 0.875rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin: 0;
    }}
    
    .metric-value {{
        font-size: 2.5rem;
        font-weight: 900;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, {color}, #fcd34d);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    
    .metric-subtitle {{
        color: #cbd5e1;
        font-size: 0.75rem;
        opacity: 0.8;
    }}
    
    .metric-indicator {{
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: rgba(255, 255, 255, 0.1);
    }}
    
    .indicator-bar {{
        height: 100%;
        width: 100%;
        transform: scaleX(0);
        transform-origin: left;
        animation: indicatorGrow 1s ease-out 0.5s forwards;
    }}
    
    @keyframes indicatorGrow {{
        to {{ transform: scaleX(1); }}
    }}
    </style>
    """, unsafe_allow_html=True)


def render_interactive_tabs(tabs_data: Dict[str, Any], default_tab: str = None):
    """Render advanced interactive tabs with smooth transitions"""
    if not tabs_data:
        return None
    
    tab_names = list(tabs_data.keys())
    default_index = tab_names.index(default_tab) if default_tab in tab_names else 0
    
    # Create Streamlit tabs
    tabs = st.tabs(tab_names)
    
    # Custom styling for tabs
    st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 0.5rem;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        gap: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 12px;
        color: #cbd5e1;
        font-weight: 500;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: none;
        position: relative;
        overflow: hidden;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.1);
        color: #f1f5f9;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #06b6d4, #0891b2);
        color: white;
        box-shadow: 0 4px 20px rgba(6, 182, 212, 0.3);
        transform: translateY(-1px);
    }
    
    .stTabs [aria-selected="true"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        to { left: 100%; }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Render tab content
    for i, (tab_name, content) in enumerate(tabs_data.items()):
        with tabs[i]:
            if callable(content):
                content()
            else:
                st.write(content)


def render_analysis_progress(progress: float, stage: str = "Analisando..."):
    """Render sophisticated analysis progress indicator"""
    st.markdown(f"""
    <div class="analysis-progress-container">
        <div class="progress-header">
            <div class="progress-icon pulse">🧠</div>
            <div class="progress-info">
                <h4 class="progress-title">{stage}</h4>
                <p class="progress-percentage">{progress:.1f}%</p>
            </div>
        </div>
        <div class="progress-bar-container">
            <div class="progress-bar-bg">
                <div class="progress-bar-fill" style="width: {progress}%;"></div>
                <div class="progress-bar-glow" style="width: {progress}%;"></div>
            </div>
        </div>
        <div class="progress-particles">
            <div class="particle"></div>
            <div class="particle"></div>
            <div class="particle"></div>
        </div>
    </div>
    
    <style>
    .analysis-progress-container {{
        background: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
    }}
    
    .progress-header {{
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }}
    
    .progress-icon {{
        font-size: 2rem;
        background: linear-gradient(135deg, #06b6d4, #f59e0b);
        border-radius: 50%;
        width: 60px;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 20px rgba(6, 182, 212, 0.3);
    }}
    
    .progress-title {{
        color: #f1f5f9;
        font-size: 1.25rem;
        font-weight: 600;
        margin: 0;
    }}
    
    .progress-percentage {{
        color: #06b6d4;
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0;
    }}
    
    .progress-bar-container {{
        position: relative;
        margin-bottom: 1rem;
    }}
    
    .progress-bar-bg {{
        width: 100%;
        height: 8px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
        overflow: hidden;
        position: relative;
    }}
    
    .progress-bar-fill {{
        height: 100%;
        background: linear-gradient(90deg, #06b6d4, #22d3ee, #f59e0b);
        border-radius: 4px;
        transition: width 0.5s ease;
        position: relative;
    }}
    
    .progress-bar-glow {{
        position: absolute;
        top: 0;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(34, 211, 238, 0.8), transparent);
        border-radius: 4px;
        animation: progressGlow 2s ease-in-out infinite;
    }}
    
    .progress-particles {{
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        pointer-events: none;
    }}
    
    .particle {{
        position: absolute;
        width: 4px;
        height: 4px;
        background: #22d3ee;
        border-radius: 50%;
        animation: particleFloat 3s ease-in-out infinite;
    }}
    
    .particle:nth-child(1) {{
        left: 20%;
        animation-delay: 0s;
    }}
    
    .particle:nth-child(2) {{
        left: 50%;
        animation-delay: 1s;
    }}
    
    .particle:nth-child(3) {{
        left: 80%;
        animation-delay: 2s;
    }}
    
    @keyframes progressGlow {{
        0%, 100% {{ transform: translateX(-100%); }}
        50% {{ transform: translateX(200%); }}
    }}
    
    @keyframes particleFloat {{
        0%, 100% {{ transform: translateY(20px); opacity: 0; }}
        50% {{ transform: translateY(-20px); opacity: 1; }}
    }}
    </style>
    """, unsafe_allow_html=True)


def render_3d_metrics_chart(metrics_data: Dict[str, float], title: str = "Métricas de Qualidade"):
    """Render advanced 3D metrics visualization"""
    if not metrics_data:
        return
    
    # Create 3D surface plot
    categories = list(metrics_data.keys())
    values = list(metrics_data.values())
    
    # Create radar chart with Plotly
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(6, 182, 212, 0.2)',
        line=dict(color='rgb(6, 182, 212)', width=3),
        marker=dict(size=8, color='rgb(245, 158, 11)'),
        name='Métricas'
    ))
    
    fig.update_layout(
        polar=dict(
            bgcolor='rgba(255, 255, 255, 0.05)',
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor='rgba(255, 255, 255, 0.2)',
                gridwidth=1,
                tickcolor='rgba(255, 255, 255, 0.6)',
                tickfont=dict(color='rgba(255, 255, 255, 0.8)', size=10)
            ),
            angularaxis=dict(
                gridcolor='rgba(255, 255, 255, 0.2)',
                gridwidth=1,
                tickcolor='rgba(255, 255, 255, 0.6)',
                tickfont=dict(color='rgba(255, 255, 255, 0.9)', size=12)
            )
        ),
        showlegend=False,
        title=dict(
            text=title,
            x=0.5,
            font=dict(color='white', size=16)
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_floating_action_menu():
    """Render floating action menu with advanced interactions"""
    st.markdown("""
    <div class="fab-container">
        <div class="fab-main" onclick="toggleFabMenu()">
            <span class="fab-icon">⚡</span>
        </div>
        <div class="fab-menu" id="fabMenu">
            <div class="fab-item" data-action="export">
                <span class="fab-item-icon">📥</span>
                <span class="fab-item-label">Exportar</span>
            </div>
            <div class="fab-item" data-action="share">
                <span class="fab-item-icon">🔗</span>
                <span class="fab-item-label">Compartilhar</span>
            </div>
            <div class="fab-item" data-action="settings">
                <span class="fab-item-icon">⚙️</span>
                <span class="fab-item-label">Configurações</span>
            </div>
        </div>
    </div>
    
    <style>
    .fab-container {
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        z-index: 1000;
    }
    
    .fab-main {
        width: 56px;
        height: 56px;
        border-radius: 50%;
        background: linear-gradient(135deg, #06b6d4, #f59e0b);
        border: none;
        box-shadow: 0 8px 25px rgba(6, 182, 212, 0.3);
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        position: relative;
    }
    
    .fab-main:hover {
        transform: scale(1.1) rotate(90deg);
        box-shadow: 0 12px 30px rgba(6, 182, 212, 0.4);
    }
    
    .fab-icon {
        font-size: 1.5rem;
        color: white;
        transition: transform 0.3s ease;
    }
    
    .fab-menu {
        position: absolute;
        bottom: 70px;
        right: 0;
        display: flex;
        flex-direction: column;
        gap: 1rem;
        opacity: 0;
        visibility: hidden;
        transform: translateY(20px);
        transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    }
    
    .fab-menu.active {
        opacity: 1;
        visibility: visible;
        transform: translateY(0);
    }
    
    .fab-item {
        display: flex;
        align-items: center;
        gap: 1rem;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 28px;
        padding: 0.75rem 1.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
        white-space: nowrap;
    }
    
    .fab-item:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateX(-10px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    }
    
    .fab-item-icon {
        font-size: 1.25rem;
    }
    
    .fab-item-label {
        color: white;
        font-weight: 500;
        font-size: 0.875rem;
    }
    </style>
    
    <script>
    function toggleFabMenu() {
        const menu = document.getElementById('fabMenu');
        menu.classList.toggle('active');
    }
    
    // Close menu when clicking outside
    document.addEventListener('click', function(e) {
        const fabContainer = document.querySelector('.fab-container');
        if (!fabContainer.contains(e.target)) {
            document.getElementById('fabMenu').classList.remove('active');
        }
    });
    </script>
    """, unsafe_allow_html=True)


def inject_advanced_css():
    """Inject the advanced CSS into the Streamlit app"""
    # Read the consolidated stylesheet used across the application.
    # Using the existing ``assets/styles.css`` ensures the file is always
    # available when running both the application and the tests.
    with open("assets/styles.css", "r", encoding="utf-8") as f:
        css_content = f.read()
    
    st.markdown(f"""
    <style>
    {css_content}
    </style>
    """, unsafe_allow_html=True)