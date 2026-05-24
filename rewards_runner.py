import asyncio
import random

from browser_manager import obter_pagina_principal
from search_generator import gerar_pesquisa


TOTAL_PESQUISAS = 1000
DELAY_MIN = 2
DELAY_MAX = 4
MODO_SEQUENCIAL = "sequencial"
MODO_SIMULTANEO = "simultaneo"


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


def normalizar_modo_pesquisa(modo_pesquisa):
    modo = str(modo_pesquisa or MODO_SEQUENCIAL).strip().lower()

    if modo in ("simultaneo", "simultanea", "simultâneo", "simultânea"):
        return MODO_SIMULTANEO

    return MODO_SEQUENCIAL


async def executar_pesquisa(
    indice,
    navegador_data,
    pesquisa,
    ultima_pesquisa,
    contador,
    log,
    detalhar=True
):
    contexto = navegador_data["contexto"]
    meta_pontos = navegador_data["meta_pontos"]
    agora = asyncio.get_running_loop().time()
    tempo_desde = agora - ultima_pesquisa[indice]

    if detalhar:
        log("\n==============================")
        log(f"[NAVEGADOR {indice + 1}] INICIANDO PESQUISA")
        log(f"[NAVEGADOR {indice + 1}] Nível Rewards: {navegador_data['nivel']}")
        log(f"[NAVEGADOR {indice + 1}] Pesquisa número: {contador + 1}")

    if detalhar and ultima_pesquisa[indice] != 0:
        log(f"[NAVEGADOR {indice + 1}] Última pesquisa há {tempo_desde:.2f}s")

    if detalhar:
        log(f"[NAVEGADOR {indice + 1}] Pesquisa: {pesquisa}")

    pagina = await obter_pagina_principal(contexto)

    if detalhar:
        log(f"[NAVEGADOR {indice + 1}] Abrindo Bing...")

    await pagina.goto(
        "https://www.bing.com/?toWww=1",
        wait_until="domcontentloaded",
        timeout=60000
    )

    await asyncio.sleep(random.uniform(0.15, 0.35))

    try:
        barra = pagina.locator('textarea[name="q"]')

        if await barra.count() == 0:
            barra = pagina.locator('input[name="q"]')

        await barra.first.click()

    except Exception:
        await pagina.keyboard.press("Ctrl+L")

    if detalhar:
        log(f"[NAVEGADOR {indice + 1}] Digitando pesquisa...")

    await pagina.keyboard.type(
        pesquisa,
        delay=random.randint(5, 12)
    )

    await asyncio.sleep(random.uniform(0.08, 0.20))

    if detalhar:
        log(f"[NAVEGADOR {indice + 1}] Enviando pesquisa...")

    await pagina.keyboard.press("Enter")
    await pagina.wait_for_load_state("domcontentloaded")

    if detalhar:
        log(f"[NAVEGADOR {indice + 1}] Página carregada.")

    await pagina.mouse.wheel(0, random.randint(400, 1200))

    tempo = random.uniform(0.7, 1.8)

    if detalhar:
        log(f"[NAVEGADOR {indice + 1}] Lendo por {tempo:.2f}s")

    await asyncio.sleep(tempo)

    ultima_pesquisa[indice] = asyncio.get_running_loop().time()

    if detalhar:
        log(f"[NAVEGADOR {indice + 1}] Pesquisa concluída.")

    navegador_data["pontos"] += 3
    pontos_atuais = navegador_data["pontos"]

    if detalhar:
        log(f"[NAVEGADOR {indice + 1}] Pontos: {pontos_atuais}/{meta_pontos}")

    if pontos_atuais >= meta_pontos:
        avisar_meta_atingida(indice, navegador_data, log)

    return {
        "indice": indice,
        "pesquisa": pesquisa,
        "pontos": pontos_atuais,
        "meta_pontos": meta_pontos,
        "erro": None
    }


async def executar_automacao_sequencial(navegadores, log):
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
                await executar_pesquisa(
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
            log(f"[NAVEGADOR {indice + 1}] Próxima pesquisa em {delay:.2f} segundos")
            log("==============================")

            await asyncio.sleep(delay)


async def executar_pesquisa_segura(
    indice,
    navegador_data,
    pesquisa,
    ultima_pesquisa,
    contador,
    log,
    detalhar=True
):
    try:
        return await executar_pesquisa(
            indice,
            navegador_data,
            pesquisa,
            ultima_pesquisa,
            contador,
            log,
            detalhar
        )

    except Exception as e:
        if detalhar:
            log(f"[NAVEGADOR {indice + 1}] Erro: {e}")

        return {
            "indice": indice,
            "pesquisa": pesquisa,
            "pontos": navegador_data.get("pontos", 0),
            "meta_pontos": navegador_data.get("meta_pontos", 0),
            "erro": str(e)
        }


async def executar_automacao_simultanea(navegadores, log):
    contador = 0
    ultima_pesquisa = {
        indice: 0
        for indice in range(len(navegadores))
    }

    log("[SISTEMA] Modo de pesquisa: simultânea")
    rodada = 1

    while contador < TOTAL_PESQUISAS:
        tarefas = []
        itens = []

        for indice, navegador_data in enumerate(navegadores):
            if contador + len(itens) >= TOTAL_PESQUISAS:
                break

            pesquisa = gerar_pesquisa()
            itens.append(
                {
                    "indice": indice,
                    "navegador_data": navegador_data,
                    "pesquisa": pesquisa,
                    "contador": contador + len(itens)
                }
            )

        if not itens:
            break

        log(f"\n========== RODADA SIMULTÂNEA {rodada} ==========")

        for item in itens:
            log(
                f"[NAVEGADOR {item['indice'] + 1}] "
                f"Pesquisa: {item['pesquisa']}"
            )
            tarefas.append(
                executar_pesquisa_segura(
                    item["indice"],
                    item["navegador_data"],
                    item["pesquisa"],
                    ultima_pesquisa,
                    item["contador"],
                    log,
                    False
                )
            )

        resultados = await asyncio.gather(*tarefas)

        log("[SISTEMA] Resultado da rodada:")

        for resultado in resultados:
            indice = resultado["indice"]

            if resultado["erro"]:
                log(f"[NAVEGADOR {indice + 1}] ERRO: {resultado['erro']}")
            else:
                log(
                    f"[NAVEGADOR {indice + 1}] OK - "
                    f"{resultado['pontos']}/{resultado['meta_pontos']} pontos"
                )

        contador += len(resultados)

        if contador >= TOTAL_PESQUISAS:
            break

        delay = random.uniform(DELAY_MIN, DELAY_MAX)
        log(f"[SISTEMA] Próxima rodada simultânea em {delay:.2f} segundos")
        log("==============================")

        rodada += 1
        await asyncio.sleep(delay)


async def executar_automacao(navegadores, log, modo_pesquisa=MODO_SEQUENCIAL):
    modo = normalizar_modo_pesquisa(modo_pesquisa)

    if modo == MODO_SIMULTANEO:
        await executar_automacao_simultanea(navegadores, log)
        return

    log("[SISTEMA] Modo de pesquisa: sequencial")
    await executar_automacao_sequencial(navegadores, log)
