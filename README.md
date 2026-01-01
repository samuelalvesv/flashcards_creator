# Flashcards Creator Backend

Backend em FastAPI para automatizar a criação de flashcards Anki a partir de vídeos do YouTube. O sistema baixa o vídeo, divide em segmentos, interage com o serviço VideoAnki e limpa automaticamente os arquivos temporários após o processamento.

## Pré-requisitos

- **Python 3.10+** instalado.
- **Python 3.10+** instalado.
- **FFmpeg** (Opcional, mas recomendado): O projeto foi ajustado para funcionar sem ele, mas ter o FFmpeg permite melhor qualidade de download em alguns casos.
    - Mac: `brew install ffmpeg`
    - Linux: `sudo apt install ffmpeg`

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

**Exemplo de requisição:**
```bash
curl -X POST "http://localhost:8000/api/generate-deck" \
     -H "Content-Type: application/json" \
     -d '{"youtube_url": "https://youtu.be/SEU_VIDEO_AQUI"}'
```

**Resposta:**
O endpoint retorna um JSON com a URL de download. O arquivo **não** é baixado diretamente nesta chamada.
```json
{
  "download_url": "/api/download/deck_NOME_DO_VIDEO.zip",
  "deck_count": 5,
  "zip_filename": "deck_NOME_DO_VIDEO.zip"
}
```

### Baixar Arquivo
**Endpoint**: `GET /api/download/{filename}`
Use a URL retornada no passo anterior para baixar o arquivo ZIP final.

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
