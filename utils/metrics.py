import spacy
import numpy as np
from typing import Dict, Any, Tuple
import re
import statistics
import logging
from config import REFERENCE_CORPUS_STATS, RECURSOS_LINGUISTICOS

logger = logging.getLogger(__name__)


def calculate_metrics(
    doc: spacy.tokens.Doc,
    domain: str = "Acadêmico",
    genre: str = "Artigo Científico",
    audience: str = "Acadêmico",
) -> Dict[str, Any]:
    """
    Calculate quality metrics for the text.

    Args:
        doc (spacy.tokens.Doc): Processed spaCy document
        domain (str): Text domain
        genre (str): Text genre
        audience (str): Target audience level

    Returns:
        Dict[str, Any]: Dictionary containing calculated metrics
    """
    # Check if we have a valid document
    if doc is None or len(doc) == 0:
        return {
            "overall_score": 50.0,
            "dimensions": {},
            "processing_time": {"metrics": 0.0},
        }

    # Start with empty metrics structure
    metrics = {
        "dimensions": {
            "coesao": {},
            "coerencia": {},
            "adequacao": {},
            "precisao": {},
            "complexidade": {},
        },
        "processing_time": {"metrics": 0.0},
    }

    # Calculate cohesion metrics
    metrics["dimensions"]["coesao"] = {
        "referencial": {
            "name": "Coesão Referencial",
            "score": calculate_referential_cohesion(doc),
            "description": "Avalia a qualidade das referências anafóricas e catafóricas",
            "expected_range": get_expected_range(
                "coesao", "referencial", domain, genre
            ),
        },
        "lexical": {
            "name": "Coesão Lexical",
            "score": calculate_lexical_cohesion(doc),
            "description": "Avalia a conectividade baseada em relações lexicais",
            "expected_range": get_expected_range("coesao", "lexical", domain, genre),
        },
        "estrutural": {
            "name": "Coesão Estrutural",
            "score": calculate_structural_cohesion(doc),
            "description": "Avalia o uso de conectivos e marcadores discursivos",
            "expected_range": get_expected_range("coesao", "estrutural", domain, genre),
        },
        "score": (
            calculate_referential_cohesion(doc)
            + calculate_lexical_cohesion(doc)
            + calculate_structural_cohesion(doc)
        )
        / 3,
    }

    # Calculate coherence metrics
    metrics["dimensions"]["coerencia"] = {
        "continuidade": {
            "name": "Continuidade Tópica",
            "score": calculate_topic_continuity(doc),
            "description": "Avalia a manutenção e transição entre tópicos",
            "expected_range": get_expected_range(
                "coerencia", "continuidade", domain, genre
            ),
        },
        "progressao": {
            "name": "Progressão Temática",
            "score": calculate_thematic_progression(doc),
            "description": "Avalia o desenvolvimento e a progressão de temas",
            "expected_range": get_expected_range(
                "coerencia", "progressao", domain, genre
            ),
        },
        "retorica": {
            "name": "Estrutura Retórica",
            "score": calculate_rhetorical_structure(doc),
            "description": "Avalia as relações retóricas entre segmentos do texto",
            "expected_range": get_expected_range(
                "coerencia", "retorica", domain, genre
            ),
        },
        "score": (
            calculate_topic_continuity(doc)
            + calculate_thematic_progression(doc)
            + calculate_rhetorical_structure(doc)
        )
        / 3,
    }

    # Calculate genre adequacy metrics
    metrics["dimensions"]["adequacao"] = {
        "conformidade": {
            "name": "Conformidade ao Gênero",
            "score": calculate_genre_conformity(doc, genre),
            "description": "Avalia a adequação às convenções do gênero textual",
            "expected_range": get_expected_range(
                "adequacao", "conformidade", domain, genre
            ),
        },
        "registro": {
            "name": "Adequação de Registro",
            "score": calculate_register_adequacy(doc, domain, audience),
            "description": "Avalia a adequação do registro ao contexto comunicativo",
            "expected_range": get_expected_range(
                "adequacao", "registro", domain, genre
            ),
        },
        "score": (
            calculate_genre_conformity(doc, genre)
            + calculate_register_adequacy(doc, domain, audience)
        )
        / 2,
    }

    # Calculate precision metrics
    metrics["dimensions"]["precisao"] = {
        "terminologica": {
            "name": "Precisão Terminológica",
            "score": calculate_terminological_precision(doc, domain),
            "description": "Avalia a precisão e consistência no uso de termos",
            "expected_range": get_expected_range(
                "precisao", "terminologica", domain, genre
            ),
        },
        "estrutural": {
            "name": "Clareza Estrutural",
            "score": calculate_structural_clarity(doc),
            "description": "Avalia a clareza das estruturas sintáticas",
            "expected_range": get_expected_range(
                "precisao", "estrutural", domain, genre
            ),
        },
        "score": (
            calculate_terminological_precision(doc, domain)
            + calculate_structural_clarity(doc)
        )
        / 2,
    }

    # Calculate complexity metrics
    metrics["dimensions"]["complexidade"] = {
        "lexical": {
            "name": "Complexidade Lexical",
            "score": calculate_lexical_complexity(doc),
            "description": "Avalia a sofisticação e diversidade do vocabulário",
            "expected_range": get_expected_range(
                "complexidade", "lexical", domain, genre
            ),
        },
        "sintatica": {
            "name": "Complexidade Sintática",
            "score": calculate_syntactic_complexity(doc),
            "description": "Avalia a complexidade das estruturas sintáticas",
            "expected_range": get_expected_range(
                "complexidade", "sintatica", domain, genre
            ),
        },
        "informacional": {
            "name": "Densidade Informacional",
            "score": calculate_informational_density(doc),
            "description": "Avalia a quantidade de informação por unidade textual",
            "expected_range": get_expected_range(
                "complexidade", "informacional", domain, genre
            ),
        },
        "score": (
            calculate_lexical_complexity(doc)
            + calculate_syntactic_complexity(doc)
            + calculate_informational_density(doc)
        )
        / 3,
    }

    # Calculate overall score as weighted average of dimension scores
    dimension_scores = [
        metrics["dimensions"]["coesao"]["score"],
        metrics["dimensions"]["coerencia"]["score"],
        metrics["dimensions"]["adequacao"]["score"],
        metrics["dimensions"]["precisao"]["score"],
        metrics["dimensions"]["complexidade"]["score"],
    ]

    metrics["overall_score"] = sum(dimension_scores) / len(dimension_scores)

    # Calculate percentile based on reference corpus
    metrics["percentile"] = calculate_percentile(metrics["overall_score"], domain)

    return metrics


