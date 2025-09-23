"""Research agent implementation."""

from typing import Any

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage

from agents.base_agent import AgentConfig, BaseAgent

from ...config.llm_config import llm_config


class ResearchAgent(BaseAgent):
    """Agent specialized in research and information gathering."""

    def __init__(self, config: AgentConfig | None = None):
        """Initialize the research agent."""
        if config is None:
            config = AgentConfig(
                name="research_agent",
                description="Specializes in research and information gathering",
                temperature=llm_config.anthropic_chat_temperature,
                max_tokens=llm_config.max_tokens,
                model_name="gpt-4",
            )
        super().__init__(config)

    async def execute(
        self,
        messages: list[BaseMessage],
        context: dict[str, Any] | None = None,
    ) -> BaseMessage:
        """Execute research task.
        
        Args:
            messages: Input messages
            context: Optional context with search parameters
            
        Returns:
            Research results as AIMessage
        """
        # TODO: Implement actual research logic with Azure OpenAI
        # This is a mockup implementation

        user_query = ""
        for msg in messages:
            if isinstance(msg, HumanMessage):
                user_query = msg.content
                break

        # Mockup research response
        research_result = f"""
        Research Results for: "{user_query}"
        
        Based on my analysis, here are the key findings:
        
        1. **Primary Information**: This appears to be a research query about {user_query}.
        2. **Context Analysis**: The query requires deep investigation and fact-gathering.
        3. **Recommendations**: Further analysis would benefit from additional context.
        
        *Note: This is a mockup response. Actual implementation will use Azure OpenAI.*
        """

        return AIMessage(content=research_result.strip())

    async def health_check(self) -> str:
        """Perform health check."""
        # TODO: Add actual Azure OpenAI connection check
        return "healthy (mockup mode)"

    def get_capabilities(self) -> list[str]:
        """Get research agent capabilities."""
        base_capabilities = super().get_capabilities()
        research_capabilities = [
            "Information gathering and synthesis",
            "Fact-checking and verification",
            "Context analysis and interpretation",
            "Multi-source research coordination",
        ]
        return base_capabilities + research_capabilities
