"""Base agent class for all LangGraph agents."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field


class AgentConfig(BaseModel):
    """Configuration for agents."""
    
    name: str = Field(..., description="Agent name")
    description: str = Field(..., description="Agent description")
    temperature: float = Field(default=0.7, description="Model temperature")
    max_tokens: int = Field(default=1000, description="Maximum tokens")
    model_name: str = Field(default="gpt-4", description="Model name")


class BaseAgent(ABC):
    """Abstract base class for all agents."""

    def __init__(self, config: AgentConfig):
        """Initialize the agent.
        
        Args:
            config: Agent configuration
        """
        self.config = config
        self.name = config.name
        self.description = config.description

    @abstractmethod
    async def execute(
        self,
        messages: List[BaseMessage],
        context: Optional[Dict[str, Any]] = None,
    ) -> BaseMessage:
        """Execute the agent's main functionality.
        
        Args:
            messages: Input messages
            context: Optional context data
            
        Returns:
            Agent's response message
        """
        pass

    @abstractmethod
    async def health_check(self) -> str:
        """Perform health check on the agent.
        
        Returns:
            Health status string
        """
        pass

    def get_capabilities(self) -> List[str]:
        """Get list of agent capabilities.
        
        Returns:
            List of capability descriptions
        """
        return [
            f"Process messages using {self.config.model_name}",
            f"Maintain temperature of {self.config.temperature}",
            f"Generate up to {self.config.max_tokens} tokens",
        ]

    def __str__(self) -> str:
        """String representation of the agent."""
        return f"{self.__class__.__name__}(name='{self.name}')"

    def __repr__(self) -> str:
        """Detailed string representation of the agent."""
        return f"{self.__class__.__name__}(name='{self.name}', model='{self.config.model_name}')"