# Application configuration

# App title and information
APP_TITLE = "LEXA"
APP_SUBTITLE = "Plataforma de Análise Linguística Computacional"

# Use emoji in UI labels
USE_EMOJI = False

# Supported languages
LANGUAGES = {
    "pt": "Português",
    "en": "English",
}

# Text domains
DOMAINS = [
    "Acadêmico",
    "Científico",
    "Jornalístico",
    "Técnico",
    "Literário",
    "Jurídico",
    "Médico",
]

# Text genres
GENRES = {
    "Acadêmico": [
        "Artigo Científico",
        "Tese/Dissertação",
        "Resumo/Abstract",
        "Resenha Acadêmica",
    ],
    "Científico": [
        "Artigo de Pesquisa",
        "Revisão de Literatura",
        "Comunicação Breve",
        "Estudo de Caso",
    ],
    "Jornalístico": [
        "Notícia",
        "Reportagem",
        "Editorial",
        "Artigo de Opinião",
    ],
    "Técnico": [
        "Manual",
        "Relatório Técnico",
        "Documentação",
        "Guia de Procedimentos",
    ],
    "Literário": [
        "Narrativa",
        "Poema",
        "Ensaio",
        "Crônica",
    ],
    "Jurídico": [
        "Petição",
        "Sentença",
        "Parecer",
        "Contrato",
    ],
    "Médico": [
        "Prontuário",
        "Laudo Médico",
        "Artigo Médico",
        "Prescrição",
    ],
}

# Audience levels
AUDIENCE_LEVELS = [
    "Especialista",
    "Profissional",
    "Acadêmico",
    "Público Geral",
    "Estudante",
]

# Character limits per subscription plan
PLANS = {"free": 5000, "pro": 50000, "enterprise": 200000}

# Metric dimensions - Versão expandida conforme as 8 dimensões especificadas
METRIC_DIMENSIONS = {
    "macro_estrutura": {
        "name": "Macro-estrutura Argumentativa",
        "color": "#45C4AF",  # Verde-azulado principal
        "description": "Sequência lógica, densidade inferencial e progressão temática",
        "metrics": {
            "sequencia_logica": "Análise da organização sequencial dos argumentos",
            "densidade_inferencial": "Medição da quantidade de inferências necessárias",
            "progressao_tematica": "Avaliação da evolução dos temas e subtemas",
        },
    },
    "coesao_coerencia": {
        "name": "Coesão e Coerência",
        "color": "#5de0a5",  # Verde claro
        "description": "Conectividade semântica e sobreposição de modelos situacionais",
        "metrics": {
            "coesao_local": "Conexão entre sentenças adjacentes",
            "coesao_global": "Conexão entre seções maiores do texto",
            "sobreposicao_lexical": "Recorrência de termos ao longo do texto",
        },
    },
    "sofisticacao_lexical": {
        "name": "Sofisticação Léxico-gramatical",
        "color": "#FFEB85",  # Amarelo claro
        "description": "Diversidade, raridade e especificidade terminológica",
        "metrics": {
            "diversidade_lexical": "Variação no vocabulário (TTR, MATTR)",
            "raridade_lexical": "Presença de termos raros ou técnicos",
            "especificidade_terminologica": "Precisão na escolha terminológica",
        },
    },
    "complexidade_sintatica": {
        "name": "Complexidade Sintática",
        "color": "#97DDD4",  # Turquesa claro
        "description": "Profundidade hierárquica e variação construcional",
        "metrics": {
            "profundidade_hierarquica": "Nível de subordinação nas frases",
            "variacao_construcional": "Diversidade de estruturas sintáticas",
            "densidade_informacional": "Quantidade de informação por unidade textual",
        },
    },
    "metadiscursividade": {
        "name": "Metadiscursividade",
        "color": "#1a7f76",  # Verde-azulado escuro
        "description": "Engajamento, atitude e marcadores de organização",
        "metrics": {
            "engajamento": "Mecanismos para envolver o leitor",
            "atitude": "Expressão de perspectivas e posicionamentos",
            "organizacao_textual": "Uso de marcadores para estruturar o texto",
        },
    },
    "intertextualidade": {
        "name": "Intertextualidade",
        "color": "#3d7df7",  # Azul
        "description": "Amplitude, equilíbrio e integração de fontes",
        "metrics": {
            "amplitude_fontes": "Variedade de referências utilizadas",
            "equilibrio_fontes": "Balanceamento entre diferentes fontes",
            "integracao_citacoes": "Qualidade da incorporação de citações",
        },
    },
    "rigor_metodologico": {
        "name": "Rigor Metodológico",
        "color": "#cc65fe",  # Roxo
        "description": "Reprodutibilidade e explicitação de procedimentos",
        "metrics": {
            "reproducibilidade": "Clareza para permitir reprodução de métodos",
            "explicitacao_procedimentos": "Detalhamento dos procedimentos utilizados",
            "fundamentacao_metodologica": "Base teórica para escolhas metodológicas",
        },
    },
    "estilo_adequacao": {
        "name": "Estilo e Adequação",
        "color": "#ff6b6b",  # Vermelho claro
        "description": "Convergência entre propósito comunicativo e comunidade discursiva",
        "metrics": {
            "adequacao_registro": "Ajuste do registro ao contexto e gênero",
            "consistencia_estilistica": "Manutenção de um estilo coerente",
            "conformidade_convencoes": "Respeito às convenções do gênero textual",
        },
    },
}

