"""Integration tests for ResearchAgent - tests the complete functionality."""

import pytest
import os
from pathlib import Path

# Set up environment variables for testing
os.environ.setdefault("RESEARCH_MAX_SOURCES", "10")
os.environ.setdefault("RESEARCH_CONFIDENCE_THRESHOLD", "0.7")
os.environ.setdefault("RESEARCH_DEFAULT_DEPTH", "standard")
os.environ.setdefault("RESEARCH_CITATION_FORMAT", "academic")
os.environ.setdefault("RESEARCH_FACT_CHECK_ENABLED", "true")
os.environ.setdefault("RESEARCH_BIAS_DETECTION_ENABLED", "true")


class TestResearchAgentIntegration:
    """Integration tests for ResearchAgent functionality."""

    def test_prompt_loading(self):
        """Test that prompt templates can be loaded."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

        from prompts.prompt_loader import PromptLoader

        prompt_file = Path(__file__).parent.parent / "src" / "prompts" / "research_agent_prompt.toml"
        loader = PromptLoader(prompt_file)

        # Test basic prompt loading
        system_prompt = loader.get_system_prompt()
        assert len(system_prompt) > 0
        assert "Research Agent" in system_prompt

        # Test synthesis components
        components = loader.get_synthesis_components()
        assert len(components) == 6
        assert "executive_summary" in components
        assert "key_findings" in components

    def test_research_config_loading(self):
        """Test that research configuration loads correctly."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

        from config.research_config import ResearchConfig

        config = ResearchConfig()
        assert config.max_sources == 10
        assert config.confidence_threshold == 0.7
        assert config.default_depth == "standard"

    def test_prompt_template_formatting(self):
        """Test that prompt templates format correctly with variables."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

        from prompts.prompt_loader import PromptLoader

        prompt_file = Path(__file__).parent.parent / "src" / "prompts" / "research_agent_prompt.toml"
        loader = PromptLoader(prompt_file)

        components = loader.get_synthesis_components()

        # Test executive summary formatting
        exec_template = components["executive_summary"]
        if "{user_query}" in exec_template:
            formatted = exec_template.format(user_query="artificial intelligence")
            assert "artificial intelligence" in formatted
            assert "{user_query}" not in formatted

    def test_synthesis_prompt_structure(self):
        """Test that synthesis prompt has the expected structure."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

        from prompts.prompt_loader import PromptLoader

        prompt_file = Path(__file__).parent.parent / "src" / "prompts" / "research_agent_prompt.toml"
        loader = PromptLoader(prompt_file)

        synthesis_prompt = loader.get_prompt("prompts", "synthesis_prompt")

        # Check for required sections
        assert "Executive Summary" in synthesis_prompt
        assert "Key Findings" in synthesis_prompt
        assert "Source Analysis" in synthesis_prompt
        assert "Confidence Assessment" in synthesis_prompt
        assert "Recommendations" in synthesis_prompt
        assert "Areas for Further Investigation" in synthesis_prompt

        # Check for template variables
        assert "{source_count}" in synthesis_prompt
        assert "{executive_summary}" in synthesis_prompt
        assert "{key_findings}" in synthesis_prompt

    @pytest.mark.parametrize("research_type", [
        "academic_research",
        "market_research",
        "technical_research",
        "competitive_intelligence",
        "trend_analysis",
        "regulatory_research"
    ])
    def test_research_types_available(self, research_type):
        """Test that all research types are available and non-empty."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

        from prompts.prompt_loader import PromptLoader

        prompt_file = Path(__file__).parent.parent / "src" / "prompts" / "research_agent_prompt.toml"
        loader = PromptLoader(prompt_file)

        prompt = loader.get_research_type_prompt(research_type)
        assert len(prompt) > 0
        assert isinstance(prompt, str)

    def test_environment_config_override(self):
        """Test that environment variables override default config values."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

        # Set custom environment variables
        os.environ["RESEARCH_MAX_SOURCES"] = "25"
        os.environ["RESEARCH_CONFIDENCE_THRESHOLD"] = "0.9"

        from config.research_config import ResearchConfig

        # Create new config instance to pick up new env vars
        config = ResearchConfig()
        assert config.max_sources == 25
        assert config.confidence_threshold == 0.9

        # Reset environment
        os.environ["RESEARCH_MAX_SOURCES"] = "10"
        os.environ["RESEARCH_CONFIDENCE_THRESHOLD"] = "0.7"

    def test_toml_file_structure(self):
        """Test that TOML file has the expected structure."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

        from prompts.prompt_loader import PromptLoader

        prompt_file = Path(__file__).parent.parent / "src" / "prompts" / "research_agent_prompt.toml"
        loader = PromptLoader(prompt_file)

        prompts = loader._prompts

        # Check main sections
        assert "template" in prompts
        assert "extra" in prompts
        assert "prompts" in prompts
        assert "research_types" in prompts

        # Check template section has synthesis components
        template_section = prompts["template"]
        synthesis_components = [
            "executive_summary_template",
            "key_findings_template",
            "source_analysis_template",
            "confidence_assessment_template",
            "recommendations_template",
            "further_research_template"
        ]

        for component in synthesis_components:
            assert component in template_section
            assert len(template_section[component]) > 0

    def test_prompt_content_quality(self):
        """Test that prompts contain expected content quality indicators."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

        from prompts.prompt_loader import PromptLoader

        prompt_file = Path(__file__).parent.parent / "src" / "prompts" / "research_agent_prompt.toml"
        loader = PromptLoader(prompt_file)

        system_prompt = loader.get_system_prompt()

        # Check for professional language and key concepts
        assert "expertise" in system_prompt.lower()
        assert "research" in system_prompt.lower()
        assert "analysis" in system_prompt.lower()
        assert "methodology" in system_prompt.lower()
        assert "quality standards" in system_prompt.lower()

    def test_component_template_variables(self):
        """Test that component templates use variables correctly."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

        from prompts.prompt_loader import PromptLoader

        prompt_file = Path(__file__).parent.parent / "src" / "prompts" / "research_agent_prompt.toml"
        loader = PromptLoader(prompt_file)

        components = loader.get_synthesis_components()

        # These components should contain {user_query} variable
        query_components = ["executive_summary", "key_findings", "recommendations", "further_research"]

        for component_name in query_components:
            component = components[component_name]
            if len(component) > 0:  # Only test non-empty components
                # Check if it has user_query variable or is static content
                has_variable = "{user_query}" in component
                # Either has variable or is meaningful static content
                assert has_variable or len(component) > 10