<p align="center">
  <img src="auto_pesquisa_bing.png" alt="Descrição" width="300">
</p>   

# 🚀 Auto Pesquisa Bing

Automação de pesquisas no Bing utilizando Python + Playwright com interface moderna em CustomTkinter.

---

## ✨ Funcionalidades

- 🌐 Abertura automática de múltiplos navegadores
- 🎯 Sistema de níveis por navegador
- ⚡ Pesquisas automáticas no Bing
- 💾 Salvamento automático das configurações
- 🖥️ Interface moderna e compacta
- 📊 Console integrado em tempo real
- 🔄 Suporte a auto início
- 👤 Perfis separados para cada navegador
- 🎲 Pesquisas aleatórias humanizadas
- 🛑 Controle de iniciar/parar processos
- 📱 Modo celular assistido com página local, QR Code e contador de 60 pontos
- 🤖 Automação Android via ADB para pesquisas comuns no navegador do celular

---

# 🖼️ Interface

## Tela Principal

- Configuração rápida
- Seleção de níveis
- Controle de navegadores
- Console em tempo real

---

# 📦 Tecnologias Utilizadas

- Python 3
- Playwright
- CustomTkinter
- qrcode
- ADB/Android Platform Tools para automação Android

---

# ⚙️ Instalação

## 1️⃣ Clone o repositório

```bash
git clone https://github.com/tomaziu/auto-pesquisa-bing.git
```

---

## 2️⃣ Entre na pasta

```bash
cd auto-pesquisa-bing
```

---

## 3️⃣ Instale as dependências

```bash
python -m pip install -r requirements.txt
```

---

# ▶️ Como usar

Execute:

```bash
python app.py
```

Tambem e possivel iniciar pelo arquivo `.bat`:

```bat
iniciar_app.bat
```

No Windows, basta dar dois cliques no arquivo `iniciar_app.bat` dentro da pasta do projeto.

---

# 🧠 Sistema de Níveis

| Nível | Meta de pontos |
|------|----------------|
| 1 | 30 pontos |
| 2 | 90 pontos |

Cada navegador pode possuir um nível diferente. Ao atingir a meta, o programa avisa no console e continua pesquisando.

---

# 📱 Modo Celular Assistido

| Meta | Pontos por pesquisa | Total |
|------|---------------------|-------|
| 60 pontos | 3 pontos | 20 pesquisas |

A aba Celular cria um pacote de 20 pesquisas e gera um QR Code para uma página local no celular. No celular, toque em **Abrir pesquisa** para abrir a busca no Bing e depois em **Marcar feita e próxima** para sincronizar o progresso com o app no PC.

O celular e o PC precisam estar na mesma rede. Se o Windows pedir acesso do firewall para o Python, permita na rede privada.

---

# 🤖 Automação Android

A aba Android usa ADB para abrir o navegador do celular, tocar no campo de pesquisa, digitar o termo e pressionar Enter.

Para usar:

1. Instale o Android Platform Tools.
2. Ative as Opções do desenvolvedor no Android.
3. Ative Depuração USB.
4. Conecte o celular no PC e aceite a autorização RSA na tela do celular.
5. Na aba Android, clique em **Verificar ADB**.
6. Gere ou cole uma lista de pesquisas.
7. Escolha o buscador (Google, Bing, DuckDuckGo, Yahoo ou Startpage), navegador, delay e tempo de abertura.
8. Clique em **Iniciar**.

Para alternar entre contas/navegadores no Android, marque os navegadores na seção **Alternar Navegadores**. Se nenhum navegador estiver marcado, o app usa apenas o navegador escolhido no campo **Navegador**. Quando houver vários marcados, cada pesquisa será executada em todos eles, um por vez.

## Contas separadas por navegador

Para usar contas diferentes no mesmo celular:

1. Instale os navegadores que pretende usar, como Chrome, Edge, Brave e Firefox.
2. Abra cada navegador manualmente no celular uma vez.
3. Faça login na conta desejada em cada navegador.
4. Aceite telas iniciais, permissões ou termos que aparecerem.
5. No app, marque esses navegadores em **Alternar Navegadores**.
6. Clique em **Iniciar**.

O Android é controlado por ADB, então apenas um navegador fica em primeiro plano por vez. Por isso o app alterna automaticamente entre os navegadores marcados em vez de tentar executar todos ao mesmo tempo.

Se o comando `adb` não estiver no PATH, coloque o caminho completo do `adb.exe` no campo ADB.

---

# 🔒 Observações

- O projeto utiliza perfis persistentes do navegador
- Pode armazenar sessões e cookies localmente
- Utilize com responsabilidade

---

# 📌 Requisitos

- Windows 10/11
- Python 3.10+
- Qualquer navegador compatível com Chromium

---

# 👨‍💻 Autor

Projeto desenvolvido por Thomaz de Morais Nunes.

---

# ⭐ Contribuição

Sinta-se livre para abrir:

- Issues
- Pull Requests
- Sugestões
- Melhorias

---

# 📄 Licença

Este projeto é apenas para fins educacionais.
