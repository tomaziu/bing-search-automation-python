import random


PALAVRAS_INICIO = [
    "impacto",
    "benefícios",
    "avanços",
    "história",
    "curiosidades",
    "o futuro"
]

PALAVRAS_TEMA = [
    "internet",
    "tecnologia",
    "astronomia",
    "robótica",
    "inteligência artificial",
    "programação"
]

PALAVRAS_CONTEXTO = [
    "moderna",
    "atual",
    "digital",
    "na educação",
    "na sociedade",
    "em 2026"
]


def gerar_pesquisa():
    return (
        f"{random.choice(PALAVRAS_INICIO)} "
        f"de {random.choice(PALAVRAS_TEMA)} "
        f"{random.choice(PALAVRAS_CONTEXTO)}"
    )
