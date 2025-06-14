import spacy
import numpy as np
from typing import Dict, List, Any, Optional


def generate_recommendations(
    doc: spacy.tokens.Doc,
    metrics: Dict[str, Any],
    domain: str = "Acadêmico",
    genre: str = "Artigo Científico",
) -> List[Dict[str, Any]]:
    """
    Generate text improvement recommendations based on metrics.

    Args:
        doc (spacy.tokens.Doc): Processed spaCy document
        metrics (Dict[str, Any]): Calculated metrics
        domain (str): Text domain
        genre (str): Text genre

    Returns:
        List[Dict[str, Any]]: List of recommendations
    """
    recommendations = []

    # Check for low-scoring metrics
    for dim_key, dim_metrics in metrics["dimensions"].items():
        for metric_key, metric_info in dim_metrics.items():
            if isinstance(metric_info, dict) and "score" in metric_info:
                score = metric_info["score"]
                expected_range = metric_info.get("expected_range", (70, 90))
                expected_min = expected_range[0]

                if score < expected_min:
                    # Generate recommendation for this low-scoring metric
                    recommendation = generate_metric_recommendation(
                        doc, dim_key, metric_key, metric_info, domain, genre
                    )

                    if recommendation is not None:
                        recommendations.append(recommendation)

    # Add general improvement recommendations if needed
    if metrics["overall_score"] < 70 and len(recommendations) < 3:
        general_recs = generate_general_recommendations(doc, metrics, domain, genre)
        recommendations.extend(general_recs)

    # Sort recommendations by priority (higher improvement potential first)
    recommendations.sort(key=lambda x: x["potential_improvement"], reverse=True)

    return recommendations


def generate_metric_recommendation(
    doc: spacy.tokens.Doc,
    dimension: str,
    metric: str,
    metric_info: Dict[str, Any],
    domain: str,
    genre: str,
) -> Dict[str, Any]:
    """
    Generate a recommendation for a specific metric.

    Args:
        doc (spacy.tokens.Doc): Processed document
        dimension (str): Metric dimension
        metric (str): Specific metric
        metric_info (Dict[str, Any]): Metric information
        domain (str): Text domain
        genre (str): Text genre

    Returns:
        Dict[str, Any]: Recommendation dictionary
    """
    # Map dimension and metric to recommendation strategies
    recommendation_strategies = {
        "coesao": {
            "referencial": recommend_referential_cohesion,
            "lexical": recommend_lexical_cohesion,
            "estrutural": recommend_structural_cohesion,
        },
        "coerencia": {
            "continuidade": recommend_topic_continuity,
            "progressao": recommend_thematic_progression,
            "retorica": recommend_rhetorical_structure,
        },
        "adequacao": {
            "conformidade": recommend_genre_conformity,
            "registro": recommend_register_adequacy,
        },
        "precisao": {
            "terminologica": recommend_terminological_precision,
            "estrutural": recommend_structural_clarity,
        },
        "complexidade": {
            "lexical": recommend_lexical_complexity,
            "sintatica": recommend_syntactic_complexity,
            "informacional": recommend_informational_density,
        },
    }

    # Get the appropriate recommendation function
    if (
        dimension in recommendation_strategies
        and metric in recommendation_strategies[dimension]
    ):
        recommendation_func = recommendation_strategies[dimension][metric]
        return recommendation_func(doc, metric_info, domain, genre)

    # Fallback to generic recommendation
    return {
        "id": f"{dimension}_{metric}_rec",
        "dimension": dimension,
        "metric": metric,
        "title": f"Melhore a {metric_info.get('name', metric)}",
        "description": f"A pontuação em {metric_info.get('name', metric)} está abaixo do esperado. Considere revisar o texto para melhorar este aspecto.",
        "priority": "medium",
        "potential_improvement": 5.0,
        "affected_segments": [],
    }


def generate_general_recommendations(
    doc: spacy.tokens.Doc, metrics: Dict[str, Any], domain: str, genre: str
) -> List[Dict[str, Any]]:
    """
    Generate general text improvement recommendations.

    Args:
        doc (spacy.tokens.Doc): Processed document
        metrics (Dict[str, Any]): Calculated metrics
        domain (str): Text domain
        genre (str): Text genre

    Returns:
        List[Dict[str, Any]]: List of general recommendations
    """
    general_recommendations = []

    # Find the lowest scoring dimension
    dimension_scores = {
        dim: np.mean(
            [
                m["score"]
                for m in metrics["dimensions"][dim].values()
                if isinstance(m, dict) and "score" in m
            ]
        )
        for dim in metrics["dimensions"]
    }

    lowest_dim = min(dimension_scores, key=dimension_scores.get)
    lowest_score = dimension_scores[lowest_dim]

    if lowest_score < 60:
        # Add a general recommendation for the lowest dimension
        dimension_name = {
            "coesao": "Coesão Textual",
            "coerencia": "Coerência Discursiva",
            "adequacao": "Adequação ao Gênero",
            "precisao": "Precisão e Clareza",
            "complexidade": "Complexidade Linguística",
        }.get(lowest_dim, lowest_dim)

        general_recommendations.append(
            {
                "id": f"general_{lowest_dim}_rec",
                "dimension": lowest_dim,
                "metric": "general",
                "title": f"Melhore a {dimension_name}",
                "description": f"A dimensão de {dimension_name} apresenta a pontuação mais baixa do texto. Concentre seus esforços de revisão neste aspecto para maior impacto.",
                "priority": "high",
                "potential_improvement": 10.0,
                "affected_segments": [],
            }
        )

    # Add recommendation about text structure if coherence or genre adequacy is low
    if (
        dimension_scores.get("coerencia", 100) < 70
        or dimension_scores.get("adequacao", 100) < 70
    ):
        general_recommendations.append(
            {
                "id": "general_structure_rec",
                "dimension": "estrutura",
                "metric": "general",
                "title": "Revise a Estrutura Geral do Texto",
                "description": "Considere reorganizar os parágrafos e seções para criar uma progressão mais clara de ideias. Uma estrutura bem definida melhora tanto a coerência quanto a adequação ao gênero textual.",
                "priority": "medium",
                "potential_improvement": 7.5,
                "affected_segments": [],
            }
        )

    return general_recommendations


