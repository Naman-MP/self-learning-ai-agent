from langgraph.graph import StateGraph , START , END
from state.state import MemoryAgentState
from nodes.memory_extractor import memory_extractor
from nodes.memory_evaluator import memory_evaluator
from nodes.memory_retriever import memory_retriever
from nodes.memory_manager import memory_manager
from nodes.response_generator import response

graph = StateGraph(MemoryAgentState)

graph.add_node("memory_extractor", memory_extractor)
graph.add_node("memory_evaluator",memory_evaluator)
graph.add_node("memory_retriever",memory_retriever)
graph.add_node("memory_manager" , memory_manager)
graph.add_node("response" , response)

graph.add_edge(START,"memory_extractor")
graph.add_edge("memory_extractor","memory_retriever")
graph.add_edge("memory_retriever","memory_evaluator")
graph.add_edge("memory_evaluator","memory_manager")
graph.add_edge("memory_manager","response")
graph.add_edge("response",END)

memory_graph = graph.compile()