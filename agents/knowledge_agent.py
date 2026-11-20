
from rag.retriever import hybrid_search
from database import get_machine_context


def retrieve_machine_knowledge(question, machine_id=None):
    """
    Knowledge Retrieval Agent:
    Combines Hybrid RAG technical knowledge
    with CAG historical machine context.
    """

    # -----------------------------------------
    # 1. Retrieve technical knowledge using RAG
    # -----------------------------------------

    technical_results = hybrid_search(
        question,
        top_k=3,
        machine_id=machine_id
    )

    if technical_results:
        technical_knowledge = "\n\n".join(technical_results)
    else:
        technical_knowledge = (
            "No relevant information found in uploaded manuals."
        )

    # -----------------------------------------
    # 2. Retrieve historical context using CAG
    # -----------------------------------------

    if machine_id:
        historical_context = get_machine_context(machine_id)
    else:
        historical_context = (
            "Machine ID not provided. "
            "Historical context is unavailable."
        )

    # -----------------------------------------
    # 3. Combine RAG and CAG context
    # -----------------------------------------

    combined_context = f"""
TECHNICAL KNOWLEDGE FROM HYBRID RAG
===================================

{technical_knowledge}


HISTORICAL MACHINE CONTEXT FROM CAG
===================================

{historical_context}
"""

    return combined_context


if __name__ == "__main__":

    machine_id = "M101"

    question = (
        "Why is machine M101 experiencing excessive vibration?"
    )

    print("\nKNOWLEDGE RETRIEVAL AGENT")
    print("-" * 40)

    result = retrieve_machine_knowledge(
        question,
        machine_id
    )

    print(result)
