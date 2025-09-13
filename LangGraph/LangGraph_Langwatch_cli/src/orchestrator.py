"""Main orchestrator for LangGraph workflows with optional monitoring."""

from typing import Any, Dict, List, Optional, Protocol

from langgraph.graph import StateGraph

from .agents.base_agent import BaseAgent
from .workflows.base_workflow import BaseWorkflow


class MonitoringTracker(Protocol):
    """Protocol for monitoring trackers (langwatch, langfuse, etc)."""
    
    def track_agent_registration(self, name: str, agent_class: str) -> None: ...
    def track_workflow_registration(self, name: str, workflow_class: str) -> None: ...
    def start_workflow_execution(self, name: str, input_data: Dict[str, Any]) -> None: ...
    def complete_workflow_execution(self, name: str, result: Dict[str, Any]) -> None: ...
    def error_workflow_execution(self, name: str, error: str) -> None: ...


class MainOrchestrator:
    """Main orchestrator that coordinates agents, workflows, and monitoring."""

    def __init__(
        self,
        tracker: Optional[MonitoringTracker] = None,
    ) -> None:
        """Initialize the orchestrator.
        
        Args:
            tracker: Optional monitoring tracker (langwatch, langfuse, etc)
        """
        self.agents: Dict[str, BaseAgent] = {}
        self.workflows: Dict[str, BaseWorkflow] = {}
        self.tracker = tracker
        self.active_graph: Optional[StateGraph] = None

    def register_agent(self, name: str, agent: BaseAgent) -> None:
        """Register an agent with the orchestrator.
        
        Args:
            name: Agent identifier
            agent: Agent instance
        """
        self.agents[name] = agent
        if self.tracker:
            self.tracker.track_agent_registration(name, agent.__class__.__name__)

    def register_workflow(self, name: str, workflow: BaseWorkflow) -> None:
        """Register a workflow with the orchestrator.
        
        Args:
            name: Workflow identifier
            workflow: Workflow instance
        """
        self.workflows[name] = workflow
        if self.tracker:
            self.tracker.track_workflow_registration(name, workflow.__class__.__name__)

    async def execute_workflow(
        self,
        workflow_name: str,
        input_data: Dict[str, Any],
        config: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Execute a registered workflow.
        
        Args:
            workflow_name: Name of the workflow to execute
            input_data: Input data for the workflow
            config: Optional configuration for execution
            
        Returns:
            Workflow execution results
            
        Raises:
            ValueError: If workflow is not registered
        """
        if workflow_name not in self.workflows:
            raise ValueError(f"Workflow '{workflow_name}' not registered")

        workflow = self.workflows[workflow_name]
        
        if self.tracker:
            self.tracker.start_workflow_execution(workflow_name, input_data)

        try:
            result = await workflow.execute(input_data, config or {})
            
            if self.tracker:
                self.tracker.complete_workflow_execution(workflow_name, result)
                
            return result
            
        except Exception as e:
            if self.tracker:
                self.tracker.error_workflow_execution(workflow_name, str(e))
            raise

    def get_available_agents(self) -> List[str]:
        """Get list of registered agent names."""
        return list(self.agents.keys())

    def get_available_workflows(self) -> List[str]:
        """Get list of registered workflow names."""
        return list(self.workflows.keys())

    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on all components.
        
        Returns:
            Health status of all components
        """
        status = {
            "orchestrator": "healthy",
            "agents": {},
            "workflows": {},
            "tracker": "disabled" if not self.tracker else "enabled"
        }

        for name, agent in self.agents.items():
            try:
                agent_status = await agent.health_check()
                status["agents"][name] = agent_status
            except Exception as e:
                status["agents"][name] = f"error: {str(e)}"

        for name, workflow in self.workflows.items():
            try:
                workflow_status = await workflow.health_check()
                status["workflows"][name] = workflow_status
            except Exception as e:
                status["workflows"][name] = f"error: {str(e)}"

        return status