from langgraph.graph import StateGraph, END

from nodes import AgentState, generate

# utilizado langgraph para caso precisarmos de um historico persistente utilizar checkpointers
def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("generate", generate)
    graph.set_entry_point("generate")
    graph.add_edge("generate", END)

    return graph.compile()
