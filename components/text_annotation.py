import streamlit as st
import pandas as pd
from config import SEVERITY_LEVELS
from utils.visualization import highlight_text


def render_text_annotation(text, analysis_results):
    """
    Render the text with annotations highlighting issues and insights.

    Args:
        text (str): The original text
        analysis_results (dict): The analysis results containing annotations
    """
    if not text or not analysis_results:
        st.info(
            "Nenhum texto analisado para mostrar anotações. Realize a análise de um texto primeiro."
        )
        return

    st.subheader("Anotações Textuais")

    # Create options for annotation display
    col1, col2 = st.columns(2)

    with col1:
        highlight_options = st.multiselect(
            "Destacar problemas por severidade",
            options=["Alta", "Média", "Baixa"],
            default=["Alta", "Média", "Baixa"],
            help="Selecione quais níveis de severidade serão destacados no texto",
        )

    with col2:
        dimension_filter = st.multiselect(
            "Filtrar por dimensão",
            options=["Coesão", "Coerência", "Adequação", "Precisão", "Complexidade"],
            default=[],
            help="Selecione dimensões específicas para filtrar as anotações",
        )

    # Generate annotations from analysis results
    annotations = generate_annotations(text, analysis_results)

    # Filter annotations based on user selection
    filtered_annotations = []
    for ann in annotations:
        severity = ann.get("severity", "low")
        severity_name = SEVERITY_LEVELS.get(severity, SEVERITY_LEVELS["low"])["name"]

        dimension = ann.get("dimension", "")

        # Apply filters
        if severity_name not in highlight_options:
            continue

        if dimension_filter and dimension not in dimension_filter:
            continue

        filtered_annotations.append(ann)

    # Display the annotated text
    st.markdown("### Texto com Anotações")

    if filtered_annotations:
        # Highlight text with annotations
        highlighted_text = highlight_text(text, filtered_annotations)

        # Display highlighted text
        st.markdown(
            f'<div style="padding: 1rem; border-radius: 0.5rem; border: 1px solid #ccc; background-color: white; font-size: 1rem; line-height: 1.5; white-space: pre-wrap;">{highlighted_text}</div>',
            unsafe_allow_html=True,
        )

        # Display legend
        st.markdown("### Legenda")

        legend_cols = st.columns(3)

        with legend_cols[0]:
            st.markdown(
                f'<div style="display: flex; align-items: center; margin-bottom: 0.5rem;"><span style="background-color: {get_severity_color("high")}; width: 15px; height: 15px; display: inline-block; margin-right: 5px;"></span> Problema de alta severidade</div>',
                unsafe_allow_html=True,
            )

        with legend_cols[1]:
            st.markdown(
                f'<div style="display: flex; align-items: center; margin-bottom: 0.5rem;"><span style="background-color: {get_severity_color("medium")}; width: 15px; height: 15px; display: inline-block; margin-right: 5px;"></span> Problema de média severidade</div>',
                unsafe_allow_html=True,
            )

        with legend_cols[2]:
            st.markdown(
                f'<div style="display: flex; align-items: center; margin-bottom: 0.5rem;"><span style="background-color: {get_severity_color("low")}; width: 15px; height: 15px; display: inline-block; margin-right: 5px;"></span> Problema de baixa severidade</div>',
                unsafe_allow_html=True,
            )

        # Display annotation details in a table
        st.markdown("### Detalhes das Anotações")

        # Create DataFrame for annotations
        ann_data = []
        for i, ann in enumerate(filtered_annotations):
            severity = ann.get("severity", "low")
            severity_name = SEVERITY_LEVELS.get(severity, SEVERITY_LEVELS["low"])[
                "name"
            ]

            ann_data.append(
                {
                    "ID": i + 1,
                    "Texto": text[ann["span_start"] : ann["span_end"]],
                    "Problema": ann.get("issue_type", ""),
                    "Métrica": ann.get("metric", ""),
                    "Dimensão": ann.get("dimension", ""),
                    "Severidade": severity_name,
                    "Descrição": ann.get("description", ""),
                }
            )

        if ann_data:
            ann_df = pd.DataFrame(ann_data)
            st.dataframe(ann_df, use_container_width=True)
        else:
            st.info("Nenhuma anotação corresponde aos filtros selecionados.")
    else:
        st.info("Nenhuma anotação encontrada com os filtros selecionados.")
        # Display the plain text
        st.markdown(
            f'<div style="padding: 1rem; border-radius: 0.5rem; border: 1px solid #ccc; background-color: white; font-size: 1rem; line-height: 1.5; white-space: pre-wrap;">{text}</div>',
            unsafe_allow_html=True,
        )


