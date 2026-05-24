import re
import subprocess
import time
import unicodedata
import xml.etree.ElementTree as ET
from urllib.parse import quote_plus
from urllib.parse import urlsplit, urlunsplit


NAVEGADORES_ANDROID = {
    "Padrao do Android": "",
    "Chrome": "com.android.chrome",
    "Edge": "com.microsoft.emmx",
    "Samsung Internet": "com.sec.android.app.sbrowser",
    "Firefox": "org.mozilla.firefox",
    "Brave": "com.brave.browser",
    "Opera": "com.opera.browser",
    "DuckDuckGo": "com.duckduckgo.mobile.android",
    "Bing": "com.microsoft.bing"
}


BUSCADORES = {
    "Google": "https://www.google.com/search?q={query}",
    "Bing": "https://www.bing.com/search?q={query}",
    "DuckDuckGo": "https://duckduckgo.com/?q={query}",
    "Yahoo": "https://search.yahoo.com/search?p={query}",
    "Startpage": "https://www.startpage.com/sp/search?query={query}"
}


PAGINAS_INICIAIS = {
    "Google": "https://www.google.com",
    "Bing": "https://www.bing.com",
    "DuckDuckGo": "https://duckduckgo.com",
    "Yahoo": "https://search.yahoo.com",
    "Startpage": "https://www.startpage.com"
}


