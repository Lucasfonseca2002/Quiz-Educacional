from matematica import obter_perguntas_matematica
from portugues import obter_perguntas_portugues
from ciencias import obter_perguntas_ciencias

def obter_perguntas():
    banco_perguntas = {
        "Matemática": obter_perguntas_matematica(),
        "Português": obter_perguntas_portugues(),
        "Ciências": obter_perguntas_ciencias()
    }

    return banco_perguntas