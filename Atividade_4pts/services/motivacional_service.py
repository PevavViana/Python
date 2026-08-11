import random

import requests

URL_FRASES = "https://raw.githubusercontent.com/devmatheusguerra/frasesJSON/main/frases.json"
TIMEOUT = 10

def buscar_frase_motivacional():
    try:
        resposta = requests.get(URL_FRASES, timeout=TIMEOUT)
        resposta.raise_for_status()
        frases = resposta.json()
        escolhida = random.choice(frases)
        frase = escolhida["frase"]
        autor = escolhida["autor"]
        return frase + " " + autor
    except requests.RequestException:
        return "Não foi possível buscar a frase do dia agora."