# Specific recommendation functions


def recommend_referential_cohesion(
    doc: spacy.tokens.Doc, metric_info: Dict[str, Any], domain: str, genre: str
) -> Dict[str, Any]:
    """Generate recommendation for improving referential cohesion"""
    # Identify problematic references
    sentences = list(doc.sents)
    reference_tokens = [
        token
        for token in doc
        if token.pos_ in ("PRON", "DET") and token.dep_ not in ("ROOT")
    ]

    problematic_refs = []
    for token in reference_tokens:
        # Simple heuristic: check if token has no obvious referent
        potential_referents = [
            t for t in token.ancestors if t.pos_ in ("NOUN", "PROPN")
        ]
        if not potential_referents:
            sent_idx = -1
            for i, sent in enumerate(sentences):
                if token.i >= sent.start and token.i < sent.end:
                    sent_idx = i
                    break

            if sent_idx >= 0:
                problematic_refs.append(
                    {
                        "token": token.text,
                        "sentence_idx": sent_idx,
                        "sentence": sentences[sent_idx].text,
                    }
                )

    # Create recommendation
    affected_segments = []
    examples = []

    for i, ref in enumerate(problematic_refs[:3]):  # Limit to 3 examples
        affected_segments.append(ref["sentence_idx"])
        examples.append(f"'{ref['token']}' em: \"{ref['sentence']}\"")

    description = f"""A coesão referencial do texto pode ser melhorada. Foram encontradas referências potencialmente ambíguas ou vagas, como:
    
{' '.join([f"- {ex}" for ex in examples])}
    
Recomendações:
- Certifique-se de que cada referência (pronomes, artigos definidos) tenha um antecedente claro
- Evite distâncias muito grandes entre referências e seus antecedentes
- Considere usar repetições lexicais em vez de pronomes quando houver risco de ambiguidade"""

    return {
        "id": "cohesion_referential_rec",
        "dimension": "coesao",
        "metric": "referencial",
        "title": "Melhore a Coesão Referencial",
        "description": description,
        "priority": "high" if metric_info["score"] < 60 else "medium",
        "potential_improvement": min(10, 80 - metric_info["score"]) / 2 + 5,
        "affected_segments": affected_segments,
    }


def recommend_lexical_cohesion(
    doc: spacy.tokens.Doc, metric_info: Dict[str, Any], domain: str, genre: str
) -> Dict[str, Any]:
    """Generate recommendation for improving lexical cohesion"""
    # Identify potential lexical cohesion issues
    content_words = [
        token
        for token in doc
        if token.pos_ in ("NOUN", "VERB", "ADJ", "ADV") and not token.is_stop
    ]

    # Check for potential synonym overuse
    lemma_counts = {}
    for token in content_words:
        lemma_counts[token.lemma_] = lemma_counts.get(token.lemma_, 0) + 1

    # Get words with high frequency that might need variation
    repeated_lemmas = [lemma for lemma, count in lemma_counts.items() if count > 5]

    # Create recommendation
    if repeated_lemmas:
        examples = repeated_lemmas[:3]  # Limit to 3 examples
        examples_str = ", ".join([f"'{ex}'" for ex in examples])

        description = f"""A coesão lexical do texto pode ser aprimorada. Foram encontrados termos com alta repetição, como {examples_str}.
        
Recomendações:
- Utilize sinônimos apropriados para evitar repetições excessivas
- Estabeleça cadeias lexicais usando termos semanticamente relacionados
- Empregue hiperônimos e hipônimos para criar variação
- Considere usar expressões equivalentes quando apropriado"""
    else:
        description = """A coesão lexical do texto pode ser aprimorada.
        
Recomendações:
- Estabeleça relações semânticas mais fortes entre os termos do texto
- Utilize repetições estratégicas de palavras-chave para reforçar temas importantes
- Crie cadeias lexicais mais consistentes ao longo dos parágrafos
- Evite mudanças abruptas de vocabulário entre seções do texto"""

    return {
        "id": "cohesion_lexical_rec",
        "dimension": "coesao",
        "metric": "lexical",
        "title": "Aprimore a Coesão Lexical",
        "description": description,
        "priority": "medium",
        "potential_improvement": min(10, 80 - metric_info["score"]) / 2 + 3,
        "affected_segments": [],
    }


