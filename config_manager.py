import json
import os


CONFIG_PATH = "config_app.json"
DEFAULT_BROWSER_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"


def config_padrao():
    return {
        "navegadores": 3,
        "tempo_login": 5,
        "browser_path": DEFAULT_BROWSER_PATH,
        "auto_inicio": False,
        "niveis": ["1", "1", "1"],
        "android_adb_path": "adb",
        "android_serial": "",
        "android_buscador": "Google",
        "android_navegador": "Padrao do Android",
        "android_navegadores": [],
        "android_quantidade": 10,
        "android_delay": 6,
        "android_tempo_abrir": 1.2,
        "android_pesquisas": ""
    }


def carregar_config():
    if not os.path.exists(CONFIG_PATH):
        return config_padrao()

    with open(CONFIG_PATH, "r", encoding="cp1252") as arquivo:
        config = json.load(arquivo)

    padrao = config_padrao()
    padrao.update(config)
    return padrao


def salvar_config(config):
    with open(CONFIG_PATH, "w", encoding="cp1252") as arquivo:
        json.dump(config, arquivo, indent=4)


def ajustar_niveis(niveis, total_navegadores):
    niveis = [str(nivel) for nivel in niveis]

    while len(niveis) < total_navegadores:
        niveis.append("1")

    return niveis[:total_navegadores]
