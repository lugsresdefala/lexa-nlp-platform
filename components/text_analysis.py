import streamlit as st
import time


def render_text_input():
    """
    Render the text input area and analysis controls.

    Returns:
        tuple: (text, analyze_button) where text is the input text and
               analyze_button is a boolean indicating if analysis should be performed
    """
    st.subheader("Entrada de Texto")

    # Text input options
    input_method = st.radio(
        "Método de entrada",
        options=["Digitar texto", "Carregar arquivo"],
        horizontal=True,
        help="Escolha entre digitar o texto manualmente ou carregar um arquivo",
    )

    text = ""
    if input_method == "Digitar texto":
        text = st.text_area(
            "Digite ou cole seu texto para análise",
            height=300,
            help="Digite ou cole um texto com pelo menos 100 palavras para obter melhores resultados de análise.",
        )

        # Sample text option
        if st.checkbox(
            "Usar texto de exemplo",
            help="Preencher automaticamente com um texto de demonstração",
        ):
            text = get_sample_text()

    else:  # Load from file
        uploaded_file = st.file_uploader(
            "Carregar arquivo de texto",
            type=["txt", "md", "pdf"],
            help="Arquivos suportados: .txt, .md, .pdf",
        )

        if uploaded_file is not None:
            # Handle different file types
            if uploaded_file.type == "application/pdf":
                st.warning(
                    "Nota: A extração de texto de PDFs pode não preservar toda a formatação original."
                )
                try:
                    import PyPDF2

                    pdf_reader = PyPDF2.PdfReader(uploaded_file)
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text()
                except Exception as e:
                    st.error(f"Erro ao processar arquivo PDF: {e}")
            else:
                # For TXT and MD files
                try:
                    text = uploaded_file.getvalue().decode("utf-8")
                except UnicodeDecodeError:
                    try:
                        text = uploaded_file.getvalue().decode("latin-1")
                    except Exception as e:
                        st.error(f"Erro ao decodificar o arquivo: {e}")

    # Text preview (if from file)
    if input_method == "Carregar arquivo" and text:
        with st.expander("Visualizar texto carregado", expanded=True):
            st.text(text[:1000] + ("..." if len(text) > 1000 else ""))

    # Analysis options
    st.subheader("Opções de Análise")

    col1, col2 = st.columns(2)

    with col1:
        _ = st.select_slider(
            "Profundidade da análise",
            options=["Básica", "Padrão", "Profunda"],
            value="Padrão",
            help="A profundidade afeta o nível de detalhe da análise linguística.",
        )

    with col2:
        _ = st.checkbox(
            "Incluir análise comparativa",
            value=True,
            help="Compara os resultados com textos de referência no mesmo domínio e gênero.",
        )

    # Analysis button
    analyze_button = st.button(
        "Analisar Texto",
        disabled=(len(text.split()) < 10),  # Require at least 10 words
        help="Inicia a análise linguística do texto fornecido.",
    )

    st.markdown(
        """
        <script>
        const buttons = window.parent.document.querySelectorAll('button');
        buttons.forEach(btn => {
            if (btn.innerText.trim() === 'Analisar Texto') {
                btn.classList.add('custom-button');
            }
        });
        </script>
        """,
        unsafe_allow_html=True,
    )

    # Warning for short texts
    if 10 <= len(text.split()) < 100:
        st.warning(
            "Textos curtos (menos de 100 palavras) podem ter resultados de análise menos precisos."
        )

    # Processing indicator (shown only during actual processing)
    if analyze_button and text:
        # Start a spinner that will be replaced by the actual analysis
        with st.spinner("Preparando análise linguística..."):
            # Simulate initial processing time
            time.sleep(0.5)

    return text, analyze_button


def get_sample_text():
    """
    Returns a sample text for analysis demonstration.
    """
    return """A análise linguística computacional constitui um campo interdisciplinar em constante evolução, combinando fundamentos da linguística teórica com métodos computacionais avançados. Este domínio científico visa compreender e modelar a linguagem humana através de algoritmos e estruturas de dados, possibilitando aplicações como tradução automática, sumarização textual e análise de sentimento.

O processamento de linguagem natural (PLN) representa um componente central desta área, focando na interação entre computadores e linguagem humana. Através de técnicas como tokenização, análise sintática e modelagem semântica, os sistemas de PLN conseguem extrair significado e estrutura de textos não estruturados, transformando-os em representações formais manipuláveis por máquinas.

A evolução dos modelos neurais de linguagem, especialmente arquiteturas baseadas em transformers, revolucionou o campo nas últimas décadas. Estes modelos capturam dependências contextuais complexas e nuances semânticas, superando limitações de abordagens anteriores baseadas em regras ou estatísticas simples.

No entanto, desafios significativos persistem, particularmente em relação à compreensão pragmática, ao conhecimento de mundo e às sutilezas culturais presentes na comunicação humana. A ambiguidade linguística, as expressões idiomáticas e o raciocínio implícito continuam representando obstáculos para sistemas automatizados.

Pesquisas recentes têm explorado abordagens multimodais, integrando processamento linguístico com percepção visual e outros sistemas cognitivos, aproximando-se gradualmente da complexidade da cognição humana. Esta tendência reflete o reconhecimento de que a linguagem não opera isoladamente, mas em constante interação com outros domínios do conhecimento e experiência.

Em conclusão, a análise linguística computacional não apenas oferece ferramentas práticas para processar informação textual em escala, mas também proporciona insights sobre a própria natureza da linguagem humana e seus mecanismos subjacentes. O avanço contínuo deste campo promete expandir nossa compreensão tanto da cognição humana quanto das possibilidades da inteligência artificial."""
