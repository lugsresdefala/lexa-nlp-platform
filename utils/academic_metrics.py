"""
LEXA Academic Metrics Implementation
Based on validated academic linguistic metrics and frameworks
"""

import re
import math
import numpy as np
from collections import Counter, defaultdict
from typing import Dict, List, Tuple, Any
import spacy
from scipy.spatial.distance import cosine
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from config.env_config import ProductionNLPConfig

class AcademicMetricsCalculator:
    """
    Implements the 8 core dimensions of LEXA academic text evaluation
    with validated academic metrics and 0.05-0.95 scoring scale
    """
    
    def __init__(self, config: ProductionNLPConfig | None = None):
        self.config = config or ProductionNLPConfig()
        self.nlp = None
        self._load_linguistic_resources()
        
    def _load_linguistic_resources(self):
        """Load Portuguese linguistic model and academic word lists"""
        try:
            self.nlp = spacy.load(self.config.spacy_model)
        except OSError:
            # Fallback to basic processing if model not available
            self.nlp = None
            
        # Academic vocabulary lists (AWL adapted for Portuguese)
        self.academic_vocab = {
            'analysis', 'approach', 'area', 'assessment', 'assume', 'authority', 'available',
            'benefit', 'concept', 'consistent', 'constitutional', 'context', 'contract', 'create',
            'data', 'definition', 'derived', 'distribution', 'economic', 'environment', 'established',
            'estimate', 'evidence', 'export', 'factors', 'financial', 'formula', 'function',
            'identified', 'income', 'indicate', 'individual', 'interpretation', 'involved', 'issues',
            'labour', 'legal', 'legislation', 'major', 'method', 'occur', 'percent', 'period',
            'policy', 'principle', 'procedure', 'process', 'required', 'research', 'response',
            'role', 'section', 'sector', 'significant', 'similar', 'source', 'specific', 'structure',
            'theory', 'variables'
        }
        
        # Discourse connectors for Portuguese
        self.discourse_connectors = {
            'causal': ['porque', 'pois', 'uma vez que', 'visto que', 'dado que', 'já que'],
            'adversative': ['mas', 'porém', 'contudo', 'entretanto', 'todavia', 'no entanto'],
            'additive': ['além disso', 'ademais', 'também', 'igualmente', 'outrossim'],
            'temporal': ['então', 'logo', 'depois', 'posteriormente', 'anteriormente', 'simultaneamente'],
            'conclusive': ['portanto', 'assim', 'logo', 'por conseguinte', 'em suma', 'enfim']
        }
        
        # Metadiscourse markers
        self.metadiscourse_markers = {
            'textual': ['primeiramente', 'em segundo lugar', 'finalmente', 'por um lado', 'por outro lado'],
            'interpersonal': ['obviamente', 'certamente', 'provavelmente', 'possivelmente', 'aparentemente'],
            'epistemic': ['acredita-se', 'considera-se', 'supõe-se', 'pode-se afirmar', 'é possível que']
        }

    def calculate_all_dimensions(self, text: str, domain: str = "academic", 
                               level: str = "graduacao") -> Dict[str, Any]:
        """
        Calculate all 8 LEXA dimensions with normalized 0.05-0.95 scores
        """
        if not text.strip():
            return self._empty_results()
            
        # Process text with spaCy if available
        doc = self.nlp(text) if self.nlp else None
        
        results = {
            'macroestrutura_argumentativa': self._calculate_macrostructure(text, doc),
            'coesao_coerencia': self._calculate_cohesion_coherence(text, doc),
            'sofisticacao_lexico_gramatical': self._calculate_lexical_sophistication(text, doc),
            'complexidade_sintatica': self._calculate_syntactic_complexity(text, doc),
            'metadiscursividade': self._calculate_metadiscourse(text, doc),
            'intertextualidade': self._calculate_intertextuality(text, doc),
            'rigor_metodologico': self._calculate_methodological_rigor(text, doc),
            'estilo_adequacao': self._calculate_style_adequacy(text, doc, domain, level)
        }
        
        # Calculate overall score
        scores = [dim['score'] for dim in results.values()]
        results['overall_score'] = {
            'score': np.mean(scores),
            'performance_level': self._get_performance_level(np.mean(scores)),
            'summary': f"Desempenho geral: {self._get_performance_level(np.mean(scores))}"
        }
        
        return results

    def _normalize_score(self, raw_score: float, min_val: float = 0, max_val: float = 1) -> float:
        """Normalize score to LEXA 0.05-0.95 scale"""
        if max_val == min_val:
            return 0.50  # Default to intermediate
        normalized = (raw_score - min_val) / (max_val - min_val)
        return max(0.05, min(0.95, 0.05 + (normalized * 0.90)))

    def _get_performance_level(self, score: float) -> str:
        """Convert score to performance level"""
        if score < 0.25:
            return "muito insatisfatório"
        elif score < 0.45:
            return "insatisfatório"
        elif score < 0.65:
            return "intermediário"
        elif score < 0.85:
            return "satisfatório"
        else:
            return "excelência textual"

    def _calculate_macrostructure(self, text: str, doc) -> Dict[str, Any]:
        """
        Dimension 1: Argumentative Macrostructure
        Evaluates logical organization and argumentative sequence
        """
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        # Detect structural elements
        has_introduction = self._detect_introduction(paragraphs)
        has_development = len(paragraphs) >= 3
        has_conclusion = self._detect_conclusion(paragraphs)
        
        # Argumentative sequence detection
        argumentative_markers = self._count_argumentative_markers(text)
        
        # Thematic progression
        thematic_consistency = self._calculate_thematic_progression(paragraphs)
        
        # Calculate raw score
        structure_score = (has_introduction + has_development + has_conclusion) / 3
        argument_score = min(1.0, argumentative_markers / 10)  # Normalize to max 10 markers
        
        raw_score = (structure_score * 0.4 + argument_score * 0.3 + thematic_consistency * 0.3)
        
        return {
            'score': self._normalize_score(raw_score),
            'details': {
                'tem_introducao': has_introduction,
                'tem_desenvolvimento': has_development,
                'tem_conclusao': has_conclusion,
                'marcadores_argumentativos': argumentative_markers,
                'progressao_tematica': thematic_consistency
            },
            'problems': self._identify_macrostructure_problems(
                has_introduction, has_development, has_conclusion, argumentative_markers
            ),
            'recommendations': self._get_macrostructure_recommendations(
                has_introduction, has_development, has_conclusion
            )
        }

    def _calculate_cohesion_coherence(self, text: str, doc) -> Dict[str, Any]:
        """
        Dimension 2: Cohesion and Coherence
        Based on Coh-Metrix principles and LSA similarity
        """
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Referential cohesion
        referential_cohesion = self._calculate_referential_cohesion(text, doc)
        
        # Sequential cohesion (connectives)
        connector_density = self._calculate_connector_density(text)
        
        # Lexical cohesion
        lexical_cohesion = self._calculate_lexical_cohesion(sentences)
        
        # Semantic coherence (sentence similarity)
        semantic_coherence = self._calculate_semantic_coherence(sentences)
        
        raw_score = (referential_cohesion * 0.25 + connector_density * 0.25 + 
                     lexical_cohesion * 0.25 + semantic_coherence * 0.25)
        
        return {
            'score': self._normalize_score(raw_score),
            'details': {
                'coesao_referencial': referential_cohesion,
                'densidade_conectores': connector_density,
                'coesao_lexical': lexical_cohesion,
                'coerencia_semantica': semantic_coherence
            },
            'problems': self._identify_cohesion_problems(connector_density, lexical_cohesion),
            'recommendations': self._get_cohesion_recommendations(connector_density, semantic_coherence)
        }

    def _calculate_lexical_sophistication(self, text: str, doc) -> Dict[str, Any]:
        """
        Dimension 3: Lexical-Grammatical Sophistication
        Implements TTR, MTLD, and academic vocabulary metrics
        """
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Type-Token Ratio (TTR)
        ttr = len(set(words)) / len(words) if words else 0
        
        # MTLD approximation
        mtld = self._calculate_mtld(words)
        
        # Academic vocabulary usage
        academic_ratio = sum(1 for word in words if word in self.academic_vocab) / len(words)
        
        # Lexical diversity
        word_freq = Counter(words)
        hapax_legomena = sum(1 for freq in word_freq.values() if freq == 1)
        hapax_ratio = hapax_legomena / len(set(words)) if words else 0
        
        # Combine metrics
        raw_score = (ttr * 0.3 + mtld * 0.3 + academic_ratio * 0.2 + hapax_ratio * 0.2)
        
        return {
            'score': self._normalize_score(raw_score),
            'details': {
                'ttr': ttr,
                'mtld': mtld,
                'vocabulario_academico': academic_ratio,
                'hapax_ratio': hapax_ratio,
                'palavras_unicas': len(set(words)),
                'total_palavras': len(words)
            },
            'problems': self._identify_lexical_problems(ttr, academic_ratio),
            'recommendations': self._get_lexical_recommendations(ttr, academic_ratio, mtld)
        }

    def _calculate_syntactic_complexity(self, text: str, doc) -> Dict[str, Any]:
        """
        Dimension 4: Syntactic Complexity
        Implements D-Level scale and syntactic depth metrics
        """
        if not doc:
            # Fallback analysis without spaCy
            return self._basic_syntactic_analysis(text)
            
        sentences = list(doc.sents)
        
        # Average sentence length
        avg_sentence_length = np.mean([len(sent) for sent in sentences])
        
        # Subordinate clauses detection
        subordinate_clauses = sum(1 for token in doc if token.dep_ in ['mark', 'advcl', 'acl'])
        subordination_ratio = subordinate_clauses / len(sentences) if sentences else 0
        
        # Complex structures (passive voice, relative clauses)
        passive_constructions = self._count_passive_voice(doc)
        relative_clauses = sum(1 for token in doc if token.dep_ == 'relcl')
        
        # Syntactic depth approximation
        max_depth = max((self._get_syntactic_depth(sent.root) for sent in sentences), default=0)
        avg_depth = np.mean([self._get_syntactic_depth(sent.root) for sent in sentences])
        
        raw_score = (
            min(1.0, avg_sentence_length / 25) * 0.3 +  # Normalize to ~25 words
            min(1.0, subordination_ratio / 2) * 0.3 +    # Normalize to ~2 per sentence
            min(1.0, (passive_constructions + relative_clauses) / 10) * 0.2 +
            min(1.0, avg_depth / 6) * 0.2                # Normalize to depth 6
        )
        
        return {
            'score': self._normalize_score(raw_score),
            'details': {
                'comprimento_medio_sentenca': avg_sentence_length,
                'clausulas_subordinadas': subordination_ratio,
                'construcoes_passivas': passive_constructions,
                'clausulas_relativas': relative_clauses,
                'profundidade_maxima': max_depth,
                'profundidade_media': avg_depth
            },
            'problems': self._identify_syntactic_problems(avg_sentence_length, subordination_ratio),
            'recommendations': self._get_syntactic_recommendations(avg_sentence_length, subordination_ratio)
        }

    def _calculate_metadiscourse(self, text: str, doc) -> Dict[str, Any]:
        """
        Dimension 5: Metadiscursivity
        Based on Hyland's metadiscourse framework
        """
        text_lower = text.lower()
        
        # Count metadiscourse markers
        textual_markers = sum(1 for marker in self.metadiscourse_markers['textual'] 
                             if marker in text_lower)
        interpersonal_markers = sum(1 for marker in self.metadiscourse_markers['interpersonal'] 
                                   if marker in text_lower)
        epistemic_markers = sum(1 for marker in self.metadiscourse_markers['epistemic'] 
                               if marker in text_lower)
        
        # Calculate density (per 1000 words)
        word_count = len(re.findall(r'\b\w+\b', text))
        textual_density = (textual_markers / word_count) * 1000 if word_count else 0
        interpersonal_density = (interpersonal_markers / word_count) * 1000 if word_count else 0
        epistemic_density = (epistemic_markers / word_count) * 1000 if word_count else 0
        
        # Overall metadiscourse score
        total_density = textual_density + interpersonal_density + epistemic_density
        raw_score = min(1.0, total_density / 30)  # Normalize to ~30 markers per 1000 words
        
        return {
            'score': self._normalize_score(raw_score),
            'details': {
                'marcadores_textuais': textual_markers,
                'marcadores_interpessoais': interpersonal_markers,
                'marcadores_epistemicos': epistemic_markers,
                'densidade_textual': textual_density,
                'densidade_interpessoal': interpersonal_density,
                'densidade_epistemica': epistemic_density,
                'densidade_total': total_density
            },
            'problems': self._identify_metadiscourse_problems(total_density),
            'recommendations': self._get_metadiscourse_recommendations(textual_density, interpersonal_density)
        }

    def _calculate_intertextuality(self, text: str, doc) -> Dict[str, Any]:
        """
        Dimension 6: Intertextuality
        Detects citations, references, and reported speech
        """
        # Citation patterns (Brazilian academic style)
        citation_patterns = [
            r'\([A-Z][a-z]+,?\s+\d{4}\)',  # (Author, 2020)
            r'[A-Z][a-z]+\s+\(\d{4}\)',    # Author (2020)
            r'apud\s+[A-Z][a-z]+',         # apud Author
            r'cf\.\s+[A-Z][a-z]+',         # cf. Author
            r'segundo\s+[A-Z][a-z]+',      # segundo Author
            r'conforme\s+[A-Z][a-z]+',     # conforme Author
        ]
        
        citation_count = sum(len(re.findall(pattern, text)) for pattern in citation_patterns)
        
        # Reported speech markers
        reported_speech_markers = [
            'afirma que', 'declara que', 'sustenta que', 'argumenta que',
            'defende que', 'propõe que', 'considera que', 'aponta que'
        ]
        reported_speech = sum(1 for marker in reported_speech_markers if marker in text.lower())
        
        # Reference integration quality
        integration_quality = self._assess_citation_integration(text)
        
        # Bibliography dialogue
        bibliography_dialogue = self._assess_bibliography_dialogue(text)
        
        word_count = len(re.findall(r'\b\w+\b', text))
        citation_density = (citation_count / word_count) * 1000 if word_count else 0
        
        raw_score = (
            min(1.0, citation_density / 20) * 0.4 +      # Normalize to ~20 citations per 1000 words
            min(1.0, reported_speech / 10) * 0.3 +       # Normalize to ~10 markers
            integration_quality * 0.2 +
            bibliography_dialogue * 0.1
        )
        
        return {
            'score': self._normalize_score(raw_score),
            'details': {
                'citacoes_detectadas': citation_count,
                'discurso_reportado': reported_speech,
                'densidade_citacoes': citation_density,
                'qualidade_integracao': integration_quality,
                'dialogo_bibliografico': bibliography_dialogue
            },
            'problems': self._identify_intertextuality_problems(citation_density, integration_quality),
            'recommendations': self._get_intertextuality_recommendations(citation_density, reported_speech)
        }

    def _calculate_methodological_rigor(self, text: str, doc) -> Dict[str, Any]:
        """
        Dimension 7: Methodological Rigor
        Assesses clarity and completeness of methodological exposition
        """
        text_lower = text.lower()
        
        # Methodological keywords
        objective_keywords = ['objetivo', 'objetivos', 'meta', 'finalidade', 'propósito']
        hypothesis_keywords = ['hipótese', 'hipóteses', 'suposição', 'pressuposto']
        method_keywords = ['método', 'metodologia', 'procedimento', 'técnica', 'abordagem']
        sample_keywords = ['amostra', 'corpus', 'população', 'participantes', 'sujeitos']
        analysis_keywords = ['análise', 'exame', 'investigação', 'estudo', 'avaliação']
        
        # Count presence of methodological elements
        has_objectives = any(keyword in text_lower for keyword in objective_keywords)
        has_hypothesis = any(keyword in text_lower for keyword in hypothesis_keywords)
        has_method = any(keyword in text_lower for keyword in method_keywords)
        has_sample = any(keyword in text_lower for keyword in sample_keywords)
        has_analysis = any(keyword in text_lower for keyword in analysis_keywords)
        
        # Methodological language precision
        precision_score = self._assess_methodological_language(text)
        
        # Procedural clarity
        procedural_clarity = self._assess_procedural_clarity(text)
        
        # Calculate components
        component_score = (has_objectives + has_hypothesis + has_method + 
                          has_sample + has_analysis) / 5
        
        raw_score = component_score * 0.5 + precision_score * 0.3 + procedural_clarity * 0.2
        
        return {
            'score': self._normalize_score(raw_score),
            'details': {
                'tem_objetivos': has_objectives,
                'tem_hipoteses': has_hypothesis,
                'tem_metodologia': has_method,
                'tem_amostra': has_sample,
                'tem_analise': has_analysis,
                'precisao_linguistica': precision_score,
                'clareza_procedimental': procedural_clarity
            },
            'problems': self._identify_methodological_problems(component_score, precision_score),
            'recommendations': self._get_methodological_recommendations(
                has_objectives, has_method, precision_score
            )
        }

    def _calculate_style_adequacy(self, text: str, doc, domain: str, level: str) -> Dict[str, Any]:
        """
        Dimension 8: Style and Adequacy
        Evaluates conformity with academic genre and linguistic norms
        """
        # Impersonality assessment
        impersonality = self._assess_impersonality(text, doc)
        
        # Formality level
        formality = self._assess_formality(text)
        
        # Objectivity
        objectivity = self._assess_objectivity(text)
        
        # Register adequacy
        register_adequacy = self._assess_register_adequacy(text, domain)
        
        # Ambiguity detection
        ambiguity_score = 1.0 - self._detect_ambiguity(text)
        
        # Redundancy detection
        redundancy_score = 1.0 - self._detect_redundancy(text)
        
        raw_score = (
            impersonality * 0.2 + formality * 0.2 + objectivity * 0.2 +
            register_adequacy * 0.15 + ambiguity_score * 0.125 + redundancy_score * 0.125
        )
        
        return {
            'score': self._normalize_score(raw_score),
            'details': {
                'impessoalidade': impersonality,
                'formalidade': formality,
                'objetividade': objectivity,
                'adequacao_registro': register_adequacy,
                'ausencia_ambiguidade': ambiguity_score,
                'ausencia_redundancia': redundancy_score
            },
            'problems': self._identify_style_problems(impersonality, formality, ambiguity_score),
            'recommendations': self._get_style_recommendations(impersonality, formality, objectivity)
        }

    # Helper methods for detailed calculations
    def _detect_introduction(self, paragraphs: List[str]) -> bool:
        """Detect if text has an introduction"""
        if not paragraphs:
            return False
        first_para = paragraphs[0].lower()
        intro_markers = ['este trabalho', 'este artigo', 'este estudo', 'esta pesquisa', 
                        'o objetivo', 'pretende-se', 'busca-se', 'visa-se']
        return any(marker in first_para for marker in intro_markers)

    def _detect_conclusion(self, paragraphs: List[str]) -> bool:
        """Detect if text has a conclusion"""
        if not paragraphs:
            return False
        last_para = paragraphs[-1].lower()
        conclusion_markers = ['conclui-se', 'em conclusão', 'portanto', 'assim', 
                             'em suma', 'finalmente', 'por fim']
        return any(marker in last_para for marker in conclusion_markers)

    def _count_argumentative_markers(self, text: str) -> int:
        """Count argumentative discourse markers"""
        text_lower = text.lower()
        markers = ['por outro lado', 'em contrapartida', 'no entanto', 'contudo', 
                  'além disso', 'ademais', 'por conseguinte', 'dessa forma']
        return sum(1 for marker in markers if marker in text_lower)

    def _calculate_thematic_progression(self, paragraphs: List[str]) -> float:
        """Assess thematic consistency across paragraphs"""
        if len(paragraphs) < 2:
            return 0.5
        
        # Simple keyword overlap between consecutive paragraphs
        similarities = []
        for i in range(len(paragraphs) - 1):
            words1 = set(re.findall(r'\b\w+\b', paragraphs[i].lower()))
            words2 = set(re.findall(r'\b\w+\b', paragraphs[i + 1].lower()))
            if words1 and words2:
                similarity = len(words1 & words2) / len(words1 | words2)
                similarities.append(similarity)
        
        return np.mean(similarities) if similarities else 0.5

    def _calculate_mtld(self, words: List[str]) -> float:
        """Calculate MTLD (Measure of Textual Lexical Diversity)"""
        if len(words) < 50:
            return len(set(words)) / len(words) if words else 0
        
        # Simplified MTLD calculation
        ttr_threshold = 0.72
        segments = []
        current_segment = []
        
        for word in words:
            current_segment.append(word)
            current_ttr = len(set(current_segment)) / len(current_segment)
            if current_ttr <= ttr_threshold:
                segments.append(len(current_segment))
                current_segment = []
        
        return np.mean(segments) if segments else len(words)

    def _calculate_referential_cohesion(self, text: str, doc) -> float:
        """Calculate referential cohesion (pronouns, determiners)"""
        if not doc:
            # Fallback: count pronouns and determiners manually
            pronouns = re.findall(r'\b(ele|ela|isso|isto|aquilo|seu|sua|dele|dela)\b', text.lower())
            words = re.findall(r'\b\w+\b', text)
            return len(pronouns) / len(words) if words else 0
        
        # Use spaCy POS tags
        pronouns = sum(1 for token in doc if token.pos_ in ['PRON', 'DET'])
        return pronouns / len(doc) if doc else 0

    def _calculate_connector_density(self, text: str) -> float:
        """Calculate density of discourse connectors"""
        text_lower = text.lower()
        all_connectors = []
        for connector_list in self.discourse_connectors.values():
            all_connectors.extend(connector_list)
        
        connector_count = sum(1 for connector in all_connectors if connector in text_lower)
        words = re.findall(r'\b\w+\b', text)
        return (connector_count / len(words)) * 100 if words else 0  # Per 100 words

    def _empty_results(self) -> Dict[str, Any]:
        """Return empty results structure"""
        empty_dim = {
            'score': 0.05,
            'details': {},
            'problems': ['Texto vazio ou muito curto'],
            'recommendations': ['Insira um texto com pelo menos 100 palavras']
        }
        
        return {
            'macroestrutura_argumentativa': empty_dim.copy(),
            'coesao_coerencia': empty_dim.copy(),
            'sofisticacao_lexico_gramatical': empty_dim.copy(),
            'complexidade_sintatica': empty_dim.copy(),
            'metadiscursividade': empty_dim.copy(),
            'intertextualidade': empty_dim.copy(),
            'rigor_metodologico': empty_dim.copy(),
            'estilo_adequacao': empty_dim.copy(),
            'overall_score': {
                'score': 0.05,
                'performance_level': 'muito insatisfatório',
                'summary': 'Texto insuficiente para análise'
            }
        }

    # Additional helper methods would continue here...
    # (Implementation of remaining helper methods for brevity)