def get_expected_range(
    dimension: str, metric: str, domain: str, genre: str
) -> Tuple[float, float]:
    """
    Get the expected range for a metric based on domain and genre.

    Args:
        dimension (str): Metric dimension
        metric (str): Specific metric
        domain (str): Text domain
        genre (str): Text genre

    Returns:
        Tuple[float, float]: Expected range as (min, max)
    """
    # Default ranges
    default_ranges = {
        "coesao": {
            "referencial": (60, 80),
            "lexical": (65, 85),
            "estrutural": (55, 75),
        },
        "coerencia": {
            "continuidade": (60, 80),
            "progressao": (55, 75),
            "retorica": (60, 80),
        },
        "adequacao": {"conformidade": (65, 85), "registro": (60, 80)},
        "precisao": {"terminologica": (65, 85), "estrutural": (60, 80)},
        "complexidade": {
            "lexical": (55, 75),
            "sintatica": (50, 70),
            "informacional": (55, 75),
        },
    }

    # Academic domains typically have higher expectations
    if domain in ["Acadêmico", "Científico"]:
        # Increase expectations by 5-10 points
        return (
            default_ranges[dimension][metric][0] + 5,
            min(default_ranges[dimension][metric][1] + 5, 95),
        )

    # Literary domain has different expectations
    elif domain == "Literário":
        # Lower some expectations, higher others
        if dimension in ["coesao", "coerencia"]:
            return (
                default_ranges[dimension][metric][0] - 5,
                default_ranges[dimension][metric][1],
            )
        elif dimension == "complexidade":
            return (
                default_ranges[dimension][metric][0] + 5,
                min(default_ranges[dimension][metric][1] + 10, 95),
            )
        else:
            return default_ranges[dimension][metric]

    # Default case
    return default_ranges[dimension][metric]


def calculate_percentile(score: float, domain: str) -> float:
    """
    Calculate percentile of the score based on reference corpus.

    Args:
        score (float): Overall quality score
        domain (str): Text domain

    Returns:
        float: Percentile (0-100)
    """
    # Get reference distribution parameters
    domain_stats = REFERENCE_CORPUS_STATS.get("overall", {}).get(
        domain, {"mean": 70, "std_dev": 10}
    )
    mean_score = domain_stats.get("mean", 70)
    std_dev = domain_stats.get("std_dev", 10)

    # Calculate z-score
    z_score = (score - mean_score) / std_dev

    # Convert to percentile (using cumulative normal distribution)
    import scipy.stats as stats

    percentile = stats.norm.cdf(z_score) * 100

    return percentile


# ============================================================
# Individual metric calculation functions
# ============================================================


def calculate_referential_cohesion(doc: spacy.tokens.Doc) -> float:
    """
    Calculate referential cohesion score.

    Args:
        doc (spacy.tokens.Doc): Processed document

    Returns:
        float: Referential cohesion score (0-100)
    """
    try:
        # Identify potential reference expressions
        reference_tokens = [
            token
            for token in doc
            if token.pos_ in ("PRON", "DET") and token.dep_ not in ("ROOT")
        ]

        # Count total sentences
        sentences = list(doc.sents)
        sentence_count = max(1, len(sentences))

        # If there are no reference tokens, assign a low score
        if not reference_tokens:
            return 50.0

        # Count reference tokens that have clear antecedents
        clear_references = 0

        for token in reference_tokens:
            # Simple heuristic: check if token has potential referents
            # (ancestors that are nouns or proper nouns)
            referents = [t for t in token.ancestors if t.pos_ in ("NOUN", "PROPN")]

            if referents:
                clear_references += 1

        # Calculate reference clarity rate
        if len(reference_tokens) > 0:
            clarity_rate = clear_references / len(reference_tokens)
        else:
            clarity_rate = 0.5  # Neutral if no references

        # Calculate reference density (references per sentence)
        ref_density = min(len(reference_tokens) / sentence_count, 3) / 3

        # Combine metrics
        score = (clarity_rate * 0.7 + ref_density * 0.3) * 100

        # Ensure score is in range 0-100
        return max(0, min(100, score))

    except Exception as e:
        logger.exception(f"Error in calculate_referential_cohesion: {e}")
        return 60.0  # Return a reasonable default


