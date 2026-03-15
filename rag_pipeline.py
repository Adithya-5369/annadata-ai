import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ── PDF Loader ──────────────────────────────────────────────
def load_pdfs(data_folder="data/"):
    print("Loading PDFs...")
    all_docs = []
    for filename in os.listdir(data_folder):
        if filename.endswith(".pdf"):
            print(f"  Loading: {filename}")
            loader = PyPDFLoader(os.path.join(data_folder, filename))
            all_docs.extend(loader.load())
    print(f"PDF pages loaded: {len(all_docs)} ✅")
    return all_docs

# ── HuggingFace Datasets ────────────────────────────────────
def load_hf_datasets():
    from datasets import load_dataset
    all_docs = []

    # 1. KisanVaani Agriculture QA
    try:
        print("Loading KisanVaani QA dataset...")
        ds = load_dataset("KisanVaani/agriculture-qa-english-only", split="train")
        for item in ds:
            text = f"Question: {item['question']}\nAnswer: {item['answer']}"
            all_docs.append(Document(
                page_content=text,
                metadata={"source": "KisanVaani"}
            ))
        print(f"KisanVaani: {len(ds)} QA pairs ✅")
    except Exception as e:
        print(f"KisanVaani failed: {e}")

    # 2. Mahesh2841 Agriculture Dataset
    try:
        print("Loading Mahesh2841 Agriculture dataset...")
        ds2 = load_dataset("Mahesh2841/Agriculture", split="train")
        for item in ds2:
            text = " | ".join([f"{k}: {v}" for k, v in item.items() if v])
            if text.strip():
                all_docs.append(Document(
                    page_content=text,
                    metadata={"source": "Mahesh2841-Agriculture"}
                ))
        print(f"Mahesh2841: {len(ds2)} records ✅")
    except Exception as e:
        print(f"Mahesh2841 failed: {e}")

    # 3. Crop Recommendation Dataset
    try:
        print("Loading Crop Recommendation dataset...")
        ds3 = load_dataset("atharvaingle/crop-recommendation", split="train")
        for item in ds3:
            text = (
                f"Crop: {item.get('label', 'N/A')}. "
                f"Best grown when: Nitrogen={item.get('N','N/A')}kg/ha, "
                f"Phosphorus={item.get('P','N/A')}kg/ha, "
                f"Potassium={item.get('K','N/A')}kg/ha, "
                f"Temperature={item.get('temperature','N/A')}°C, "
                f"Humidity={item.get('humidity','N/A')}%, "
                f"pH={item.get('ph','N/A')}, "
                f"Rainfall={item.get('rainfall','N/A')}mm."
            )
            all_docs.append(Document(
                page_content=text,
                metadata={"source": "CropRecommendation-ICAR"}
            ))
        print(f"Crop Recommendation: {len(ds3)} records ✅")
    except Exception as e:
        print(f"Crop Recommendation failed: {e}")

    print(f"Total HF docs loaded: {len(all_docs)} ✅")
    return all_docs

# ── Build Knowledge Base ────────────────────────────────────
def build_knowledge_base(docs):
    print("Splitting into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=50
    )
    chunks = splitter.split_documents(docs)
    print(f"Total chunks: {len(chunks)} ✅")

    print("Building FAISS vector database...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local("faiss_index")
    print("Knowledge base saved! ✅")
    return vectorstore

# ── Load Existing ───────────────────────────────────────────
def load_knowledge_base():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return FAISS.load_local(
        "faiss_index", embeddings,
        allow_dangerous_deserialization=True
    )

# ── Retrieve Context ────────────────────────────────────────
def get_relevant_context(query, vectorstore, k=4):
    docs = vectorstore.similarity_search(query, k=k)
    return "\n\n".join([doc.page_content for doc in docs])