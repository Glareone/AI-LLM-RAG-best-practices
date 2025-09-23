"""Research agent implementation."""

from pathlib import Path
from typing import Any

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage

from agents.base_agent import AgentConfig, BaseAgent

from ...config.llm_config import llm_config
from ...config.research_config import research_config
from ...prompts.prompt_loader import PromptLoader


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

        # Load prompt templates
        prompt_file = (
            Path(__file__).parent.parent.parent / "prompts" / "research_agent_prompt.toml"
        )
        self.prompt_loader = PromptLoader(prompt_file)

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

        # Generate research response using synthesis prompt template
        synthesis_template = self.prompt_loader.get_prompt("prompts", "synthesis_prompt")

        # Load synthesis component templates
        components = self.prompt_loader.get_synthesis_components()

        # Format each component with user query (for templates that need it)
        research_result = synthesis_template.format(
            source_count=research_config.max_sources,
            executive_summary=components["executive_summary"].format(user_query=user_query),
            key_findings=components["key_findings"].format(user_query=user_query).strip(),
            source_analysis=components["source_analysis"].strip(),
            confidence_assessment=components["confidence_assessment"].strip(),
            recommendations=components["recommendations"].format(user_query=user_query).strip(),
            further_research=components["further_research"].format(user_query=user_query).strip()
        )

        # Add implementation note
        research_result += "\n\n*Note: This is a mockup response using prompt templates. Actual implementation will integrate with Azure OpenAI for real research capabilities.*"

        return AIMessage(content=research_result)

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

    def get_research_config(self) -> dict[str, Any]:
        """Get current research configuration.

        Returns:
            Dictionary containing research configuration settings
        """
        return {
            "max_sources": research_config.max_sources,
            "confidence_threshold": research_config.confidence_threshold,
            "default_depth": research_config.default_depth,
            "citation_format": research_config.citation_format,
            "fact_check_enabled": research_config.fact_check_enabled,
            "bias_detection_enabled": research_config.bias_detection_enabled,
        }
