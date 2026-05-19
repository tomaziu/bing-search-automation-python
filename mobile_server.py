import html
import json
import socket
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse


class MobileSearchServer:
    def __init__(self, app, token, port_inicial=8765):
        self.app = app
        self.token = token
        self.port_inicial = port_inicial
        self.httpd = None
        self.thread = None
        self.porta = None
        self.url = ""

    def iniciar(self):
        if self.httpd:
            return self.url

        handler = self._criar_handler()

        for porta in range(self.port_inicial, self.port_inicial + 20):
            try:
                self.httpd = ThreadingHTTPServer(("0.0.0.0", porta), handler)
                self.porta = porta
                break
            except OSError:
                continue

        if not self.httpd:
            raise OSError("Nao foi possivel iniciar o servidor celular.")

        self.thread = threading.Thread(
            target=self.httpd.serve_forever,
            daemon=True
        )
        self.thread.start()

        ip = self._obter_ip_local()
        self.url = f"http://{ip}:{self.porta}/?token={self.token}"
        return self.url

    def parar(self):
        if not self.httpd:
            return

        self.httpd.shutdown()
        self.httpd.server_close()
        self.httpd = None
        self.thread = None
        self.porta = None
        self.url = ""

    def _obter_ip_local(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.connect(("8.8.8.8", 80))
                return sock.getsockname()[0]
        except OSError:
            try:
                return socket.gethostbyname(socket.gethostname())
            except OSError:
                return "127.0.0.1"

    def _executar_na_interface(self, func):
        return func()

    def _estado(self):
        return self._executar_na_interface(self.app.obter_estado_mobile)

    def _gerar(self):
        return self._executar_na_interface(self.app.gerar_lote_celular)

    def _marcar_feita(self):
        return self._executar_na_interface(self.app.marcar_pesquisa_celular_mobile)

    def _criar_handler(self):
        servidor = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, formato, *args):
                return

            def do_GET(self):
                if not self._token_valido():
                    self._responder_texto("Acesso negado", 403)
                    return

                if self.path.startswith("/api/state"):
                    self._responder_json(servidor._estado())
                    return

                estado = servidor._estado()
                self._responder_html(servidor._renderizar_html(estado))

            def do_POST(self):
                if not self._token_valido():
                    self._responder_texto("Acesso negado", 403)
                    return

                rota = urlparse(self.path).path

                if rota == "/generate":
                    servidor._gerar()
                    self._redirecionar()
                    return

                if rota == "/done":
                    servidor._marcar_feita()
                    self._redirecionar()
                    return

                self._responder_texto("Rota nao encontrada", 404)

            def _token_valido(self):
                query = parse_qs(urlparse(self.path).query)
                return query.get("token", [""])[0] == servidor.token

            def _redirecionar(self):
                self.send_response(303)
                self.send_header("Location", f"/?token={servidor.token}")
                self.end_headers()

            def _responder_html(self, conteudo):
                dados = conteudo.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(dados)))
                self.end_headers()
                self.wfile.write(dados)

            def _responder_json(self, conteudo):
                dados = json.dumps(conteudo).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(dados)))
                self.end_headers()
                self.wfile.write(dados)

            def _responder_texto(self, conteudo, status=200):
                dados = conteudo.encode("utf-8")
                self.send_response(status)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.send_header("Content-Length", str(len(dados)))
                self.end_headers()
                self.wfile.write(dados)

        return Handler

    def _renderizar_html(self, estado):
        atual = estado["atual"]
        pesquisas = estado["pesquisas"]
        token = html.escape(self.token)
        progresso = int(estado["progresso"] * 100)

        if atual:
            pesquisa_atual = html.escape(atual["pesquisa"])
            link_atual = html.escape(atual["link"], quote=True)
            bloco_atual = f"""
                <section class="current">
                    <span class="kicker">Pesquisa atual</span>
                    <h1>{pesquisa_atual}</h1>
                    <a class="primary" href="{link_atual}" target="_blank" rel="noopener">Abrir pesquisa</a>
                    <form method="post" action="/done?token={token}">
                        <button type="submit">Marcar feita e proxima</button>
                    </form>
                </section>
            """
        else:
            bloco_atual = """
                <section class="current">
                    <span class="kicker">Pesquisa atual</span>
                    <h1>Meta concluida</h1>
                </section>
            """

        itens = []
        for item in pesquisas:
            numero = item["numero"]
            pesquisa = html.escape(item["pesquisa"])
            link = html.escape(item["link"], quote=True)
            classe = "done" if item["concluida"] else ""
            marcador = "Feita" if item["concluida"] else "Pendente"
            itens.append(
                f"""
                <li class="{classe}">
                    <div>
                        <strong>{numero}. {pesquisa}</strong>
                        <span>{marcador}</span>
                    </div>
                    <a href="{link}" target="_blank" rel="noopener">Abrir</a>
                </li>
                """
            )

        lista = "\n".join(itens) or "<li>Nenhum pacote gerado.</li>"

        return f"""<!doctype html>
<html lang="pt-BR">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Auto Pesquisa Celular</title>
    <style>
        :root {{
            color-scheme: dark;
            --bg: #0f172a;
            --panel: #111827;
            --panel-2: #0b1220;
            --line: #263449;
            --text: #e5edf6;
            --muted: #94a3b8;
            --green: #10b981;
            --blue: #2563eb;
        }}
        * {{
            box-sizing: border-box;
        }}
        body {{
            margin: 0;
            background: var(--bg);
            color: var(--text);
            font-family: Segoe UI, system-ui, sans-serif;
        }}
        main {{
            width: min(760px, 100%);
            margin: 0 auto;
            padding: 18px;
        }}
        .top {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            margin-bottom: 14px;
        }}
        .score {{
            font-size: 24px;
            font-weight: 800;
        }}
        .progress {{
            height: 12px;
            overflow: hidden;
            border-radius: 999px;
            background: var(--line);
            margin-bottom: 16px;
        }}
        .progress div {{
            width: {progresso}%;
            height: 100%;
            background: var(--green);
        }}
        section, li {{
            border: 1px solid var(--line);
            background: var(--panel);
            border-radius: 8px;
        }}
        .current {{
            padding: 16px;
            margin-bottom: 14px;
        }}
        .kicker, li span {{
            display: block;
            color: var(--muted);
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
        }}
        h1 {{
            margin: 8px 0 16px;
            font-size: 22px;
            line-height: 1.2;
        }}
        a, button {{
            display: block;
            width: 100%;
            min-height: 46px;
            border: 0;
            border-radius: 8px;
            color: white;
            font: inherit;
            font-weight: 800;
            text-align: center;
            text-decoration: none;
            padding: 12px 14px;
            cursor: pointer;
        }}
        .primary {{
            background: var(--blue);
            margin-bottom: 10px;
        }}
        button {{
            background: var(--green);
        }}
        .secondary {{
            background: transparent;
            border: 1px solid var(--line);
            color: var(--text);
            margin: 12px 0 16px;
        }}
        ul {{
            list-style: none;
            margin: 0;
            padding: 0;
            display: grid;
            gap: 8px;
        }}
        li {{
            display: grid;
            grid-template-columns: 1fr 86px;
            gap: 10px;
            align-items: center;
            padding: 12px;
        }}
        li.done {{
            opacity: .55;
        }}
        li a {{
            min-height: 38px;
            padding: 9px 10px;
            background: var(--panel-2);
            border: 1px solid var(--line);
        }}
    </style>
</head>
<body>
    <main>
        <div class="top">
            <div>
                <span class="kicker">Celular assistido</span>
                <div class="score">{estado["pontos"]}/{estado["meta"]} pontos</div>
            </div>
            <span class="kicker">{estado["feitas"]}/{estado["total"]} pesquisas</span>
        </div>
        <div class="progress"><div></div></div>
        {bloco_atual}
        <form method="post" action="/generate?token={token}">
            <button class="secondary" type="submit">Gerar novo pacote</button>
        </form>
        <ul>{lista}</ul>
    </main>
</body>
</html>"""
