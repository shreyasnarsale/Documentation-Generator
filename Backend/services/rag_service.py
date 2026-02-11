import os
import uuid
import time
from typing import List, Dict, Any

from dotenv import load_dotenv

from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI
)

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# In-memory session storage
vector_stores: Dict[str, FAISS] = {}


# =====================================================
# EMBEDDINGS (CORRECT MODEL NAME - NO "models/")
# =====================================================
def get_embeddings():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found")

    return GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        google_api_key=api_key
    )


# =====================================================
# LLM (CORRECT MODEL NAME)
# =====================================================
def get_llm():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found")

    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=api_key,
        temperature=0.3
    )


# =====================================================
# INITIALIZE VECTOR STORE
# =====================================================
def initialize_vector_store(documentation: str) -> str:
    session_id = str(uuid.uuid4())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    texts = splitter.split_text(documentation)

    vector_store = FAISS.from_texts(
        texts=texts,
        embedding=get_embeddings()
    )

    vector_stores[session_id] = vector_store
    return session_id


# =====================================================
# GET ANSWER (UPDATED FOR NEW LANGCHAIN)
# =====================================================
def get_answer(
    session_id: str,
    question: str,
    history: List[Dict[str, str]] = []
) -> Dict[str, Any]:

    if session_id not in vector_stores:
        raise ValueError("Invalid session_id")

    retriever = vector_stores[session_id].as_retriever(
        search_kwargs={"k": 4}
    )

    # ✅ NEW WAY (LangChain latest versions)
    docs = retriever.invoke(question)

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = ChatPromptTemplate.from_template("""
You are a professional software documentation assistant.

Answer the question ONLY using the provided context.
If the answer is not found in context, say:
"I don't know based on the provided documentation."

Context:
{context}

Question:
{question}

Answer clearly and professionally:
""")

    llm = get_llm()

    # small delay to avoid burst rate limit
    time.sleep(1)

    try:
        response = llm.invoke(
            prompt.format_messages(
                context=context,
                question=question
            )
        )
    except Exception as e:
        print("🔥 LLM ERROR:", e)
        raise Exception("LLM failed. Check API key, billing, or model access.")

    return {
        "response": response.content,
        "sources": [doc.page_content[:200] + "..." for doc in docs]
    }