def recommend_structural_cohesion(
    doc: spacy.tokens.Doc, metric_info: Dict[str, Any], domain: str, genre: str
) -> Dict[str, Any]:
    """Generate recommendation for improving structural cohesion"""
    # Identify connecting words
    connectives = [
        token
        for token in doc
        if token.pos_ in ("CCONJ", "SCONJ")
        or (token.pos_ == "ADV" and token.dep_ == "advmod")
    ]

    sentences = list(doc.sents)
    connective_types = set(token.lemma_ for token in connectives)

    low_variety = len(connective_types) < 5
    low_density = len(connectives) / len(sentences) < 0.5 if sentences else True

    # Create recommendation
    if low_density:
        description = """A coesão estrutural do texto pode ser aprimorada com o uso mais frequente de marcadores discursivos e conectivos.
        
Recomendações:
- Adicione conectivos para explicitar as relações entre sentenças e parágrafos
- Utilize marcadores de transição entre seções e tópicos do texto
- Empregue expressões que sinalizem a progressão do texto (primeiro, em seguida, finalmente)
- Certifique-se de que as relações lógicas entre ideias estejam explícitas"""
    elif low_variety:
        description = """A coesão estrutural do texto pode ser aprimorada com uma maior variedade de conectivos e marcadores discursivos.
        
Recomendações:
- Amplie o repertório de conectivos utilizados (além de 'e', 'mas', 'porque')
- Utilize conectivos mais específicos para as relações pretendidas (consequência, contraste, exemplificação)
- Empregue marcadores discursivos no início de parágrafos para sinalizar sua função
- Varie a estrutura das ligações entre sentenças para evitar repetitividade"""
    else:
        description = """A coesão estrutural do texto pode ser aprimorada com melhor distribuição e uso de conectivos.
        
Recomendações:
- Verifique se os conectivos utilizados são os mais adequados para as relações pretendidas
- Distribua marcadores discursivos estrategicamente nos pontos de transição do texto
- Certifique-se de que as relações entre parágrafos estejam claramente sinalizadas
- Mantenha consistência no uso de marcadores ao longo do texto"""

    return {
        "id": "cohesion_structural_rec",
        "dimension": "coesao",
        "metric": "estrutural",
        "title": "Melhore a Coesão Estrutural",
        "description": description,
        "priority": "medium",
        "potential_improvement": min(10, 80 - metric_info["score"]) / 2 + 4,
        "affected_segments": [],
    }


def recommend_topic_continuity(
    doc: spacy.tokens.Doc,
    metric_info: Dict[str, Any],
    domain: str,
    genre: str,
) -> Optional[Dict[str, Any]]:
    """Generate recommendation for improving topic continuity.

    Returns ``None`` when there are not enough sentences to analyse.
    """
    sentences = list(doc.sents)

    if len(sentences) < 3:
        # Not enough sentences to analyze
        return None

    # Calculate semantic similarity between adjacent sentences
    sentence_embeddings = [sent.vector for sent in sentences]

    # Find potential topic shifts
    shifts = []
    for i in range(len(sentence_embeddings) - 1):
        # Calculate cosine similarity
        vec1 = sentence_embeddings[i]
        vec2 = sentence_embeddings[i + 1]

        # Normalize vectors
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 > 0 and norm2 > 0:
            sim = np.dot(vec1, vec2) / (norm1 * norm2)

            if sim < 0.3:  # Threshold for potential topic shift
                shifts.append(i)

    # Create recommendation
    affected_segments = []
    examples = []

    for i, shift_idx in enumerate(shifts[:2]):  # Limit to 2 examples
        affected_segments.append(shift_idx)
        affected_segments.append(shift_idx + 1)

        sent1 = sentences[shift_idx].text
        sent2 = sentences[shift_idx + 1].text

        examples.append(f'Entre: "{sent1}" e "{sent2}"')

    if shifts:
        description = f"""A continuidade tópica do texto pode ser melhorada. Foram identificadas possíveis mudanças abruptas de tópico:
        
{' '.join([f"- {ex}" for ex in examples])}
        
Recomendações:
- Adicione sentenças de transição entre tópicos diferentes
- Mantenha o mesmo sujeito/tema em sentenças consecutivas quando possível
- Utilize referências explícitas ao tópico anterior ao introduzir um novo
- Considere reorganizar o texto para agrupar ideias relacionadas"""
    else:
        description = """A continuidade tópica do texto pode ser melhorada.
        
Recomendações:
- Fortaleça as conexões semânticas entre sentenças adjacentes
- Mantenha um foco claro em cada parágrafo, desenvolvendo um único tópico
- Faça transições graduais ao mudar de tópico
- Utilize elementos de retomada para manter a continuidade temática"""

    return {
        "id": "coherence_continuity_rec",
        "dimension": "coerencia",
        "metric": "continuidade",
        "title": "Melhore a Continuidade Tópica",
        "description": description,
        "priority": "high" if metric_info["score"] < 60 else "medium",
        "potential_improvement": min(10, 80 - metric_info["score"]) / 2 + 5,
        "affected_segments": affected_segments,
    }


def recommend_thematic_progression(
    doc: spacy.tokens.Doc,
    metric_info: Dict[str, Any],
    domain: str,
    genre: str,
) -> Optional[Dict[str, Any]]:
    """Generate recommendation for improving thematic progression.

    Returns ``None`` when there are not enough sentences to analyse.
    """
    sentences = list(doc.sents)

    if len(sentences) < 3:
        # Not enough sentences to analyze
        return None

    # Extract sentence subjects (simplified)
    sentence_subjects = []
    for sent in sentences:
        subjects = [token for token in sent if token.dep_ in ("nsubj", "nsubjpass")]
        if subjects:
            sentence_subjects.append(subjects[0])
        else:
            # Fallback to first noun or first token
            nouns = [token for token in sent if token.pos_ in ("NOUN", "PROPN")]
            if nouns:
                sentence_subjects.append(nouns[0])
            else:
                sentence_subjects.append(sent[0])

    # Check for thematic patterns
    constant_theme = 0
    for i in range(len(sentence_subjects) - 1):
        if sentence_subjects[i].lemma_ == sentence_subjects[i + 1].lemma_:
            constant_theme += 1

    constant_rate = constant_theme / (len(sentences) - 1)

    # Create recommendation
    if constant_rate > 0.7:
        description = """A progressão temática do texto pode ser aprimorada, evitando o uso excessivo do padrão de tema constante.
        
Recomendações:
- Varie a estrutura das sentenças para evitar começar todas com o mesmo tema
- Incorpore o padrão de progressão linear, onde o rema de uma sentença se torna o tema da próxima
- Utilize o padrão de tema derivado, introduzindo temas relacionados a um hipertema
- Alterne entre diferentes padrões de progressão para criar um texto mais dinâmico"""
    elif constant_rate < 0.2:
        description = """A progressão temática do texto pode ser aprimorada, estabelecendo conexões mais fortes entre os temas das sentenças.
        
Recomendações:
- Crie mais instâncias do padrão de tema constante para estabelecer tópicos claros
- Desenvolva cadeias de referência mais explícitas entre sentenças
- Verifique se há temas não relacionados que prejudicam a unidade do texto
- Organize as sentenças de modo a criar uma progressão lógica de ideias"""
    else:
        description = """A progressão temática do texto pode ser aprimorada, com um equilíbrio mais eficaz entre continuidade e desenvolvimento.
        
Recomendações:
- Estabeleça uma estratégia clara de progressão temática em cada parágrafo
- Inicie parágrafos com sentenças tópico claras que anunciem o tema
- Desenvolva cada tema adequadamente antes de passar ao próximo
- Utilize expressões de transição que sinalizem mudanças temáticas"""

    return {
        "id": "coherence_progression_rec",
        "dimension": "coerencia",
        "metric": "progressao",
        "title": "Aprimore a Progressão Temática",
        "description": description,
        "priority": "medium",
        "potential_improvement": min(10, 80 - metric_info["score"]) / 2 + 4,
        "affected_segments": [],
    }


