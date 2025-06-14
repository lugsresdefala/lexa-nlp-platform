import streamlit as st
import numpy as np
import random
from utils.visualization import (
    create_radar_chart,
    create_3d_radar_chart,
    create_bar_chart,
    create_score_gauge,
    create_dimension_bar_chart,
    create_3d_metrics_visualization,
    create_pydeck_3d_map,
    create_interactive_metric_explorer,
    create_text_heatmap,
    create_comparison_heatmap,
)
from config import METRIC_DIMENSIONS, USE_EMOJI
from utils.ui import emoji_label
from streamlit_extras.colored_header import colored_header
from streamlit_extras.metric_cards import style_metric_cards


def render_metrics_dashboard(metrics):
    """
    Render an enhanced metrics dashboard with advanced 3D visualizations.

    Args:
        metrics (dict): Dictionary containing the metrics results
    """
    # Apply custom styles for metric cards
    style_metric_cards(
        background_color="rgba(20, 45, 78, 0.7)",
        border_left_color="#45C4AF",
        border_color="#1a7f76",
    )

    # Enhanced header
    colored_header(
        label="Métricas de Qualidade Textual",
        description="Análise multidimensional avançada para avaliação de qualidade linguística",
        color_name="blue-green",
    )

    # Calculate dimension scores
    dimension_scores = {}
    for dim_key, dim_metrics in metrics["dimensions"].items():
        if isinstance(dim_metrics, dict) and "score" in dim_metrics:
            dimension_scores[dim_key] = dim_metrics["score"]
        else:
            dimension_scores[dim_key] = np.mean(
                [
                    m["score"]
                    for m in dim_metrics.values()
                    if isinstance(m, dict) and "score" in m
                ]
            )

    # Main visualization selector tabs
    viz_tabs = st.tabs(
        [
            "Dashboard",
            "Visualização 3D",
            "Visualização Interativa",
            "Análise Detalhada",
            "Mapa de Calor",
        ]
    )

    with viz_tabs[0]:
        # Card-style layout with glassmorphism effect
        st.markdown('<div class="card glass">', unsafe_allow_html=True)

        # Top section with overall score and radar chart
        col1, col2 = st.columns([1, 2])

        with col1:
            # Overall score gauge in a metric container
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            overall_score = metrics["overall_score"]

            # Create and display gauge chart
            gauge_fig = create_score_gauge(overall_score, "Pontuação Global")
            st.plotly_chart(gauge_fig, use_container_width=True)

            # Add percentile information with enhanced styling
            if "percentile" in metrics:
                percentile = metrics["percentile"]
                st.metric(
                    "Percentil no Domínio",
                    f"{percentile:.1f}",
                    delta=(
                        f"{percentile - 50:.1f} vs média"
                        if percentile > 50
                        else f"{percentile - 50:.1f} vs média"
                    ),
                    delta_color="normal",
                    help="Percentil em relação ao corpus de referência no mesmo domínio",
                )
            st.markdown("</div>", unsafe_allow_html=True)

            # Add summarized text metrics in a styled card
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(
                '<h3 class="metric-label">Resumo de Performance</h3>',
                unsafe_allow_html=True,
            )

            # Select top and bottom metrics
            all_metrics = []
            for dim_key, dim_metrics in metrics["dimensions"].items():
                for metric_key, metric_info in dim_metrics.items():
                    if isinstance(metric_info, dict) and "score" in metric_info:
                        all_metrics.append(
                            {
                                "dimension": dim_key,
                                "metric": metric_key,
                                "name": metric_info.get("name", metric_key),
                                "score": metric_info["score"],
                            }
                        )

            # Sort metrics by score
            sorted_metrics = sorted(all_metrics, key=lambda x: x["score"])

            # Display top metrics with enhanced styling
            if sorted_metrics:
                top_metrics = sorted_metrics[-3:]  # Top 3 metrics
                st.markdown(
                    '<div class="dimension dimension-high">', unsafe_allow_html=True
                )
                st.markdown('<div class="dimension-content">', unsafe_allow_html=True)
                st.markdown(f"##### {emoji_label('🌟', 'Pontos fortes')}")
                for metric in reversed(top_metrics):
                    dim_name = METRIC_DIMENSIONS[metric["dimension"]]["name"]
                    color = METRIC_DIMENSIONS[metric["dimension"]]["color"]
                    st.markdown(
                        f'<span style="color:{color}; font-weight:bold;">● {metric["name"]}</span>: {metric["score"]:.1f}',
                        unsafe_allow_html=True,
                    )
                st.markdown("</div></div>", unsafe_allow_html=True)

                # Display bottom metrics with enhanced styling
                bottom_metrics = sorted_metrics[:3]  # Bottom 3 metrics
                st.markdown(
                    '<div class="dimension dimension-low">', unsafe_allow_html=True
                )
                st.markdown('<div class="dimension-content">', unsafe_allow_html=True)
                st.markdown(f"##### {emoji_label('🔍', 'Áreas para melhoria')}")
                for metric in bottom_metrics:
                    dim_name = METRIC_DIMENSIONS[metric["dimension"]]["name"]
                    color = METRIC_DIMENSIONS[metric["dimension"]]["color"]
                    st.markdown(
                        f'<span style="color:{color}; font-weight:bold;">● {metric["name"]}</span>: {metric["score"]:.1f}',
                        unsafe_allow_html=True,
                    )
                st.markdown("</div></div>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            # Visualization container with glassmorphism effect
            st.markdown('<div class="graph-container">', unsafe_allow_html=True)

            # Enhanced radar chart for dimension scores
            radar_fig = create_radar_chart(
                {
                    METRIC_DIMENSIONS[dim]["name"]: score
                    for dim, score in dimension_scores.items()
                }
            )
            st.plotly_chart(radar_fig, use_container_width=True)

            # Horizontal bar chart for dimensions with enhanced styling
            st.markdown('<div class="graph-container">', unsafe_allow_html=True)
            bar_fig = create_dimension_bar_chart(dimension_scores)
            st.plotly_chart(bar_fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # Dimension metrics summary in a card grid layout
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(
            '<h3 class="metric-label">Resumo por Dimensão</h3>', unsafe_allow_html=True
        )

        # Create row for dimension metric cards
        cols = st.columns(len(dimension_scores))

        # Add metric cards for each dimension
        for i, (dim_key, score) in enumerate(dimension_scores.items()):
            with cols[i]:
                dim_name = METRIC_DIMENSIONS[dim_key]["name"]
                dim_color = METRIC_DIMENSIONS[dim_key]["color"]

                # Create styled metric display
                st.markdown(
                    f'<div style="text-align: center; padding: 0.5rem; background: linear-gradient(90deg, {dim_color}20, {dim_color}05); border-radius: 10px; border: 1px solid {dim_color}40;">',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<p style="color: {dim_color}; font-weight: bold; font-size: 1rem; margin-bottom: 0.5rem;">{dim_name}</p>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<h2 style="color: white; margin: 0; font-size: 2rem;">{score:.1f}</h2>',
                    unsafe_allow_html=True,
                )

                # Add simple progress bar
                st.markdown(
                    f"""
                <div style="width: 100%; background-color: rgba(255,255,255,0.1); height: 4px; border-radius: 2px; margin: 0.5rem 0;">
                    <div style="width: {score}%; background-color: {dim_color}; height: 100%; border-radius: 2px;"></div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # 3D Visualization tab with advanced visualizations
    with viz_tabs[1]:
        view_options = st.radio(
            "Selecione o tipo de visualização 3D",
            ["Radar 3D", "Rede de Relacionamento 3D", "Visualização Geográfica 3D"],
            horizontal=True,
            help="Escolha como visualizar graficamente as métricas em três dimensões",
        )

        st.markdown('<div class="graph-3d-container">', unsafe_allow_html=True)

        if view_options == "Radar 3D":
            # 3D radar chart
            radar_3d_fig = create_3d_radar_chart(dimension_scores)
            st.plotly_chart(radar_3d_fig, use_container_width=True, height=700)

            # Add information overlay
            with st.expander("ℹ️ Sobre esta visualização"):
                st.markdown(
                    """
                **Radar 3D de Dimensões**
                
                Esta visualização apresenta as dimensões de qualidade textual em um espaço tridimensional, permitindo uma comparação mais intuitiva das diferentes métricas.
                
                - **Altura da superfície**: Representa o valor de cada métrica
                - **Cor da superfície**: Gradiente baseado no valor das métricas
                - **Interação**: Você pode girar, aproximar e mover o gráfico para explorar diferentes ângulos
                """
                )

        elif view_options == "Rede de Relacionamento 3D":
            # 3D metrics network visualization
            network_3d_fig = create_3d_metrics_visualization(metrics)
            st.plotly_chart(network_3d_fig, use_container_width=True, height=700)

            # Add information overlay
            with st.expander("ℹ️ Sobre esta visualização"):
                st.markdown(
                    """
                **Rede de Relacionamento 3D**
                
                Esta visualização mostra as relações entre diferentes métricas e dimensões em um espaço tridimensional.
                
                - **Nós grandes**: Representam as dimensões principais
                - **Nós menores**: Representam métricas individuais
                - **Conexões**: Mostram relações entre métricas da mesma dimensão
                - **Tamanho dos nós**: Proporcional à pontuação de cada métrica
                """
                )

        else:  # Geographical visualization
            # Geographic 3D visualization
            st.pydeck_chart(create_pydeck_3d_map(metrics))

            # Add information overlay
            with st.expander("ℹ️ Sobre esta visualização"):
                st.markdown(
                    """
                **Visualização Geográfica 3D**
                
                Esta visualização apresenta as dimensões de qualidade em um mapa abstrato 3D.
                
                - **Agrupamentos**: Representam as diferentes dimensões de qualidade
                - **Altura das formações**: Proporcional às pontuações de cada métrica
                - **Cores**: Indicam a performance em cada dimensão (verde = boa, amarelo = média, vermelho = precisa melhorar)
                """
                )

        st.markdown("</div>", unsafe_allow_html=True)

    # Interactive visualization tab with streamlit_elements
    with viz_tabs[2]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(
            '<h3 class="metric-label">Dashboard Interativo</h3>', unsafe_allow_html=True
        )
        st.markdown(
            """
        Este dashboard interativo permite arrastar e reorganizar os componentes. 
        Experimente reorganizar os painéis e interagir com as visualizações.
        """
        )

        # Render interactive dashboard using streamlit_elements
        create_interactive_metric_explorer(metrics)

        st.markdown("</div>", unsafe_allow_html=True)

    # Detailed metrics by dimension
    with viz_tabs[3]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(
            '<h3 class="metric-label">Análise Detalhada por Dimensão</h3>',
            unsafe_allow_html=True,
        )

        # Create tabs for each dimension with enhanced styling
        dimension_tabs = st.tabs(
            [METRIC_DIMENSIONS[dim]["name"] for dim in METRIC_DIMENSIONS]
        )

        # Populate each dimension tab
        for i, dim_key in enumerate(METRIC_DIMENSIONS):
            with dimension_tabs[i]:
                if dim_key in metrics["dimensions"]:
                    render_dimension_metrics(dim_key, metrics["dimensions"][dim_key])
                else:
                    st.info(
                        f"Nenhum dado disponível para a dimensão {METRIC_DIMENSIONS[dim_key]['name']}"
                    )

        st.markdown("</div>", unsafe_allow_html=True)

    # Heat Map visualizations tab
    with viz_tabs[4]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(
            '<h3 class="metric-label">Visualizações de Mapa de Calor</h3>',
            unsafe_allow_html=True,
        )

        # Tabs for different heat map visualizations
        heat_tabs = st.tabs(["Análise por Sentença", "Comparação de Textos"])

        # Sentence-level analysis heat map
        with heat_tabs[0]:
            if (
                "analysis_results" in st.session_state
                and st.session_state.analysis_results
            ):
                doc = st.session_state.analysis_results.get("doc")
                if doc:
                    # Create and display text heat map
                    text_heatmap = create_text_heatmap(doc, metrics)
                    st.plotly_chart(text_heatmap, use_container_width=True)

                    # Add explanation
                    st.markdown(
                        """
                    ### Análise por Sentença
                    
                    Esta visualização identifica as sentenças problemáticas em relação às dimensões que precisam de mais atenção.
                    As cores vermelhas indicam pontuações mais baixas, enquanto as verdes indicam pontuações mais altas.
                    
                    #### Como usar esta visualização:
                    
                    1. Identifique as sentenças com cores vermelhas/amarelas
                    2. Passe o mouse sobre cada sentença para ver seu conteúdo completo
                    3. Use as recomendações detalhadas para melhorar estas áreas específicas
                    """
                    )
                else:
                    st.info(
                        "Nenhuma análise textual disponível. Realize a análise de um texto primeiro."
                    )
            else:
                st.info(
                    "Nenhuma análise textual disponível. Realize a análise de um texto primeiro."
                )

        # Text comparison heat map
        with heat_tabs[1]:
            st.markdown(
                """
            ### Comparação de Múltiplos Textos
            
            Esta visualização permite comparar diferentes versões de um texto ou textos distintos
            em relação a todas as dimensões de qualidade.
            
            **Para demonstração**, estamos mostrando uma comparação simulada entre três versões de um texto.
            """
            )

            # Create sample data for demonstration
            # In a real implementation, this would use actual stored texts from the user
            sample_texts_metrics = []
            text_names = [
                "Versão 1 (Original)",
                "Versão 2 (Revisada)",
                "Versão 3 (Final)",
            ]

            # Create sample metrics data for demonstration
            # Sample text 1 - original version with lower scores
            sample_text1 = {"dimensions": {}}
            for dim_key in METRIC_DIMENSIONS:
                base_score = 55 + random.randint(
                    -10, 10
                )  # Lower base score for first version
                sample_text1["dimensions"][dim_key] = {
                    "score": max(0, min(100, base_score))
                }

            # Sample text 2 - revised version with medium scores
            sample_text2 = {"dimensions": {}}
            for dim_key in METRIC_DIMENSIONS:
                base_score = 70 + random.randint(
                    -10, 10
                )  # Medium base score for second version
                sample_text2["dimensions"][dim_key] = {
                    "score": max(0, min(100, base_score))
                }

            # Sample text 3 - final version with higher scores
            sample_text3 = {"dimensions": {}}
            for dim_key in METRIC_DIMENSIONS:
                base_score = 85 + random.randint(
                    -10, 5
                )  # Higher base score for final version
                sample_text3["dimensions"][dim_key] = {
                    "score": max(0, min(100, base_score))
                }

            sample_texts_metrics = [sample_text1, sample_text2, sample_text3]

            # Create and display comparison heatmap
            comparison_heatmap = create_comparison_heatmap(
                sample_texts_metrics, text_names
            )
            st.plotly_chart(comparison_heatmap, use_container_width=True)

            # Add explanation about the visualization
            st.markdown(
                """
            #### Como usar esta visualização:
            
            1. Compare as pontuações de diferentes versões do mesmo texto
            2. Identifique as dimensões que melhoraram ou pioraram entre versões
            3. Use as cores mais intensas para detectar os pontos fortes de cada versão
            4. As pontuações numéricas permitem comparações precisas entre textos
            
            #### Em um sistema completo:
            
            - Você poderia carregar múltiplos documentos para comparação
            - O sistema salvaria versões anteriores do mesmo texto automaticamente
            - Seria possível exportar os resultados comparativos em formato de relatório
            """
            )

            with st.expander("Sobre os dados de demonstração"):
                st.markdown(
                    """
                **Nota:** Os dados exibidos são simulados para demonstração.
                
                Em um sistema completo, você teria:
                - Histórico de versões dos seus textos
                - Opção de comparar com outros textos do mesmo domínio
                - Estatísticas comparativas detalhadas
                """
                )

        st.markdown("</div>", unsafe_allow_html=True)

    # Processing time information
    if "processing_time" in metrics:
        st.caption(
            emoji_label(
                "⏱️",
                f"Tempo de processamento: {metrics['processing_time'].get('metrics', 0):.2f} segundos",
            )
        )


def render_dimension_metrics(dimension_key, dimension_metrics):
    """
    Render the metrics for a specific dimension with enhanced styling and interactions.

    Args:
        dimension_key (str): The dimension key
        dimension_metrics (dict): Dictionary of metrics for this dimension
    """
    dimension_info = METRIC_DIMENSIONS[dimension_key]
    dimension_color = dimension_info["color"]

    # Description of the dimension with icons
    dimension_descriptions = {
        "coesao": {
            "description": "Avalia como os elementos do texto estão conectados, incluindo referências, repetições lexicais e uso de conectivos.",
            "icon": "🔄",
            "details": "A coesão é responsável pela unidade formal do texto e é construída através de mecanismos linguísticos que estabelecem relações de sentido.",
        },
        "coerencia": {
            "description": "Mede a qualidade da organização das ideias, progressão temática e estrutura retórica do texto.",
            "icon": "🧩",
            "details": "A coerência estabelece a relação lógica entre as ideias, criando uma unidade de sentido que permite ao leitor compreender a mensagem global do texto.",
        },
        "adequacao": {
            "description": "Analisa a conformidade do texto às convenções do gênero e a adequação do registro ao contexto comunicativo.",
            "icon": "🎯",
            "details": "A adequação verifica se o texto está apropriado à situação comunicativa, ao gênero textual escolhido e às expectativas do público-alvo.",
        },
        "precisao": {
            "description": "Avalia a precisão terminológica e a clareza estrutural das sentenças no texto.",
            "icon": "🔍",
            "details": "A precisão refere-se à escolha exata de termos e estruturas para expressar ideias com clareza, evitando ambiguidades e imprecisões.",
        },
        "complexidade": {
            "description": "Mede o nível de sofisticação lexical, sintática e informacional do texto.",
            "icon": "🧠",
            "details": "A complexidade indica o grau de elaboração e sofisticação do texto, considerando a diversidade vocabular, estruturas sintáticas e densidade informacional.",
        },
    }

    dim_info = dimension_descriptions.get(
        dimension_key, {"description": "", "icon": "📊", "details": ""}
    )

    icon_html = (
        f"<span style=\"font-size: 1.8rem; margin-right: 0.5rem;\">{dim_info['icon']}</span>"
        if USE_EMOJI
        else ""
    )
    # Header with styling
    st.markdown(
        f"""
    <div style="background: linear-gradient(90deg, {dimension_color}30, rgba(20, 45, 78, 0.4)); border-radius: 10px; padding: 1rem; margin-bottom: 1rem; border-left: 4px solid {dimension_color};">
        <h3 style="color: white; margin: 0; display: flex; align-items: center;">
            {icon_html}{dimension_info['name']}
        </h3>
        <p style="margin: 0.5rem 0; opacity: 0.9;">{dim_info['description']}</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Enhanced dimension information
    with st.expander(emoji_label("ℹ️", "Mais informações sobre esta dimensão")):
        st.markdown(
            f"""
        **Sobre a dimensão {dimension_info['name']}**
        
        {dim_info['details']}
        
        Esta dimensão contribui para a qualidade global do texto avaliando aspectos específicos da linguagem e do discurso que 
        impactam diretamente a clareza, adequação e eficácia comunicativa.
        """
        )

    # Display dimension score with custom gauge
    if "score" in dimension_metrics:
        dimension_score = dimension_metrics["score"]
    else:
        # Calculate from individual metrics
        dimension_score = np.mean(
            [
                m["score"]
                for m in dimension_metrics.values()
                if isinstance(m, dict) and "score" in m
            ]
        )

    # Determine color and status based on score
    if dimension_score >= 80:
        level_color = "#5de0a5"  # Green
        level_text = "Excelente"
        icon = "🌟"
    elif dimension_score >= 70:
        level_color = "#97DDD4"  # Light green
        level_text = "Bom"
        icon = "✅"
    elif dimension_score >= 60:
        level_color = "#FFEB85"  # Yellow
        level_text = "Satisfatório"
        icon = "⚠️"
    else:
        level_color = "#ff7f7f"  # Red
        level_text = "Precisa Melhorar"
        icon = "❗"

    # Score card with gradient
    cols = st.columns([1, 2])
    with cols[0]:
        st.markdown(
            f"""
        <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, {dimension_color}40, {dimension_color}10); 
             border-radius: 10px; border: 1px solid {dimension_color}60; margin-bottom: 1rem;">
            <p style="font-size: 1rem; color: {dimension_color}; margin: 0;">Pontuação</p>
            <h1 style="font-size: 3.5rem; margin: 0.5rem 0; color: white;">{dimension_score:.1f}</h1>
            <div style="width: 80%; margin: 0.5rem auto; background-color: rgba(255,255,255,0.1); height: 8px; border-radius: 4px;">
                <div style="width: {dimension_score}%; background-color: {level_color}; height: 100%; border-radius: 4px;"></div>
            </div>
            <p style="font-size: 1.2rem; color: {level_color}; margin: 0.5rem 0; font-weight: bold;">{emoji_label(icon, level_text)}</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Create radar chart for detailed metrics
    metric_data = {
        k: v
        for k, v in dimension_metrics.items()
        if isinstance(v, dict) and "score" in v
    }

    with cols[1]:
        if metric_data:
            # Convert metrics to format for radar chart
            radar_metrics = {}
            for metric_key, metric_info in metric_data.items():
                metric_name = metric_info.get("name", metric_key)
                radar_metrics[metric_name] = metric_info["score"]

            # Create and display radar chart for metrics
            radar_fig = create_radar_chart(radar_metrics)
            st.plotly_chart(radar_fig, use_container_width=True)

    # Create enhanced bar chart for detailed metrics
    if metric_data:
        bar_fig = create_bar_chart(metric_data, dimension_key)
        st.plotly_chart(bar_fig, use_container_width=True)

    # Display detailed metrics with enhanced cards
    st.markdown(
        f"""
    <div style="background: rgba(20, 45, 78, 0.4); border-radius: 10px; padding: 1rem; margin-top: 1rem;">
        <h4 style="color: {dimension_color}; margin-top: 0;">Métricas Detalhadas</h4>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Add metrics explanation
    st.markdown(
        """
    Cada métrica abaixo representa um aspecto específico da dimensão avaliada. 
    Clique em cada card para obter informações detalhadas e recomendações de melhoria.
    """
    )

    # Display metric cards in a grid
    metric_count = len(
        [
            m
            for m in dimension_metrics.items()
            if isinstance(m[1], dict) and "score" in m[1]
        ]
    )
    cols_per_row = min(3, metric_count)

    # Create rows of metrics
    rows = []
    current_row = []

    for metric_key, metric_info in dimension_metrics.items():
        if not isinstance(metric_info, dict) or "score" not in metric_info:
            continue

        current_row.append((metric_key, metric_info))

        if len(current_row) >= cols_per_row:
            rows.append(current_row)
            current_row = []

    # Add any remaining items
    if current_row:
        rows.append(current_row)

    # Create grid of metric cards
    for row in rows:
        cols = st.columns(len(row))

        for i, (metric_key, metric_info) in enumerate(row):
            with cols[i]:
                # Get metric data
                name = metric_info.get("name", metric_key)
                score = metric_info["score"]
                description = metric_info.get("description", "")
                expected_range = metric_info.get("expected_range", (50, 80))

                # Determine status
                if score < expected_range[0]:
                    status_icon = "⚠️"
                    status_text = "Abaixo do esperado"
                    status_color = "#ff7f7f"
                elif score > expected_range[1]:
                    status_icon = "⚠️"
                    status_text = "Acima do esperado"
                    status_color = "#FFEB85"
                else:
                    status_icon = "✅"
                    status_text = "Adequado"
                    status_color = "#5de0a5"

                # Create metric card with expander for details
                with st.container():
                    st.markdown(
                        f"""
                    <div style="border: 1px solid {dimension_color}40; border-radius: 10px; overflow: hidden; height: 100%; 
                         background: linear-gradient(160deg, rgba(20, 45, 78, 0.7), rgba(20, 45, 78, 0.4));">
                        <div style="padding: 0.75rem; background: {dimension_color}30; border-bottom: 1px solid {dimension_color}40;">
                            <h5 style="margin: 0; color: white;">{name}</h5>
                        </div>
                        <div style="padding: 1rem; text-align: center;">
                            <div style="font-size: 2rem; font-weight: bold; color: {dimension_color};">{score:.1f}</div>
                            <div style="width: 80%; margin: 0.75rem auto; background-color: rgba(255,255,255,0.1); height: 6px; border-radius: 3px;">
                                <div style="width: {score}%; background-color: {dimension_color}; height: 100%; border-radius: 3px;"></div>
                            </div>
                            <div style="color: {status_color}; font-weight: bold; margin-top: 0.5rem;">{emoji_label(status_icon, status_text)}</div>
                        </div>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

                    # Add expandable details
                    with st.expander("Ver detalhes"):
                        st.markdown(f"**Descrição**: {description}")
                        st.markdown(
                            f"**Faixa esperada**: {expected_range[0]} - {expected_range[1]}"
                        )

                        # Add recommendations based on status
                        st.markdown("#### Recomendações")

                        if score < expected_range[0]:
                            st.markdown(
                                f"""
                            <div class="recommendation">
                                <div class="recommendation-title">Como melhorar</div>
                                <p>Esta métrica está abaixo do esperado para textos deste tipo. Considere:</p>
                                <ul>
                                    <li>Revisar a estrutura do texto para melhorar este aspecto</li>
                                    <li>Consultar exemplos de boas práticas para {name.lower()}</li>
                                    <li>Aplicar técnicas específicas de escrita focadas nesta dimensão</li>
                                </ul>
                            </div>
                            """,
                                unsafe_allow_html=True,
                            )
                        elif score > expected_range[1]:
                            st.markdown(
                                f"""
                            <div class="recommendation">
                                <div class="recommendation-title">Observações</div>
                                <p>Esta métrica está acima do esperado, o que pode indicar:</p>
                                <ul>
                                    <li>Uso excessivo ou desnecessário de recursos relacionados a {name.lower()}</li>
                                    <li>Possível desbalanceamento com outras dimensões do texto</li>
                                    <li>Potencial complexidade adicional que pode não ser adequada ao público-alvo</li>
                                </ul>
                            </div>
                            """,
                                unsafe_allow_html=True,
                            )
                        else:
                            st.markdown(
                                """
                            <div class="recommendation">
                                <div class="recommendation-title">Análise</div>
                                <p>Esta métrica está dentro da faixa esperada para textos deste tipo.</p>
                                <p>O texto demonstra um bom equilíbrio neste aspecto, contribuindo positivamente para a qualidade global.</p>
                            </div>
                            """,
                                unsafe_allow_html=True,
                            )
