import os 
from dotenv import load_dotenv 
from qdrant_client import QdrantClient ,models 

from langchain_qdrant import QdrantVectorStore 
from embeddings import embeddings 
from splitter import create_parent_child_splitter

from langchain_classic.retrievers import ParentDocumentRetriever
from langchain_core.stores import InMemoryStore

load_dotenv()

def create_retriever():

    client =QdrantClient(
        url =os.getenv("QDRANT_URL") , 
        api_key  = os.getenv("QDRANT_API_KEY")
    )
    if not client.collection_exists('github_code'):
        client .create_collection(
            collection_name = "github_code" ,
            vectors_config = models.VectorParams(
                size = 384 , distance = models.Distance.COSINE
            )
        )



    vector_store =QdrantVectorStore(
        client=client ,collection_name="github_code",
        embedding =embeddings
    )

    parent_splitter , child_splitter =create_parent_child_splitter()


    store = InMemoryStore()


    retriever = ParentDocumentRetriever(
        vectorstore=vector_store,
        docstore=store,
        child_splitter=child_splitter,
        parent_splitter=parent_splitter
    )

    return retriever
