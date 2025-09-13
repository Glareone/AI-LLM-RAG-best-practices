"""Summarization agent implementation."""

from typing import Any, Dict, List, Optional

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage

from .base_agent import AgentConfig, BaseAgent


class SummarizationAgent(BaseAgent):
    """Agent specialized in content summarization and synthesis."""

    def __init__(self, config: Optional[AgentConfig] = None):
        """Initialize the summarization agent."""
        if config is None:
            config = AgentConfig(
                name="summarization_agent",
                description="Specializes in content summarization and synthesis",
                temperature=0.2,
                max_tokens=1500,
                model_name="gpt-4",
            )
        super().__init__(config)

    async def execute(
        self,
        messages: List[BaseMessage],
        context: Optional[Dict[str, Any]] = None,
    ) -> BaseMessage:
        """Execute summarization task.
        
        Args:
            messages: Input messages containing content to summarize
            context: Optional context with summarization parameters
            
        Returns:
            Summary as AIMessage
        """
        # TODO: Implement actual summarization logic with Azure OpenAI
        # This is a mockup implementation
        
        content_to_summarize = ""
        for msg in messages:
            if isinstance(msg, HumanMessage):
                content_to_summarize = msg.content
                break

        # Get summarization style from context
        summary_style = "comprehensive"
        if context and "summary_style" in context:
            summary_style = context["summary_style"]

        # Mockup summarization response
        summary = f"""
        ## Summary ({summary_style} style)
        
        **Main Points:**
        - Key insight 1 from the provided content
        - Key insight 2 highlighting important details
        - Key insight 3 providing actionable information
        
        **Core Message:**
        The content discusses important concepts that require attention and further consideration.
        
        **Length:** Original content was {len(content_to_summarize)} characters, summarized to essential points.
        
        *Note: This is a mockup response. Actual implementation will use Azure OpenAI.*
        """

        return AIMessage(content=summary.strip())

    async def health_check(self) -> str:
        """Perform health check."""
        # TODO: Add actual Azure OpenAI connection check
        return "healthy (mockup mode)"

    def get_capabilities(self) -> List[str]:
        """Get summarization agent capabilities."""
        base_capabilities = super().get_capabilities()
        summarization_capabilities = [
            "Content summarization and synthesis",
            "Key point extraction",
            "Multi-document summarization",
            "Adaptive summary length control",
            "Style-aware summarization",
        ]
        return base_capabilities + summarization_capabilities