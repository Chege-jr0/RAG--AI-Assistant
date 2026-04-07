from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import os
from rag import build_rag_chain, ask_question
from ingest import ingest_dataframe

app = FastAPI(title="Data Analytics RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store chain in memory
rag_chain = None
data_summary = None

class Question(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "Data Analytics RAG is running! Upload a CSV/Excel file to get started."}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    global rag_chain, data_summary

    if not file.filename.endswith((".csv", ".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Only CSV and Excel files are supported.")

    contents = await file.read()

    if file.filename.endswith(".csv"):
        import io
        df = pd.read_csv(io.BytesIO(contents))
    else:
        import io
        df = pd.read_excel(io.BytesIO(contents))

    data_summary = {
        "filename": file.filename,
        "rows": len(df),
        "columns": list(df.columns),
        "shape": df.shape,
        "preview": df.head(3).to_dict(orient="records")
    }

    try:
        texts = ingest_dataframe(df)
        rag_chain = build_rag_chain(texts)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline error: {str(e)}")

    return {
        "message": f"✅ File '{file.filename}' loaded successfully!",
        "data_info": data_summary
    }


@app.post("/ask")
def ask(body: Question):
    """Ask a question about your uploaded data."""
    global rag_chain

    if rag_chain is None:
        raise HTTPException(status_code=400, detail="No data loaded yet. Please upload a CSV or Excel file first.")

    answer = ask_question(rag_chain, body.question)
    return {"question": body.question, "answer": answer}


@app.get("/data-info")
def data_info():
    """Get info about the currently loaded dataset."""
    if data_summary is None:
        return {"message": "No data loaded yet."}
    return data_summary
