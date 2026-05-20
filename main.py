import asyncio

from playwright.async_api import async_playwright

from browser_manager import abrir_navegadores, fechar_navegadores
from config_manager import ajustar_niveis, carregar_config
from logger import log
from rewards_runner import executar_automacao


async def main():
    config = carregar_config()

    total_navegadores = int(config["navegadores"])
    tempo_login = int(config["tempo_login"])
    browser_path = config["browser_path"]
    niveis = ajustar_niveis(config.get("niveis", []), total_navegadores)
    modo_pesquisa = config.get("pc_modo_pesquisa", "sequencial")

    async with async_playwright() as playwright:
        navegadores = await abrir_navegadores(
            playwright,
            total_navegadores,
            browser_path,
            niveis,
            log
        )

        try:
            log(f"\n[SISTEMA] {total_navegadores} navegadores abertos.")
            log("[SISTEMA] Aguardando comando para iniciar...")

            await asyncio.to_thread(input)

            log(f"[SISTEMA] Aguardando {tempo_login}s...")
            await asyncio.sleep(tempo_login)

            await executar_automacao(navegadores, log, modo_pesquisa)

            log("\n[SISTEMA] Pesquisas finalizadas.")

        finally:
            await fechar_navegadores(navegadores)


if __name__ == "__main__":
    asyncio.run(main())
