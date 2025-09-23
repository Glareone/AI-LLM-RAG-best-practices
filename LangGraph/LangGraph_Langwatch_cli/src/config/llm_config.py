from typing import Optional

from pydantic_settings import BaseSettings

class LLMConfig(BaseSettings):
    # anthropic model configuration
    # left it here to easily switch from openai to anthropic
    anthropic_region: Optional[str]
    anthropic_inference_profile_id: Optional[str]
    anthropic_inference_profile_id_sonnet_3_7: Optional[str]
    anthropic_inference_profile_id_sonnet_4_0: Optional[str]
    anthropic_version: Optional[str]
    anthropic_max_tokens: Optional[int]
    anthropic_chat_temperature: Optional[float]
    anthropic_reasoning_temperature: Optional[float]
    anthropic_thinking_budget_tokens: Optional[int]

    # azure openai model configuration
    openai_api_base: Optional[str]
    openai_api_version: Optional[str]
    openai_api_key: Optional[str]
    openai_reasoning_deployment_name: Optional[str]
    openai_chat_deployment_name: Optional[str]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"

llm_config = LLMConfig()