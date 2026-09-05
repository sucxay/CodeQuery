from fastapi import FastAPI

from schemas import requestURL , askQuestion
from github import clone_repo
from loader import load_repository
from vectorstore import create_vector_store
from llm import llm


app = FastAPI()


# Current repository's vector store
vector_store = None


# Current repository name
current_repo = None


@app.get("/")
def home():
    return {
        "message": "GitHub RAG API is running"
    }


@app.post("/index")
def index_repository(request: requestURL):

    global vector_store
    global current_repo

    # Clone repository
    repo_path = clone_repo(request.github_url)

    # Get repository name
    current_repo = request.github_url.rstrip("/").split("/")[-1]
    current_repo = current_repo.replace(".git", "")

    # Load files
    documents = load_repository(repo_path)

    # Create Qdrant collection for this repository
    vector_store = create_vector_store(current_repo)

    # Index documents
    vector_store.add_documents(documents)

    return {
        "message": "Repository indexed successfully",
        "repository": current_repo,
        "files_loaded": len(documents)
    }


@app.post("/ask")
def ask_question(request: askQuestion):

    global vector_store

    # Make sure a repository has been indexed
    if vector_store is None:

        return {
            "answer": "Please index a repository first."
        }

    # Search ONLY the currently indexed repository
    documents = vector_store.similarity_search(
        request.question,
        k=5
    )

    print("\n==============================")
    print("QUESTION:", request.question)
    print("REPOSITORY:", current_repo)
    print("RETRIEVED:", len(documents))

    for document in documents:
        print(
            "FILE:",
            document.metadata.get("file_path")
        )

    print("==============================\n")

    # Create context
    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    if not context:

        return {
            "answer": "I couldn't find relevant information in this repository."
        }

    # Prompt
    prompt = f"""
You are a code assistant.

Answer the user's question using ONLY the repository
code provided below.

Do not use outside knowledge.

If the answer cannot be found in the provided code,
say:

"I couldn't find this in the repository."

Repository code:

{context}

User question:

{request.question}
"""

    # Mistral
    response = llm.invoke(prompt)

    return {
        "repository": current_repo,
        "answer": response.content
    }