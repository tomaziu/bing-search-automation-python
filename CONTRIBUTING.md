# Contribuindo

Obrigado por considerar contribuir com este projeto.

## Como preparar o ambiente

1. Faca um fork ou clone do repositorio.
2. Crie um ambiente Python 3.10 ou superior.
3. Instale as dependencias:

```bash
python -m pip install -r requirements.txt
```

4. Se for testar a automacao PC, instale os navegadores do Playwright:

```bash
python -m playwright install
```

## Antes de enviar mudancas

Execute as verificacoes basicas:

```bash
python -B -m py_compile app.py main.py rewards_runner.py browser_manager.py config_manager.py android_automation.py search_generator.py logger.py
python -m unittest discover -s tests
```

## Boas praticas

- Mantenha as alteracoes pequenas e focadas.
- Evite mudar comportamento fora do escopo da contribuicao.
- Atualize o README ou CHANGELOG quando a mudanca afetar o uso do app.
- Nao inclua arquivos locais de configuracao, perfis de navegador ou dados pessoais.

## Pull requests

Ao abrir um pull request, descreva:

- O que mudou.
- Por que a mudanca foi feita.
- Como foi testada.
