from langchain_text_splitters  import RecursiveCharacterTextSplitter 

def split_documents(documents):
    parent_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 2000 , chunk_overlap =200
    )
    child_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500 , chunk_overlap = 100
    )

    parents = parent_splitter.split_documents(documents)

    children = []
    for parent in parents:
        child_chunks = child_splitter.split_documents([parent])
        


        for child in child_chunks:
            child.metadata['parent_content'] = parent.page_content

        children.extend(child_chunks)


    return parents ,children




