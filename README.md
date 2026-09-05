# Code RAG

Code RAG is a repository question-answering API. It clones a public GitHub repository, indexes supported source files in Qdrant, retrieves the most relevant code for a question, and uses a Groq-hosted language model to generate an answer grounded in that repository.

The project currently exposes an API-first backend. The `frontend/` directory is reserved for the future web client.

## Features

- Clone a GitHub repository for indexing
- Read common source-code, markup, stylesheet, and Markdown files
- Generate normalized embeddings with `BAAI/bge-small-en-v1.5`
- Store vectors in a repository-specific Qdrant collection
- Retrieve the five most relevant documents for a question
- Generate answers using repository context only
- Expose interactive OpenAPI documentation through FastAPI

## Architecture

The active request flow is:

```text
GitHub URL
		-> clone repository
		-> load supported files
		-> create or open Qdrant collection
		-> embed and index documents

Question
		-> similarity search
		-> build repository-only prompt
		-> Groq LLM
		-> answer
```

| Path | Responsibility |
| --- | --- |
| `backend/main.py` | FastAPI application and active `/index` and `/ask` workflow |
| `backend/github.py` | Clone repositories with GitPython |
| `backend/loader.py` | Load supported files into LangChain documents |
| `backend/embeddings.py` | Configure the Hugging Face embedding model |
| `backend/vectorstore.py` | Create and connect to Qdrant collections |
| `backend/llm.py` | Configure the Groq chat model |
| `backend/schemas.py` | Request models for the API |
| `backend/splitter.py` | Character-splitting helper for planned chunking |
| `backend/retriever.py` and `backend/rag.py` | Planned retrieval and RAG helpers; not used by the current API |
| `frontend/` | Reserved for the future frontend application |

## Requirements

- Python 3.10 or newer
- A reachable Qdrant instance
- A Groq API key
- Git, for cloning repositories

## Setup

Clone the project and create a virtual environment:

```bash
git clone <repository-url>
cd code-rag

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
QDRANT_URL=https://your-qdrant-endpoint
QDRANT_API_KEY=your-qdrant-api-key
GROQ_API_KEY=your-groq-api-key
```

The embedding model is downloaded from Hugging Face when the application initializes. The first startup can therefore take longer and requires network access.

## Run the API

Start the server from `backend/` because the current modules use local top-level imports:

```bash
cd backend
uvicorn main:app 
```

The API is available at `http://127.0.0.1:8000`.

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## API Usage

Check that the service is running:

```bash
curl http://127.0.0.1:8000/
```

Index a repository:

```bash
curl -X POST http://127.0.0.1:8000/index \
	-H "Content-Type: application/json" \
	-d '{"github_url":"https://github.com/owner/repository"}'
```

Example response:

```json
{
	"message": "Repository indexed successfully",
	"repository": "repository",
	"files_loaded": 42
}
```

Ask a question about the currently indexed repository:

```bash
curl -X POST http://127.0.0.1:8000/ask \
	-H "Content-Type: application/json" \
	-d '{"question":"How is authentication implemented?"}'
```

Index a repository before calling `/ask`. The server keeps the active vector store and repository name in process memory.

## Supported Files

The loader currently indexes files with these extensions:

`.py`, `.js`, `.jsx`, `.ts`, `.tsx`, `.java`, `.c`, `.cpp`, `.h`, `.hpp`, `.go`, `.rs`, `.php`, `.rb`, `.html`, `.css`, and `.md`.

It skips `.git`, `node_modules`, Python caches, and virtual-environment directories.

## Development Notes

- Indexing is synchronous and may take time while cloning, loading, embedding, and uploading documents.
- A Qdrant collection is created per repository using the `github_<repository-name>` naming convention.
- Re-indexing the same repository may append duplicate vectors to its existing collection.
- The current indexing path loads complete files; `splitter.py` is not yet used by `main.py`.
- Only one repository is active per server process. Restarting the API clears the in-memory active repository reference, although Qdrant collections remain available.
- Runtime data, local environments, credentials, caches, and vector database files are excluded by `.gitignore`.

## Current Limitations

- There is no authentication, authorization, rate limiting, or repository-size limit.
- The API currently expects public GitHub repositories that Git can clone without additional credentials.
- Repository URL validation and clone safety policies still need to be added.
- The helper modules `retriever.py`, `rag.py`, and the manual `backend/test.py` script are incomplete and are not part of the active API path.
- No automated test suite or frontend application is currently included.

## License

No license has been specified yet.