def recommend_rhetorical_structure(
    doc: spacy.tokens.Doc, metric_info: Dict[str, Any], domain: str, genre: str
) -> Dict[str, Any]:
    """Generate recommendation for improving rhetorical structure"""
    sentences = list(doc.sents)

    # Simple check for discourse markers
    relation_markers = {
        "contrast": ["but", "however", "yet", "although", "though", "while", "whereas"],
        "cause": ["because", "since", "as", "therefore", "thus", "consequently", "so"],
        "elaboration": ["furthermore", "moreover", "in addition", "additionally"],
        "example": ["for example", "for instance", "such as", "including"],
        "conclusion": ["in conclusion", "to summarize", "finally", "in summary"],
    }

    # Count relation types in text
    relation_counts = {relation: 0 for relation in relation_markers}

    for sent in sentences:
        sent_text = sent.text.lower()
        for relation, markers in relation_markers.items():
            for marker in markers:
                if marker in sent_text:
                    relation_counts[relation] += 1

    # Identify missing or underrepresented relations
    missing_relations = [rel for rel, count in relation_counts.items() if count == 0]

    # Create genre-specific recommendations
    if genre in ["Artigo Científico", "Tese/Dissertação", "Artigo de Pesquisa"]:
        # Academic/scientific writing
        academic_structure = """Para textos acadêmicos/científicos, considere a seguinte estrutura retórica:
- Introdução: contexto, problema, objetivos, justificativa
- Fundamentação teórica: revisão da literatura, definição de conceitos
- Metodologia: procedimentos, materiais, etapas
- Resultados: apresentação objetiva dos achados
- Discussão: interpretação, comparação com literatura, limitações
- Conclusão: síntese, implicações, pesquisas futuras"""

        description = f"""A estrutura retórica do texto pode ser aprimorada para maior eficácia no gênero acadêmico/científico.
        
{academic_structure}
        
Recomendações específicas:"""

        if "contrast" in missing_relations:
            description += "\n- Adicione marcadores de contraste (porém, entretanto) para comparar diferentes perspectivas teóricas"
        if "cause" in missing_relations:
            description += "\n- Incorpore mais relações de causa-efeito para explicar resultados e fenômenos"
        if "example" in missing_relations:
            description += (
                "\n- Inclua exemplos concretos para ilustrar conceitos abstratos"
            )
        if "conclusion" in missing_relations or relation_counts["conclusion"] < 2:
            description += (
                "\n- Fortaleça a conclusão com marcadores de síntese e implicações"
            )

    elif genre in ["Editorial", "Artigo de Opinião", "Ensaio"]:
        # Opinion/argumentative writing
        description = """A estrutura retórica do texto pode ser aprimorada para maior eficácia argumentativa.
        
Recomendações:
- Estabeleça uma tese clara no início do texto
- Desenvolva argumentos em ordem de complexidade ou força
- Incorpore contra-argumentos e refutações para fortalecer sua posição
- Utilize marcadores de contraste para comparar diferentes perspectivas
- Empregue relações de causa-efeito para explicar consequências
- Conclua retomando a tese com evidência acumulada"""

    else:
        # General recommendations
        description = """A estrutura retórica do texto pode ser aprimorada com melhor uso de relações discursivas.
        
Recomendações:
- Incorpore uma maior variedade de relações retóricas (contraste, causa, elaboração, exemplo)
- Utilize marcadores explícitos para sinalizar as relações entre partes do texto
- Estruture o texto com uma progressão lógica de ideias
- Equilibre a distribuição entre diferentes tipos de relações retóricas
- Certifique-se de que as relações mais importantes para seu objetivo comunicativo estejam bem representadas"""

    return {
        "id": "coherence_rhetorical_rec",
        "dimension": "coerencia",
        "metric": "retorica",
        "title": "Melhore a Estrutura Retórica",
        "description": description,
        "priority": "high" if metric_info["score"] < 60 else "medium",
        "potential_improvement": min(10, 80 - metric_info["score"]) / 2 + 5,
        "affected_segments": [],
    }


