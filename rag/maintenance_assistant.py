
from rag.retriever import hybrid_search


def investigate_fault(question):
    """
    Retrieve relevant machine information
    and prepare context for AI investigation.
    """

    retrieved_information = hybrid_search(
        question,
        top_k=3
    )

    if not retrieved_information:
        return {
            "question": question,
            "context": "No relevant information found in uploaded documents."
        }

    context = "\n\n".join(retrieved_information)

    return {
        "question": question,
        "context": context
    }


if __name__ == "__main__":

    question = "Why is machine M101 experiencing excessive vibration?"

    result = investigate_fault(question)

    print("\nFAULT INVESTIGATION")
    print("Question:", result["question"])

    print("\nRETRIEVED CONTEXT:")
    print(result["context"])
