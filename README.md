# RPA Challenge Automation

Automação do [RPA Challenge](https://rpachallenge.com/) em Python com Playwright. Lê registros de uma planilha Excel, preenche o formulário round a round e gera screenshot do resultado.

## Requisitos

- Python 3.11+
- Navegador Chromium (via Playwright)

## Instalação

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

> No Ubuntu 26, se `playwright install` falhar, use um Chromium já instalado ou defina `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH` no `.env`.

## Configuração

Copie o exemplo e ajuste se necessário:

```bash
cp .env.example .env
```

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `EXCEL_FILE_PATH` | Planilha com os dados | `data/challenge.xlsx` |
| `CHALLENGE_URL` | URL do challenge | `https://rpachallenge.com/` |
| `HEADLESS` | Browser sem interface | `False` |
| `TIMEOUT` | Timeout Playwright (ms) | `15000` |

A planilha deve ter as colunas: `First Name`, `Last Name`, `Company Name`, `Role in Company`, `Address`, `Email`, `Phone Number`.

## Execução

```bash
python main.py
```

Fluxo:

1. Lê o Excel e monta o payload (`ChallengeInput`)
2. `RpaService` resolve o RPA no registry (`rpa-challenge`)
3. `ChallengeRunner` abre o site, clica em Start e processa cada linha como um round
4. Salva screenshot em `output/score.png`

## Estrutura do projeto

```
app/
├── browser/          # Playwright e gerenciamento do browser
├── core/             # config, logger, exceptions
├── domain/           # models e enums
├── rpa/
│   ├── base.py       # ciclo de vida do runner
│   ├── registry.py   # mapeia slug → input + runner
│   └── challenge/
│       ├── input.py  # dados de entrada (records do Excel)
│       ├── pages.py  # seletores e page object
│       └── runner.py # orquestração do challenge
└── services/
    ├── excel_service.py
    └── rpa_service.py
data/                 # planilha Excel
logs/                 # logs da execução
output/               # screenshot final
main.py               # ponto de entrada
```

## Logs

Os logs ficam em **`logs/app.log`** (criado automaticamente ao rodar `main.py`).

Também são exibidos no console. Formato:

```
2026-05-29 14:00:00 | INFO     | app.rpa.base | rpa.start operator=rpa_challenge
```

## Saída

| Artefato | Caminho |
|----------|---------|
| Log | `logs/app.log` |
| Screenshot | `output/score.png` |

## Uso programático

```python
from app.rpa.challenge.input import ChallengeInput
from app.services.rpa_service import RpaService

result = await RpaService.run("rpa-challenge", ChallengeInput.build_payload())
print(result.success, result.message)
```
