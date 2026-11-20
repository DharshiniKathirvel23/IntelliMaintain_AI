
import chromadb

client = chromadb.PersistentClient(
    path="data/chroma_db"
)

collection = client.get_or_create_collection(
    name="machine_documents"
)

print("\nTOTAL DOCUMENT CHUNKS:")
print(collection.count())

data = collection.get(
    include=["documents", "metadatas"]
)

print("\nSTORED DOCUMENT METADATA:")

for i, metadata in enumerate(data["metadatas"]):
    print(f"\nChunk {i + 1}")
    print("Metadata:", metadata)
    print("Text:", data["documents"][i][:150])
