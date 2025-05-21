"""This module defines Pydantic models for configuration."""

from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field


class ModelConfig(BaseModel):
    """Configuration for language models."""

    provider: str = "openai"
    model_name: str = "gpt-4o"
    api_key: Optional[str] = None
    api_base: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 2000
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    request_timeout: int = 120
    streaming: bool = False
    additional_params: Dict[str, Union[str, int, float, bool]] = Field(
        default_factory=dict
    )


class MemoryConfig(BaseModel):
    """Configuration for memory systems."""

    short_term_memory_provider: str = "in_memory"  # e.g., "in_memory", "redis"
    long_term_memory_provider: str = "vector_db"  # e.g., "vector_db", "elasticsearch"
    embedding_model: ModelConfig = Field(default_factory=ModelConfig)
    vector_db_config: Dict[str, Any] = Field(default_factory=dict) # type: ignore
    # Example: {"provider": "chroma", "path": "/path/to/chroma_db"}
    redis_config: Dict[str, Any] = Field(default_factory=dict) # type: ignore
    # Example: {"host": "localhost", "port": 6379, "db": 0}


class ToolConfig(BaseModel):
    """Configuration for tools."""

    name: str
    description: Optional[str] = None
    module: str  # The Python module where the tool class is defined
    tool_class: str  # The name of the tool class
    enabled: bool = True
    config: Dict[str, Any] = Field(default_factory=dict) # type: ignore


class AgentConfig(BaseModel):
    """Configuration for agents."""

    name: str
    role: str
    description: str
    llm_config: ModelConfig = Field(default_factory=ModelConfig)
    memory_config: Optional[MemoryConfig] = None
    tools: List[ToolConfig] = Field(default_factory=list)
    max_iterations: int = 10
    verbose: bool = False
    system_prompt_template: Optional[str] = None
    human_input_prompt_template: Optional[str] = None
    allow_delegation: bool = False
    additional_params: Dict[str, Any] = Field(default_factory=dict) # type: ignore
