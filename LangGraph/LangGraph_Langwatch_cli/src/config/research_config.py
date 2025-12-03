"""Research agent configuration management."""

from typing import Literal

from pydantic_settings import BaseSettings


class ResearchConfig(BaseSettings):
    """Configuration for research agent operations."""

    max_sources: int = 10
    confidence_threshold: float = 0.7
    default_depth: Literal["surface", "standard", "deep"] = "standard"
    citation_format: Literal["academic", "apa", "mla", "chicago"] = "academic"
    fact_check_enabled: bool = True
    bias_detection_enabled: bool = True

    model_config = {"env_prefix": "RESEARCH_", "case_sensitive": False}


# Global instance
research_config = ResearchConfig()
