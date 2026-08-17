# pegasus_assistant
Virtual assistant for Pegasus Technologies Enterprise.


Directory structure

```
/agente_corporativo
├── src/
│   ├── api/             # Rotas do FastAPI para receber as perguntas
│   ├── core/            # Lógica do LangChain (configuração do RAG)
│   ├── ingestion/       # Scripts de limpeza de texto e embeddings
│   └── scripts/         # Ferramentas CLI (ex: argparse) para atualizar os dados
├── data/                # (Opcional) Armazenamento do ChromaDB local
├── documentos/                # Fonte de arquivos usados pelo agente, pdf e outros
├── Dockerfile           # Instruções para construir a imagem do agente
├── docker-compose.yml   # Orquestração da API e do Vector DB
└── requirements.txt
```