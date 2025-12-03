"""Tests for prompt management and template loading."""

import pytest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from prompts.prompt_loader import PromptLoader


class TestPromptLoader:
    """Test suite for PromptLoader class."""

    @pytest.fixture
    def prompt_loader(self):
        """Create a PromptLoader instance for testing."""
        prompt_file = Path(__file__).parent.parent / "src" / "prompts" / "research_agent_prompt.toml"
        return PromptLoader(prompt_file)

    def test_init_valid_file(self, prompt_loader):
        """Test PromptLoader initialization with valid file."""
        assert prompt_loader.prompt_file.exists()
        assert prompt_loader._prompts is not None
        assert isinstance(prompt_loader._prompts, dict)

    def test_init_invalid_file(self):
        """Test PromptLoader initialization with invalid file."""
        invalid_file = Path("/nonexistent/file.toml")

        with pytest.raises(FileNotFoundError):
            PromptLoader(invalid_file)

    def test_get_system_prompt(self, prompt_loader):
        """Test getting system message template."""
        system_prompt = prompt_loader.get_system_prompt()

        assert isinstance(system_prompt, str)
        assert len(system_prompt) > 0
        assert "Research Agent" in system_prompt
        assert "information gathering" in system_prompt

    def test_get_user_prompt(self, prompt_loader):
        """Test getting user message template."""
        user_prompt = prompt_loader.get_user_prompt()

        assert isinstance(user_prompt, str)
        assert len(user_prompt) > 0
        assert "Research Request" in user_prompt
        assert "{query}" in user_prompt

    def test_get_prompt_valid_section(self, prompt_loader):
        """Test getting specific prompt from valid section."""
        synthesis_prompt = prompt_loader.get_prompt("prompts", "synthesis_prompt")

        assert isinstance(synthesis_prompt, str)
        assert len(synthesis_prompt) > 0
        assert "Executive Summary" in synthesis_prompt
        assert "{source_count}" in synthesis_prompt

    def test_get_prompt_invalid_section(self, prompt_loader):
        """Test getting prompt from invalid section."""
        result = prompt_loader.get_prompt("nonexistent", "key")
        assert result == ""

    def test_get_prompt_invalid_key(self, prompt_loader):
        """Test getting invalid prompt key."""
        result = prompt_loader.get_prompt("prompts", "nonexistent_prompt")
        assert result == ""

    def test_format_user_prompt(self, prompt_loader):
        """Test formatting user prompt with values."""
        formatted = prompt_loader.format_user_prompt(
            query="Test query",
            context="Test context",
            primary_focus="Test focus",
            depth_level="standard",
            time_frame="immediate",
            requirements="none",
            deliverables="summary"
        )

        assert "Test query" in formatted
        assert "Test context" in formatted
        assert "Test focus" in formatted
        assert "{query}" not in formatted  # Ensure substitution worked

    def test_get_research_type_prompt(self, prompt_loader):
        """Test getting research type specific prompts."""
        academic_prompt = prompt_loader.get_research_type_prompt("academic_research")

        assert isinstance(academic_prompt, str)
        assert len(academic_prompt) > 0
        assert "peer-reviewed" in academic_prompt.lower()

    def test_get_research_type_prompt_invalid(self, prompt_loader):
        """Test getting invalid research type."""
        result = prompt_loader.get_research_type_prompt("nonexistent_type")
        assert result == ""

    def test_get_template(self, prompt_loader):
        """Test getting individual template."""
        exec_template = prompt_loader.get_template("executive_summary_template")

        assert isinstance(exec_template, str)
        assert len(exec_template) > 0
        assert "{user_query}" in exec_template

    def test_get_template_invalid(self, prompt_loader):
        """Test getting invalid template."""
        result = prompt_loader.get_template("nonexistent_template")
        assert result == ""

    def test_get_synthesis_components(self, prompt_loader):
        """Test getting all synthesis component templates."""
        components = prompt_loader.get_synthesis_components()

        assert isinstance(components, dict)

        expected_keys = [
            "executive_summary",
            "key_findings",
            "source_analysis",
            "confidence_assessment",
            "recommendations",
            "further_research"
        ]

        for key in expected_keys:
            assert key in components
            assert isinstance(components[key], str)
            assert len(components[key]) > 0

    def test_synthesis_components_formatting(self, prompt_loader):
        """Test that synthesis components format correctly."""
        components = prompt_loader.get_synthesis_components()
        test_query = "artificial intelligence"

        # Test components that should have user_query placeholder
        query_components = ["executive_summary", "key_findings", "recommendations", "further_research"]

        for component_name in query_components:
            component = components[component_name]
            if "{user_query}" in component:
                formatted = component.format(user_query=test_query)
                assert test_query in formatted
                assert "{user_query}" not in formatted

    def test_toml_structure_integrity(self, prompt_loader):
        """Test that TOML file has expected structure."""
        prompts = prompt_loader._prompts

        # Check main sections exist
        assert "template" in prompts
        assert "extra" in prompts
        assert "prompts" in prompts
        assert "research_types" in prompts

        # Check template section has required templates
        template_section = prompts["template"]
        assert "system_message_template" in template_section
        assert "user_message_template" in template_section
        assert "executive_summary_template" in template_section
        assert "key_findings_template" in template_section

    def test_all_research_types_available(self, prompt_loader):
        """Test that all expected research types are available."""
        expected_types = [
            "market_research",
            "academic_research",
            "technical_research",
            "competitive_intelligence",
            "trend_analysis",
            "regulatory_research"
        ]

        for research_type in expected_types:
            prompt = prompt_loader.get_research_type_prompt(research_type)
            assert len(prompt) > 0
            assert isinstance(prompt, str)

    def test_prompt_content_quality(self, prompt_loader):
        """Test that prompts have reasonable content quality."""
        system_prompt = prompt_loader.get_system_prompt()

        # Check for key research agent concepts
        assert "research" in system_prompt.lower()
        assert "analysis" in system_prompt.lower()
        assert "information" in system_prompt.lower()

        # Check for professional language indicators
        assert "capabilities" in system_prompt.lower()
        assert "methodology" in system_prompt.lower()
        assert "quality" in system_prompt.lower()

    def test_template_variable_consistency(self, prompt_loader):
        """Test that template variables are used consistently."""
        synthesis_prompt = prompt_loader.get_prompt("prompts", "synthesis_prompt")

        # Check that synthesis prompt expects all component variables
        expected_variables = [
            "{source_count}",
            "{executive_summary}",
            "{key_findings}",
            "{source_analysis}",
            "{confidence_assessment}",
            "{recommendations}",
            "{further_research}"
        ]

        for variable in expected_variables:
            assert variable in synthesis_prompt