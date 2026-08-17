import argparse
from pathlib import Path
from src.core.rag import ask_question

def main():
    parser = argparse.ArgumentParser(
        description="CLI para realizar consultas na base de conhecimento corporativa."
    )
    parser.add_argument(
        "pergunta", 
        type=str, 
        help="Texto da pergunta a ser enviada ao RAG."
    )
    
    args = parser.parse_args()
    
    print(f"\n[?] Pergunta: {args.pergunta}\n")
    print("Buscando resposta nos documentos internos...")
    
    response = ask_question(args.pergunta)
    
    print("\n[+] Resposta:\n")
    print(response["answer"])
    
    # Exibe as fontes recuperadas para auditoria
    print("\n" + "-" * 40)
    print("Fontes consultadas:")
    for doc in response.get("context", []):
        fonte = doc.metadata.get("source", "Desconhecido")
        pagina = doc.metadata.get("page", "N/A")
        print(f" - Arquivo: {fonte} | Página: {pagina}")

if __name__ == "__main__":
    main()