class AndroidSearchAutomator:
    def __init__(self, adb_path="adb", serial=""):
        self.adb_path = adb_path.strip() or "adb"
        self.serial = serial.strip()

    def _base_cmd(self):
        cmd = [self.adb_path]

        if self.serial:
            cmd.extend(["-s", self.serial])

        return cmd

    def executar(self, args, timeout=20):
        startupinfo = None

        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        except AttributeError:
            pass

        resultado = subprocess.run(
            self._base_cmd() + args,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            startupinfo=startupinfo
        )

        saida = (resultado.stdout or "").strip()
        erro = (resultado.stderr or "").strip()

        if resultado.returncode != 0:
            mensagem = erro or saida or "Comando ADB falhou."
            raise RuntimeError(mensagem)

        return saida

    def verificar(self):
        versao = self.executar(["version"], timeout=10)
        dispositivos = self.listar_dispositivos()
        return versao, dispositivos

    def listar_dispositivos(self):
        saida = self.executar(["devices"], timeout=10)
        dispositivos = []

        for linha in saida.splitlines()[1:]:
            partes = linha.split()

            if len(partes) >= 2:
                dispositivos.append(
                    {
                        "serial": partes[0],
                        "estado": partes[1]
                    }
                )

        return dispositivos

    def montar_url(self, pesquisa, buscador):
        modelo = BUSCADORES.get(buscador, BUSCADORES["Google"])
        return modelo.format(query=quote_plus(pesquisa))

    def formatar_texto_adb(self, texto):
        texto = unicodedata.normalize("NFKD", texto)
        texto = texto.encode("ascii", "ignore").decode("ascii")
        texto = re.sub(r"[^A-Za-z0-9 ._-]+", " ", texto)
        texto = re.sub(r"\s+", " ", texto).strip()
        return texto.replace(" ", "%s")

    def preparar_dispositivo(self):
        comandos = [
            ["shell", "input", "keyevent", "KEYCODE_WAKEUP"],
            ["shell", "wm", "dismiss-keyguard"]
        ]

        for comando in comandos:
            try:
                self.executar(comando, timeout=8)
            except Exception:
                pass

    def adicionar_marcador_url(self, url):
        partes = urlsplit(url)
        separador = "&" if partes.query else ""
        query = f"{partes.query}{separador}ap_ts={int(time.time() * 1000)}"
        return urlunsplit(
            (
                partes.scheme,
                partes.netloc,
                partes.path,
                query,
                partes.fragment
            )
        )

    def abrir_url(self, url, navegador):
        pacote = NAVEGADORES_ANDROID.get(navegador, "")
        cmd = [
            "shell",
            "am",
            "start",
            "-W",
            "--activity-clear-top",
            "-a",
            "android.intent.action.VIEW",
            "-d",
            url
        ]

        if pacote:
            cmd.extend(["-p", pacote])

        return self.executar(cmd, timeout=20)

    def abrir_navegador(self, navegador):
        pacote = NAVEGADORES_ANDROID.get(navegador, "")

        if pacote:
            try:
                return self.executar(
                    [
                        "shell",
                        "monkey",
                        "-p",
                        pacote,
                        "-c",
                        "android.intent.category.LAUNCHER",
                        "1"
                    ],
                    timeout=15
                )
            except Exception:
                return self.abrir_url("about:blank", navegador)

        return self.abrir_url("about:blank", navegador)

    def obter_xml_tela(self):
        self.executar(
            ["shell", "uiautomator", "dump", "/sdcard/window.xml"],
            timeout=10
        )
        return self.executar(["shell", "cat", "/sdcard/window.xml"], timeout=10)

    def encontrar_barra_pesquisa(self):
        palavras = (
            "search",
            "pesquis",
            "buscar",
            "digite",
            "type",
            "address",
            "endereco",
            "endereço",
            "url",
            "web"
        )

        try:
            xml = self.obter_xml_tela()
            raiz = ET.fromstring(xml)
        except Exception:
            return None

        candidatos = []

        for node in raiz.iter("node"):
            atributos = " ".join(
                [
                    node.attrib.get("text", ""),
                    node.attrib.get("content-desc", ""),
                    node.attrib.get("resource-id", ""),
                    node.attrib.get("class", "")
                ]
            ).lower()

            if not any(palavra in atributos for palavra in palavras):
                continue

            bounds = node.attrib.get("bounds", "")
            match = re.match(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]", bounds)

            if not match:
                continue

            x1, y1, x2, y2 = [int(valor) for valor in match.groups()]
            largura = x2 - x1
            altura = y2 - y1

            if largura < 80 or altura < 20:
                continue

            centro_x = (x1 + x2) // 2
            centro_y = (y1 + y2) // 2
            score = 0

            if centro_y > 150:
                score += 2

            if "edittext" in atributos:
                score += 1

            if any(palavra in atributos for palavra in ("search", "pesquis", "buscar")):
                score += 2

            if any(palavra in atributos for palavra in ("address", "endereco", "url")):
                score -= 2

            candidatos.append((score, centro_x, centro_y))

        if not candidatos:
            return None

        candidatos.sort(reverse=True)
        _, x, y = candidatos[0]
        return (x, y)

    def focar_barra_pesquisa(self):
        coordenadas = self.encontrar_barra_pesquisa()

        if coordenadas:
            x, y = coordenadas
            self.executar(["shell", "input", "tap", str(x), str(y)], timeout=8)
            time.sleep(0.4)
            return True

        try:
            self.executar(["shell", "input", "keyevent", "KEYCODE_SEARCH"], timeout=8)
            time.sleep(0.4)
            return True
        except Exception:
            return False

    def pesquisar_digitando(self, pesquisa, buscador, navegador, tempo_abrir):
        texto = self.formatar_texto_adb(pesquisa)

        if not texto:
            raise RuntimeError("Pesquisa vazia depois da normalização.")

        self.preparar_dispositivo()
        pagina_inicial = PAGINAS_INICIAIS.get(buscador)

        if pagina_inicial:
            self.abrir_url(pagina_inicial, navegador)
            time.sleep(tempo_abrir)
        else:
            self.abrir_navegador(navegador)
            time.sleep(tempo_abrir)

        if not self.focar_barra_pesquisa():
            raise RuntimeError("Não foi possível focar a barra de pesquisa.")

        self.executar(["shell", "input", "text", texto], timeout=20)
        time.sleep(0.2)
        self.executar(["shell", "input", "keyevent", "ENTER"], timeout=8)
        return "Pesquisa digitada e enviada pelo teclado ADB."

    def normalizar_navegadores(self, navegadores):
        if isinstance(navegadores, str):
            candidatos = [navegadores]
        else:
            candidatos = list(navegadores or [])

        resultado = []

        for navegador in candidatos:
            nome = str(navegador).strip()

            if nome not in NAVEGADORES_ANDROID:
                continue

            if nome not in resultado:
                resultado.append(nome)

        return resultado or ["Padrao do Android"]

    def executar_pesquisas(
        self,
        pesquisas,
        buscador,
        navegadores,
        delay,
        tempo_abrir,
        log,
        deve_parar
    ):
        navegadores = self.normalizar_navegadores(navegadores)
        total_pesquisas = len(pesquisas)
        total_acoes = total_pesquisas * len(navegadores)
        acao_atual = 0

        log(
            "[ANDROID] Navegadores: "
            + ", ".join(navegadores)
        )

        for indice_pesquisa, pesquisa in enumerate(pesquisas, start=1):
            for navegador in navegadores:
                if deve_parar():
                    log("[ANDROID] Automação parada.")
                    return

                acao_atual += 1
                log(
                    f"[ANDROID] Pesquisa {indice_pesquisa}/{total_pesquisas} "
                    f"em {navegador} ({acao_atual}/{total_acoes}): {pesquisa}"
                )
                log(
                    f"[ANDROID] Abrindo {buscador} no {navegador} "
                    "e digitando no campo de pesquisa..."
                )
                resposta = self.pesquisar_digitando(
                    pesquisa,
                    buscador,
                    navegador,
                    tempo_abrir
                )
                log(f"[ANDROID] {resposta}")
                log(f"[ANDROID] Enviadas: {acao_atual}/{total_acoes}")
                log(f"[ANDROID] Buscador selecionado: {buscador}")

                if acao_atual >= total_acoes:
                    break

                log(f"[ANDROID] Aguardando {delay:.1f}s...")
                fim = time.time() + delay
                while time.time() < fim:
                    if deve_parar():
                        log("[ANDROID] Automação parada.")
                        return

                    time.sleep(0.2)

        log("[ANDROID] Automação finalizada.")