def calculate_lexical_cohesion(doc: spacy.tokens.Doc) -> float:
    """
    Calculate lexical cohesion score.

    Args:
        doc (spacy.tokens.Doc): Processed document

    Returns:
        float: Lexical cohesion score (0-100)
    """
    try:
        # Get content words (nouns, verbs, adjectives, adverbs)
        content_words = [
            token
            for token in doc
            if token.pos_ in ("NOUN", "VERB", "ADJ", "ADV")
            and not token.is_stop
            and len(token.text) > 1
        ]

        if len(content_words) < 5:
            return 50.0  # Default for very short texts

        # Count lemma repetitions
        lemma_counts = {}
        for token in content_words:
            lemma = token.lemma_.lower()
            lemma_counts[lemma] = lemma_counts.get(lemma, 0) + 1

        # Calculate lexical repetition rate
        repetition_rate = (
            sum(count > 1 for count in lemma_counts.values()) / len(lemma_counts)
            if lemma_counts
            else 0
        )

        # Calculate lexical density
        total_tokens = max(
            1, len([t for t in doc if not t.is_punct and not t.is_space])
        )
        lexical_density = len(content_words) / total_tokens

        # Calculate TTR (Type-Token Ratio) with normalization
        # Use MATTR-like approach (Moving Average TTR)
        window_size = min(100, len(content_words))
        ttrs = []

        for i in range(
            0, len(content_words) - window_size + 1, 20
        ):  # Step by 20 tokens
            window = content_words[i : i + window_size]
            unique_lemmas = set(token.lemma_.lower() for token in window)
            ttrs.append(len(unique_lemmas) / len(window))

        # If no full windows, calculate for the whole text
        if not ttrs:
            unique_lemmas = set(token.lemma_.lower() for token in content_words)
            normalized_ttr = len(unique_lemmas) / len(content_words)
        else:
            normalized_ttr = sum(ttrs) / len(ttrs)

        # Combine metrics
        # Good lexical cohesion has moderate repetition, good lexical density, and not extreme TTR
        repetition_score = 100 - abs(repetition_rate - 0.3) * 200  # Optimal around 0.3
        density_score = lexical_density * 150  # More is generally better
        ttr_score = 100 - abs(normalized_ttr - 0.65) * 200  # Optimal around 0.65

        # Combine scores
        score = repetition_score * 0.3 + density_score * 0.3 + ttr_score * 0.4

        # Ensure score is in range 0-100
        return max(0, min(100, score))

    except Exception as e:
        logger.exception(f"Error in calculate_lexical_cohesion: {e}")
        return 65.0  # Return a reasonable default


def calculate_structural_cohesion(doc: spacy.tokens.Doc) -> float:
    """
    Calculate structural cohesion score based on connectives and discourse markers.

    Args:
        doc (spacy.tokens.Doc): Processed document

    Returns:
        float: Structural cohesion score (0-100)
    """
    try:
        # Get connectives (conjunctions and certain adverbs)
        connectives = [
            token
            for token in doc
            if token.pos_ in ("CCONJ", "SCONJ")
            or (token.pos_ == "ADV" and token.dep_ == "advmod")
        ]

        # Count sentences
        sentences = list(doc.sents)
        sentence_count = max(1, len(sentences))

        # If very short text, return default score
        if sentence_count < 3:
            return 70.0

        # Calculate connective density (connectives per sentence)
        connective_density = len(connectives) / sentence_count

        # Calculate connective variety
        connective_types = set(token.lemma_.lower() for token in connectives)
        variety_score = min(1, len(connective_types) / 10)  # Cap at 10 different types

        # Look for common connective phrases not caught by simple token analysis
        text = doc.text.lower()

        # Get discourse connectives from resources
        discourse_markers = []
        for category, markers in RECURSOS_LINGUISTICOS.get("conectivos", {}).items():
            discourse_markers.extend(markers)

        # Count occurrences of multi-word connectives
        phrase_count = 0
        for phrase in discourse_markers:
            if phrase.lower() in text:
                phrase_count += text.count(phrase.lower())

        # Adjust connective density with phrase connectives
        adjusted_density = connective_density + (phrase_count / sentence_count)

        # Score based on density and variety
        density_score = min(1, adjusted_density / 2)  # Optimal is 2+ per sentence

        # Combine scores
        score = (density_score * 0.6 + variety_score * 0.4) * 100

        # Ensure score is in range 0-100
        return max(0, min(100, score))

    except Exception as e:
        logger.exception(f"Error in calculate_structural_cohesion: {e}")
        return 65.0  # Return a reasonable default


def calculate_topic_continuity(doc: spacy.tokens.Doc) -> float:
    """
    Calculate topic continuity score.

    Args:
        doc (spacy.tokens.Doc): Processed document

    Returns:
        float: Topic continuity score (0-100)
    """
    try:
        # Get sentences
        sentences = list(doc.sents)

        # If too few sentences, return default score
        if len(sentences) < 3:
            return 70.0

        # Check if sentence vectors are available
        has_vectors = hasattr(sentences[0], "vector") and sentences[0].vector.size > 0

        if has_vectors:
            # Calculate semantic similarity between adjacent sentences
            similarities = []

            for i in range(len(sentences) - 1):
                # Get sentence vectors
                vec1 = sentences[i].vector
                vec2 = sentences[i + 1].vector

                # Calculate cosine similarity only if both vectors have non-zero norm
                norm1 = np.linalg.norm(vec1)
                norm2 = np.linalg.norm(vec2)

                if norm1 > 0 and norm2 > 0:
                    sim = np.dot(vec1, vec2) / (norm1 * norm2)
                    similarities.append(sim)
                else:
                    # Default similarity if vectors unavailable
                    similarities.append(0.5)

            # Average similarity
            if similarities:
                avg_similarity = sum(similarities) / len(similarities)
            else:
                avg_similarity = 0.5  # Default if no similarities could be calculated
        else:
            # Fallback method if vectors aren't available
            # Use lexical overlap as proxy for semantic similarity
            similarities = []

            for i in range(len(sentences) - 1):
                # Get sentence tokens (excluding stopwords and punctuation)
                sent1_tokens = set(
                    token.lemma_.lower()
                    for token in sentences[i]
                    if not token.is_stop and not token.is_punct
                )
                sent2_tokens = set(
                    token.lemma_.lower()
                    for token in sentences[i + 1]
                    if not token.is_stop and not token.is_punct
                )

                # Calculate overlap (Jaccard similarity)
                if not sent1_tokens or not sent2_tokens:
                    similarities.append(0.5)  # Default for empty sentences
                else:
                    overlap = len(sent1_tokens.intersection(sent2_tokens)) / len(
                        sent1_tokens.union(sent2_tokens)
                    )
                    similarities.append(overlap)

            # Average similarity
            if similarities:
                avg_similarity = sum(similarities) / len(similarities)
            else:
                avg_similarity = 0.5  # Default

        # Check for subject consistency
        consistent_subjects = 0

        for i in range(len(sentences) - 1):
            # Get subjects in adjacent sentences
            subj1 = [
                token for token in sentences[i] if token.dep_ in ("nsubj", "nsubjpass")
            ]
            subj2 = [
                token
                for token in sentences[i + 1]
                if token.dep_ in ("nsubj", "nsubjpass")
            ]

            if subj1 and subj2:
                # Check if any subjects share the same lemma
                for s1 in subj1:
                    for s2 in subj2:
                        if s1.lemma_ == s2.lemma_:
                            consistent_subjects += 1
                            break

        # Calculate subject consistency rate
        if len(sentences) > 1:
            consistency_rate = consistent_subjects / (len(sentences) - 1)
        else:
            consistency_rate = 1.0  # Perfect for single-sentence text

        # Convert similarity to score (optimal around 0.6-0.7)
        similarity_score = 100 - abs(avg_similarity - 0.65) * 150

        # Combine with consistency rate
        score = similarity_score * 0.6 + consistency_rate * 100 * 0.4

        # Ensure score is in range 0-100
        return max(0, min(100, score))

    except Exception as e:
        logger.exception(f"Error in calculate_topic_continuity: {e}")
        return 65.0  # Return a reasonable default


