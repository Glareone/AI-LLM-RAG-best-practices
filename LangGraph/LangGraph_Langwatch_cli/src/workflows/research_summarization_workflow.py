"""Research and Summarization workflow implementation."""

from typing import Any, Dict, List, Optional

from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph

from agents.research_agent.research_agent import ResearchAgent
from agents.summarization_agent.summarization_agent import SummarizationAgent
from .base_workflow import BaseWorkflow, WorkflowConfig


class ResearchSummarizationWorkflow(BaseWorkflow):
    """Workflow that combines research and summarization agents."""

    def __init__(
        self,
        research_agent: Optional[ResearchAgent] = None,
        summarization_agent: Optional[SummarizationAgent] = None,
        config: Optional[WorkflowConfig] = None,
    ):
        """Initialize the research summarization workflow.
        
        Args:
            research_agent: Research agent instance
            summarization_agent: Summarization agent instance
            config: Workflow configuration
        """
        if config is None:
            config = WorkflowConfig(
                name="research_summarization_workflow",
                description="Combines research and summarization for comprehensive analysis",
                max_iterations=5,
                timeout_seconds=600,
            )
        
        super().__init__(config)
        
        self.research_agent = research_agent or ResearchAgent()
        self.summarization_agent = summarization_agent or SummarizationAgent()

    async def build_graph(self) -> StateGraph:
        """Build the workflow graph.
        
        Returns:
            Configured LangGraph graph
        """
        # TODO: Implement actual LangGraph graph construction
        # This is a mockup implementation
        
        # Define the workflow state
        class WorkflowState(Dict[str, Any]):
            """Workflow state container."""
            pass

        # Create state graph
        graph = StateGraph(WorkflowState)
        
        # Define nodes
        async def research_node(state: WorkflowState) -> WorkflowState:
            """Research node execution."""
            query = state.get("query", "")
            messages = [HumanMessage(content=query)]
            result = await self.research_agent.execute(messages, state.get("context"))
            state["research_result"] = result.content
            return state

        async def summarization_node(state: WorkflowState) -> WorkflowState:
            """Summarization node execution."""
            research_content = state.get("research_result", "")
            messages = [HumanMessage(content=research_content)]
            result = await self.summarization_agent.execute(messages, state.get("context"))
            state["summary"] = result.content
            return state

        # Add nodes to graph
        graph.add_node("research", research_node)
        graph.add_node("summarization", summarization_node)
        
        # Define edges
        graph.add_edge("research", "summarization")
        
        # Set entry and exit points
        graph.set_entry_point("research")
        graph.set_finish_point("summarization")
        
        compiled_graph = graph.compile()
        self.graph = compiled_graph
        
        return compiled_graph

    async def execute(
        self,
        input_data: Dict[str, Any],
        config: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Execute the workflow.
        
        Args:
            input_data: Must contain 'query' key
            config: Optional execution configuration
            
        Returns:
            Dictionary containing research_result and summary
        """
        if not await self.validate_input(input_data):
            raise ValueError("Invalid input data")

        # Ensure graph is built
        if self.graph is None:
            await self.build_graph()

        # Prepare initial state
        initial_state = {
            "query": input_data.get("query", ""),
            "context": input_data.get("context", {}),
        }

        # TODO: Execute actual graph when LangGraph is properly integrated
        # For now, execute steps sequentially as mockup
        
        # Step 1: Research
        research_messages = [HumanMessage(content=initial_state["query"])]
        research_result = await self.research_agent.execute(
            research_messages, 
            initial_state["context"]
        )
        
        # Step 2: Summarization
        summary_messages = [HumanMessage(content=research_result.content)]
        summary_result = await self.summarization_agent.execute(
            summary_messages,
            {**initial_state["context"], "summary_style": "comprehensive"}
        )

        return {
            "query": initial_state["query"],
            "research_result": research_result.content,
            "summary": summary_result.content,
            "workflow_status": "completed",
        }

    async def health_check(self) -> str:
        """Perform health check on the workflow."""
        research_health = await self.research_agent.health_check()
        summary_health = await self.summarization_agent.health_check()
        
        if "healthy" in research_health and "healthy" in summary_health:
            return "healthy"
        else:
            return f"degraded (research: {research_health}, summary: {summary_health})"

    def get_workflow_steps(self) -> List[str]:
        """Get workflow steps."""
        return [
            "Validate input query",
            "Execute research agent to gather information",
            "Execute summarization agent on research results",
            "Combine results and return comprehensive analysis",
        ]

    async def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data."""
        return (
            super().validate_input(input_data) 
            and "query" in input_data 
            and bool(input_data["query"].strip())
        )