from langchain_huggingface import HuggingFaceEmbeddings 

embeddings = HuggingFaceEmbeddings(
    model_name = "BAAI/bge-small-en-v1.5",
    encode_kwargs ={
        'normalize_embeddings':True
    }
)