def calculate_thematic_progression(doc: spacy.tokens.Doc) -> float:
    """
    Calculate thematic progression score.

    Args:
        doc (spacy.tokens.Doc): Processed document

    Returns:
        float: Thematic progression score (0-100)
    """
    try:
        # Get sentences
        sentences = list(doc.sents)

        # If too few sentences, return default score
        if len(sentences) < 3:
            return 70.0

        # Extract sentence subjects as themes
        themes = []
        for sent in sentences:
            # Look for grammatical subject
            subjects = [token for token in sent if token.dep_ in ("nsubj", "nsubjpass")]

            if subjects:
                # Use first subject as theme
                themes.append(subjects[0])
            else:
                # Fallback to first non-punctuation token
                non_punct = [token for token in sent if not token.is_punct]
                if non_punct:
                    themes.append(non_punct[0])
                else:
                    themes.append(None)  # No suitable theme

        # Analyze theme patterns
        constant_theme = 0  # Same theme repeats in consecutive sentences
        linear_progression = 0  # Rheme becomes theme of next sentence

        for i in range(len(themes) - 1):
            current = themes[i]
            next_theme = themes[i + 1]

            if current is None or next_theme is None:
                continue

            # Check for constant theme pattern
            if current.lemma_ == next_theme.lemma_:
                constant_theme += 1
                continue

            # Check for linear progression (simplified)
            # Rheme is roughly everything after the theme
            # Check if any content word in current sentence's rheme matches next theme
            current_sent = sentences[i]
            rheme_tokens = [
                t
                for t in current_sent
                if t.i > current.i and t.pos_ in ("NOUN", "PROPN", "VERB", "ADJ")
            ]

            for token in rheme_tokens:
                if token.lemma_ == next_theme.lemma_:
                    linear_progression += 1
                    break

        # Calculate pattern rates
        if len(themes) > 1:
            constant_rate = constant_theme / (len(themes) - 1)
            linear_rate = linear_progression / (len(themes) - 1)
        else:
            constant_rate = 0
            linear_rate = 0

        # Calculate pattern variety
        pattern_variety = min(constant_rate + linear_rate, 1)

        # Balance of patterns - both constant themes and development are good
        balance_score = 100 - abs(constant_rate - 0.4) * 100

        # Combine with pattern variety
        score = balance_score * 0.6 + pattern_variety * 100 * 0.4

        # Ensure score is in range 0-100
        return max(0, min(100, score))

    except Exception as e:
        logger.exception(f"Error in calculate_thematic_progression: {e}")
        return 65.0  # Return a reasonable default


