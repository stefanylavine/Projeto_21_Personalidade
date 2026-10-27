
import random
from pathlib import Path
import math

import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Qual meme é você?",
    page_icon="🐊",
    layout="wide"
)

# Configurações das imagens
PASTA_IMAGENS = Path("preview")
POR_PAGINA = 8
COLUNAS = 4

# Signos
SIGNOS = [
    "Áries", "Touro", "Gêmeos", "Câncer", "Leão", "Virgem",
    "Libra", "Escorpião", "Sagitário", "Capricórnio",
    "Aquário", "Peixes"
]

# Frases personalizadas
FRASES = [
    "{nome}, {idade} anos e do signo de {signo}: o universo conspirou e te entregou ESSE meme. Aceita.",
    "Os astros de {signo} não mentem, {nome}. Essa é a sua alma em forma de meme.",
    "Com {idade} anos de experiência de vida, {nome}, você ainda é exatamente isso aqui. 💀",
    "Todo {signo} tem um lado meme, {nome}. O seu ficou exposto agora.",
    "Laudo oficial: {nome} ({signo}, {idade} anos) é 100% esse personagem. Sem recurso.",
    "Mercúrio retrógrado me contou que {nome} acorda segunda-feira com essa energia."
]

# Estilo visual
st.markdown("""
<style>
.stApp {
    background-color: #101018;
    color: white;
}

h1, h2, h3, p, label {
    color: white !important;
}

.stButton > button {
    background-color: #8A2BE2;
    color: white;
    border-radius: 10px;
    border: none;
    font-weight: bold;
    width: 100%;
}

.stButton > button:hover {
    background-color: #6A0DAD;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# Título
st.title("🔮 Qual meme é a sua personalidade?")
st.write(
    "Preencha seus dados e descubra a verdade "
    "(científica... ou quase 😂) sobre você!"
)

# Formulário
with st.form("formulario_personalidade"):
    nome = st.text_input("Seu nome")
    idade = st.number_input(
        "Sua idade",
        min_value=1,
        max_value=120,
        value=18,
        step=1
    )
    signo = st.selectbox("Seu signo", SIGNOS)

    descobrir = st.form_submit_button(
        "🔮 Descubra sua personalidade"
    )

# Carrega as imagens disponíveis
if PASTA_IMAGENS.exists():
    imagens = sorted(
        list(PASTA_IMAGENS.glob("*.jpg"))
        + list(PASTA_IMAGENS.glob("*.jpeg"))
        + list(PASTA_IMAGENS.glob("*.png"))
        + list(PASTA_IMAGENS.glob("*.webp"))
    )
else:
    imagens = []

# Descoberta da personalidade
if descobrir:
    if not nome.strip():
        st.warning("Digite seu nome para os astros te encontrarem! ✨")

    elif not imagens:
        st.error(
            f"Nenhuma imagem encontrada na pasta '{PASTA_IMAGENS}'. "
            "Verifique se a pasta existe e contém imagens."
        )

    else:
        st.session_state["meme_escolhido"] = random.choice(imagens)
        st.session_state["frase_escolhida"] = random.choice(FRASES).format(
            nome=nome.strip(),
            idade=int(idade),
            signo=signo
        )

# Exibe o resultado salvo
if "meme_escolhido" in st.session_state:
    st.divider()
    st.subheader("✨ Sua personalidade foi revelada!")

    st.write(st.session_state["frase_escolhida"])

    st.image(
        str(st.session_state["meme_escolhido"]),
        caption=f"Meme nº {st.session_state['meme_escolhido'].stem}",
        width=400
    )

    if st.button("😂 Quero outro meme!"):
        st.session_state["meme_escolhido"] = random.choice(imagens)
        st.session_state["frase_escolhida"] = random.choice(FRASES).format(
            nome=nome.strip() or "Você",
            idade=int(idade),
            signo=signo
        )
        st.rerun()

# Galeria de memes
st.divider()
st.header("🖼️ Galeria de memes")

if not imagens:
    st.info(
        f"Adicione imagens à pasta '{PASTA_IMAGENS}' "
        "para visualizar a galeria."
    )

else:
    total_memes = len(imagens)
    total_paginas = math.ceil(total_memes / POR_PAGINA)

    st.write(f"Temos **{total_memes} memes** disponíveis!")

    pagina = st.number_input(
        "Escolha a página",
        min_value=1,
        max_value=total_paginas,
        value=1,
        step=1,
        key="pagina_galeria"
    )

    inicio = (pagina - 1) * POR_PAGINA
    fim = inicio + POR_PAGINA
    imagens_da_pagina = imagens[inicio:fim]

    st.caption(f"Página {pagina} de {total_paginas}")

    colunas = st.columns(COLUNAS)

    for i, caminho in enumerate(imagens_da_pagina):
        coluna = colunas[i % COLUNAS]

        with coluna:
            st.image(
                str(caminho),
                caption=caminho.stem,
                width="stretch"
            )

st.divider()
st.caption("🔮 Feito com Python e Streamlit | Os astros não garantem os resultados 😂")
