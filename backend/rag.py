from retriever import retrieve_code 
from llm import llm 

def ask_question(question:str):
    documents = retrieve_code(question)
    context = "\n\n".join(
        documents.page_content for document in documents


    )

    prompt = f"""
    You are a code assistant.

    Answer the user's question using only the provided repository code.

    If the answer cannot be found in the code, say:
    "I couldn't find this in the repository."

    Repository code:

    {context}

    Question:
    {question}
    """

    response = llm.invoke(prompt)

    return response.content