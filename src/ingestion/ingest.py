import sys
from pathlib import Path
from dotenv import load_dotenv

# Localiza a raiz do projeto e carrega o arquivo .env
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import FastEmbedEmbeddings

# Definição dos caminhos das pastas de entrada e saída
DOCS_DIR = BASE_DIR / "documentos"
CHROMA_DIR = BASE_DIR / "data" / "chroma_db"

def run_ingestion():
    """Lê PDFs de ./documentos, gera chunks e armazena na base vetorial ChromaDB."""
    
    # 1. Valida se a pasta de documentos existe
    if not DOCS_DIR.exists():
        DOCS_DIR.mkdir(parents=True, exist_ok=True)
        print(f"[!] Pasta '{DOCS_DIR}' criada. Adicione arquivos PDF nela e execute novamente.")
        return

    # 2. Carrega todos os arquivos PDF do diretório
    print(f"[*] Carregando PDFs do diretório: {DOCS_DIR}")
    loader = PyPDFDirectoryLoader(str(DOCS_DIR))
    documents = loader.load()

    if not documents:
        print(f"[!] Nenhum arquivo PDF encontrado em '{DOCS_DIR}'. Insira documentos e tente novamente.")
        return

    print(f"[+] Total de páginas extraídas: {len(documents)}")

    # 3. Divide os textos em blocos (chunks) com sobreposição de contexto
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )
    chunks = text_splitter.split_documents(documents)
    print(f"[+] Texto segmentado em {len(chunks)} blocos (chunks).")

    # 4. Inicializa o modelo de embeddings FastEmbed (rápido e local)
    embeddings = FastEmbedEmbeddings()

    # 5. Vetoriza os chunks e grava persistentemente no ChromaDB
    print(f"[*] Gerando embeddings e persistindo vetores em: {CHROMA_DIR}")
    
    # Se já existir um banco no local, novos documentos serão adicionados à coleção existente
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR)
    )

    print("\n[✔] Processo de ingestão concluído com sucesso!")

if __name__ == "__main__":
    run_ingestion()