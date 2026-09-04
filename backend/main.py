from fastapi import FastAPI

from schemas import RepositoryRequest, QuestionRequest
from github import clone_repo
from loader import load_repository
from vectorstore import create_vector_store
from llm import llm


app = FastAPI()


# Create the vector store when the API starts
vector_store = create_vector_store()


@app.get("/")
def home():
    return {
        "message": "GitHub RAG API is running"
    }


@app.post("/index")
def index_repository(request: RepositoryRequest):

    # Clone GitHub repository
    repo_path = clone_repo(request.github_url)

    # Load repository files
    documents = load_repository(repo_path)

    # Store documents in Qdrant
    vector_store.add_documents(documents)

    return {
        "message": "Repository indexed successfully",
        "files_loaded": len(documents)
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):

    # Search Qdrant
    documents = vector_store.similarity_search(
        request.question,
        k=5
    )

    # Debug information
    print("\n==============================")
    print("QUESTION:", request.question)
    print("RETRIEVED DOCUMENTS:", len(documents))

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

    # Nothing retrieved
    if not context:
        return {
            "answer": "No documents retrieved from Qdrant."
        }

    # Prompt for Mistral
    prompt = f"""
You are a code assistant.

Answer the user's question using ONLY the repository
code provided below.

If the answer cannot be found in the repository,
say:

"I couldn't find this in the repository."

Repository code:

{context}

User question:

{request.question}
"""

    # Send to Mistral
    response = llm.invoke(prompt)

    # Return answer
    return {
        "answer": response.content
    }