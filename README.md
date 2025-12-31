# Flashcards Creator Backend

Backend em FastAPI para automatizar a criação de flashcards Anki a partir de vídeos do YouTube. O sistema baixa o vídeo, divide em segmentos e interage com o serviço VideoAnki.

## Pré-requisitos

- **Python 3.10+** instalado.
- **FFmpeg** instalado e acessível no PATH do sistema.
    - Mac: `brew install ffmpeg`
    - Linux: `sudo apt install ffmpeg`
    - Windows: Baixar do site oficial e adicionar ao PATH.

## Instalação e Configuração

### 1. Clonar o repositório
```bash
git clone https://github.com/samuelalvesv/flashcards_creator
cd flashcards_creator
```

### 2. Criar Ambiente Virtual (venv)
Recomendamos usar um ambiente virtual para isolar as dependências.

```bash
# Criar o ambiente (pasta .venv)
python3 -m venv .venv

# Ativar o ambiente
# No Mac/Linux:
source .venv/bin/activate
# No Windows:
# .venv\Scripts\activate
```

### 3. Instalar Dependências
Com o ambiente ativado, instale as dependências do projeto em modo editável:

```bash
pip install -e .
```
Isso instalará todas as libs listadas no `pyproject.toml` (FastAPI, yt-dlp, httpx, etc).

### 4. Configurar Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto baseado no exemplo (ou use os valores padrão hardcoded para dev):

```bash
cp .env.example .env
# Edite o .env se necessário com seus tokens do VideoAnki
```

## Executando o Projeto

Para rodar o servidor de desenvolvimento:

```bash
uvicorn app.main:app --reload
```
O servidor estará rodando em `http://localhost:8000`.

## Documentação Interativa (Swagger UI)

Acesse `http://localhost:8000/docs` para ver a documentação interativa da API, onde você pode testar os endpoints diretamente pelo navegador.

## Uso da API

### Gerar Deck
**Endpoint**: `POST /api/generate-deck`

**Exemplo de requisição (cURL):**
```bash
curl -X POST "http://localhost:8000/api/generate-deck" \
     -H "Content-Type: application/json" \
     -d '{"youtube_url": "https://youtu.be/SEU_VIDEO_AQUI"}' \
     --output deck_final.zip
```

## Desenvolvimento

### Reinstalar do zero
Caso precise limpar o ambiente e reinstalar tudo:

```bash
# Desativar venv atual
deactivate

# Remover pasta do venv
rm -rf .venv

# Recomeçar do passo 2 acima
```

### Rodar Verificações (Linting)
O projeto usa `ruff` e `pyright`. Para rodar a verificação de código:

```bash
# Lint e formatação
ruff check .

# Checagem de tipos
pyright .
```
