"""Base workflow class for all LangGraph workflows."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph
from pydantic import BaseModel, Field


class WorkflowConfig(BaseModel):
    """Configuration for workflows."""
    
    name: str = Field(..., description="Workflow name")
    description: str = Field(..., description="Workflow description")
    max_iterations: int = Field(default=10, description="Maximum workflow iterations")
    timeout_seconds: int = Field(default=300, description="Workflow timeout in seconds")


class BaseWorkflow(ABC):
    """Abstract base class for all workflows."""

    def __init__(self, config: WorkflowConfig):
        """Initialize the workflow.
        
        Args:
            config: Workflow configuration
        """
        self.config = config
        self.name = config.name
        self.description = config.description
        self.graph: Optional[StateGraph] = None

    @abstractmethod
    async def build_graph(self) -> StateGraph:
        """Build the LangGraph graph for this workflow.
        
        Returns:
            Configured LangGraph graph
        """
        pass

    @abstractmethod
    async def execute(
        self,
        input_data: Dict[str, Any],
        config: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Execute the workflow.
        
        Args:
            input_data: Input data for the workflow
            config: Optional execution configuration
            
        Returns:
            Workflow execution results
        """
        pass

    @abstractmethod
    async def health_check(self) -> str:
        """Perform health check on the workflow.
        
        Returns:
            Health status string
        """
        pass

    def get_workflow_steps(self) -> List[str]:
        """Get list of workflow steps.
        
        Returns:
            List of step descriptions
        """
        # Default implementation - should be overridden by subclasses
        return [
            "Initialize workflow",
            "Process input data",
            "Execute main logic",
            "Return results",
        ]

    async def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data for the workflow.
        
        Args:
            input_data: Input data to validate
            
        Returns:
            True if input is valid, False otherwise
        """
        # Basic validation - ensure input_data is not empty
        return bool(input_data)

    def __str__(self) -> str:
        """String representation of the workflow."""
        return f"{self.__class__.__name__}(name='{self.name}')"

    def __repr__(self) -> str:
        """Detailed string representation of the workflow."""
        return f"{self.__class__.__name__}(name='{self.name}', max_iterations={self.config.max_iterations})"