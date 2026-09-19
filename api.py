from fastapi import FastAPI, UploadFile, File, HTTPException
from starlette.concurrency import run_in_threadpool
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
from secrets import token_urlsafe

from pipeline import RagPipeline
from indexing.embedder import get_embedder


@asynccontextmanager
async def lifespan(app: FastAPI):

    app.state.embedder = get_embedder()
    app.state.pipelines={}
   
    yield


app = FastAPI(lifespan=lifespan)

def get_session_pipeline(document_id: str):
    try:
        return app.state.pipelines[document_id]
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )



class Query(BaseModel):
    question: str = Field(...,min_length=1)

class UploadResponse(BaseModel):
    document_id: str = Field(...)

class QueryResponse(BaseModel):
    answer: str
    text_sources: list[str]
    table_sources: list[str]

class HealthCheck(BaseModel):
    status: str="OK"

@app.post("/documents", response_model = UploadResponse, status_code=201)
async def upload_pdf(pdf: UploadFile=File(...)):
    if pdf.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only files of type PDF are allowed"
        )

    pdf_bytes = await pdf.read()

    if not pdf_bytes.startswith(b"%PDF-"):
        raise HTTPException(
                    status_code=400,
                    detail="Uploaded File isn't a valid PDF"
                )
    document_id = token_urlsafe(8)
    pipeline=RagPipeline(embedder=app.state.embedder,
                         cloud=True)
    await run_in_threadpool(pipeline.ingest, pdf_bytes)
    app.state.pipelines[document_id]=pipeline

    return UploadResponse(
        document_id=document_id
    )


@app.post("/documents/{document_id}/query", response_model=QueryResponse)
async def answer_question(query: Query, document_id: str):
    
    pipeline = get_session_pipeline(document_id=document_id)
    answer = await run_in_threadpool(pipeline.ask, query.question)
    return QueryResponse(
        answer=answer.answer,
        text_sources=answer.sources.text_chunks,
        table_sources=answer.sources.table_chunks
        )


@app.post("/health", status_code=200, response_model=HealthCheck)
def get_health()->HealthCheck:
    return HealthCheck(response="OK")
    
    



