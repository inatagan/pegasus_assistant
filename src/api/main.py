from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from src.core.rag import ask_question

app = FastAPI(
    title="Pegasus Assistant API",
    description="API HTTP para consulta à base de conhecimento corporativa via RAG.",
    version="1.0.0"
)

# Esquemas de entrada e saída com Pydantic
class QueryRequest(BaseModel):
    question: str = Field(
        ..., 
        description="Pergunta a ser enviada ao assistente.", 
        json_schema_extra={"example": "Qual é a Filosofia SRE e a Gênese da Confiabilidade sob a Ótica da Santo Pegasus Soluciones?"}
    )

class SourceMetadata(BaseModel):
    source: str
    page: str | int

class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceMetadata]

@app.get("/health", tags=["Health"])
def health_check():
    """Endpoint para verificação do status da aplicação."""
    return {"status": "healthy"}

@app.post("/ask", response_model=QueryResponse, tags=["RAG"])
def ask_endpoint(payload: QueryRequest):
    """Recebe uma pergunta via JSON, executa a busca no ChromaDB e gera a resposta com Gemini."""
    try:
        result = ask_question(payload.question)
        
        # Extrai os metadados de auditoria dos documentos retornados
        sources = [
            SourceMetadata(
                source=doc.metadata.get("source", "Desconhecido"),
                page=doc.metadata.get("page", "N/A")
            )
            for doc in result.get("context", [])
        ]

        return QueryResponse(
            answer=result["answer"],
            sources=sources
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erro interno ao processar a requisição: {str(e)}"
        )