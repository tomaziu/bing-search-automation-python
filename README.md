# Bing Search Automation Python

Aplicativo em Python para automatizar pesquisas no Bing pelo PC e executar pesquisas comuns em navegadores Android via ADB.

## Recursos

- Interface desktop com CustomTkinter.
- Automacao PC com Playwright.
- Perfis separados por navegador no PC.
- Modo sequencial ou simultaneo para pesquisas no PC.
- Automacao Android via ADB.
- Alternancia entre navegadores Android marcados.
- Salvamento automatico das configuracoes.
- Alternancia entre tema classico e tema editor.

## Requisitos

- Windows 10/11.
- Python 3.10 ou superior.
- Microsoft Edge ou outro navegador Chromium instalado.
- Android Platform Tools para usar a aba Android.
- Um celular Android com Depuracao USB ativada, caso use ADB.

## Instalacao

Clone o repositorio:

```bash
git clone https://github.com/tomaziu/bing-search-automation-python.git
cd bing-search-automation-python
```

Instale as dependencias:

```bash
python -m pip install -r requirements.txt
```

Se necessario, instale os navegadores do Playwright:

```bash
python -m playwright install
```

## Como executar

Pelo terminal:

```bash
python app.py
```

Ou pelo Windows:

```bat
iniciar_app.bat
```

## Aba PC

1. Informe a quantidade de navegadores.
2. Escolha o tempo de espera inicial.
3. Confirme o caminho do navegador.
4. Escolha o nivel de cada navegador.
5. Escolha o modo de pesquisa:
   - Sequencial: pesquisa navegador por navegador.
   - Simultanea: executa uma rodada de pesquisa em todos os navegadores ao mesmo tempo.
6. Clique em Abrir navegadores.
7. Clique em Iniciar, ou marque Iniciar automaticamente.

## Aba Android

A aba Android usa ADB para abrir o navegador no celular, tocar no campo de pesquisa, digitar o termo e pressionar Enter.

Passos basicos:

1. Instale o Android Platform Tools no PC.
2. Ative as Opcoes do desenvolvedor no Android.
3. Ative Depuracao USB.
4. Conecte o celular no PC e aceite a autorizacao RSA.
5. No app, informe o caminho do `adb.exe`.
6. Clique em Verificar ADB.
7. Escolha o buscador.
8. Marque pelo menos um navegador em Alternar Navegadores.
9. Gere ou cole a lista de pesquisas.
10. Clique em Iniciar.

Para conexao ADB sem fio ou pareamento local, uma opcao recomendada e o LADB Connect. Ele pode ajudar na configuracao do ADB no Android, especialmente quando voce estiver usando Depuracao sem fio.

Se o comando `adb` nao estiver no PATH, use o caminho completo, por exemplo:

```text
C:\Users\Admin\platform-tools\adb.exe
```

Teste rapido do ADB:

```bash
adb devices
```

O dispositivo deve aparecer como `device`.

## Contas por navegador no Android

Para usar contas diferentes no mesmo celular:

1. Instale os navegadores que pretende usar, como Chrome, Edge, Brave, Firefox ou Bing.
2. Abra cada navegador manualmente uma vez.
3. Faca login na conta desejada em cada navegador.
4. Aceite telas iniciais, permissoes e termos.
5. Marque os navegadores no app em Alternar Navegadores.

O Android e controlado por ADB, entao apenas um navegador fica em primeiro plano por vez. Por isso o app alterna entre os navegadores marcados.

## Observacoes

- O projeto usa perfis persistentes do navegador.
- Sessoes e cookies podem ficar salvos localmente.
- Use com responsabilidade.
