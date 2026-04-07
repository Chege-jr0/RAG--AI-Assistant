# This is the brain of the AI and where the actual intelligence lives
#It takes chunks from ingest.py and embeds them - converts text into number(vectors) the AI can search
#Embeding is the process of converting the question and answer into numbers called vectors and when the user asks the question
# The ChromaDB finds the most similar chunks and GPT reads the chunk and asnswers



# It stores them in chromaDB -  a searchable memory bank
# It retrieves the most relevant chunks when you ask a question
#It passes those chunks to GPT to generate an answer

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import PromptTemplate
from typing import List
import os


def build_rag_chain(texts: List[str]):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    all_chunks = []
    for text in texts:
        chunks = splitter.split_text(text)
        all_chunks.extend(chunks)

    print(f" Total chunks for vector store: {len(all_chunks)}")
    

    try:
        print(" Creating embeddings...")
        embeddings = OllamaEmbeddings(model = "tinyllama")
        print(" Embeddings created!")
    except Exception as e:
        print(f"Embeddings error: {e}")
        raise

    try:
        print(" Storing in ChromaDB...")
        vectorstore = Chroma.from_texts(
            texts=all_chunks,
            embedding=embeddings,
            collection_name="data_analytics_rag"
        )
        print("Stored in ChromaDB!")
    except Exception as e:
        print(f"ChromaDB error: {e}")
        raise

    try:
        print(" Creating LLM...")
        llm = ChatOllama(
            model="tinyllama",
            temperature=0,
            
        )
        print(" LLM created!")
    except Exception as e:
        print(f"LLM error: {e}")
        raise

    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    prompt_template = """You are a helpful data analyst assistant.
You have been given context from a dataset. Use the context below to answer the user's question.
Be specific, mention numbers, trends, or insights where relevant.
If you cannot find the answer in the context, say "I don't have enough data to answer that."

Context:
{context}

Question: {question}

Answer:"""

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=prompt_template
    )

    print("RAG chain built successfully!")
    return {"llm": llm, "retriever": retriever, "prompt": prompt}

def ask_question(chain, question: str) -> str:
    retriever = chain["retriever"]
    llm = chain["llm"]
    prompt = chain["prompt"]

    docs = retriever.invoke(question)
    context = "\n\n".join([doc.page_content for doc in docs])

    final_prompt = prompt.format(context=context, question=question)
    
    from langchain_core.messages import HumanMessage
    result = llm.invoke([HumanMessage(content=final_prompt)])

    return result.content