# Severity levels
SEVERITY_LEVELS = {
    "high": {"name": "Alta", "color": "#ff7f7f", "threshold": 8},  # Vermelho suave
    "medium": {"name": "Média", "color": "#FFEB85", "threshold": 5},  # Amarelo claro
    "low": {"name": "Baixa", "color": "#5de0a5", "threshold": 0},  # Verde claro
}

# Model configuration
NLP_MODELS = {"pt": "pt_core_news_lg", "en": "en_core_web_lg"}

# Default corpus for benchmarking
DEFAULT_CORPUS = {
    "Acadêmico": {"mean_score": 75, "std_dev": 10},
    "Científico": {"mean_score": 78, "std_dev": 8},
    "Jornalístico": {"mean_score": 72, "std_dev": 12},
    "Técnico": {"mean_score": 70, "std_dev": 15},
    "Literário": {"mean_score": 68, "std_dev": 18},
    "Jurídico": {"mean_score": 80, "std_dev": 7},
    "Médico": {"mean_score": 82, "std_dev": 6},
}

# Estatísticas do corpus de referência por dimensão
REFERENCE_CORPUS_STATS = {
    "macro_estrutura": {
        "Acadêmico": {"mean": 0.68, "std_dev": 0.12},
        "Científico": {"mean": 0.72, "std_dev": 0.10},
        "Jornalístico": {"mean": 0.65, "std_dev": 0.14},
        "Técnico": {"mean": 0.62, "std_dev": 0.15},
        "Literário": {"mean": 0.60, "std_dev": 0.18},
        "Jurídico": {"mean": 0.75, "std_dev": 0.08},
        "Médico": {"mean": 0.70, "std_dev": 0.09},
    },
    "coesao_coerencia": {
        "Acadêmico": {"mean": 0.70, "std_dev": 0.11},
        "Científico": {"mean": 0.73, "std_dev": 0.09},
        "Jornalístico": {"mean": 0.68, "std_dev": 0.13},
        "Técnico": {"mean": 0.66, "std_dev": 0.14},
        "Literário": {"mean": 0.72, "std_dev": 0.15},
        "Jurídico": {"mean": 0.78, "std_dev": 0.07},
        "Médico": {"mean": 0.72, "std_dev": 0.08},
    },
    "sofisticacao_lexical": {
        "Acadêmico": {"mean": 0.72, "std_dev": 0.10},
        "Científico": {"mean": 0.75, "std_dev": 0.08},
        "Jornalístico": {"mean": 0.65, "std_dev": 0.12},
        "Técnico": {"mean": 0.68, "std_dev": 0.11},
        "Literário": {"mean": 0.78, "std_dev": 0.14},
        "Jurídico": {"mean": 0.76, "std_dev": 0.09},
        "Médico": {"mean": 0.79, "std_dev": 0.07},
    },
    "complexidade_sintatica": {
        "Acadêmico": {"mean": 0.69, "std_dev": 0.12},
        "Científico": {"mean": 0.71, "std_dev": 0.11},
        "Jornalístico": {"mean": 0.60, "std_dev": 0.15},
        "Técnico": {"mean": 0.64, "std_dev": 0.13},
        "Literário": {"mean": 0.70, "std_dev": 0.16},
        "Jurídico": {"mean": 0.79, "std_dev": 0.08},
        "Médico": {"mean": 0.68, "std_dev": 0.10},
    },
    "metadiscursividade": {
        "Acadêmico": {"mean": 0.71, "std_dev": 0.11},
        "Científico": {"mean": 0.73, "std_dev": 0.09},
        "Jornalístico": {"mean": 0.67, "std_dev": 0.13},
        "Técnico": {"mean": 0.62, "std_dev": 0.14},
        "Literário": {"mean": 0.64, "std_dev": 0.17},
        "Jurídico": {"mean": 0.70, "std_dev": 0.10},
        "Médico": {"mean": 0.66, "std_dev": 0.12},
    },
    "intertextualidade": {
        "Acadêmico": {"mean": 0.74, "std_dev": 0.09},
        "Científico": {"mean": 0.78, "std_dev": 0.07},
        "Jornalístico": {"mean": 0.65, "std_dev": 0.12},
        "Técnico": {"mean": 0.58, "std_dev": 0.15},
        "Literário": {"mean": 0.60, "std_dev": 0.18},
        "Jurídico": {"mean": 0.72, "std_dev": 0.11},
        "Médico": {"mean": 0.76, "std_dev": 0.08},
    },
    "rigor_metodologico": {
        "Acadêmico": {"mean": 0.76, "std_dev": 0.08},
        "Científico": {"mean": 0.80, "std_dev": 0.06},
        "Jornalístico": {"mean": 0.58, "std_dev": 0.15},
        "Técnico": {"mean": 0.65, "std_dev": 0.13},
        "Literário": {"mean": 0.50, "std_dev": 0.20},
        "Jurídico": {"mean": 0.72, "std_dev": 0.10},
        "Médico": {"mean": 0.78, "std_dev": 0.07},
    },
    "estilo_adequacao": {
        "Acadêmico": {"mean": 0.72, "std_dev": 0.10},
        "Científico": {"mean": 0.75, "std_dev": 0.08},
        "Jornalístico": {"mean": 0.70, "std_dev": 0.12},
        "Técnico": {"mean": 0.68, "std_dev": 0.13},
        "Literário": {"mean": 0.76, "std_dev": 0.15},
        "Jurídico": {"mean": 0.80, "std_dev": 0.07},
        "Médico": {"mean": 0.74, "std_dev": 0.09},
    },
}