def recommend_genre_conformity(
    doc: spacy.tokens.Doc, metric_info: Dict[str, Any], domain: str, genre: str
) -> Dict[str, Any]:
    """Generate recommendation for improving genre conformity"""
    # Create genre-specific recommendations
    genre_templates = {
        "Artigo Científico": """Para aumentar a conformidade ao gênero Artigo Científico:
        
- Estruture o texto com as seções convencionais: Introdução, Métodos, Resultados, Discussão, Conclusão
- Utilize linguagem objetiva e impessoal (terceira pessoa, voz passiva)
- Inclua citações e referências em formato adequado
- Apresente claramente os objetivos e a questão de pesquisa na introdução
- Detalhe os procedimentos metodológicos para permitir replicabilidade
- Apresente resultados de forma neutra, sem interpretações
- Reserve interpretações e comparações com a literatura para a discussão
- Conclua com implicações e sugestões para pesquisas futuras""",
        "Tese/Dissertação": """Para aumentar a conformidade ao gênero Tese/Dissertação:
        
- Desenvolva uma estrutura completa com elementos pré-textuais, textuais e pós-textuais
- Inclua capítulos bem delimitados e interconectados
- Estabeleça claramente o problema de pesquisa, objetivos e justificativa
- Desenvolva um capítulo robusto de fundamentação teórica
- Detalhe minuciosamente os procedimentos metodológicos
- Apresente resultados com auxílio de tabelas e figuras quando apropriado
- Discuta os resultados em profundidade, relacionando-os com a literatura
- Conclua retomando objetivos e destacando contribuições originais""",
        "Resumo/Abstract": """Para aumentar a conformidade ao gênero Resumo/Abstract:
        
- Limite-se à extensão convencional (150-300 palavras)
- Inclua concisamente: contexto, objetivo, método, resultados, conclusão
- Utilize frases diretas e objetivas, evitando detalhes excessivos
- Elimine informações secundárias e exemplos
- Evite citações e referências
- Mantenha o tempo verbal consistente (geralmente presente para conclusões)
- Inclua palavras-chave relevantes
- Utilize a terceira pessoa e voz passiva (conforme convenção da área)""",
        "Notícia": """Para aumentar a conformidade ao gênero Notícia:
        
- Estruture o texto com pirâmide invertida (informações mais importantes primeiro)
- Inclua um lide que responda: o quê, quem, quando, onde, como, por quê
- Utilize parágrafos curtos e objetivos
- Separe claramente fatos de opiniões
- Inclua citações diretas de fontes relevantes
- Mantenha linguagem clara e acessível
- Utilize subtítulos para organizar informações extensas
- Conclua sem necessariamente apresentar uma conclusão formal""",
    }

    if genre in genre_templates:
        description = genre_templates[genre]
    else:
        # Generic recommendation
        description = f"""Para aumentar a conformidade ao gênero {genre}, verifique:
        
- A estrutura geral do texto está alinhada com as convenções do gênero?
- Os movimentos retóricos esperados estão presentes e desenvolvidos adequadamente?
- O registro linguístico é apropriado para o gênero e público-alvo?
- A extensão dos parágrafos e seções segue o padrão convencional?
- As marcas linguísticas típicas do gênero estão presentes?
- O formato e a organização visual atendem às expectativas do leitor?"""

    return {
        "id": "adequacy_genre_rec",
        "dimension": "adequacao",
        "metric": "conformidade",
        "title": f"Aumente a Conformidade ao Gênero {genre}",
        "description": description,
        "priority": "high" if metric_info["score"] < 60 else "medium",
        "potential_improvement": min(10, 80 - metric_info["score"]) / 2 + 6,
        "affected_segments": [],
    }


def recommend_register_adequacy(
    doc: spacy.tokens.Doc, metric_info: Dict[str, Any], domain: str, genre: str
) -> Dict[str, Any]:
    """Generate recommendation for improving register adequacy"""
    # Check formality markers
    formality_indicators = {
        "formal": [
            "would",
            "shall",
            "may",
            "might",
            "could",
            "therefore",
            "thus",
            "consequently",
            "moreover",
            "furthermore",
            "accordingly",
            "hence",
        ],
        "informal": [
            "well",
            "anyway",
            "actually",
            "basically",
            "really",
            "sort of",
            "kind of",
            "you know",
            "i mean",
            "like",
            "so",
            "pretty",
            "stuff",
            "things",
        ],
    }

    formal_count = 0
    informal_count = 0

    for token in doc:
        token_lower = token.text.lower()
        if token_lower in formality_indicators["formal"]:
            formal_count += 1
        if token_lower in formality_indicators["informal"]:
            informal_count += 1

    total_markers = formal_count + informal_count
    formality_ratio = formal_count / total_markers if total_markers > 0 else 0.5

    # Create domain and audience specific recommendations
    if domain in ["Acadêmico", "Científico", "Jurídico", "Médico"]:

        if formality_ratio < 0.6:
            description = """O registro linguístico do texto está menos formal do que o esperado para o domínio.
            
Recomendações para aumentar a formalidade:
- Evite contrações linguísticas (ex.: "não é" em vez de "num é")
- Substitua expressões coloquiais por equivalentes formais
- Utilize voz passiva e construções impessoais quando apropriado
- Evite gírias, clichês e expressões idiomáticas informais
- Mantenha um tom objetivo e distanciado
- Utilize vocabulário técnico e preciso
- Prefira estruturas sintáticas completas a frases fragmentadas"""
        else:
            description = """O registro linguístico pode ser ajustado para maior adequação ao domínio.
            
Recomendações:
- Verifique o uso consistente da terminologia especializada
- Mantenha o nível de formalidade consistente em todo o texto
- Assegure que os conceitos técnicos sejam apresentados com precisão
- Equilibre o uso de jargão técnico com clareza explicativa (dependendo do público)
- Utilize expressões e fraseologia típicas do gênero e domínio"""

    elif domain in ["Literário"]:
        if genre in ["Narrativa", "Crônica", "Poema"]:
            description = """Para adequar o registro ao texto literário:
            
Recomendações:
- Ajuste o registro de acordo com a voz narrativa e personagens
- Utilize recursos estilísticos apropriados ao subgênero (metáforas, aliterações, etc.)
- Crie um equilíbrio entre linguagem poética e clareza
- Adapte o vocabulário ao período histórico retratado (se aplicável)
- Varie o registro entre narração e diálogos para caracterização
- Permita licenças poéticas e criativas quando justificadas pelo efeito estético"""
        else:
            description = """Para adequar o registro ao texto literário:
            
Recomendações:
- Ajuste o nível de formalidade ao propósito comunicativo
- Equilibre expressividade estética e clareza comunicativa
- Utilize recursos literários sem comprometer a compreensão
- Adapte o vocabulário à proposta estética do texto
- Mantenha consistência estilística ao longo do texto"""

    else:
        # General recommendations
        description = """Para adequar o registro ao contexto comunicativo:
        
Recomendações:
- Ajuste o nível de formalidade ao público-alvo e propósito
- Mantenha consistência no tom e estilo ao longo do texto
- Adapte o vocabulário técnico ao nível de conhecimento do leitor
- Equilibre precisão terminológica e acessibilidade
- Evite misturar registros sem propósito comunicativo claro
- Considere as expectativas do gênero textual quanto ao registro"""

    return {
        "id": "adequacy_register_rec",
        "dimension": "adequacao",
        "metric": "registro",
        "title": "Adeque o Registro Linguístico",
        "description": description,
        "priority": "medium",
        "potential_improvement": min(10, 80 - metric_info["score"]) / 2 + 4,
        "affected_segments": [],
    }


