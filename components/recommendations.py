import streamlit as st
from config import METRIC_DIMENSIONS, SEVERITY_LEVELS


def render_recommendations(recommendations):
    """
    Render text improvement recommendations based on analysis results.

    Args:
        recommendations (list): List of recommendation dictionaries
    """
    if not recommendations:
        st.info(
            "Nenhuma recomendação disponível. Realize a análise de um texto primeiro."
        )
        return

    st.subheader("Recomendações para Melhoria do Texto")

    # Display priority legend
    st.markdown("### Prioridades de Melhoria")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f'<div style="display: flex; align-items: center;"><span style="background-color: {SEVERITY_LEVELS["high"]["color"]}; width: 12px; height: 12px; display: inline-block; margin-right: 5px; border-radius: 2px;"></span> Alta Prioridade</div>',
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f'<div style="display: flex; align-items: center;"><span style="background-color: {SEVERITY_LEVELS["medium"]["color"]}; width: 12px; height: 12px; display: inline-block; margin-right: 5px; border-radius: 2px;"></span> Média Prioridade</div>',
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f'<div style="display: flex; align-items: center;"><span style="background-color: {SEVERITY_LEVELS["low"]["color"]}; width: 12px; height: 12px; display: inline-block; margin-right: 5px; border-radius: 2px;"></span> Baixa Prioridade</div>',
            unsafe_allow_html=True,
        )

    # Group recommendations by dimension
    dimension_recs = {}

    for rec in recommendations:
        dim = rec.get("dimension", "geral")
        if dim not in dimension_recs:
            dimension_recs[dim] = []
        dimension_recs[dim].append(rec)

    # Summary of recommendations
    st.markdown("### Resumo das Recomendações")

    # Create summary cards
    cols = st.columns(len(dimension_recs) if len(dimension_recs) <= 3 else 3)

    for i, (dim, recs) in enumerate(dimension_recs.items()):
        col_idx = i % 3

        with cols[col_idx]:
            # Get dimension name and color
            dim_info = METRIC_DIMENSIONS.get(dim, {"name": "Geral", "color": "#6c757d"})
            dim_name = dim_info["name"]
            dim_color = dim_info["color"]

            # Count recommendations by priority
            high_count = sum(1 for r in recs if r.get("priority") == "high")
            medium_count = sum(1 for r in recs if r.get("priority") == "medium")
            low_count = sum(1 for r in recs if r.get("priority") == "low")

            # Calculate potential improvement
            potential_improvement = sum(r.get("potential_improvement", 0) for r in recs)

            # Create card
            st.markdown(
                f"""
                <div style="padding: 1rem; border-radius: 0.5rem; border-left: 5px solid {dim_color}; background-color: white; margin-bottom: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.12);">
                    <h4 style="margin-top: 0; color: {dim_color};">{dim_name}</h4>
                    <p><strong>Recomendações:</strong> {len(recs)}</p>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                        <span>Alta: {high_count}</span>
                        <span>Média: {medium_count}</span>
                        <span>Baixa: {low_count}</span>
                    </div>
                    <p><strong>Potencial de melhoria:</strong> +{potential_improvement:.1f} pontos</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Detailed recommendations
    st.markdown("### Recomendações Detalhadas")

    # Create expanders for each dimension
    for dim, recs in dimension_recs.items():
        # Get dimension name
        dim_info = METRIC_DIMENSIONS.get(dim, {"name": "Geral", "color": "#6c757d"})
        dim_name = dim_info["name"]

        with st.expander(f"{dim_name} ({len(recs)} recomendações)", expanded=True):
            # Sort recommendations by priority and potential improvement
            sorted_recs = sorted(
                recs,
                key=lambda r: (
                    (
                        0
                        if r.get("priority") == "high"
                        else (1 if r.get("priority") == "medium" else 2)
                    ),
                    -r.get("potential_improvement", 0),
                ),
            )

            # Display each recommendation
            for rec in sorted_recs:
                render_recommendation_card(rec)


def render_recommendation_card(recommendation):
    """
    Render a single recommendation card.

    Args:
        recommendation (dict): Recommendation dictionary
    """
    # Get priority and color
    priority = recommendation.get("priority", "medium")
    priority_color = SEVERITY_LEVELS.get(priority, SEVERITY_LEVELS["medium"])["color"]

    # Get dimension and metric info
    dimension = recommendation.get("dimension", "geral")

    dim_info = METRIC_DIMENSIONS.get(dimension, {"name": "Geral", "color": "#6c757d"})
    dim_name = dim_info["name"]
    dim_color = dim_info["color"]

    # Get affected segments
    affected_segments = recommendation.get("affected_segments", [])

    # Create card
    st.markdown(
        f"""
        <div style="padding: 1.5rem; border-radius: 0.5rem; border-left: 5px solid {priority_color}; background-color: white; margin-bottom: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.12);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h4 style="margin: 0; color: {priority_color};">{recommendation.get("title", "Recomendação")}</h4>
                <span style="background-color: {priority_color}; color: white; padding: 0.25rem 0.5rem; border-radius: 0.25rem; font-size: 0.8rem;">{priority.upper()}</span>
            </div>
            <p style="margin-bottom: 1rem;"><strong>Dimensão:</strong> <span style="color: {dim_color};">{dim_name}</span></p>
            <p>{recommendation.get("description", "")}</p>
            {f'<p><strong>Segmentos afetados:</strong> {", ".join([f"Segmento {s+1}" for s in affected_segments])}</p>' if affected_segments else ''}
            <p style="margin-top: 1rem;"><strong>Potencial de melhoria:</strong> +{recommendation.get("potential_improvement", 0):.1f} pontos</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
