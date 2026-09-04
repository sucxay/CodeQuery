from github import clone_repo
from loader import load_repository
from vectorstore import create_retriever


# 1. Clone repository
github_url = "https://github.com/sucxay/Summify"

repo_path = clone_repo(github_url)
print("Repository cloned:", repo_path)


# 2. Load repository files
documents = load_repository(repo_path)
print("Documents loaded:", len(documents))


# 3. Create retriever
retriever = create_retriever()


# 4. Index documents
retriever.add_documents(documents)

print("Repository indexed successfully!")


# 5. Ask a question
question = "How does the application generate summaries?"

documents = retriever.invoke(question)


# 6. Print retrieved code
print("\n========== RETRIEVED DOCUMENTS ==========")

for document in documents:
    print("\nFILE:", document.metadata.get("file_path"))
    print(document.page_content[:1000])
    print("----------------------------------------")