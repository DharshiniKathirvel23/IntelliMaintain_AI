
from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from agents.knowledge_agent import retrieve_machine_knowledge
from agents.fault_agent import investigate_fault
from agents.recommendation_agent import generate_maintenance_plan


# Shared information passed between agents
class MaintenanceState(TypedDict):
    question: str
    machine_id: str
    technical_context: str
    fault_analysis: str
    maintenance_plan: str


# Agent 1: Retrieve knowledge using Hybrid RAG + CAG
def knowledge_node(state: MaintenanceState):

    print("\n[Agent 1] Retrieving machine knowledge...")

    context = retrieve_machine_knowledge(
        question=state["question"],
        machine_id=state["machine_id"]
    )

    return {
        "technical_context": context
    }


# Agent 2: Investigate possible faults
def fault_node(state: MaintenanceState):

    print("\n[Agent 2] Investigating possible faults...")

    analysis = investigate_fault(
        state["question"],
        state["technical_context"]
    )

    return {
        "fault_analysis": analysis
    }


# Agent 3: Generate maintenance recommendations
def recommendation_node(state: MaintenanceState):

    print("\n[Agent 3] Preparing maintenance plan...")

    plan = generate_maintenance_plan(
        state["fault_analysis"]
    )

    return {
        "maintenance_plan": plan
    }


# Build LangGraph workflow
workflow = StateGraph(MaintenanceState)

workflow.add_node("knowledge", knowledge_node)
workflow.add_node("fault_investigation", fault_node)
workflow.add_node("recommendation", recommendation_node)

workflow.add_edge(START, "knowledge")
workflow.add_edge("knowledge", "fault_investigation")
workflow.add_edge("fault_investigation", "recommendation")
workflow.add_edge("recommendation", END)

maintenance_app = workflow.compile()


# Run the complete workflow
if __name__ == "__main__":

    initial_state = {
        "machine_id": "M101",
        "question": "Why is machine M101 experiencing excessive vibration?",
        "technical_context": "",
        "fault_analysis": "",
        "maintenance_plan": ""
    }

    result = maintenance_app.invoke(initial_state)

    print("\n" + "=" * 50)
    print("INTELLIMAINTAIN AI - FINAL INVESTIGATION REPORT")
    print("=" * 50)

    print("\n1. TECHNICAL INFORMATION")
    print(result["technical_context"])

    print("\n2. FAULT INVESTIGATION")
    print(result["fault_analysis"])

    print("\n3. MAINTENANCE RECOMMENDATION")
    print(result["maintenance_plan"])
