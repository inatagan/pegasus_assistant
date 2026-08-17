from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import FastEmbedEmbeddings

# 1. Carregar documentos PDF
loader = PyPDFDirectoryLoader("./docs")
docs = loader.load()

# 2. Dividir o texto em chunks (blocos com sobreposição)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
chunks = text_splitter.split_documents(docs)

# 3. Vetorizar e armazenar no ChromaDB local
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=FastEmbedEmbeddings(),
    persist_directory="./chroma_db"
)
print(f"Sucesso! {len(chunks)} blocos de texto foram vetorizados.")