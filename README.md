# Bing Search Automation Python

Aplicativo em Python para automatizar pesquisas no Bing pelo PC e executar pesquisas comuns em navegadores Android via ADB.

## Recursos

- Interface desktop com CustomTkinter.
- Automação PC com Playwright.
- Perfis separados por navegador no PC.
- Modo sequencial ou simultâneo para pesquisas no PC.
- Automação Android via ADB.
- Alternância entre navegadores Android marcados.
- Salvamento automático das configurações.
- Alternância entre tema clássico e tema editor.

## Requisitos

- Windows 10/11.
- Python 3.10 ou superior.
- Microsoft Edge ou outro navegador Chromium instalado.
- Android Platform Tools para usar a aba Android.
- Um celular Android com Depuração USB ativada, caso use ADB.

## Instalação

Clone o repositório:

```bash
git clone https://github.com/tomaziu/bing-search-automation-python.git
cd bing-search-automation-python
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

Se necessário, instale os navegadores do Playwright:

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

## Testes

Execute a validação de sintaxe:

```bash
python -B -m py_compile app.py main.py rewards_runner.py browser_manager.py config_manager.py android_automation.py search_generator.py logger.py
```

Execute os testes automatizados:

```bash
python -m unittest discover -s tests
```

## Aba PC

1. Informe a quantidade de navegadores.
2. Escolha o tempo de espera inicial.
3. Confirme o caminho do navegador.
4. Escolha o nível de cada navegador.
5. Escolha o modo de pesquisa:
   - Sequencial: pesquisa navegador por navegador.
   - Simultânea: executa uma rodada de pesquisa em todos os navegadores ao mesmo tempo.
6. Clique em Abrir navegadores.
7. Clique em Iniciar, ou marque Iniciar automaticamente.

## Aba Android

A aba Android usa ADB para abrir o navegador no celular, tocar no campo de pesquisa, digitar o termo e pressionar Enter.

Passos básicos:

1. Instale o Android Platform Tools no PC.
2. Ative as Opções do desenvolvedor no Android.
3. Ative Depuração USB.
4. Conecte o celular no PC e aceite a autorização RSA.
5. No app, informe o caminho do `adb.exe`.
6. Clique em Verificar ADB.
7. Escolha o buscador.
8. Marque pelo menos um navegador em Alternar Navegadores.
9. Gere ou cole a lista de pesquisas.
10. Clique em Iniciar.

Para conexão ADB sem fio ou pareamento local, uma opção recomendada é o LADB Connect. Ele pode ajudar na configuração do ADB no Android, especialmente quando você estiver usando Depuração sem fio.

Se o comando `adb` não estiver no PATH, use o caminho completo, por exemplo:

```text
C:\Users\Admin\platform-tools\adb.exe
```

Teste rápido do ADB:

```bash
adb devices
```

O dispositivo deve aparecer como `device`.

## Contas por navegador no Android

Para usar contas diferentes no mesmo celular:

1. Instale os navegadores que pretende usar, como Chrome, Edge, Brave, Firefox ou Bing.
2. Abra cada navegador manualmente uma vez.
3. Faça login na conta desejada em cada navegador.
4. Aceite telas iniciais, permissões e termos.
5. Marque os navegadores no app em Alternar Navegadores.

O Android é controlado por ADB, então apenas um navegador fica em primeiro plano por vez. Por isso o app alterna entre os navegadores marcados.

## Observações

- O projeto usa perfis persistentes do navegador.
- Sessões e cookies podem ficar salvos localmente.
- Use com responsabilidade.

## Contribuição

Leia o arquivo `CONTRIBUTING.md` antes de enviar mudanças.

## Changelog

As mudanças relevantes ficam registradas em `CHANGELOG.md`.

## Licença

Este projeto está licenciado sob a licença MIT. Veja `LICENSE`.