def calculate_rhetorical_structure(doc: spacy.tokens.Doc) -> float:
    """
    Calculate rhetorical structure score based on discourse markers.

    Args:
        doc (spacy.tokens.Doc): Processed document

    Returns:
        float: Rhetorical structure score (0-100)
    """
    try:
        # Get sentences
        sentences = list(doc.sents)
        text = doc.text.lower()

        # If very short text, return default score
        if len(sentences) < 3:
            return 70.0

        # Define rhetorical relation markers by category
        relation_markers = {
            "thesis": ["argumento", "defendo", "proponho", "sustento", "tese"],
            "contrast": [
                "mas",
                "porém",
                "entretanto",
                "contudo",
                "todavia",
                "no entanto",
                "por outro lado",
            ],
            "cause": [
                "porque",
                "pois",
                "já que",
                "como resultado",
                "em razão de",
                "devido a",
            ],
            "elaboration": [
                "ademais",
                "além disso",
                "outro aspecto",
                "adicionalmente",
                "somado a isso",
            ],
            "example": [
                "por exemplo",
                "como exemplo",
                "para ilustrar",
                "nomeadamente",
                "a saber",
            ],
            "conclusion": [
                "portanto",
                "logo",
                "assim",
                "consequentemente",
                "conclui-se",
                "em suma",
            ],
        }

        # Count relation categories present in text
        relation_counts = {}
        for relation, markers in relation_markers.items():
            relation_counts[relation] = 0
            for marker in markers:
                relation_counts[relation] += sum(
                    1 for _ in re.finditer(r"\b" + re.escape(marker) + r"\b", text)
                )

        # Calculate variety of relations (how many different categories are used)
        relations_used = sum(1 for count in relation_counts.values() if count > 0)
        relation_variety = min(relations_used / len(relation_markers), 1)

        # Calculate relation density (markers per sentence)
        total_markers = sum(relation_counts.values())
        relation_density = (
            min(total_markers / len(sentences), 2) / 2
        )  # Cap at 2 per sentence

        # Check for presence of key discourse sections
        has_introduction = any(
            marker in text[: len(text) // 3] for marker in relation_markers["thesis"]
        )
        has_conclusion = any(
            marker in text[len(text) * 2 // 3 :]
            for marker in relation_markers["conclusion"]
        )

        structure_score = 50
        if has_introduction:
            structure_score += 25
        if has_conclusion:
            structure_score += 25

        # Combine metrics
        score = (
            relation_variety * 100 * 0.3
            + relation_density * 100 * 0.3
            + structure_score * 0.4
        )

        # Ensure score is in range 0-100
        return max(0, min(100, score))

    except Exception as e:
        logger.exception(f"Error in calculate_rhetorical_structure: {e}")
        return 65.0  # Return a reasonable default


def calculate_genre_conformity(doc: spacy.tokens.Doc, genre: str) -> float:
    """
    Calculate genre conformity score.

    Args:
        doc (spacy.tokens.Doc): Processed document
        genre (str): Text genre

    Returns:
        float: Genre conformity score (0-100)
    """
    try:
        # Define genre-specific features
        genre_features = {
            "Artigo Científico": {
                "patterns": [
                    r"\b(objetivo|propósito|finalidade)\b",
                    r"\b(metodologia|método|procedimento)\b",
                    r"\b(resultado|resultados)\b",
                    r"\b(conclusão|conclusões)\b",
                ],
                "section_markers": [
                    "introdução",
                    "metodologia",
                    "resultados",
                    "discussão",
                    "conclusão",
                ],
                "citation_patterns": [
                    r"\b\(\w+,\s+\d{4}\)",
                    r"\b\w+\s+et\s+al\.",
                    r"\bcitado\s+por\b",
                ],
            },
            "Tese/Dissertação": {
                "patterns": [
                    r"\b(objetivo|propósito|finalidade)\b",
                    r"\b(metodologia|método|procedimento)\b",
                    r"\b(resultado|resultados)\b",
                    r"\b(conclusão|conclusões)\b",
                    r"\b(capítulo|seção)\b",
                ],
                "section_markers": [
                    "introdução",
                    "revisão",
                    "metodologia",
                    "resultados",
                    "discussão",
                    "conclusão",
                ],
                "citation_patterns": [
                    r"\b\(\w+,\s+\d{4}\)",
                    r"\b\w+\s+et\s+al\.",
                    r"\bcitado\s+por\b",
                ],
            },
            "Resumo/Abstract": {
                "patterns": [
                    r"\b(objetivo|propósito|finalidade)\b",
                    r"\b(metodologia|método|procedimento)\b",
                    r"\b(resultado|resultados)\b",
                    r"\b(conclusão|conclusões)\b",
                ],
                "section_markers": [],
                "citation_patterns": [],
            },
            "Notícia": {
                "patterns": [
                    r"\bquem\b",
                    r"\bonde\b",
                    r"\bquando\b",
                    r"\bcomo\b",
                    r"\bporque\b",
                    r"\b(afirmou|declarou|disse)\b",
                ],
                "section_markers": [],
                "citation_patterns": [
                    r"\bdisse\b",
                    r"\bdeclarou\b",
                    r"\bafirmou\b",
                    r"\bsegundo\b",
                ],
            },
            "Editorial": {
                "patterns": [
                    r"\b(posição|posicionamento|opinião|defende)\b",
                    r"\b(necessário|devemos|é preciso)\b",
                ],
                "section_markers": [],
                "citation_patterns": [],
            },
        }

        # If genre not in defined list, use default scoring
        if genre not in genre_features:
            return 70.0

        # Get text
        text = doc.text.lower()

        # Check for pattern matches
        pattern_matches = 0
        for pattern in genre_features[genre].get("patterns", []):
            if re.search(pattern, text):
                pattern_matches += 1

        pattern_score = pattern_matches / max(
            1, len(genre_features[genre].get("patterns", []))
        )

        # Check for section markers
        section_matches = 0
        for marker in genre_features[genre].get("section_markers", []):
            if re.search(r"\b" + re.escape(marker) + r"\b", text):
                section_matches += 1

        section_score = section_matches / max(
            1, len(genre_features[genre].get("section_markers", []))
        )

        # Check for citation patterns if applicable
        citation_score = 0
        citation_patterns = genre_features[genre].get("citation_patterns", [])
        if citation_patterns:
            citation_matches = 0
            for pattern in citation_patterns:
                if re.search(pattern, text):
                    citation_matches += 1

            citation_score = citation_matches / len(citation_patterns)

        # Combine scores
        if citation_patterns:
            score = (
                pattern_score * 0.4 + section_score * 0.3 + citation_score * 0.3
            ) * 100
        else:
            score = (pattern_score * 0.6 + section_score * 0.4) * 100

        # Ensure score is in range 0-100
        return max(0, min(100, score))

    except Exception as e:
        logger.exception(f"Error in calculate_genre_conformity: {e}")
        return 70.0  # Return a reasonable default


def calculate_register_adequacy(
    doc: spacy.tokens.Doc, domain: str, audience: str
) -> float:
    """
    Calculate register adequacy score.

    Args:
        doc (spacy.tokens.Doc): Processed document
        domain (str): Text domain
        audience (str): Target audience

    Returns:
        float: Register adequacy score (0-100)
    """
    try:
        # Define expected formality by domain and audience
        formality_expectations = {
            "Acadêmico": {
                "Especialista": 0.9,
                "Acadêmico": 0.85,
                "Profissional": 0.8,
                "Estudante": 0.75,
                "Público Geral": 0.7,
            },
            "Científico": {
                "Especialista": 0.9,
                "Acadêmico": 0.85,
                "Profissional": 0.8,
                "Estudante": 0.75,
                "Público Geral": 0.7,
            },
            "Técnico": {
                "Especialista": 0.85,
                "Acadêmico": 0.8,
                "Profissional": 0.8,
                "Estudante": 0.7,
                "Público Geral": 0.65,
            },
            "Jurídico": {
                "Especialista": 0.95,
                "Acadêmico": 0.9,
                "Profissional": 0.85,
                "Estudante": 0.8,
                "Público Geral": 0.75,
            },
            "Médico": {
                "Especialista": 0.9,
                "Acadêmico": 0.85,
                "Profissional": 0.8,
                "Estudante": 0.7,
                "Público Geral": 0.65,
            },
            "Jornalístico": {
                "Especialista": 0.8,
                "Acadêmico": 0.75,
                "Profissional": 0.7,
                "Estudante": 0.65,
                "Público Geral": 0.6,
            },
            "Literário": {
                "Especialista": 0.7,
                "Acadêmico": 0.7,
                "Profissional": 0.65,
                "Estudante": 0.6,
                "Público Geral": 0.5,
            },
        }

        # Get expected formality
        expected_formality = formality_expectations.get(domain, {}).get(audience, 0.7)

        # Define formality markers
        formality_indicators = {
            "formal": [
                # Formal connectives
                "portanto",
                "assim",
                "consequentemente",
                "ademais",
                "entretanto",
                "todavia",
                "outrossim",
                "conforme",
                "mediante",
                "conquanto",
                # Academic vocabulary
                "metodologia",
                "análise",
                "pesquisa",
                "estudo",
                "evidência",
                "investigação",
                "paradigma",
                "abordagem",
                "hipótese",
                "conceito",
            ],
            "informal": [
                # Informal markers
                "né",
                "daí",
                "tipo",
                "tá",
                "beleza",
                "cara",
                "aí",
                "massa",
                "pra",
                "pro",
                "numa",
                "num",
                "tranquilo",
                "ó",
                "olha",
                "viu",
                # Contractions and informal expressions
                "tô",
                "tá",
                "vamo",
                "cadê",
                "a gente",
                "legal",
                "bacana",
                "valeu",
            ],
        }

        # Count formal and informal markers
        formal_count = 0
        informal_count = 0

        text = doc.text.lower()

        for marker in formality_indicators["formal"]:
            formal_count += sum(
                1 for _ in re.finditer(r"\b" + re.escape(marker) + r"\b", text)
            )

        for marker in formality_indicators["informal"]:
            informal_count += sum(
                1 for _ in re.finditer(r"\b" + re.escape(marker) + r"\b", text)
            )

        # Check for first-person usage (less formal)
        first_person = 0
        for token in doc:
            if token.text.lower() in ["eu", "minha", "meu", "nós", "nossa", "nosso"]:
                first_person += 1

        # Check for imperative verbs (can be less formal)
        imperatives = sum(
            1 for token in doc if token.mood == "Imp" if hasattr(token, "mood")
        )

        # Calculate actual formality
        total_markers = max(
            1, formal_count + informal_count + first_person + imperatives
        )
        formality_score = (
            formal_count - informal_count - first_person / 2 - imperatives / 2
        ) / total_markers + 0.5

        # Calculate how close the text is to expected formality (100 = perfect match)
        register_score = 100 - abs(formality_score - expected_formality) * 200

        # Ensure score is in range 0-100
        return max(0, min(100, register_score))

    except Exception as e:
        logger.exception(f"Error in calculate_register_adequacy: {e}")
        return 70.0  # Return a reasonable default


def calculate_terminological_precision(doc: spacy.tokens.Doc, domain: str) -> float:
    """
    Calculate terminological precision score.

    Args:
        doc (spacy.tokens.Doc): Processed document
        domain (str): Text domain

    Returns:
        float: Terminological precision score (0-100)
    """
    try:
        # Get all nouns and proper nouns that might be terms
        terms = [
            token
            for token in doc
            if token.pos_ in ("NOUN", "PROPN") and len(token.text) > 2
        ]

        if len(terms) < 5:
            return 65.0  # Default for very short texts

        # Check for consistent usage (term-lemma consistency)
        term_forms = {}
        for term in terms:
            lemma = term.lemma_.lower()
            if lemma not in term_forms:
                term_forms[lemma] = set()
            term_forms[lemma].add(term.text.lower())

        # Check how many terms have inconsistent forms
        inconsistent_terms = sum(1 for forms in term_forms.values() if len(forms) > 1)
        consistency_score = 1 - (inconsistent_terms / max(1, len(term_forms)))

        # Check for domain-specific terminology
        domain_terms = {
            "Acadêmico": RECURSOS_LINGUISTICOS.get("lexico_academico", []),
            "Científico": RECURSOS_LINGUISTICOS.get("lexico_academico", []),
            # Add other domains as needed
        }

        # Count domain-specific terms used
        domain_term_count = 0
        if domain in domain_terms:
            for term in terms:
                if term.lemma_.lower() in domain_terms[domain]:
                    domain_term_count += 1

        # Calculate domain terminology ratio
        if domain in domain_terms and domain_terms[domain]:
            domain_ratio = min(domain_term_count / len(terms), 0.4)  # Cap at 40%
            domain_score = domain_ratio / 0.4  # Normalize to 0-1
        else:
            domain_score = 0.7  # Default if no domain terms defined

        # Check for term repetitions within close proximity (potential precision issue)
        repetition_issues = 0
        window_size = 50  # tokens

        for i, token in enumerate(doc):
            if token.pos_ in ("NOUN", "PROPN") and i + window_size < len(doc):
                window = doc[i + 1 : i + window_size]
                for t in window:
                    if t.lemma_ == token.lemma_ and t.pos_ in ("NOUN", "PROPN"):
                        repetition_issues += 1
                        break

        repetition_score = 1 - min(repetition_issues / max(1, len(terms)), 0.5)

        # Combine metrics
        score = (
            consistency_score * 0.5 + domain_score * 0.3 + repetition_score * 0.2
        ) * 100

        # Ensure score is in range 0-100
        return max(0, min(100, score))

    except Exception as e:
        logger.exception(f"Error in calculate_terminological_precision: {e}")
        return 65.0  # Return a reasonable default


def calculate_structural_clarity(doc: spacy.tokens.Doc) -> float:
    """
    Calculate structural clarity score.

    Args:
        doc (spacy.tokens.Doc): Processed document

    Returns:
        float: Structural clarity score (0-100)
    """
    try:
        # Get sentences
        sentences = list(doc.sents)

        if len(sentences) < 3:
            return 70.0  # Default for very short texts

        # Analyze sentence complexity
        sentence_lengths = []
        clause_counts = []
        dependency_distances = []

        for sent in sentences:
            # Count words (excluding punctuation)
            words = [
                token for token in sent if not token.is_punct and not token.is_space
            ]
            sentence_lengths.append(len(words))

            # Count clauses (using verbs as proxy)
            verbs = [token for token in sent if token.pos_ == "VERB"]
            clause_counts.append(len(verbs))

            # Calculate average dependency distance
            distances = []
            for token in sent:
                if token.head != token:  # Skip root
                    distance = abs(token.i - token.head.i)
                    distances.append(distance)

            if distances:
                dependency_distances.append(sum(distances) / len(distances))
            else:
                dependency_distances.append(0)

        # Calculate average sentence length and variance
        avg_length = sum(sentence_lengths) / len(sentence_lengths)
        length_variance = (
            statistics.variance(sentence_lengths) if len(sentence_lengths) > 1 else 0
        )

        # Calculate average clause count
        avg_clauses = sum(clause_counts) / len(clause_counts)

        # Calculate average dependency distance
        avg_dependency = (
            sum(dependency_distances) / len(dependency_distances)
            if dependency_distances
            else 0
        )

        # Evaluate sentence length (optimal around 15-25 words)
        if avg_length < 8:
            length_score = avg_length / 8  # Too short
        elif avg_length > 30:
            length_score = 1 - ((avg_length - 30) / 30)  # Too long
        else:
            length_score = 1  # Optimal

        # Evaluate clause density (optimal around 1.5-2.5 clauses per sentence)
        if avg_clauses < 1:
            clause_score = avg_clauses  # Too simple
        elif avg_clauses > 3:
            clause_score = 1 - ((avg_clauses - 3) / 3)  # Too complex
        else:
            clause_score = 1  # Optimal

        # Evaluate dependency distance (shorter distances are generally clearer)
        distance_score = 1 - min(avg_dependency / 3, 1)

        # Evaluate variance (some variance is good for readability)
        variance_score = min(length_variance / 25, 1)

        # Combine metrics
        score = (
            length_score * 0.3
            + clause_score * 0.3
            + distance_score * 0.2
            + variance_score * 0.2
        ) * 100

        # Ensure score is in range 0-100
        return max(0, min(100, score))

    except Exception as e:
        logger.exception(f"Error in calculate_structural_clarity: {e}")
        return 65.0  # Return a reasonable default


def calculate_lexical_complexity(doc: spacy.tokens.Doc) -> float:
    """
    Calculate lexical complexity score.

    Args:
        doc (spacy.tokens.Doc): Processed document

    Returns:
        float: Lexical complexity score (0-100)
    """
    try:
        # Get content words
        content_words = [
            token
            for token in doc
            if token.pos_ in ("NOUN", "VERB", "ADJ", "ADV")
            and not token.is_stop
            and len(token.text) > 1
        ]

        if len(content_words) < 10:
            return 60.0  # Default for very short texts

        # Calculate average word length
        avg_word_length = sum(len(token.text) for token in content_words) / len(
            content_words
        )

        # Calculate lexical diversity (TTR with window approach to account for text length)
        windows = []
        window_size = min(100, len(content_words))

        for i in range(0, len(content_words) - window_size + 1, 20):
            window = content_words[i : i + window_size]
            unique_lemmas = set(token.lemma_.lower() for token in window)
            windows.append(len(unique_lemmas) / window_size)

        lexical_diversity = sum(windows) / len(windows) if windows else 0.6

        # Check for rare/sophisticated words
        # Simple heuristic: longer words tend to be more sophisticated
        sophisticated_words = [token for token in content_words if len(token.text) > 8]
        sophistication_ratio = len(sophisticated_words) / len(content_words)

        # Calculate lexical density
        total_tokens = len(
            [token for token in doc if not token.is_punct and not token.is_space]
        )
        lexical_density = len(content_words) / total_tokens

        # Combine metrics
        # Convert to scores where higher is more complex
        length_score = min(avg_word_length / 10, 1)  # Cap at words of length 10
        diversity_score = lexical_diversity  # Already normalized
        sophistication_score = min(
            sophistication_ratio / 0.2, 1
        )  # Cap at 20% sophisticated
        density_score = min(lexical_density / 0.6, 1)  # Cap at 60% density

        # Combine scores
        score = (
            length_score * 0.25
            + diversity_score * 0.3
            + sophistication_score * 0.2
            + density_score * 0.25
        ) * 100

        # Ensure score is in range 0-100
        return max(0, min(100, score))

    except Exception as e:
        logger.exception(f"Error in calculate_lexical_complexity: {e}")
        return 60.0  # Return a reasonable default


def calculate_syntactic_complexity(doc: spacy.tokens.Doc) -> float:
    """
    Calculate syntactic complexity score.

    Args:
        doc (spacy.tokens.Doc): Processed document

    Returns:
        float: Syntactic complexity score (0-100)
    """
    try:
        # Get sentences
        sentences = list(doc.sents)

        if len(sentences) < 3:
            return 65.0  # Default for very short texts

        # Count clauses per sentence
        clause_counts = []
        for sent in sentences:
            verbs = [token for token in sent if token.pos_ == "VERB"]
            clause_counts.append(len(verbs))

        # Calculate subordination (simplified as dependency depth)
        max_depths = []
        for sent in sentences:
            depths = {}

            # Calculate depth for each token
            for token in sent:
                if token.dep_ == "ROOT":
                    depths[token.i] = 0
                    continue

                depth = 1
                head = token.head
                while head.dep_ != "ROOT":
                    depth += 1
                    head = head.head
                depths[token.i] = depth

            max_depths.append(max(depths.values()) if depths else 0)

        # Calculate average clause count and max depth
        avg_clauses = sum(clause_counts) / len(clause_counts)
        avg_depth = sum(max_depths) / len(max_depths)

        # Calculate sentence length
        sentence_lengths = [
            len([token for token in sent if not token.is_punct]) for sent in sentences
        ]
        avg_length = sum(sentence_lengths) / len(sentence_lengths)

        # Check for complex constructions
        complex_constructions = 0
        for sent in sentences:
            # Count subordinate clauses
            subordinate = sum(
                1 for token in sent if token.dep_ in ("ccomp", "xcomp", "advcl", "acl")
            )

            # Count passive constructions
            passive = sum(1 for token in sent if "pass" in token.dep_)

            # Count preposition chains
            prep_chains = 0
            for token in sent:
                if token.dep_ == "prep":
                    chain = 1
                    for child in token.children:
                        if child.dep_ == "prep":
                            chain += 1
                    prep_chains += chain - 1 if chain > 1 else 0

            complex_constructions += subordinate + passive + prep_chains

        # Normalize complex constructions per sentence
        complex_per_sentence = complex_constructions / len(sentences)

        # Convert to scores (higher means more complex)
        clause_score = min(avg_clauses / 3, 1)  # Cap at 3 clauses per sentence
        depth_score = min(avg_depth / 5, 1)  # Cap at depth of 5
        length_score = min(avg_length / 30, 1)  # Cap at 30 words
        construction_score = min(
            complex_per_sentence / 3, 1
        )  # Cap at 3 complex features per sentence

        # Combine scores
        score = (
            clause_score * 0.3
            + depth_score * 0.3
            + length_score * 0.2
            + construction_score * 0.2
        ) * 100

        # Ensure score is in range 0-100
        return max(0, min(100, score))

    except Exception as e:
        logger.exception(f"Error in calculate_syntactic_complexity: {e}")
        return 65.0  # Return a reasonable default


def calculate_informational_density(doc: spacy.tokens.Doc) -> float:
    """
    Calculate informational density score.

    Args:
        doc (spacy.tokens.Doc): Processed document

    Returns:
        float: Informational density score (0-100)
    """
    try:
        # Count content words vs. functional words
        content_tokens = [
            token
            for token in doc
            if token.pos_ in ("NOUN", "VERB", "ADJ", "ADV") and not token.is_stop
        ]
        function_tokens = [
            token
            for token in doc
            if token.pos_ in ("ADP", "AUX", "CCONJ", "DET", "PART", "PRON", "SCONJ")
        ]

        if len(content_tokens) + len(function_tokens) < 20:
            return 60.0  # Default for very short texts

        # Calculate content-function ratio
        cf_ratio = len(content_tokens) / max(1, len(function_tokens))

        # Count unique content lemmas (information richness)
        unique_lemmas = set(token.lemma_.lower() for token in content_tokens)

        # Calculate type-token ratio for content words
        content_ttr = len(unique_lemmas) / max(1, len(content_tokens))

        # Count named entities (indication of specific information)
        entities = list(doc.ents)
        entity_density = len(entities) / max(1, len(list(doc.sents)))

        # Check for nominalization (often increases information density)
        nominal_endings = [
            "ção",
            "são",
            "mento",
            "ância",
            "ência",
            "idade",
            "ismo",
            "itude",
        ]
        nominalizations = sum(
            1
            for token in doc
            if any(token.text.lower().endswith(ending) for ending in nominal_endings)
        )
        nominalization_density = nominalizations / max(1, len(content_tokens))

        # Convert to scores
        cf_score = min(cf_ratio / 1.5, 1)  # Optimal around 1.5
        ttr_score = min(content_ttr / 0.7, 1)  # Optimal around 0.7
        entity_score = min(entity_density / 2, 1)  # Cap at 2 entities per sentence
        nominalization_score = min(
            nominalization_density / 0.1, 1
        )  # Cap at 10% nominalizations

        # Combine scores
        score = (
            cf_score * 0.4
            + ttr_score * 0.3
            + entity_score * 0.15
            + nominalization_score * 0.15
        ) * 100

        # Ensure score is in range 0-100
        return max(0, min(100, score))

    except Exception as e:
        logger.exception(f"Error in calculate_informational_density: {e}")
        return 60.0  # Return a reasonable default
