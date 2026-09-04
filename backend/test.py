from github import clone_repo
from loader import load_repository
from vectorstore import create_vector_store
from llm import llm


# 1. Clone repository
github_url = "https://github.com/sucxay/Summify"

repo_path = clone_repo(github_url)

print("Repository cloned:", repo_path)


# 2. Load repository
documents = load_repository(repo_path)

print("Documents loaded:", len(documents))


# 3. Create vector store
vector_store = create_vector_store()


# 4. Index repository
vector_store.add_documents(documents)

print("Repository indexed successfully!")


# 5. Ask question
question = "How does the application generate summaries?"

print("\nQuestion:", question)


# 6. Retrieve relevant code
results = vector_store.similarity_search(
    question,
    k=5
)

print("Retrieved:", len(results))


# 7. Build context
context = "\n\n".join(
    doc.page_content
    for doc in results
)


# 8. Create prompt
prompt = f"""
You are a code assistant.

Answer the question using ONLY the repository code below.

If the answer cannot be found in the code,
say that you couldn't find it.

Repository code:

{context}

Question:

{question}
"""


# 9. Ask Mistral
response = llm.invoke(prompt)


# 10. Print answer
print("\n==========================================")
print("FINAL ANSWER")
print("==========================================")

print(response.content)