from vectorstore import create_retriever 

def retrieve_code(question:str):
    retriver = create_retriever()

    documents= retriver.invoke(question)

    return documents
