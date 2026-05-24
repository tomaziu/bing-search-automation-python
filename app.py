import customtkinter as ctk
from tkinter import END
import os
import subprocess
import sys
import threading
import ctypes
import ctypes.wintypes

from android_automation import BUSCADORES, NAVEGADORES_ANDROID, AndroidSearchAutomator
from config_manager import DEFAULT_BROWSER_PATH, carregar_config, salvar_config
from search_generator import gerar_pesquisa


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Auto Pesquisa - Bing")
        self.tema_visual = self.obter_tema_inicial()
        self.aplicar_tema_visual(self.tema_visual)
        self.geometry(self.janela_tamanho)
        self.minsize(*self.janela_minima)
        self.centralizar_janela(*self.janela_dimensoes)

        self.attributes("-topmost", True)
        self.bind("<Unmap>", lambda e: self.attributes("-topmost", False))
        self.bind("<Map>", lambda e: self.attributes("-topmost", True))

        self.processo = None
        self.niveis_vars = []
        self.pc_modo_pesquisa = ctk.StringVar(value="Sequencial")
        self.android_thread = None
        self.android_stop_event = threading.Event()
        self.android_navegador_vars = {}

        self.criar_topo()
        self.criar_conteudo()
        self.carregar_config()
        self.atualizar_niveis()
        self.atualizar_botoes()
        self.log("[SISTEMA] Interface carregada com sucesso.")

    # =========================================================

    def obter_tema_inicial(self):
        try:
            config = carregar_config()
            tema = config.get("tema_visual", "editor")
        except Exception:
            tema = "editor"

        if tema not in ("editor", "classico"):
            return "editor"

        return tema

    # =========================================================

    def aplicar_tema_visual(self, tema):
        if tema == "classico":
            self.tema_visual = "classico"
            self.janela_dimensoes = (540, 640)
            self.janela_minima = (500, 590)
            self.altura_topo = 82
            self.titulo_topo = "Auto Pesquisa Bing"
            self.subtitulo_topo = "Automação de pesquisas com perfis separados"
            self.fonte_titulo = ("Segoe UI", 23, "bold")
            self.fonte_subtitulo = ("Segoe UI", 11)
            self.tabs_pady = (14, 10)
            self.raio_card = 16
            self.raio_painel = 12
            self.raio_input = 9
            self.raio_botao = 9
            self.pad_externo = 18
            self.pad_interno = 16
            self.pad_secao = 20
            self.cor_principal = "#38bdf8"
            self.cor_secundaria = "#10b981"
            self.hover_secundaria = "#059669"
            self.cor_bg = "#0f172a"
            self.cor_card = "#111827"
            self.cor_card_claro = "#182235"
            self.cor_input = "#0b1220"
            self.cor_borda = "#263449"
            self.cor_texto = "#e5edf6"
            self.cor_texto_suave = "#94a3b8"
            self.cor_console = "#070d18"
            self.cor_console_texto = "#7dd3fc"
            self.cor_sucesso = "#22c55e"
            self.cor_erro = "#fb7185"
            self.cor_info = "#60a5fa"
            self.cor_botao_neutro = "#2563eb"
            self.hover_botao_neutro = "#1d4ed8"
            self.cor_botao_iniciar = "#0891b2"
            self.hover_botao_iniciar = "#0e7490"
            self.cor_botao_parar = "#e11d48"
            self.hover_botao_parar = "#be123c"
        else:
            self.tema_visual = "editor"
            self.janela_dimensoes = (620, 670)
            self.janela_minima = (560, 620)
            self.altura_topo = 44
            self.titulo_topo = "Auto Pesquisa"
            self.subtitulo_topo = "Painel de automação Bing"
            self.fonte_titulo = ("Segoe UI", 13, "bold")
            self.fonte_subtitulo = ("Segoe UI", 10)
            self.tabs_pady = (8, 10)
            self.raio_card = 5
            self.raio_painel = 5
            self.raio_input = 5
            self.raio_botao = 5
            self.pad_externo = 12
            self.pad_interno = 12
            self.pad_secao = 14
            self.cor_principal = "#c8a94a"
            self.cor_secundaria = "#9a7a2f"
            self.hover_secundaria = "#b08d38"
            self.cor_bg = "#050606"
            self.cor_card = "#0a0b0c"
            self.cor_card_claro = "#101113"
            self.cor_input = "#070808"
            self.cor_borda = "#191b1f"
            self.cor_texto = "#d7d7d7"
            self.cor_texto_suave = "#777b82"
            self.cor_console = "#050606"
            self.cor_console_texto = "#a7abb3"
            self.cor_sucesso = "#6fbf73"
            self.cor_erro = "#d9534f"
            self.cor_info = "#8b8f99"
            self.cor_botao_neutro = "#1d1f24"
            self.hover_botao_neutro = "#272a31"
            self.cor_botao_iniciar = "#17321c"
            self.hover_botao_iniciar = "#214728"
            self.cor_botao_parar = "#341316"
            self.hover_botao_parar = "#461b1f"

        largura, altura = self.janela_dimensoes
        self.janela_tamanho = f"{largura}x{altura}"
        self.configure(fg_color=self.cor_bg)

    # =========================================================

    def centralizar_janela(self, largura, altura):
        self.update_idletasks()

        area_trabalho = ctypes.wintypes.RECT()

        ctypes.windll.user32.SystemParametersInfoW(
            0x0030,
            0,
            ctypes.byref(area_trabalho),
            0
        )

        largura_tela = area_trabalho.right - area_trabalho.left
        altura_tela = area_trabalho.bottom - area_trabalho.top

        pos_x = area_trabalho.left + int((largura_tela - largura) / 2)
        pos_y = area_trabalho.top + int((altura_tela - altura) / 2)

        self.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

    # =========================================================

    def criar_topo(self):
        self.topo = ctk.CTkFrame(
            self,
            fg_color=self.cor_card,
            corner_radius=0,
            height=self.altura_topo
        )
        self.topo.pack(fill="x")
        self.topo.pack_propagate(False)

        self.topo.grid_columnconfigure(1, weight=1)

        self.titulo = ctk.CTkLabel(
            self.topo,
            text=self.titulo_topo,
            font=self.fonte_titulo,
            text_color=self.cor_texto
        )

        self.subtitulo = ctk.CTkLabel(
            self.topo,
            text=self.subtitulo_topo,
            font=self.fonte_subtitulo,
            text_color=self.cor_texto_suave
        )

        texto_tema = "Tema: Editor" if self.tema_visual == "editor" else "Tema: Clássico"
        self.btn_tema = ctk.CTkButton(
            self.topo,
            text=texto_tema,
            width=112,
            height=28,
            corner_radius=self.raio_botao,
            fg_color=self.cor_input,
            hover_color=self.cor_borda,
            text_color=self.cor_texto,
            font=("Segoe UI", 10, "bold"),
            command=self.alternar_tema_visual
        )

        if self.tema_visual == "classico":
            self.topo.grid_columnconfigure(0, weight=1)
            self.titulo.grid(row=0, column=0, padx=(126, 12), pady=(10, 0), sticky="ew")
            self.subtitulo.grid(row=1, column=0, padx=(126, 12), pady=(0, 4), sticky="ew")
            self.btn_tema.grid(row=0, column=1, rowspan=2, padx=14, pady=10, sticky="e")
            ctk.CTkFrame(
                self.topo,
                fg_color=self.cor_secundaria,
                height=3
            ).grid(row=2, column=0, columnspan=2, padx=76, pady=(0, 0), sticky="ew")
        else:
            self.titulo.grid(row=0, column=0, padx=14, pady=10, sticky="w")
            self.subtitulo.grid(row=0, column=1, padx=8, pady=10, sticky="w")
            self.btn_tema.grid(row=0, column=2, padx=14, pady=8, sticky="e")

    # =========================================================

    def criar_conteudo(self):
        self.tabs = ctk.CTkTabview(
            self,
            fg_color=self.cor_bg,
            segmented_button_fg_color=self.cor_card,
            segmented_button_selected_color=self.cor_secundaria,
            segmented_button_selected_hover_color=self.hover_secundaria,
            segmented_button_unselected_color=self.cor_input,
            segmented_button_unselected_hover_color=self.cor_borda,
            text_color=self.cor_texto
        )
        self.tabs.pack(
            fill="both",
            expand=True,
            padx=self.pad_externo,
            pady=self.tabs_pady
        )
        self.tabs.add("PC")
        self.tabs.add("Android")

        self.container = ctk.CTkScrollableFrame(
            self.tabs.tab("PC"),
            fg_color=self.cor_card,
            corner_radius=self.raio_card,
            border_width=1,
            border_color=self.cor_borda
        )
        self.container.pack(
            fill="both",
            expand=True,
            padx=0,
            pady=(6, 0)
        )

        self.status_frame = ctk.CTkFrame(
            self.container,
            fg_color=self.cor_input,
            corner_radius=self.raio_painel,
            border_width=1,
            border_color=self.cor_borda
        )
        self.status_frame.pack(fill="x", padx=self.pad_interno, pady=(8, 8))

        self.status = ctk.CTkLabel(
            self.status_frame,
            text="PARADO",
            font=("Segoe UI", 11, "bold"),
            text_color=self.cor_erro
        )
        self.status.pack(pady=7)

        self.criar_secao("Configurações", self.container)

        self.frame_inputs = ctk.CTkFrame(self.container, fg_color="transparent")
        self.frame_inputs.pack(fill="x", padx=self.pad_interno, pady=(0, 6))
        self.frame_inputs.grid_columnconfigure((0, 1), weight=1)

        self.criar_input(self.frame_inputs, "Navegadores", "navegadores", "4", 0)
        self.criar_input(self.frame_inputs, "Tempo (s)", "login", "5", 1)
        self.entry_navegadores.bind("<KeyRelease>", lambda e: self.atualizar_niveis())

        self.criar_input_full("Caminho do Navegador")

        self.criar_secao("Nível de Cada Navegador", self.container)

        self.frame_niveis = ctk.CTkFrame(self.container, fg_color="transparent")
        self.frame_niveis.pack(fill="x", padx=self.pad_interno, pady=(0, 8))

        self.auto_inicio = ctk.BooleanVar(value=False)
        self.checkbox_auto = ctk.CTkCheckBox(
            self.container,
            text="Iniciar automaticamente",
            variable=self.auto_inicio,
            font=("Segoe UI", 12),
            text_color=self.cor_texto,
            checkbox_width=17,
            checkbox_height=17,
            fg_color=self.cor_secundaria,
            hover_color=self.hover_secundaria,
            border_color=self.cor_borda,
            command=self.checkbox_evento
        )
        self.checkbox_auto.pack(anchor="w", padx=self.pad_secao, pady=(4, 12))

        self.criar_secao("Modo de Pesquisa", self.container)

        self.segmento_pc_modo = ctk.CTkSegmentedButton(
            self.container,
            values=["Sequencial", "Simultânea"],
            variable=self.pc_modo_pesquisa,
            command=lambda valor: self.salvar_config(),
            height=36,
            corner_radius=self.raio_botao,
            selected_color=self.cor_secundaria,
            selected_hover_color=self.hover_secundaria,
            unselected_color=self.cor_input,
            unselected_hover_color=self.cor_borda,
            text_color=self.cor_texto,
            font=("Segoe UI", 11, "bold")
        )
        self.segmento_pc_modo.pack(fill="x", padx=self.pad_secao, pady=(0, 12))

        self.frame_botoes = ctk.CTkFrame(self.container, fg_color="transparent")
        self.frame_botoes.pack(fill="x", padx=self.pad_interno, pady=(2, 10))
        self.frame_botoes.grid_columnconfigure((0, 1), weight=1)

        self.btn_abrir = ctk.CTkButton(
            self.frame_botoes,
            text="Abrir navegadores",
            height=38,
            corner_radius=self.raio_botao,
            font=("Segoe UI", 11, "bold"),
            fg_color=self.cor_secundaria,
            hover_color=self.hover_secundaria,
            command=self.iniciar
        )
        self.btn_abrir.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=4,
            pady=(0, 8),
            sticky="ew"
        )

        self.btn_iniciar = ctk.CTkButton(
            self.frame_botoes,
            text="Iniciar",
            height=36,
            corner_radius=self.raio_botao,
            font=("Segoe UI", 11, "bold"),
            fg_color=self.cor_botao_neutro,
            hover_color=self.hover_botao_neutro,
            command=self.enviar_enter
        )

        self.btn_parar = ctk.CTkButton(
            self.frame_botoes,
            text="Parar",
            height=36,
            corner_radius=self.raio_botao,
            font=("Segoe UI", 11, "bold"),
            fg_color=self.cor_botao_parar,
            hover_color=self.hover_botao_parar,
            command=self.parar
        )

        self.btn_iniciar.grid(row=1, column=0, padx=4, pady=4, sticky="ew")
        self.btn_parar.grid(row=1, column=1, padx=4, pady=4, sticky="ew")

        self.criar_secao("Console", self.container)

        self.terminal = ctk.CTkTextbox(
            self.container,
            height=220,
            corner_radius=self.raio_painel,
            fg_color=self.cor_console,
            font=("Consolas", 11),
            text_color=self.cor_console_texto,
            border_width=1,
            border_color=self.cor_borda
        )
        self.terminal.pack(fill="both", expand=True, padx=self.pad_interno, pady=(4, 12))

        self.criar_conteudo_android(self.tabs.tab("Android"))

    # =========================================================

    def criar_conteudo_android(self, parent):
        self.android_container = ctk.CTkScrollableFrame(
            parent,
            fg_color=self.cor_card,
            corner_radius=self.raio_card,
            border_width=1,
            border_color=self.cor_borda
        )
        self.android_container.pack(
            fill="both",
            expand=True,
            padx=0,
            pady=(6, 0)
        )

        self.criar_secao("Automação Android", self.android_container)

        self.android_status = ctk.CTkLabel(
            self.android_container,
            text="ADB não verificado",
            font=("Segoe UI", 11, "bold"),
            text_color=self.cor_texto_suave
        )
        self.android_status.pack(anchor="w", padx=self.pad_secao, pady=(0, 8))

        self.android_grid = ctk.CTkFrame(
            self.android_container,
            fg_color="transparent"
        )
        self.android_grid.pack(fill="x", padx=self.pad_interno, pady=(0, 8))
        self.android_grid.grid_columnconfigure((0, 1), weight=1)

        self.entry_android_adb = self.criar_entry_android(
            self.android_grid,
            "ADB",
            "adb",
            0,
            0
        )
        self.entry_android_serial = self.criar_entry_android(
            self.android_grid,
            "Serial",
            "",
            0,
            1
        )

        self.frame_android_opcoes = ctk.CTkFrame(
            self.android_container,
            fg_color="transparent"
        )
        self.frame_android_opcoes.pack(fill="x", padx=self.pad_interno, pady=(0, 8))
        self.frame_android_opcoes.grid_columnconfigure(0, weight=1)

        self.combo_android_buscador = self.criar_combo_android(
            self.frame_android_opcoes,
            "Buscador",
            list(BUSCADORES.keys()),
            "Google",
            0,
            0
        )

        self.criar_secao("Alternar Navegadores", self.android_container)

        self.frame_android_navegadores = ctk.CTkFrame(
            self.android_container,
            fg_color=self.cor_input,
            corner_radius=self.raio_painel,
            border_width=1,
            border_color=self.cor_borda
        )
        self.frame_android_navegadores.pack(fill="x", padx=self.pad_interno, pady=(4, 10))
        self.frame_android_navegadores.grid_columnconfigure((0, 1), weight=1)

        navegadores_alternaveis = [
            nome
            for nome in NAVEGADORES_ANDROID
            if nome != "Padrao do Android"
        ]
        self.android_navegador_vars.clear()

        for indice, nome in enumerate(navegadores_alternaveis):
            var = ctk.BooleanVar(value=False)
            self.android_navegador_vars[nome] = var

            checkbox = ctk.CTkCheckBox(
                self.frame_android_navegadores,
                text=nome,
                variable=var,
                command=self.salvar_config,
                corner_radius=self.raio_input,
                border_width=2,
                fg_color=self.cor_secundaria,
                hover_color=self.hover_secundaria,
                text_color=self.cor_texto,
                font=("Segoe UI", 11)
            )
            checkbox.grid(
                row=indice // 2,
                column=indice % 2,
                padx=10,
                pady=7,
                sticky="w"
            )

        self.frame_android_execucao = ctk.CTkFrame(
            self.android_container,
            fg_color="transparent"
        )
        self.frame_android_execucao.pack(fill="x", padx=self.pad_interno, pady=(0, 8))
        self.frame_android_execucao.grid_columnconfigure((0, 1), weight=1)

        self.entry_android_quantidade = self.criar_entry_android(
            self.frame_android_execucao,
            "Quantidade",
            "10",
            0,
            0
        )
        self.entry_android_delay = self.criar_entry_android(
            self.frame_android_execucao,
            "Delay (s)",
            "6",
            0,
            1
        )
        self.entry_android_tempo_abrir = self.criar_entry_android(
            self.frame_android_execucao,
            "Abrir (s)",
            "1.2",
            1,
            0
        )

        self.criar_secao("Pesquisas", self.android_container)

        self.texto_android_pesquisas = ctk.CTkTextbox(
            self.android_container,
            height=130,
            corner_radius=self.raio_painel,
            fg_color=self.cor_console,
            font=("Consolas", 11),
            text_color=self.cor_console_texto,
            border_width=1,
            border_color=self.cor_borda
        )
        self.texto_android_pesquisas.pack(
            fill="both",
            expand=True,
            padx=self.pad_interno,
            pady=(4, 10)
        )

        self.frame_android_botoes = ctk.CTkFrame(
            self.android_container,
            fg_color="transparent"
        )
        self.frame_android_botoes.pack(fill="x", padx=self.pad_interno, pady=(0, 10))
        self.frame_android_botoes.grid_columnconfigure((0, 1), weight=1)

        self.btn_android_verificar = ctk.CTkButton(
            self.frame_android_botoes,
            text="Verificar ADB",
            height=36,
            corner_radius=self.raio_botao,
            font=("Segoe UI", 11, "bold"),
            fg_color=self.cor_secundaria,
            hover_color=self.hover_secundaria,
            command=self.verificar_android
        )
        self.btn_android_verificar.grid(row=0, column=0, padx=4, pady=4, sticky="ew")

        self.btn_android_gerar = ctk.CTkButton(
            self.frame_android_botoes,
            text="Gerar lista",
            height=36,
            corner_radius=self.raio_botao,
            font=("Segoe UI", 11, "bold"),
            fg_color=self.cor_botao_neutro,
            hover_color=self.hover_botao_neutro,
            command=self.gerar_lista_android
        )
        self.btn_android_gerar.grid(row=0, column=1, padx=4, pady=4, sticky="ew")

        self.btn_android_iniciar = ctk.CTkButton(
            self.frame_android_botoes,
            text="Iniciar",
            height=36,
            corner_radius=self.raio_botao,
            font=("Segoe UI", 11, "bold"),
            fg_color=self.cor_botao_iniciar,
            hover_color=self.hover_botao_iniciar,
            command=self.iniciar_android
        )
        self.btn_android_iniciar.grid(row=1, column=0, padx=4, pady=4, sticky="ew")

        self.btn_android_parar = ctk.CTkButton(
            self.frame_android_botoes,
            text="Parar",
            height=36,
            corner_radius=self.raio_botao,
            font=("Segoe UI", 11, "bold"),
            fg_color=self.cor_botao_parar,
            hover_color=self.hover_botao_parar,
            command=self.parar_android
        )
        self.btn_android_parar.grid(row=1, column=1, padx=4, pady=4, sticky="ew")

        self.criar_secao("Console Android", self.android_container)

        self.console_android = ctk.CTkTextbox(
            self.android_container,
            height=160,
            corner_radius=self.raio_painel,
            fg_color=self.cor_console,
            font=("Consolas", 11),
            text_color=self.cor_console_texto,
            border_width=1,
            border_color=self.cor_borda
        )
        self.console_android.pack(
            fill="both",
            expand=True,
            padx=self.pad_interno,
            pady=(4, 12)
        )

    # =========================================================

    def criar_entry_android(self, parent, texto, valor_padrao, linha, coluna):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=linha, column=coluna, padx=4, pady=4, sticky="ew")

        ctk.CTkLabel(
            frame,
            text=texto,
            font=("Segoe UI", 11, "bold"),
            text_color=self.cor_texto_suave
        ).pack(anchor="w", pady=(0, 3))

        entry = ctk.CTkEntry(
            frame,
            height=34,
            corner_radius=self.raio_input,
            border_width=1,
            border_color=self.cor_borda,
            fg_color=self.cor_input,
            text_color=self.cor_texto,
            font=("Segoe UI", 11)
        )
        entry.pack(fill="x")
        entry.insert(0, valor_padrao)
        entry.bind("<KeyRelease>", lambda e: self.salvar_config())
        return entry

    # =========================================================

    def criar_combo_android(self, parent, texto, valores, valor_padrao, linha, coluna):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=linha, column=coluna, padx=4, pady=4, sticky="ew")

        ctk.CTkLabel(
            frame,
            text=texto,
            font=("Segoe UI", 11, "bold"),
            text_color=self.cor_texto_suave
        ).pack(anchor="w", pady=(0, 3))

        combo = ctk.CTkComboBox(
            frame,
            values=valores,
            height=34,
            corner_radius=self.raio_input,
            border_width=1,
            border_color=self.cor_borda,
            fg_color=self.cor_input,
            button_color=self.cor_secundaria,
            button_hover_color=self.hover_secundaria,
            dropdown_fg_color=self.cor_card_claro,
            dropdown_hover_color=self.cor_borda,
            text_color=self.cor_texto,
            font=("Segoe UI", 11),
            command=lambda valor: self.salvar_config()
        )
        combo.pack(fill="x")
        combo.set(valor_padrao)
        return combo

    # =========================================================

    def obter_navegadores_android_marcados(self):
        return [
            nome
            for nome, var in self.android_navegador_vars.items()
            if var.get()
        ]

    # =========================================================

    def obter_navegadores_android_execucao(self):
        return self.obter_navegadores_android_marcados()

    def log_android(self, texto):
        def escrever():
            self.console_android.insert(END, f"{texto}\n")
            self.console_android.see("end")

        if self.executar_na_thread_interface():
            escrever()
            return

        try:
            self.after(0, escrever)
        except RuntimeError:
            print(texto, flush=True)

    # =========================================================

    def criar_automator_android(self):
        return AndroidSearchAutomator(
            self.entry_android_adb.get(),
            self.entry_android_serial.get()
        )

    # =========================================================

    def atualizar_status_android(self, texto, cor):
        def aplicar():
            self.android_status.configure(text=texto, text_color=cor)

        if self.executar_na_thread_interface():
            aplicar()
            return

        try:
            self.after(0, aplicar)
        except RuntimeError:
            print(f"[ANDROID] {texto}", flush=True)

    # =========================================================

    def obter_pesquisas_android(self):
        conteudo = self.texto_android_pesquisas.get("1.0", "end").strip()
        return [
            linha.strip()
            for linha in conteudo.splitlines()
            if linha.strip()
        ]

    # =========================================================

    def verificar_android(self):
        self.salvar_config()
        self.android_status.configure(
            text="Verificando ADB...",
            text_color=self.cor_texto_suave
        )
        adb_path = self.entry_android_adb.get()
        serial = self.entry_android_serial.get()

        def rodar():
            try:
                automator = AndroidSearchAutomator(adb_path, serial)
                versao, dispositivos = automator.verificar()
                self.log_android("[ANDROID] ADB encontrado.")

                primeira_linha = versao.splitlines()[0] if versao else "ADB OK"
                self.log_android(f"[ANDROID] {primeira_linha}")

                if not dispositivos:
                    mensagem = "Nenhum Android conectado"
                    self.log_android("[ANDROID] Nenhum dispositivo listado.")
                    cor = self.cor_erro
                else:
                    partes = [
                        f"{item['serial']} ({item['estado']})"
                        for item in dispositivos
                    ]
                    mensagem = "; ".join(partes)
                    self.log_android(f"[ANDROID] Dispositivos: {mensagem}")
                    cor = self.cor_secundaria

                self.atualizar_status_android(mensagem, cor)

            except Exception as e:
                self.log_android(f"[ANDROID][ERRO] {e}")
                self.atualizar_status_android(
                    "ADB não encontrado ou sem permissão",
                    self.cor_erro
                )

        threading.Thread(target=rodar, daemon=True).start()

    # =========================================================

    def gerar_lista_android(self):
        try:
            quantidade = int(self.entry_android_quantidade.get())
        except Exception:
            quantidade = 10

        quantidade = max(1, min(100, quantidade))
        pesquisas = [gerar_pesquisa() for _ in range(quantidade)]

        self.texto_android_pesquisas.delete("1.0", "end")
        self.texto_android_pesquisas.insert("end", "\n".join(pesquisas))
        self.log_android(f"[ANDROID] Lista gerada com {quantidade} pesquisas.")
        self.salvar_config()

    # =========================================================

    def iniciar_android(self):
        if self.android_thread and self.android_thread.is_alive():
            self.log_android("[ANDROID] Automação já está em execução.")
            return

        pesquisas = self.obter_pesquisas_android()

        if not pesquisas:
            self.gerar_lista_android()
            pesquisas = self.obter_pesquisas_android()

        try:
            delay = float(self.entry_android_delay.get().replace(",", "."))
        except Exception:
            delay = 6

        delay = max(1, delay)

        try:
            tempo_abrir = float(
                self.entry_android_tempo_abrir.get().replace(",", ".")
            )
        except Exception:
            tempo_abrir = 1.2

        tempo_abrir = max(0.4, tempo_abrir)
        buscador = self.combo_android_buscador.get()
        navegadores = self.obter_navegadores_android_execucao()

        if not navegadores:
            self.log_android(
                "[ANDROID] Marque pelo menos um navegador em Alternar Navegadores."
            )
            self.atualizar_status_android(
                "Selecione um navegador Android",
                self.cor_erro
            )
            return

        adb_path = self.entry_android_adb.get()
        serial = self.entry_android_serial.get()
        self.android_stop_event.clear()
        self.salvar_config()

        def rodar():
            try:
                self.atualizar_status_android(
                    "Executando automação Android",
                    self.cor_secundaria
                )
                automator = AndroidSearchAutomator(adb_path, serial)
                automator.executar_pesquisas(
                    pesquisas,
                    buscador,
                    navegadores,
                    delay,
                    tempo_abrir,
                    self.log_android,
                    self.android_stop_event.is_set
                )
                self.atualizar_status_android(
                    "Automação Android finalizada",
                    self.cor_info
                )

            except Exception as e:
                self.log_android(f"[ANDROID][ERRO] {e}")
                self.atualizar_status_android(
                    "Erro na automação Android",
                    self.cor_erro
                )

        self.android_thread = threading.Thread(target=rodar, daemon=True)
        self.android_thread.start()

    # =========================================================

    def parar_android(self):
        self.android_stop_event.set()
        self.log_android("[ANDROID] Parada solicitada.")

    # =========================================================

    def executar_na_thread_interface(self):
        return threading.current_thread() is threading.main_thread()

    # =========================================================

    def criar_secao(self, titulo, parent):
        label = ctk.CTkLabel(
            parent,
            text=titulo.upper(),
            font=("Segoe UI", 11, "bold"),
            text_color=self.cor_principal
        )
        label.pack(anchor="w", padx=self.pad_secao, pady=(10, 4))

    # =========================================================

    def criar_input(self, parent, texto, nome, valor_padrao, coluna):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=0, column=coluna, padx=4, sticky="ew")

        ctk.CTkLabel(
            frame,
            text=texto,
            font=("Segoe UI", 11, "bold"),
            text_color=self.cor_texto_suave
        ).pack(anchor="w", pady=(0, 3))

        entry = ctk.CTkEntry(
            frame,
            height=34,
            corner_radius=self.raio_input,
            border_width=1,
            border_color=self.cor_borda,
            fg_color=self.cor_input,
            text_color=self.cor_texto,
            font=("Segoe UI", 11)
        )
        entry.pack(fill="x")
        entry.insert(0, valor_padrao)
        entry.bind("<KeyRelease>", lambda e: self.salvar_config())

        setattr(self, f"entry_{nome}", entry)

    # =========================================================

    def criar_input_full(self, texto):
        ctk.CTkLabel(
            self.container,
            text=texto,
            font=("Segoe UI", 11, "bold"),
            text_color=self.cor_texto_suave
        ).pack(anchor="w", padx=self.pad_secao, pady=(8, 3))

        self.entry_path = ctk.CTkEntry(
            self.container,
            height=34,
            corner_radius=self.raio_input,
            border_width=1,
            border_color=self.cor_borda,
            fg_color=self.cor_input,
            text_color=self.cor_texto,
            font=("Segoe UI", 11)
        )
        self.entry_path.pack(fill="x", padx=self.pad_secao)
        self.entry_path.insert(
            0,
            DEFAULT_BROWSER_PATH
        )
        self.entry_path.bind("<KeyRelease>", lambda e: self.salvar_config())

    # =========================================================

    def atualizar_niveis(self):
        niveis_anteriores = [var.get() for var in self.niveis_vars]

        for widget in self.frame_niveis.winfo_children():
            widget.destroy()

        self.niveis_vars.clear()

        try:
            total = int(self.entry_navegadores.get())
        except Exception:
            total = 1

        for i in range(total):
            frame = ctk.CTkFrame(
                self.frame_niveis,
                fg_color=self.cor_card_claro,
                corner_radius=self.raio_painel,
                height=42,
                border_width=1,
                border_color=self.cor_borda
            )
            frame.pack(fill="x", pady=4)

            label = ctk.CTkLabel(
                frame,
                text=f"Navegador {i + 1}",
                font=("Segoe UI", 11, "bold"),
                text_color=self.cor_texto
            )
            label.pack(side="left", padx=12, pady=8)

            valor = "1"
            if i < len(niveis_anteriores):
                valor = niveis_anteriores[i]

            var = ctk.StringVar(value=valor)

            combo = ctk.CTkComboBox(
                frame,
                values=["1", "2"],
                variable=var,
                width=90,
                height=30,
                corner_radius=self.raio_input,
                border_width=1,
                border_color=self.cor_borda,
                fg_color=self.cor_input,
                button_color=self.cor_secundaria,
                button_hover_color=self.hover_secundaria,
                dropdown_fg_color=self.cor_card_claro,
                dropdown_hover_color=self.cor_borda,
                font=("Segoe UI", 11),
                command=lambda valor: self.salvar_config()
            )
            combo.pack(side="right", padx=8, pady=5)
            self.niveis_vars.append(var)

        self.salvar_config()

    # =========================================================

    def checkbox_evento(self):
        self.atualizar_botoes()
        self.salvar_config()

    # =========================================================

    def alternar_tema_visual(self):
        processo_ativo = self.processo and self.processo.poll() is None
        android_ativo = self.android_thread and self.android_thread.is_alive()

        if processo_ativo or android_ativo:
            self.log("[SISTEMA] Pare a automação antes de trocar o tema.")
            return

        novo_tema = "classico" if self.tema_visual == "editor" else "editor"

        try:
            self.salvar_config()
            config = carregar_config()
            config["tema_visual"] = novo_tema
            salvar_config(config)
        except Exception:
            pass

        for widget in self.winfo_children():
            widget.destroy()

        self.niveis_vars.clear()
        self.android_navegador_vars.clear()
        self.aplicar_tema_visual(novo_tema)
        self.geometry(self.janela_tamanho)
        self.minsize(*self.janela_minima)
        self.centralizar_janela(*self.janela_dimensoes)
        self.criar_topo()
        self.criar_conteudo()
        self.carregar_config()
        self.atualizar_niveis()
        self.atualizar_botoes()
        tema_exibicao = "clássico" if novo_tema == "classico" else "editor"
        self.log(f"[SISTEMA] Tema visual alterado para {tema_exibicao}.")

    # =========================================================

    def obter_modo_pesquisa_pc(self):
        valor = self.pc_modo_pesquisa.get().strip().lower()

        if valor.startswith("simult"):
            return "simultaneo"

        return "sequencial"

    # =========================================================

    def log(self, texto):
        if "META DE PONTOS ATINGIDA" in texto:
            self.terminal.insert(END, f"{texto}\n", "verde")
        else:
            self.terminal.insert(END, f"{texto}\n")

        self.terminal.tag_config("verde", foreground=self.cor_sucesso)
        self.terminal.see("end")

    # =========================================================

    def atualizar_botoes(self):
        if self.auto_inicio.get():
            self.btn_iniciar.grid_remove()
            self.btn_parar.grid(
                row=1,
                column=0,
                columnspan=2,
                padx=4,
                pady=4,
                sticky="ew"
            )
        else:
            self.btn_parar.grid(row=1, column=1, padx=4, pady=4, sticky="ew")
            self.btn_iniciar.grid(row=1, column=0, padx=4, pady=4, sticky="ew")

    # =========================================================

    def carregar_config(self):
        try:
            config = carregar_config()

            self.entry_navegadores.delete(0, "end")
            self.entry_navegadores.insert(0, config.get("navegadores", 4))

            self.entry_login.delete(0, "end")
            self.entry_login.insert(0, config.get("tempo_login", 5))

            self.entry_path.delete(0, "end")
            self.entry_path.insert(0, config.get("browser_path", DEFAULT_BROWSER_PATH))

            self.auto_inicio.set(config.get("auto_inicio", False))
            modo_pc = config.get("pc_modo_pesquisa", "sequencial")
            self.pc_modo_pesquisa.set(
                "Simultânea"
                if str(modo_pc).lower().startswith("simult")
                else "Sequencial"
            )

            self.entry_android_adb.delete(0, "end")
            self.entry_android_adb.insert(0, config.get("android_adb_path", "adb"))

            self.entry_android_serial.delete(0, "end")
            self.entry_android_serial.insert(0, config.get("android_serial", ""))

            self.combo_android_buscador.set(config.get("android_buscador", "Google"))

            navegadores_android = config.get("android_navegadores", [])

            if isinstance(navegadores_android, str):
                navegadores_android = [navegadores_android]

            navegador_antigo = config.get("android_navegador", "")

            if (
                not navegadores_android
                and navegador_antigo
                and navegador_antigo != "Padrao do Android"
            ):
                navegadores_android = [navegador_antigo]

            for nome, var in self.android_navegador_vars.items():
                var.set(nome in navegadores_android)

            self.entry_android_quantidade.delete(0, "end")
            self.entry_android_quantidade.insert(
                0,
                config.get("android_quantidade", 10)
            )

            self.entry_android_delay.delete(0, "end")
            self.entry_android_delay.insert(0, config.get("android_delay", 6))

            self.entry_android_tempo_abrir.delete(0, "end")
            self.entry_android_tempo_abrir.insert(
                0,
                config.get("android_tempo_abrir", 1.2)
            )

            self.texto_android_pesquisas.delete("1.0", "end")
            self.texto_android_pesquisas.insert(
                "end",
                config.get("android_pesquisas", "")
            )

            self.atualizar_niveis()

            niveis = config.get("niveis", [])
            for i, nivel in enumerate(niveis):
                if i < len(self.niveis_vars):
                    self.niveis_vars[i].set(str(nivel))

            self.log("[CONFIG] Configurações carregadas.")

        except Exception as e:
            self.log(f"[ERRO] {e}")

    # =========================================================

    def salvar_config(self):
        try:
            config = {
                "navegadores": int(self.entry_navegadores.get()),
                "tempo_login": int(self.entry_login.get()),
                "browser_path": self.entry_path.get(),
                "auto_inicio": self.auto_inicio.get(),
                "tema_visual": self.tema_visual,
                "pc_modo_pesquisa": self.obter_modo_pesquisa_pc(),
                "niveis": [var.get() for var in self.niveis_vars],
                "android_adb_path": self.entry_android_adb.get(),
                "android_serial": self.entry_android_serial.get(),
                "android_buscador": self.combo_android_buscador.get(),
                "android_navegadores": self.obter_navegadores_android_marcados(),
                "android_quantidade": int(self.entry_android_quantidade.get()),
                "android_delay": float(
                    self.entry_android_delay.get().replace(",", ".")
                ),
                "android_tempo_abrir": float(
                    self.entry_android_tempo_abrir.get().replace(",", ".")
                ),
                "android_pesquisas": self.texto_android_pesquisas.get(
                    "1.0",
                    "end"
                ).strip()
            }

            salvar_config(config)

        except Exception:
            pass

    # =========================================================

    def iniciar(self):
        self.status.configure(text="EXECUTANDO", text_color=self.cor_sucesso)
        self.btn_abrir.configure(state="disabled")
        self.log("[SISTEMA] Abrindo navegadores...")

        def rodar():
            try:
                self.salvar_config()

                self.processo = subprocess.Popen(
                    [
                        sys.executable,
                        "main.py"
                    ],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    env={**os.environ, "PYTHONIOENCODING": "utf-8"}
                )

                if self.auto_inicio.get():
                    self.processo.stdin.write("\n")
                    self.processo.stdin.flush()

                while True:
                    linha = self.processo.stdout.readline()

                    if not linha:
                        break

                    linha = linha.strip()
                    if linha:
                        self.after(0, lambda l=linha: self.log(l))

            except Exception as e:
                self.after(0, lambda: self.log(f"[ERRO] {e}"))

            finally:
                self.after(0, self.finalizar_execucao)

        threading.Thread(target=rodar, daemon=True).start()

    # =========================================================

    def finalizar_execucao(self):
        self.status.configure(text="FINALIZADO", text_color=self.cor_info)
        self.btn_abrir.configure(state="normal")

    # =========================================================

    def enviar_enter(self):
        if self.processo:
            try:
                self.processo.stdin.write("\n")
                self.processo.stdin.flush()
                self.log("[SISTEMA] Sinal de início enviado.")

            except Exception:
                self.log("[ERRO] Não foi possível enviar comando.")

    # =========================================================

    def parar(self):
        if self.processo:
            try:
                self.processo.terminate()
                self.log("[SISTEMA] Processo parado pelo usuário.")

            except Exception:
                pass

            self.status.configure(text="PARADO", text_color=self.cor_erro)
            self.btn_abrir.configure(state="normal")

    # =========================================================

    def destroy(self):
        self.android_stop_event.set()
        super().destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