def recommend_terminological_precision(
    doc: spacy.tokens.Doc, metric_info: Dict[str, Any], domain: str, genre: str
) -> Dict[str, Any]:
    """Generate recommendation for improving terminological precision"""
    # Identify potential terminology issues
    nouns = [
        token
        for token in doc
        if token.pos_ in ("NOUN", "PROPN") and len(token.text) > 3
    ]

    # Count unique lemmas and their text variations
    lemma_variations = {}
    for token in nouns:
        lemma = token.lemma_
        if lemma not in lemma_variations:
            lemma_variations[lemma] = set()
        lemma_variations[lemma].add(token.text.lower())

    # Find terms with inconsistent usage
    inconsistent_terms = []
    for lemma, variants in lemma_variations.items():
        if len(variants) > 1:
            variants_list = list(variants)
            if len(variants_list) > 1:
                inconsistent_terms.append({"lemma": lemma, "variants": variants_list})

    # Create recommendation
    if inconsistent_terms:
        examples = [
            f"'{term['lemma']}': {', '.join(term['variants'][:3])}"
            for term in inconsistent_terms[:3]
        ]
        examples_str = "\n".join([f"- {ex}" for ex in examples])

        description = f"""A precisão terminológica do texto pode ser aprimorada corrigindo inconsistências no uso de termos:
        
{examples_str}
        
Recomendações:
- Padronize o uso de cada termo, escolhendo uma única forma
- Mantenha consistência na grafia de termos técnicos e especializados
- Utilize a mesma forma para se referir a um conceito ao longo de todo o texto
- Considere criar um glossário de termos para manter consistência"""
    else:
        description = """A precisão terminológica do texto pode ser aprimorada:
        
Recomendações:
- Utilize termos técnicos específicos em vez de expressões genéricas
- Defina conceitos importantes na primeira ocorrência
- Evite ambiguidades terminológicas que possam gerar interpretações diversas
- Verifique a exatidão dos termos técnicos utilizados
- Considere o uso de vocabulário especializado adequado ao domínio
- Mantenha consistência no uso de siglas e abreviações"""

    return {
        "id": "precision_terminological_rec",
        "dimension": "precisao",
        "metric": "terminologica",
        "title": "Aprimore a Precisão Terminológica",
        "description": description,
        "priority": "high" if metric_info["score"] < 65 else "medium",
        "potential_improvement": min(10, 80 - metric_info["score"]) / 2 + 5,
        "affected_segments": [],
    }


def recommend_structural_clarity(
    doc: spacy.tokens.Doc, metric_info: Dict[str, Any], domain: str, genre: str
) -> Dict[str, Any]:
    """Generate recommendation for improving structural clarity"""
    sentences = list(doc.sents)

    # Identify long and complex sentences
    complex_sentences = []
    for i, sent in enumerate(sentences):
        # Count clauses (using verbs as proxy)
        verbs = [token for token in sent if token.pos_ == "VERB"]
        clause_count = len(verbs)

        # Count words
        words = [token for token in sent if not token.is_punct and not token.is_space]
        word_count = len(words)

        # Count nested structures
        nested_depth = 0
        for token in sent:
            if token.dep_ in ("ccomp", "xcomp", "advcl", "acl"):
                depth = 1
                parent = token.head
                while parent.i < len(doc) and parent.dep_ != "ROOT":
                    if parent.dep_ in ("ccomp", "xcomp", "advcl", "acl"):
                        depth += 1
                    parent = parent.head
                nested_depth = max(nested_depth, depth)

        # Identify potentially complex sentences
        if (clause_count > 3 and word_count > 25) or nested_depth > 2:
            complex_sentences.append(
                {
                    "index": i,
                    "text": sent.text,
                    "clauses": clause_count,
                    "words": word_count,
                    "nesting": nested_depth,
                }
            )

    # Create recommendation
    if complex_sentences:
        examples = [
            cs["text"][:100] + "..." if len(cs["text"]) > 100 else cs["text"]
            for cs in complex_sentences[:2]
        ]
        examples_str = "\n".join([f'- "{ex}"' for ex in examples])

        description = f"""A clareza estrutural do texto pode ser aprimorada simplificando estruturas sintáticas complexas.
        
Foram identificadas sentenças potencialmente complexas, como:
{examples_str}
        
Recomendações:
- Divida sentenças longas em unidades menores e mais gerenciáveis
- Reduza o nível de aninhamento de cláusulas subordinadas
- Aproxime sujeitos de seus verbos e verbos de seus complementos
- Evite intercalar muitas informações entre elementos relacionados
- Prefira a ordem direta (sujeito-verbo-objeto) quando possível
- Utilize pontuação adequada para separar elementos estruturais"""
    else:
        description = """A clareza estrutural do texto pode ser aprimorada:
        
Recomendações:
- Verifique se a estrutura sintática das sentenças facilita a compreensão
- Mantenha uma distância curta entre elementos relacionados (sujeito-verbo, verbo-objeto)
- Evite ambiguidades estruturais que permitam múltiplas interpretações
- Utilize paralelismo estrutural em enumerações e comparações
- Organize informações em uma sequência lógica dentro das sentenças
- Mantenha consistência nos padrões sintáticos utilizados"""

    return {
        "id": "precision_structural_rec",
        "dimension": "precisao",
        "metric": "estrutural",
        "title": "Melhore a Clareza Estrutural",
        "description": description,
        "priority": "high" if metric_info["score"] < 65 else "medium",
        "potential_improvement": min(10, 80 - metric_info["score"]) / 2 + 5,
        "affected_segments": [
            cs["index"] for cs in complex_sentences[:5]
        ],  # Limit to first 5
    }


