import customtkinter as ctk
from tkinter import END
import subprocess
import sys
import threading
import ctypes
import ctypes.wintypes

from config_manager import DEFAULT_BROWSER_PATH, carregar_config, salvar_config


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Auto Pesquisa - Bing")
        self.geometry("540x640")
        self.minsize(500, 590)
        self.centralizar_janela(540, 640)

        self.cor_principal = "#38bdf8"
        self.cor_secundaria = "#10b981"
        self.cor_bg = "#0f172a"
        self.cor_card = "#111827"
        self.cor_card_claro = "#182235"
        self.cor_input = "#0b1220"
        self.cor_borda = "#263449"
        self.cor_texto = "#e5edf6"
        self.cor_texto_suave = "#94a3b8"

        self.configure(fg_color=self.cor_bg)

        self.attributes("-topmost", True)
        self.bind("<Unmap>", lambda e: self.attributes("-topmost", False))
        self.bind("<Map>", lambda e: self.attributes("-topmost", True))

        self.processo = None
        self.niveis_vars = []

        self.criar_topo()
        self.criar_conteudo()
        self.carregar_config()
        self.atualizar_niveis()
        self.atualizar_botoes()
        self.log("[SISTEMA] Interface carregada com sucesso.")

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
            height=82
        )
        self.topo.pack(fill="x")

        self.titulo = ctk.CTkLabel(
            self.topo,
            text="Auto Pesquisa Bing",
            font=("Segoe UI", 23, "bold"),
            text_color=self.cor_texto
        )
        self.titulo.pack(pady=(10, 0))

        self.subtitulo = ctk.CTkLabel(
            self.topo,
            text="Automacao de pesquisas com perfis separados",
            font=("Segoe UI", 11),
            text_color=self.cor_texto_suave
        )
        self.subtitulo.pack()

        ctk.CTkFrame(
            self.topo,
            fg_color=self.cor_secundaria,
            height=3
        ).pack(fill="x", padx=76, pady=(9, 0))

    # =========================================================

    def criar_conteudo(self):
        self.container = ctk.CTkScrollableFrame(
            self,
            fg_color=self.cor_card,
            corner_radius=16,
            border_width=1,
            border_color=self.cor_borda
        )
        self.container.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=(14, 10)
        )

        self.status_frame = ctk.CTkFrame(
            self.container,
            fg_color=self.cor_input,
            corner_radius=12,
            border_width=1,
            border_color=self.cor_borda
        )
        self.status_frame.pack(fill="x", padx=16, pady=(10, 8))

        self.status = ctk.CTkLabel(
            self.status_frame,
            text="PARADO",
            font=("Segoe UI", 13, "bold"),
            text_color="#fb7185"
        )
        self.status.pack(pady=8)

        self.criar_secao("Configuracoes", self.container)

        self.frame_inputs = ctk.CTkFrame(self.container, fg_color="transparent")
        self.frame_inputs.pack(fill="x", padx=16, pady=(0, 6))
        self.frame_inputs.grid_columnconfigure((0, 1), weight=1)

        self.criar_input(self.frame_inputs, "Navegadores", "navegadores", "4", 0)
        self.criar_input(self.frame_inputs, "Tempo (s)", "login", "5", 1)
        self.entry_navegadores.bind("<KeyRelease>", lambda e: self.atualizar_niveis())

        self.criar_input_full("Caminho do Navegador")

        self.criar_secao("Nivel de Cada Navegador", self.container)

        self.frame_niveis = ctk.CTkFrame(self.container, fg_color="transparent")
        self.frame_niveis.pack(fill="x", padx=16, pady=(0, 8))

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
            hover_color="#059669",
            border_color=self.cor_borda,
            command=self.checkbox_evento
        )
        self.checkbox_auto.pack(anchor="w", padx=20, pady=(4, 12))

        self.frame_botoes = ctk.CTkFrame(self.container, fg_color="transparent")
        self.frame_botoes.pack(fill="x", padx=16, pady=(2, 10))
        self.frame_botoes.grid_columnconfigure((0, 1), weight=1)

        self.btn_abrir = ctk.CTkButton(
            self.frame_botoes,
            text="Abrir navegadores",
            height=42,
            corner_radius=9,
            font=("Segoe UI", 12, "bold"),
            fg_color=self.cor_secundaria,
            hover_color="#059669",
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
            height=40,
            corner_radius=9,
            font=("Segoe UI", 12, "bold"),
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            command=self.enviar_enter
        )

        self.btn_parar = ctk.CTkButton(
            self.frame_botoes,
            text="Parar",
            height=40,
            corner_radius=9,
            font=("Segoe UI", 12, "bold"),
            fg_color="#e11d48",
            hover_color="#be123c",
            command=self.parar
        )

        self.btn_iniciar.grid(row=1, column=0, padx=4, pady=4, sticky="ew")
        self.btn_parar.grid(row=1, column=1, padx=4, pady=4, sticky="ew")

        self.criar_secao("Console", self.container)

        self.terminal = ctk.CTkTextbox(
            self.container,
            height=220,
            corner_radius=12,
            fg_color="#070d18",
            font=("Consolas", 11),
            text_color="#7dd3fc",
            border_width=1,
            border_color=self.cor_borda
        )
        self.terminal.pack(fill="both", expand=True, padx=16, pady=(4, 14))

    # =========================================================

    def criar_secao(self, titulo, parent):
        label = ctk.CTkLabel(
            parent,
            text=titulo.upper(),
            font=("Segoe UI", 11, "bold"),
            text_color=self.cor_principal
        )
        label.pack(anchor="w", padx=20, pady=(10, 4))

    # =========================================================

    def criar_input(self, parent, texto, nome, valor_padrao, coluna):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=0, column=coluna, padx=4, sticky="ew")

        ctk.CTkLabel(
            frame,
            text=texto,
            font=("Segoe UI", 11, "bold"),
            text_color=self.cor_texto
        ).pack(anchor="w", pady=(0, 3))

        entry = ctk.CTkEntry(
            frame,
            height=36,
            corner_radius=9,
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
            text_color=self.cor_texto
        ).pack(anchor="w", padx=20, pady=(8, 3))

        self.entry_path = ctk.CTkEntry(
            self.container,
            height=36,
            corner_radius=9,
            border_width=1,
            border_color=self.cor_borda,
            fg_color=self.cor_input,
            text_color=self.cor_texto,
            font=("Segoe UI", 11)
        )
        self.entry_path.pack(fill="x", padx=20)
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
                corner_radius=10,
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
                corner_radius=8,
                border_width=1,
                border_color=self.cor_borda,
                fg_color=self.cor_input,
                button_color=self.cor_secundaria,
                button_hover_color="#059669",
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

    def log(self, texto):
        if "META DE PONTOS ATINGIDA" in texto:
            self.terminal.insert(END, f"{texto}\n", "verde")
        else:
            self.terminal.insert(END, f"{texto}\n")

        self.terminal.tag_config("verde", foreground="#22c55e")
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
            self.atualizar_niveis()

            niveis = config.get("niveis", [])
            for i, nivel in enumerate(niveis):
                if i < len(self.niveis_vars):
                    self.niveis_vars[i].set(str(nivel))

            self.log("[CONFIG] Configuracoes carregadas.")

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
                "niveis": [var.get() for var in self.niveis_vars]
            }

            salvar_config(config)

        except Exception:
            pass

    # =========================================================

    def iniciar(self):
        self.status.configure(text="EXECUTANDO", text_color="#22c55e")
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
                    encoding="cp1252"
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
        self.status.configure(text="FINALIZADO", text_color="#60a5fa")
        self.btn_abrir.configure(state="normal")

    # =========================================================

    def enviar_enter(self):
        if self.processo:
            try:
                self.processo.stdin.write("\n")
                self.processo.stdin.flush()
                self.log("[SISTEMA] Sinal de inicio enviado.")

            except Exception:
                self.log("[ERRO] Nao foi possivel enviar comando.")

    # =========================================================

    def parar(self):
        if self.processo:
            try:
                self.processo.terminate()
                self.log("[SISTEMA] Processo parado pelo usuario.")

            except Exception:
                pass

            self.status.configure(text="PARADO", text_color="#fb7185")
            self.btn_abrir.configure(state="normal")


if __name__ == "__main__":
    app = App()
    app.mainloop()
