import spacy
import numpy as np
import streamlit as st
from typing import Dict, List, Any

# Import NLP model configuration
from config import NLP_MODELS
from config.env_config import ProductionNLPConfig

# Load environment configuration once
_env_config = ProductionNLPConfig()


def ensure_nltk_data() -> None:
    """Ensure required NLTK resources are available."""
    import nltk

    resources = [
        ("tokenizers/punkt", "punkt"),
        ("corpus/stopwords", "stopwords"),
    ]

    for path, name in resources:
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(name, quiet=True)


# Initialize and cache NLP models
_nlp_models = {}


def get_nlp_model(language: str) -> spacy.language.Language:
    """
    Get or load the appropriate spaCy model for the specified language.

    Args:
        language (str): Language code (e.g., 'pt', 'en')

    Returns:
        spacy.language.Language: Loaded spaCy model
    """
    if language not in _nlp_models:
        if language == "pt":
            model_name = _env_config.spacy_model
        else:
            model_name = NLP_MODELS.get(language, NLP_MODELS["en"])
        try:
            _nlp_models[language] = spacy.load(model_name)
        except OSError:
            # If model not found, use a small model instead of downloading
            # (downloading large models can time out in this environment)
            if language == "pt":
                # Use small Portuguese model
                _nlp_models[language] = spacy.blank("pt")
                # Add sentencizer to the pipeline
                _nlp_models[language].add_pipe("sentencizer")
                st.warning(
                    "Modelo linguístico completo não encontrado. Usando modelo simplificado."
                )
            else:
                # Use small English model
                _nlp_models[language] = spacy.blank("en")
                # Add sentencizer to the pipeline
                _nlp_models[language].add_pipe("sentencizer")
                st.warning("Complete language model not found. Using simplified model.")

    return _nlp_models[language]


def process_text(text: str, language: str = "pt") -> spacy.tokens.Doc:
    """
    Process the input text using spaCy's NLP pipeline.

    Args:
        text (str): Input text for analysis
        language (str): Language code

    Returns:
        spacy.tokens.Doc: Processed document
    """
    # Get the appropriate NLP model
    nlp = get_nlp_model(language)

    # Process the text
    doc = nlp(text)

    return doc


def segment_text(doc: spacy.tokens.Doc) -> List[Dict[str, Any]]:
    """
    Segment the text into logical units (sentences, paragraphs).

    Args:
        doc (spacy.tokens.Doc): Processed spaCy document

    Returns:
        List[Dict[str, Any]]: List of text segments with metadata
    """
    # Split text into paragraphs
    paragraphs = [p for p in doc.text.split("\n") if p.strip()]

    segments = []
    sent_idx = 0

    for p_idx, paragraph in enumerate(paragraphs):
        # Process paragraph sentences
        sentences = [s for s in doc.sents if s.text in paragraph]

        if not sentences:
            continue

        for sentence in sentences:
            segments.append(
                {
                    "id": f"s{sent_idx}",
                    "paragraph_id": f"p{p_idx}",
                    "text": sentence.text,
                    "start_char": sentence.start_char,
                    "end_char": sentence.end_char,
                    "tokens": [token.text for token in sentence],
                    "pos_tags": [token.pos_ for token in sentence],
                    "dependencies": [
                        (token.text, token.dep_, token.head.text) for token in sentence
                    ],
                    "entities": [(ent.text, ent.label_) for ent in sentence.ents],
                }
            )
            sent_idx += 1

    return segments


def extract_linguistic_features(doc: spacy.tokens.Doc) -> Dict[str, Any]:
    """
    Extract linguistic features from the processed document.

    Args:
        doc (spacy.tokens.Doc): Processed spaCy document

    Returns:
        Dict[str, Any]: Dictionary containing linguistic features
    """
    # Tokenization statistics
    tokens = [token for token in doc if not token.is_punct and not token.is_space]
    content_tokens = [token for token in tokens if not token.is_stop]

    # Lexical features
    unique_lemmas = set(token.lemma_ for token in content_tokens)

    # Syntactic features
    sentences = list(doc.sents)
    sentence_lengths = [
        len([token for token in sent if not token.is_punct]) for sent in sentences
    ]

    # Dependency features
    dep_distances = []
    for token in doc:
        if token.head != token:  # Exclude root
            distance = abs(token.i - token.head.i)
            dep_distances.append(distance)

    # Entity recognition
    entities = list(doc.ents)
    entity_labels = [ent.label_ for ent in entities]

    # Named entity density
    entity_density = len(entities) / len(sentences) if sentences else 0

    # Part of speech statistics
    pos_counts = {}
    for token in doc:
        pos = token.pos_
        pos_counts[pos] = pos_counts.get(pos, 0) + 1

    # Compilation of features
    features = {
        "token_count": len(tokens),
        "content_token_count": len(content_tokens),
        "unique_lemma_count": len(unique_lemmas),
        "lexical_diversity": (
            len(unique_lemmas) / len(content_tokens) if content_tokens else 0
        ),
        "sentence_count": len(sentences),
        "avg_sentence_length": np.mean(sentence_lengths) if sentence_lengths else 0,
        "median_sentence_length": (
            np.median(sentence_lengths) if sentence_lengths else 0
        ),
        "sentence_length_std": np.std(sentence_lengths) if sentence_lengths else 0,
        "avg_dependency_distance": np.mean(dep_distances) if dep_distances else 0,
        "max_dependency_distance": max(dep_distances) if dep_distances else 0,
        "entity_count": len(entities),
        "entity_density": entity_density,
        "entity_types": dict(
            [(label, entity_labels.count(label)) for label in set(entity_labels)]
        ),
        "pos_distribution": pos_counts,
    }

    return features
