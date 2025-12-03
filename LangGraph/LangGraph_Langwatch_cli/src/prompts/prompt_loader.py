"""Utility for loading prompt templates from TOML files."""

import tomllib
from pathlib import Path
from typing import Any


class PromptLoader:
    """Load and manage prompt templates from TOML files."""

    def __init__(self, prompt_file: str | Path) -> None:
        """Initialize the prompt loader.

        Args:
            prompt_file: Path to the TOML prompt file
        """
        self.prompt_file = Path(prompt_file)
        self._prompts: dict[str, Any] = {}
        self._load_prompts()

    def _load_prompts(self) -> None:
        """Load prompts from the TOML file."""
        if not self.prompt_file.exists():
            msg = f"Prompt file not found: {self.prompt_file}"
            raise FileNotFoundError(msg)

        with self.prompt_file.open("rb") as f:
            self._prompts = tomllib.load(f)

    def get_system_prompt(self) -> str:
        """Get the system message template."""
        return self._prompts.get("template", {}).get("system_message_template", "")

    def get_user_prompt(self) -> str:
        """Get the user message template."""
        return self._prompts.get("template", {}).get("user_message_template", "")

    def get_prompt(self, section: str, key: str) -> str:
        """Get a specific prompt from a section.

        Args:
            section: TOML section name
            key: Prompt key within the section

        Returns:
            The prompt template string
        """
        return self._prompts.get(section, {}).get(key, "")

    def format_user_prompt(self, **kwargs: Any) -> str:
        """Format the user prompt template with provided values.

        Args:
            **kwargs: Values to substitute in the template

        Returns:
            Formatted prompt string
        """
        template = self.get_user_prompt()
        return template.format(**kwargs)

    def get_research_type_prompt(self, research_type: str) -> str:
        """Get a specific research type prompt.

        Args:
            research_type: Type of research (e.g., "academic_research")

        Returns:
            Research type specific instructions
        """
        return self._prompts.get("research_types", {}).get(research_type, "")

    def get_template(self, template_name: str) -> str:
        """Get a template from the template section.

        Args:
            template_name: Name of the template (e.g., "executive_summary_template")

        Returns:
            Template string
        """
        return self._prompts.get("template", {}).get(template_name, "")

    def get_synthesis_components(self) -> dict[str, str]:
        """Get all synthesis component templates.

        Returns:
            Dictionary of synthesis component templates
        """
        template_section = self._prompts.get("template", {})
        return {
            "executive_summary": template_section.get("executive_summary_template", ""),
            "key_findings": template_section.get("key_findings_template", ""),
            "source_analysis": template_section.get("source_analysis_template", ""),
            "confidence_assessment": template_section.get(
                "confidence_assessment_template", ""
            ),
            "recommendations": template_section.get("recommendations_template", ""),
            "further_research": template_section.get("further_research_template", ""),
        }
