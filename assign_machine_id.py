
import chromadb

client = chromadb.PersistentClient(
    path="data/chroma_db"
)

collection = client.get_or_create_collection(
    name="machine_documents"
)

# Get existing document IDs and metadata
data = collection.get(
    include=["metadatas"]
)

ids = data["ids"]
metadatas = data["metadatas"]

if not ids:
    print("No document chunks found.")

else:
    # Add M101 to existing document metadata
    updated_metadatas = []

    for metadata in metadatas:
        updated_metadata = metadata.copy()
        updated_metadata["machine_id"] = "M101"
        updated_metadatas.append(updated_metadata)

    collection.update(
        ids=ids,
        metadatas=updated_metadatas
    )

    print("Machine IDs updated successfully!")
    print("Total updated chunks:", len(ids))

    # Verify
    updated_data = collection.get(
        include=["metadatas"]
    )

    print("\nUPDATED METADATA:")

    for metadata in updated_data["metadatas"]:
        print(metadata)
