from langgraph.graph import END, StateGraph, START
from models.models import GraphState
from models.schemas import retrieve, grade_documents, generate, web_search, decide_to_generate, transform_query
from dataclasses import dataclass

@dataclass
class Agent():
    app: object = None

    def compile(self) -> None:
        workflow = StateGraph(GraphState)

        # Define the nodes
        workflow.add_node("retrieve", retrieve)  # retrieve
        workflow.add_node("grade_documents", grade_documents)  # grade documents
        workflow.add_node("generate", generate)  # generatae
        workflow.add_node("transform_query", transform_query)  # transform_query
        workflow.add_node("web_search_node", web_search)  # web search

        # Build graph
        workflow.add_edge(START, "retrieve")
        workflow.add_edge("retrieve", "grade_documents")
        workflow.add_conditional_edges(
            "grade_documents",
            decide_to_generate,
            {
                "transform_query": "transform_query",
                "generate": "generate",
            },
        )
        workflow.add_edge("transform_query", "web_search_node")
        workflow.add_edge("web_search_node", "generate")
        workflow.add_edge("generate", END)

        # Compile
        self.app = workflow.compile()
    def run(self, query) -> None:
        output = self.app.invoke(query)
        return output