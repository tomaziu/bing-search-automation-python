import asyncio


def calcular_meta_pontos(nivel):
    if int(nivel) == 2:
        return 90

    return 30


async def fechar_abas_extras(contexto):
    paginas = contexto.pages.copy()

    for extra in paginas[1:]:
        try:
            await extra.close()
        except Exception:
            pass


async def obter_pagina_principal(contexto):
    await fechar_abas_extras(contexto)

    if len(contexto.pages) == 0:
        return await contexto.new_page()

    return contexto.pages[0]


async def abrir_navegadores(playwright, total_navegadores, browser_path, niveis, log):
    navegadores = []

    for indice in range(total_navegadores):
        contexto = await playwright.chromium.launch_persistent_context(
            user_data_dir=f"perfil_{indice + 1}",
            executable_path=browser_path,
            headless=False,
            channel="msedge",
            args=[
                "--start-maximized",
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-session-crashed-bubble",
                "--disable-features=msRestoreTabsOnStartup",
                "--homepage=about:blank"
            ],
            no_viewport=True
        )

        await asyncio.sleep(2)

        pagina = await obter_pagina_principal(contexto)
        await pagina.goto("about:blank", wait_until="domcontentloaded")

        nivel = int(niveis[indice])
        meta_pontos = calcular_meta_pontos(nivel)

        navegadores.append(
            {
                "contexto": contexto,
                "nivel": nivel,
                "meta_pontos": meta_pontos,
                "pontos": 0,
                "meta_avisada": False
            }
        )

        log(
            f"[NAVEGADOR {indice + 1}] "
            f"Inicializado com sucesso "
            f"(Nivel {nivel} - Meta {meta_pontos} pontos)"
        )

    return navegadores


async def fechar_navegadores(navegadores):
    for navegador_data in navegadores:
        try:
            await navegador_data["contexto"].close()
        except Exception:
            pass
