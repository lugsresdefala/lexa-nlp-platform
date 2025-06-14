# LEXA – Linguística Exploratória e Análise Textual Avançada

**LEXA** é uma plataforma interativa de *Natural Language Processing* construída sobre [Streamlit](https://streamlit.io/). O sistema fornece um ambiente visual, extensível e escalável para inspeção, processamento e visualização de corpora de grande porte.

---

## Índice

1. [Visão Geral](#visão-geral)
2. [Principais Recursos](#principais-recursos)
3. [Requisitos](#requisitos)
4. [Instalação](#instalação)
5. [Configuração do Banco de Dados](#configuração-do-banco-de-dados)
6. [Execução](#execução)
7. [Estrutura de Diretórios](#estrutura-de-diretórios)
8. [Planos de Assinatura](#planos-de-assinatura)
9. [Contribuição](#contribuição)
10. [Licença](#licença)

---

## Visão Geral

LEXA atende a pesquisadores, engenheiros e profissionais de NLP que necessitam de:

* **Processamento avançado de texto**: tokenização, lematização, dependências sintáticas, NER, classificação e sumarização.
* **Dashboards analíticos** em tempo real com gráficos interativos e relatórios exportáveis.
* **Arquitetura modular** que habilita a adição de novos modelos, *pipelines* e componentes de visualização sem alterar o núcleo.

## Principais Recursos

| Categoria           | Descrição                                                                                             |
| ------------------- | ----------------------------------------------------------------------------------------------------- |
| **Núcleo NLP**      | Integrações nativas com spaCy, modelos Transformers (BERT, RoBERTa), Stanza e LanguageTool.           |
| **Visualização**    | Componentes reativos (radar, barras, nuvem de palavras) via `streamlit-echarts`.                      |
| **Persistência**    | Banco de dados SQLite (padrão) abstraído por SQLAlchemy; suporte a Postgres via variável de ambiente. |
| **Gerenciamento**   | Painel administrativo para controle de usuários, cotas e auditoria de uso.                            |
| **Extensibilidade** | API interna para registro dinâmico de *pipelines* e visualizações adicionais.                         |

## Requisitos

| Ferramenta | Versão mínima                |
| ---------- | ---------------------------- |
| **Python** | 3.11                         |
| **pip**    | 23.0                         |
| Sistemas   | Linux, macOS ou Windows 10 + |

> Para acelerar inferências com Transformers recomenda‑se GPU CUDA 11 ou superior (opcional).

## Instalação

```bash
# Clone o repositório
$ git clone https://github.com/<usuario>/lexa.git && cd lexa

# Instale em modo editável
$ pip install -e .
```

Todas as dependências estão declaradas em `pyproject.toml`; a instalação compilará extensões C++ quando necessário.

## Configuração do Banco de Dados

O backend de persistência utiliza SQLite por padrão. Para inicializar:

```bash
$ python utils/init_db.py
```

Para alternar para Postgres ou outro SGBD, defina `LEXA_DATABASE_URL`. Exemplo:

```bash
export LEXA_DATABASE_URL="postgresql+psycopg://user:password@host:5432/lexa"
```

## Execução

```bash
$ streamlit run app.py
```

O servidor abrirá em `http://localhost:8501` (porta padrão do Streamlit). A página **Home** resume infraestrutura, métricas e últimas análises.

## Estrutura de Diretórios

```
lexa/
├── app.py                 # Ponto de entrada Streamlit
├── config/                # Variáveis globais, constantes e temas
├── utils/                 # Funções auxiliares, pipelines NLP, init_db
├── models/                # ORM (SQLAlchemy) e classes de domínio
├── components/            # Componentes Streamlit reutilizáveis
├── assets/                # CSS customizado, ícones, imagens
└── tests/                 # Pytest suites
```

## Planos de Assinatura

| Plano          | Cota mensal (caracteres) | Público-alvo                       |
| -------------- | ------------------------ | ---------------------------------- |
| **Grátis**     | 30 000                   | Uso eventual, testes exploratórios |
| **Pro**        | 200 000                  | Pesquisadores e pequenas equipes   |
| **Enterprise** | Ilimitada                | Instituições com grande volume     |

Cotas contam todo texto processado em janelas de 30 dias.

## Contribuição

1. Abra uma *issue* para discussões substanciais.
2. Siga o padrão **Conventional Commits**.
3. Garanta *lint* e testes limpos antes do *push*:

```bash
$ ruff check . && black --check .
$ pytest -q
```

Pull‑requests são revisados sob *GitHub Actions*.

## Changelog

* Removido `stackbit.config.ts` (não utilizado).
* Removido `generated-icon.png` (ativo obsoleto).
* Unificado foco da UI em Streamlit; protótipos React foram descartados.

## Licença

Distribuído sob a licença **MIT**. Consulte [`LICENSE`](LICENSE) para detalhes.