# Recursos linguísticos para análise
RECURSOS_LINGUISTICOS = {
    # Léxico acadêmico (amostra pequena - seria expandido num sistema real)
    "lexico_academico": [
        "análise",
        "metodologia",
        "hipótese",
        "teoria",
        "conceito",
        "paradigma",
        "perspectiva",
        "abordagem",
        "fenômeno",
        "contexto",
        "critério",
        "parâmetro",
        "processo",
        "síntese",
        "sistemático",
        "evidência",
        "corroborar",
        "refutar",
        "pressuposto",
        "inferir",
        "depreender",
        "postular",
        "elucidar",
        "investigar",
    ],
    # Conectivos formais categorizados por função (amostra)
    "conectivos": {
        "aditivos": [
            "além disso",
            "adicionalmente",
            "outrossim",
            "igualmente",
            "do mesmo modo",
        ],
        "adversativos": ["contudo", "entretanto", "não obstante", "porém", "todavia"],
        "causais": [
            "porquanto",
            "visto que",
            "uma vez que",
            "considerando que",
            "posto que",
        ],
        "conclusivos": [
            "portanto",
            "logo",
            "consequentemente",
            "por conseguinte",
            "destarte",
        ],
        "explicativos": [
            "isto é",
            "ou seja",
            "a saber",
            "em outras palavras",
            "por exemplo",
        ],
        "temporais": [
            "anteriormente",
            "subsequentemente",
            "simultaneamente",
            "posteriormente",
        ],
    },
    # Marcadores metadiscursivos (amostra)
    "metadiscurso": {
        "interativos": {
            "transicao": [
                "primeiro",
                "segundo",
                "finalmente",
                "por um lado",
                "por outro lado",
            ],
            "enquadramento": [
                "conforme mencionado",
                "até agora",
                "a seguir",
                "resumindo",
            ],
            "evidencialidade": [
                "de acordo com",
                "conforme",
                "segundo",
                "como indicado por",
            ],
        },
        "interacionais": {
            "atenuadores": [
                "possivelmente",
                "talvez",
                "sugere-se",
                "parece que",
                "geralmente",
            ],
            "enfatizadores": [
                "claramente",
                "indiscutivelmente",
                "de fato",
                "evidentemente",
            ],
            "atitude": [
                "surpreendentemente",
                "curiosamente",
                "infelizmente",
                "curiosamente",
            ],
            "auto_referencia": [
                "nosso estudo",
                "argumentamos que",
                "nossa análise",
                "propomos",
            ],
        },
    },
}
