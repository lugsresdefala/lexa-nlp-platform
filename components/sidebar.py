import streamlit as st
from config import LANGUAGES, DOMAINS, GENRES, AUDIENCE_LEVELS
from utils.ui import emoji_label
from components.plan_upgrade import render_plan_upgrade

def render_sidebar():
    """
    Render the sidebar with enhanced styling and configuration options.

    Returns:
        tuple: (language, domain, genre, audience) selected by user
    """
    # Styling for sidebar header
    st.sidebar.markdown(
        """
    <div style="background: linear-gradient(90deg, #45C4AF30, #1e3a5f); 
               padding: 1rem 0.5rem; border-radius: 10px; margin-bottom: 1rem;
               border-left: 4px solid #45C4AF; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
        <h2 style="color: white; margin: 0; text-align: center; text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);">
            LEXA
        </h2>
        <p style="color: #97DDD4; margin: 0; text-align: center; font-size: 0.9rem;">
            Configurações de Análise
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Add a divider with gradient
    st.sidebar.markdown(
        """
    <div style="height: 3px; background: linear-gradient(90deg, transparent, #45C4AF, transparent);
               margin: 0.5rem 0 1.5rem 0;"></div>
    """,
        unsafe_allow_html=True,
    )

    # Add plan upgrade section
    render_plan_upgrade()

    # Language selection with styled label
    st.sidebar.markdown(
        '<p style="color: #45C4AF; font-weight: bold; margin-bottom: 0.2rem;">Idioma do texto</p>',
        unsafe_allow_html=True,
    )
    language = st.sidebar.selectbox(
        label="Idioma do texto",
        options=list(LANGUAGES.keys()),
        format_func=lambda x: LANGUAGES[x],
        index=0,
        label_visibility="collapsed",
        help="Escolha o idioma predominante do texto que será analisado.",
    )

    # Domain selection with styled label
    st.sidebar.markdown(
        '<p style="color: #45C4AF; font-weight: bold; margin: 1rem 0 0.2rem 0;">Domínio de texto</p>',
        unsafe_allow_html=True,
    )
    domain = st.sidebar.selectbox(
        label="Domínio de texto",
        options=DOMAINS,
        index=0,
        label_visibility="collapsed",
        help="Indique o campo temático principal ao qual o texto pertence.",
    )

    # Get genres for selected domain
    domain_genres = GENRES.get(domain, [])

    # Genre selection with styled label
    st.sidebar.markdown(
        '<p style="color: #45C4AF; font-weight: bold; margin: 1rem 0 0.2rem 0;">Gênero textual</p>',
        unsafe_allow_html=True,
    )
    genre = st.sidebar.selectbox(
        label="Gênero textual",
        options=domain_genres,
        index=0 if domain_genres else None,
        label_visibility="collapsed",
        help="Escolha o gênero que melhor descreve o texto fornecido.",
    )

    # Audience selection with styled label
    st.sidebar.markdown(
        '<p style="color: #45C4AF; font-weight: bold; margin: 1rem 0 0.2rem 0;">Público-alvo</p>',
        unsafe_allow_html=True,
    )
    audience = st.sidebar.selectbox(
        label="Público-alvo",
        options=AUDIENCE_LEVELS,
        index=2,  # Default to "Acadêmico"
        label_visibility="collapsed",
        help="Determine o nível de conhecimento esperado de quem lerá o texto.",
    )

    # Add another divider with gradient
    st.sidebar.markdown(
        """
    <div style="height: 3px; background: linear-gradient(90deg, transparent, #45C4AF, transparent); 
               margin: 1.5rem 0 1.5rem 0;"></div>
    """,
        unsafe_allow_html=True,
    )

    # Information section with styled card
    bullet_items = """
        <li style="margin-bottom: 0.2rem;"><span style="color: #45C4AF;">{coesao}</span> Textual</li>
        <li style="margin-bottom: 0.2rem;"><span style="color: #5de0a5;">{coerencia}</span> Discursiva</li>
        <li style="margin-bottom: 0.2rem;"><span style="color: #FFEB85;">{adequacao}</span> ao Gênero</li>
        <li style="margin-bottom: 0.2rem;"><span style="color: #97DDD4;">{precisao}</span> e Clareza</li>
        <li style="margin-bottom: 0.2rem;"><span style="color: #1a7f76;">{complexidade}</span> Linguística</li>
    """.format(
        coesao=emoji_label("🔄", "Coesão"),
        coerencia=emoji_label("🧩", "Coerência"),
        adequacao=emoji_label("🎯", "Adequação"),
        precisao=emoji_label("🔍", "Precisão"),
        complexidade=emoji_label("🧠", "Complexidade"),
    )

    st.sidebar.markdown(
        f"""
    <div style="background: rgba(20, 45, 78, 0.6); border-radius: 10px; padding: 1rem;
               box-shadow: 0 4px 6px rgba(0,0,0,0.1); border: 1px solid rgba(69, 196, 175, 0.2);
               backdrop-filter: blur(10px);">
        <h4 style="color: #FFFCC7; margin-top: 0; margin-bottom: 0.5rem; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 0.5rem;">
            Sobre LEXA
        </h4>
        <p style="color: white; margin-bottom: 0.5rem; font-size: 0.9rem;">
            <b>L</b>inguística <b>Ex</b>ploratória e <b>A</b>nálise Textual Avançada é uma plataforma para análise multidimensional de qualidade textual.
        </p>
        <p style="color: #97DDD4; margin-top: 0.5rem; font-size: 0.9rem; font-weight: bold;">Dimensões analisadas:</p>
        <ul style="color: white; margin: 0; padding-left: 1.2rem; font-size: 0.85rem;">
            {bullet_items}
        </ul>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Set up advanced options as expander with styling
    with st.sidebar.expander(emoji_label("⚙️", "Opções Avançadas")):
        # Add styled container for options
        st.markdown(
            """
        <div style="background: rgba(20, 45, 78, 0.4); border-radius: 8px; padding: 0.75rem;
                   border: 1px solid rgba(69, 196, 175, 0.1);">
            <p style="color: #FFFCC7; font-weight: bold; margin: 0 0 0.5rem 0; font-size: 0.9rem;">
                Métricas de Análise
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Let user select which metrics to calculate with custom styling
        cols = st.columns(2)

        with cols[0]:
            st.checkbox(
                emoji_label("🔄", "Coesão"),
                value=True,
                key="metric_cohesion",
                help="Analisa conexões entre elementos textuais",
            )
            st.checkbox(
                emoji_label("🧩", "Coerência"),
                value=True,
                key="metric_coherence",
                help="Avalia organização lógica das ideias",
            )
            st.checkbox(
                emoji_label("🎯", "Adequação"),
                value=True,
                key="metric_adequacy",
                help="Conformidade com convenções do gênero",
            )

        with cols[1]:
            st.checkbox(
                emoji_label("🔍", "Precisão"),
                value=True,
                key="metric_precision",
                help="Clareza e exatidão da expressão",
            )
            st.checkbox(
                emoji_label("🧠", "Complexidade"),
                value=True,
                key="metric_complexity",
                help="Sofisticação linguística do texto",
            )

        # Additional options with styling
        st.markdown(
            """
        <div style="background: rgba(20, 45, 78, 0.4); border-radius: 8px; padding: 0.75rem;
                   border: 1px solid rgba(69, 196, 175, 0.1); margin-top: 1rem;">
            <p style="color: #FFFCC7; font-weight: bold; margin: 0 0 0.5rem 0; font-size: 0.9rem;">
                Opções Adicionais
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Additional option checkboxes with custom styling
        st.checkbox(
            emoji_label("📊", "Análise Comparativa"),
            value=False,
            key="comparative_analysis",
            help="Compara com corpus de referência no mesmo domínio",
        )
        st.checkbox(
            emoji_label("💾", "Exportar Resultados"),
            value=False,
            key="export_results",
            help="Baixar resultados em formato CSV/JSON",
        )
        st.checkbox(
            emoji_label("🔍", "Análise Detalhada"),
            value=True,
            key="detailed_analysis",
            help="Inclui análise profunda de cada dimensão",
        )

        # Add a button for reset
        if st.button(
            emoji_label("🔄", "Redefinir Configurações"), use_container_width=True
        ):
            # Reset all configurations to default
            st.session_state.metric_cohesion = True
            st.session_state.metric_coherence = True
            st.session_state.metric_adequacy = True
            st.session_state.metric_precision = True
            st.session_state.metric_complexity = True
            st.session_state.comparative_analysis = False
            st.session_state.export_results = False
            st.session_state.detailed_analysis = True
            st.rerun()

    return language, domain, genre, audience
