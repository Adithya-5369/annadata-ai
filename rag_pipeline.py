import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def load_pdfs(data_folder="data/"):
    print("Loading PDFs...")
    all_docs = []
    for filename in os.listdir(data_folder):
        if filename.endswith(".pdf"):
            print(f"  Loading: {filename}")
            loader = PyPDFLoader(os.path.join(data_folder, filename))
            all_docs.extend(loader.load())
    print(f"Total pages: {len(all_docs)} ✅")
    return all_docs

def build_knowledge_base(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=50
    )
    chunks = splitter.split_documents(docs)
    print(f"Total chunks: {len(chunks)} ✅")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local("faiss_index")
    print("Knowledge base saved! ✅")
    return vectorstore

def load_knowledge_base():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return FAISS.load_local(
        "faiss_index", embeddings,
        allow_dangerous_deserialization=True
    )

def get_relevant_context(query, vectorstore, k=4):
    docs = vectorstore.similarity_search(query, k=k)
    return "\n\n".join([doc.page_content for doc in docs])