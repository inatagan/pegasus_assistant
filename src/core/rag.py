import os
from pathlib import Path
from dotenv import load_dotenv

# Localiza a raiz do projeto e carrega as variáveis do arquivo .env
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

from langchain_chroma import Chroma
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

CHROMA_DIR = BASE_DIR / "data" / "chroma_db"

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def get_rag_chain(data_dir: Path = CHROMA_DIR, k: int = 3):
    embeddings = FastEmbedEmbeddings()
    
    vectorstore = Chroma(
        persist_directory=str(data_dir), 
        embedding_function=embeddings
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        temperature=0
    )
    
    template = (
        "Você é um assistente corporativo interno. Responda à pergunta usando APENAS "
        "os trechos de contexto fornecidos abaixo. Se a resposta não estiver nos documentos, "
        "responda expressamente 'Não encontrei essa informação nos documentos internos'.\n\n"
        "Contexto:\n{context}\n\n"
        "Pergunta: {question}"
    )
    
    prompt = ChatPromptTemplate.from_template(template)

    rag_chain = (
        {
            "context": retriever | format_docs, 
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain, retriever

def ask_question(question: str) -> dict:
    chain, retriever = get_rag_chain()
    
    answer = chain.invoke(question)
    docs = retriever.invoke(question)
    
    return {
        "answer": answer,
        "context": docs
    }