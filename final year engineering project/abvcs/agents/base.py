"""
Base agent abstractions and interfaces for ABVCS multi-agent swarm.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseAgent(ABC):
    """Abstract Base Class for all specialized ABVCS sub-agents."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def execute(self, payload: Dict[str, Any]) -> Any:
        """Executes the specialized agent task on the given payload."""
        pass