def generate_annotations(text, analysis_results):
    """
    Generate text annotations from analysis results.

    Args:
        text (str): The original text
        analysis_results (dict): The analysis results

    Returns:
        list: List of annotation dictionaries
    """
    annotations = []

    # Check if we have a proper doc object to work with
    if "doc" not in analysis_results:
        return annotations

    doc = analysis_results["doc"]
    metrics = analysis_results.get("metrics", {})
    recommendations = analysis_results.get("recommendations", [])

    # Helper to map dimension keys to names
    dimension_map = {
        "coesao": "Coesão",
        "coerencia": "Coerência",
        "adequacao": "Adequação",
        "precisao": "Precisão",
        "complexidade": "Complexidade",
    }

    # Process each dimension and its metrics
    for dim_key, dim_metrics in metrics.get("dimensions", {}).items():
        # Skip the overall score
        if isinstance(dim_metrics, (int, float)):
            continue

        dimension_name = dimension_map.get(dim_key, dim_key)

        for metric_key, metric_info in dim_metrics.items():
            if not isinstance(metric_info, dict) or "score" not in metric_info:
                continue

            # Check if this metric has a low score
            score = metric_info["score"]
            expected_range = metric_info.get("expected_range", (50, 80))

            if score < expected_range[0]:
                # This metric needs improvement
                # Find the relevant segments based on recommendations
                related_recs = [
                    r
                    for r in recommendations
                    if r.get("dimension") == dim_key and r.get("metric") == metric_key
                ]

                # Get affected segments from recommendations
                segments = []
                for rec in related_recs:
                    segments.extend(rec.get("affected_segments", []))

                # If no specific segments, try to find issues in the text
                if not segments:
                    # Add annotations based on the specific metric type
                    if dim_key == "coesao" and metric_key == "referencial":
                        # Look for potential referential issues
                        for sent_idx, sent in enumerate(doc.sents):
                            for token in sent:
                                if token.pos_ in ("PRON", "DET") and token.dep_ not in (
                                    "ROOT"
                                ):
                                    potential_referents = [
                                        t
                                        for t in token.ancestors
                                        if t.pos_ in ("NOUN", "PROPN")
                                    ]
                                    if not potential_referents:
                                        # Add annotation for possible ambiguous reference
                                        annotations.append(
                                            {
                                                "span_start": token.idx,
                                                "span_end": token.idx + len(token.text),
                                                "severity": get_severity_level(score),
                                                "dimension": dimension_name,
                                                "metric": metric_info.get(
                                                    "name", metric_key
                                                ),
                                                "issue_type": "Referência ambígua",
                                                "description": "Possível referência ambígua ou vaga sem antecedente claro.",
                                            }
                                        )

                    elif dim_key == "coerencia" and metric_key == "continuidade":
                        # Look for potential topic discontinuities
                        sentences = list(doc.sents)
                        for i in range(len(sentences) - 1):
                            # Simplified check for semantic similarity
                            if (
                                sentences[i].vector.dot(sentences[i + 1].vector)
                                / (
                                    sentences[i].vector_norm
                                    * sentences[i + 1].vector_norm
                                )
                                < 0.3
                            ):
                                # Add annotation for potential topic shift
                                annotations.append(
                                    {
                                        "span_start": sentences[i + 1].start_char,
                                        "span_end": sentences[i + 1].end_char,
                                        "severity": get_severity_level(score),
                                        "dimension": dimension_name,
                                        "metric": metric_info.get("name", metric_key),
                                        "issue_type": "Descontinuidade tópica",
                                        "description": "Possível mudança abrupta de tópico sem transição adequada.",
                                    }
                                )

                    elif dim_key == "precisao" and metric_key == "estrutural":
                        # Look for complex sentence structures
                        for sent_idx, sent in enumerate(doc.sents):
                            # Simplified check for syntactic complexity
                            tokens = [
                                t for t in sent if not t.is_punct and not t.is_space
                            ]
                            verbs = [t for t in sent if t.pos_ == "VERB"]

                            if len(tokens) > 25 and len(verbs) > 3:
                                # Add annotation for complex sentence
                                annotations.append(
                                    {
                                        "span_start": sent.start_char,
                                        "span_end": sent.end_char,
                                        "severity": get_severity_level(score),
                                        "dimension": dimension_name,
                                        "metric": metric_info.get("name", metric_key),
                                        "issue_type": "Estrutura complexa",
                                        "description": "Sentença com estrutura sintática complexa que pode dificultar a compreensão.",
                                    }
                                )

                # If we still don't have annotations for this metric, add a general one
                if not any(
                    a["metric"] == metric_info.get("name", metric_key)
                    for a in annotations
                ):
                    # Find first paragraph
                    paragraphs = [p for p in text.split("\n") if p.strip()]
                    if paragraphs:
                        first_para = paragraphs[0]
                        annotations.append(
                            {
                                "span_start": text.find(first_para),
                                "span_end": text.find(first_para) + len(first_para),
                                "severity": get_severity_level(score),
                                "dimension": dimension_name,
                                "metric": metric_info.get("name", metric_key),
                                "issue_type": f"{metric_info.get('name', metric_key)} abaixo do esperado",
                                "description": f"A pontuação em {metric_info.get('name', metric_key)} está abaixo do esperado para o gênero e domínio.",
                            }
                        )

    return annotations


def get_severity_level(score):
    """
    Determine severity level based on score.

    Args:
        score (float): The metric score

    Returns:
        str: Severity level (high, medium, low)
    """
    if score < 50:
        return "high"
    elif score < 65:
        return "medium"
    else:
        return "low"


def get_severity_color(severity):
    """
    Get the color for a severity level.

    Args:
        severity (str): Severity level

    Returns:
        str: Color code
    """
    severity_colors = {
        "high": "#b91c1c",  # Dark red for better contrast
        "medium": "#b45309",  # Dark orange for better contrast
        "low": "#047857",  # Dark green for better contrast
    }

    return severity_colors.get(severity, "#f3f4f6")