def recommend_lexical_complexity(
    doc: spacy.tokens.Doc, metric_info: Dict[str, Any], domain: str, audience: str
) -> Dict[str, Any]:
    """Generate recommendation for improving lexical complexity"""
    # Determine if complexity is too high or too low for audience
    score = metric_info["score"]

    # Audience-based expected ranges
    audience_ranges = {
        "Especialista": (65, 85),
        "Acadêmico": (60, 80),
        "Profissional": (55, 75),
        "Estudante": (45, 65),
        "Público Geral": (40, 60),
    }

    expected_range = audience_ranges.get(audience, (50, 70))
    expected_mid = sum(expected_range) / 2

    if score < expected_range[0]:
        # Complexity too low
        description = f"""A complexidade lexical do texto parece estar abaixo do esperado para o público-alvo ({audience}).
        
Recomendações para aumentar a sofisticação lexical:
- Substitua termos genéricos por vocabulário mais específico e preciso
- Introduza terminologia especializada com explicações apropriadas
- Amplie a variação lexical, evitando repetições desnecessárias
- Utilize sinônimos mais sofisticados quando apropriado
- Considere incorporar termos técnicos relevantes ao domínio
- Aumente a densidade informacional com nominalizações quando apropriado"""

    elif score > expected_range[1]:
        # Complexity too high
        description = f"""A complexidade lexical do texto parece estar acima do adequado para o público-alvo ({audience}).
        
Recomendações para ajustar a sofisticação lexical:
- Substitua termos altamente especializados por equivalentes mais acessíveis
- Defina ou explique terminologia técnica essencial
- Reduza o uso de palavras raras ou eruditas quando existirem alternativas claras
- Evite jargão desnecessário que possa alienar o leitor
- Considere o nível de familiaridade do público com o vocabulário do domínio
- Use analogias e exemplos para facilitar a compreensão de conceitos complexos"""

    else:
        # Within expected range, but can be optimized
        if score < expected_mid:
            description = f"""A complexidade lexical do texto está adequada, mas poderia ser ligeiramente aumentada para o público-alvo ({audience}).
            
Recomendações para otimização:
- Identifique oportunidades pontuais para introduzir vocabulário mais preciso
- Aumente a variedade lexical em seções-chave do texto
- Incorpore terminologia especializada em pontos estratégicos
- Mantenha um equilíbrio entre precisão terminológica e acessibilidade"""
        else:
            description = f"""A complexidade lexical do texto está adequada, mas poderia ser ajustada para melhor equilíbrio para o público-alvo ({audience}).
            
Recomendações para otimização:
- Verifique se há termos técnicos que poderiam beneficiar-se de explicações breves
- Mantenha consistência no nível lexical ao longo do texto
- Certifique-se de que a terminologia especializada está sendo usada com precisão
- Avalie se há seções onde a simplificação lexical poderia melhorar a clareza"""

    return {
        "id": "complexity_lexical_rec",
        "dimension": "complexidade",
        "metric": "lexical",
        "title": "Ajuste a Complexidade Lexical",
        "description": description,
        "priority": "medium",
        "potential_improvement": abs(score - expected_mid) / 5 + 3,
        "affected_segments": [],
    }


