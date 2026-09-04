from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_parent_child_splitter():

    parent_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200
    )

    child_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    return parent_splitter, child_splitter