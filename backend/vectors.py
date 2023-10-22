from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter

# Define a function to create a search section
def create_search_section(documents, collection_name, splitter_args, embeddings):
    text_splitter = CharacterTextSplitter(**splitter_args)
    texts = text_splitter.split_documents(documents)
    return Chroma.from_documents(texts, embeddings, collection_name=collection_name)