def recommend_syntactic_complexity(
    doc: spacy.tokens.Doc, metric_info: Dict[str, Any], domain: str, genre: str
) -> Dict[str, Any]:
    """Generate recommendation for improving syntactic complexity"""
    score = metric_info["score"]

    # Determine if adjustment is needed based on genre
    academic_genres = [
        "Artigo Científico",
        "Tese/Dissertação",
        "Artigo de Pesquisa",
        "Resenha Acadêmica",
    ]
    journalistic_genres = ["Notícia", "Reportagem"]
    literary_genres = ["Narrativa", "Poema", "Ensaio", "Crônica"]

    if genre in academic_genres:
        # Academic writing typically expects moderate to high complexity
        expected_range = (65, 85)
    elif genre in journalistic_genres:
        # News writing typically expects lower complexity
        expected_range = (45, 65)
    elif genre in literary_genres:
        # Literary writing has variable complexity
        expected_range = (50, 80)
    else:
        # Default range
        expected_range = (55, 75)

    expected_mid = sum(expected_range) / 2

    if score < expected_range[0]:
        # Complexity too low
        description = f"""A complexidade sintática do texto parece estar abaixo do esperado para o gênero ({genre}).
        
Recomendações para aumentar a complexidade sintática:
- Combine sentenças simples utilizando conjunções coordenativas e subordinativas
- Incorpore estruturas como orações relativas para adicionar informações sem iniciar novas sentenças
- Utilize construções participiais e gerundivas para expressar relações temporais e causais
- Adicione modificadores e qualificadores para aumentar a precisão e detalhe
- Empregue inversões sintáticas estratégicas para ênfase
- Varie a estrutura e o comprimento das sentenças para criar ritmo"""

    elif score > expected_range[1]:
        # Complexity too high
        description = f"""A complexidade sintática do texto parece estar acima do adequado para o gênero ({genre}).
        
Recomendações para reduzir a complexidade sintática:
- Divida sentenças longas em unidades menores e independentes
- Reduza o número de orações subordinadas por sentença
- Aproxime sujeitos de seus verbos e verbos de seus objetos
- Elimine estruturas aninhadas que criam múltiplos níveis de subordinação
- Prefira a ordem direta (sujeito-verbo-objeto) em sentenças-chave
- Utilize sentenças simples para informações cruciais e conceitos-chave"""

    else:
        # Within expected range, but can be optimized
        if abs(score - expected_mid) < 5:
            description = f"""A complexidade sintática do texto está bem adequada ao gênero ({genre}).
            
Recomendações para refinamento:
- Mantenha o equilíbrio atual entre sentenças simples e complexas
- Varie a estrutura sintática para evitar monotonia
- Reserve construções mais complexas para relações lógicas sofisticadas
- Utilize sentenças mais simples para informações cruciais
- Verifique se a complexidade está distribuída adequadamente ao longo do texto"""
        else:
            description = f"""A complexidade sintática do texto está adequada, mas poderia ser ajustada para melhor equilíbrio no gênero ({genre}).
            
Recomendações para otimização:
- Identifique seções onde a complexidade pode ser ajustada para melhor efeito
- Varie o padrão sintático para criar ritmo e ênfase
- Verifique se todas as estruturas complexas são justificadas pelo conteúdo
- Ajuste a complexidade de acordo com a importância relativa das informações"""

    return {
        "id": "complexity_syntactic_rec",
        "dimension": "complexidade",
        "metric": "sintatica",
        "title": "Ajuste a Complexidade Sintática",
        "description": description,
        "priority": "medium",
        "potential_improvement": abs(score - expected_mid) / 5 + 3,
        "affected_segments": [],
    }


def recommend_informational_density(
    doc: spacy.tokens.Doc, metric_info: Dict[str, Any], domain: str, genre: str
) -> Dict[str, Any]:
    """Generate recommendation for improving informational density"""
    score = metric_info["score"]

    # Determine if adjustment is needed based on domain and genre
    academic_domains = ["Acadêmico", "Científico"]
    technical_domains = ["Técnico", "Jurídico", "Médico"]

    if domain in academic_domains:
        # Academic writing typically expects higher density
        expected_range = (65, 85)
    elif domain in technical_domains:
        # Technical writing typically expects moderate to high density
        expected_range = (60, 80)
    else:
        # Default range
        expected_range = (50, 70)

    expected_mid = sum(expected_range) / 2

    if score < expected_range[0]:
        # Density too low
        description = f"""A densidade informacional do texto parece estar abaixo do esperado para o domínio ({domain}).
        
Recomendações para aumentar a densidade informacional:
- Elimine redundâncias e repetições desnecessárias
- Substitua expressões verbosas por formulações mais concisas
- Utilize nominalizações para compactar informações
- Incorpore mais conceitos técnicos e especializados
- Aumente a especificidade dos substantivos e a precisão dos modificadores
- Elimine palavras vazias e expressões de preenchimento
- Condense explicações básicas quando o público já possui o conhecimento necessário"""

    elif score > expected_range[1]:
        # Density too high
        description = f"""A densidade informacional do texto parece estar acima do adequado para o domínio ({domain}).
        
Recomendações para ajustar a densidade informacional:
- Adicione explicações para conceitos complexos ou técnicos
- Desenvolva ideias importantes com exemplos e elaborações
- Divida sentenças de alta densidade em unidades mais gerenciáveis
- Introduza transições entre ideias densas
- Utilize paráfrases explanatórias para conceitos-chave
- Considere o uso de recursos visuais para complementar informações complexas
- Equilibre seções densas com passagens de menor complexidade"""

    else:
        # Within expected range, but can be optimized
        if abs(score - expected_mid) < 5:
            description = f"""A densidade informacional do texto está bem adequada ao domínio ({domain}).
            
Recomendações para refinamento:
- Mantenha o equilíbrio atual entre concisão e desenvolvimento adequado
- Verifique a distribuição da densidade ao longo do texto
- Reserve maior densidade para conceitos e informações principais
- Garanta que a densidade não comprometa a clareza comunicativa"""
        else:
            description = f"""A densidade informacional do texto está adequada, mas poderia ser ajustada para melhor equilíbrio no domínio ({domain}).
            
Recomendações para otimização:
- Identifique seções específicas onde a densidade poderia ser ajustada
- Varie a densidade de acordo com a importância relativa das informações
- Equilibre passagens de alta densidade com transições e elaborações
- Adapte a densidade às expectativas específicas do gênero dentro do domínio"""

    return {
        "id": "complexity_informational_rec",
        "dimension": "complexidade",
        "metric": "informacional",
        "title": "Ajuste a Densidade Informacional",
        "description": description,
        "priority": "medium",
        "potential_improvement": abs(score - expected_mid) / 5 + 3,
        "affected_segments": [],
    }
