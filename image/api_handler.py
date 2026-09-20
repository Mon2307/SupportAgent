from fastapi import FastAPI
from mangum import Mangum
from pydantic import BaseModel
from rag_app.query_rag import query_rag

app = FastAPI(title="SupportAgent RAG API")
handler = Mangum(app)


class QueryRequest(BaseModel):
    query_text: str


class QueryResponse(BaseModel):
    query_text: str
    response_text: str
    sources: list[str | None]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    result = query_rag(request.query_text)
    return QueryResponse(
        query_text=result.query_text,
        response_text=result.response_text,
        sources=result.sources,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api_handler:app", host="0.0.0.0", port=8000)
