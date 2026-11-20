
import os
import chromadb

from dotenv import load_dotenv
from openai import OpenAI
from rank_bm25 import BM25Okapi

# Load Nexus API credentials
load_dotenv()

# Connect to Nexus API
client = OpenAI(
    api_key=os.getenv("NEXUS_API_KEY"),
    base_url=os.getenv("NEXUS_API_BASE_URL", "").rstrip("/") + "/v1"
)

EMBEDDING_MODEL = "text-embedding-3-small"

# Create persistent ChromaDB database
chroma_client = chromadb.PersistentClient(
    path="data/chroma_db"
)

collection = chroma_client.get_or_create_collection(
    name="machine_documents"
)


def generate_embeddings(texts):
    """Generate embeddings using the Nexus API."""

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts
    )

    return [item.embedding for item in response.data]


def store_chunks(chunks, document_name, machine_id="GENERAL"):
    """Store document chunks with Nexus embeddings."""

    if not chunks:
        return

    embeddings = generate_embeddings(chunks)

    document_ids = [
        f"{machine_id}_{document_name}_{i}"
        for i in range(len(chunks))
    ]

    collection.upsert(
        ids=document_ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=[
            {
                "document": document_name,
                "machine_id": machine_id
            }
            for _ in chunks
        ]
    )


def semantic_search(query, top_k=3, machine_id=None):
    """Search documents using Nexus semantic embeddings."""

    if collection.count() == 0:
        return []

    query_embedding = generate_embeddings([query])

    search_args = {
        "query_embeddings": query_embedding,
        "n_results": min(top_k, collection.count())
    }

    if machine_id:
        search_args["where"] = {
            "machine_id": machine_id
        }

    results = collection.query(**search_args)

    return results.get("documents", [[]])[0]


def keyword_search(query, top_k=3, machine_id=None):
    """Search documents using BM25 keyword matching."""

    search_data = collection.get(
        include=["documents", "metadatas"]
    )

    documents = search_data.get("documents", [])
    metadatas = search_data.get("metadatas", [])

    if machine_id:
        documents = [
            doc
            for doc, metadata in zip(documents, metadatas)
            if metadata.get("machine_id") == machine_id
        ]

    if not documents:
        return []

    tokenized_documents = [
        document.lower().split()
        for document in documents
    ]

    bm25 = BM25Okapi(tokenized_documents)

    scores = bm25.get_scores(query.lower().split())

    ranked_indices = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )

    return [
        documents[i]
        for i in ranked_indices[:top_k]
        if scores[i] > 0
    ]


def hybrid_search(query, top_k=3, machine_id=None):
    """Combine semantic and keyword search."""

    semantic_results = semantic_search(
        query, top_k, machine_id
    )

    keyword_results = keyword_search(
        query, top_k, machine_id
    )

    combined_results = list(dict.fromkeys(
        semantic_results + keyword_results
    ))

    return combined_results[:top_k]


if __name__ == "__main__":

    print("Nexus Embedding Model:", EMBEDDING_MODEL)
    print("Embedding dimensions: 1536")
    print("Stored document chunks:", collection.count())

    question = "Why is machine M101 experiencing excessive vibration?"

    results = hybrid_search(
        question,
        top_k=3,
        machine_id="M101"
    )

    print("\nHYBRID SEARCH RESULTS")

    for i, result in enumerate(results, start=1):
        print(f"\nResult {i}:")
        print(result)
