from pathlib import Path
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Diretório padrão para os vetores armazenados
BASE_DIR = Path(__file__).resolve().parent.parent.parent
CHROMA_DIR = BASE_DIR / "data" / "chroma_db"

def format_docs(docs):
    """Formata a lista de documentos em um único bloco de texto."""
    return "\n\n".join(doc.page_content for doc in docs)

def get_rag_chain(data_dir: Path = CHROMA_DIR, k: int = 3):
    """Inicializa a base vetorial, o LLM e constrói a cadeia RAG com LCEL."""
    embeddings = FastEmbedEmbeddings()
    vectorstore = Chroma(
        persist_directory=str(data_dir), 
        embedding_function=embeddings
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    template = (
        "Você é um assistente corporativo interno. Responda à pergunta usando APENAS "
        "os trechos de contexto fornecidos abaixo. Se a resposta não estiver nos documentos, "
        "responda expressamente 'Não encontrei essa informação nos documentos internos'.\n\n"
        "Contexto:\n{context}\n\n"
        "Pergunta: {question}"
    )
    
    prompt = ChatPromptTemplate.from_template(template)

    # Construção do pipeline via LCEL
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
    """Executa a consulta no pipeline RAG e recupera o contexto para auditoria."""
    chain, retriever = get_rag_chain()
    
    answer = chain.invoke(question)
    docs = retriever.invoke(question)
    
    return {
        "answer": answer,
        "context": docs
    }