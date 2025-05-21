"""This module defines the Plan and PlanStep Pydantic models."""

import time
import uuid
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class PlanStep(BaseModel):
    """Represents a single step in a plan."""

    id: str = Field(default_factory=lambda: f"step-{uuid.uuid4()}")
    name: str
    description: str
    tool: str
    tool_input: Dict[str, Any] = Field(default_factory=dict)
    expected_output: Optional[str] = None
    dependencies: List[str] = Field(default_factory=list)
    status: str = "pending"  # e.g., pending, active, completed, failed
    result: Optional[Dict[str, Any]] = None
    created_at: float = Field(default_factory=time.time)
    completed_at: Optional[float] = None


class Plan(BaseModel):
    """Represents a plan consisting of multiple steps."""

    id: str = Field(default_factory=lambda: f"plan-{uuid.uuid4()}")
    task: str
    status: str = "created"  # e.g., created, active, completed, failed, updated
    created_at: float = Field(default_factory=time.time)
    updated_at: Optional[float] = None
    completed_at: Optional[float] = None
    steps: List[PlanStep] = Field(default_factory=list)
    reasoning: Optional[str] = None
    current_step_index: int = 0
    metadata: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None
