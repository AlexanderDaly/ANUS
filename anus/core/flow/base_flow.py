"""This module defines the BaseFlow abstract class."""

from abc import ABC, abstractmethod
from typing import Any, Dict

from anus.core.agent.base_agent import BaseAgent


class BaseFlow(ABC):
    """Abstract base class for all flow controllers."""

    def __init__(self, agents: Dict[str, BaseAgent]):
        """
        Initializes the BaseFlow with a dictionary of agents.

        Args:
            agents: A dictionary mapping agent names to BaseAgent instances.
        """
        self.agents = agents

    @abstractmethod
    def execute(self, input_text: str, **kwargs) -> Any:
        """
        Executes the flow with the given input text.

        Args:
            input_text: The input text to process.
            **kwargs: Additional keyword arguments for the flow execution.

        Returns:
            The result of the flow execution.
        """
        pass
