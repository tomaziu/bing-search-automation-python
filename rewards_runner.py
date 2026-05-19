import random
import time

from browser_manager import obter_pagina_principal
from search_generator import gerar_pesquisa


TOTAL_PESQUISAS = 1000
DELAY_MIN = 2
DELAY_MAX = 4


def avisar_meta_atingida(indice, navegador_data, log):
    if navegador_data["meta_avisada"]:
        return

    meta_pontos = navegador_data["meta_pontos"]

    log(
        f"\n[NAVEGADOR {indice + 1}] "
        f"META DE PONTOS ATINGIDA "
        f"({navegador_data['pontos']}/{meta_pontos}) - continuando pesquisas"
    )

    navegador_data["meta_avisada"] = True


def executar_pesquisa(indice, navegador_data, pesquisa, ultima_pesquisa, contador, log):
    contexto = navegador_data["contexto"]
    meta_pontos = navegador_data["meta_pontos"]
    agora = time.time()
    tempo_desde = agora - ultima_pesquisa[indice]

    log("\n==============================")
    log(f"[NAVEGADOR {indice + 1}] INICIANDO PESQUISA")
    log(f"[NAVEGADOR {indice + 1}] Nivel Rewards: {navegador_data['nivel']}")
    log(f"[NAVEGADOR {indice + 1}] Pesquisa numero: {contador + 1}")

    if ultima_pesquisa[indice] != 0:
        log(f"[NAVEGADOR {indice + 1}] Ultima pesquisa ha {tempo_desde:.2f}s")

    log(f"[NAVEGADOR {indice + 1}] Pesquisa: {pesquisa}")

    pagina = obter_pagina_principal(contexto)

    log(f"[NAVEGADOR {indice + 1}] Abrindo Bing...")

    pagina.goto(
        "https://www.bing.com/?toWww=1",
        wait_until="domcontentloaded",
        timeout=60000
    )

    time.sleep(random.uniform(0.15, 0.35))

    try:
        barra = pagina.locator('textarea[name="q"]')

        if barra.count() == 0:
            barra = pagina.locator('input[name="q"]')

        barra.first.click()

    except Exception:
        pagina.keyboard.press("Ctrl+L")

    log(f"[NAVEGADOR {indice + 1}] Digitando pesquisa...")

    pagina.keyboard.type(
        pesquisa,
        delay=random.randint(5, 12)
    )

    time.sleep(random.uniform(0.08, 0.20))

    log(f"[NAVEGADOR {indice + 1}] Enviando pesquisa...")

    pagina.keyboard.press("Enter")
    pagina.wait_for_load_state("domcontentloaded")

    log(f"[NAVEGADOR {indice + 1}] Pagina carregada.")

    pagina.mouse.wheel(0, random.randint(400, 1200))

    tempo = random.uniform(0.7, 1.8)
    log(f"[NAVEGADOR {indice + 1}] Lendo por {tempo:.2f}s")

    time.sleep(tempo)

    ultima_pesquisa[indice] = time.time()
    log(f"[NAVEGADOR {indice + 1}] Pesquisa concluida.")

    navegador_data["pontos"] += 3
    pontos_atuais = navegador_data["pontos"]

    log(f"[NAVEGADOR {indice + 1}] Pontos: {pontos_atuais}/{meta_pontos}")

    if pontos_atuais >= meta_pontos:
        avisar_meta_atingida(indice, navegador_data, log)


def executar_automacao(navegadores, log):
    contador = 0
    ultima_pesquisa = {
        indice: 0
        for indice in range(len(navegadores))
    }

    while contador < TOTAL_PESQUISAS:
        for indice, navegador_data in enumerate(navegadores):
            if contador >= TOTAL_PESQUISAS:
                break

            pesquisa = gerar_pesquisa()

            try:
                executar_pesquisa(
                    indice,
                    navegador_data,
                    pesquisa,
                    ultima_pesquisa,
                    contador,
                    log
                )

            except Exception as e:
                log(f"[NAVEGADOR {indice + 1}] Erro: {e}")

            contador += 1

            delay = random.uniform(DELAY_MIN, DELAY_MAX)
            log(f"[NAVEGADOR {indice + 1}] Proxima pesquisa em {delay:.2f} segundos")
            log("==============================")

            time.sleep(delay)
