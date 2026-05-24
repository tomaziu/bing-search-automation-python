# Contribuindo

Obrigado por considerar contribuir com este projeto.

## Como preparar o ambiente

1. Faça um fork ou clone do repositório.
2. Crie um ambiente Python 3.10 ou superior.
3. Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

4. Se for testar a automação PC, instale os navegadores do Playwright:

```bash
python -m playwright install
```

## Antes de enviar mudanças

Execute as verificações básicas:

```bash
python -B -m py_compile app.py main.py rewards_runner.py browser_manager.py config_manager.py android_automation.py search_generator.py logger.py
python -m unittest discover -s tests
```

## Boas práticas

- Mantenha as alterações pequenas e focadas.
- Evite mudar comportamento fora do escopo da contribuição.
- Atualize o README ou CHANGELOG quando a mudança afetar o uso do app.
- Não inclua arquivos locais de configuração, perfis de navegador ou dados pessoais.

## Pull requests

Ao abrir um pull request, descreva:

- O que mudou.
- Por que a mudança foi feita.
- Como foi testada.
