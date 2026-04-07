#  Data Analytics RAG

Chat with your CSV and Excel files using plain English — powered by FastAPI + LangChain + Ollama

I created a technical article expalining how the system works

Here is the link: https://medium.com/@paulgikonyo100/retrieval-augmented-generation-assistant-that-enables-users-to-communicate-with-data-in-plain-41bf9e9d01e7

---

##  Setup (Step by Step)

### 1. Open this folder in VS Code terminal

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set your Ollama Server 
Open the terminal:
```bash
ollama serve
```
Pull the tinyllama model:
```bash
ollama pull tinyllama
```

### 5. Run the backend app
```bash
uvicorn main:app --reload
```
 ## Running the frontend
````bash
streamlit run frontend.py
```


### 6. Open the interactive API docs
Go to: **http://127.0.0.1:8000/docs**

---

##  How to Use

1. **Upload your CSV/Excel** → `POST /upload`
2. **Ask questions** → `POST /ask`
   - "What are the top 5 values in column X?"
   - "What is the average sales?"
   - "Are there any missing values?"
   - "What trends do you see in the data?"
3. **Check data info** → `GET /data-info`

---

##  Project Structure
```
data-analytics-rag/
├── main.py          # FastAPI app & endpoints
├── ingest.py        # Converts DataFrame to text chunks
├── rag.py           # LangChain RAG chain logic
├── requirements.txt
└── README.md
```

---

## Tech Stack

-FastAPI -> BackendAPI
-Streamlit -> Frontend Interface
-LangChain -> RAG Orchestration
-ChromaDB -> Vector Storage
-Ollama -> Free Local AI Model
-Tinyllama -> The AI model
-Pandas-> Data Cleaning and Processing

##  Example Questions to Ask
- "How many rows are in this dataset?"
- "What is the average of a certain column?"
- "Which category has the highest value?"
- "Are there missing values in the data?"
- "Give me a summary of the dataset"
- "What are the top 5 categorical columns?"
