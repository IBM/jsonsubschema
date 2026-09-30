"""
Explain context module for collecting subschema check failure reasons.

This module provides thread-local context for capturing why a subschema check
fails, enabling detailed error messages without modifying existing method signatures.
"""

import threading
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class SubschemaResult:
    """
    Result of a subschema check with optional failure reasons.

    Attributes:
        is_subtype: True if s1 is a subschema of s2, False otherwise.
        reasons: List of failure reasons if is_subtype is False.
                 Empty list if is_subtype is True.

    Example:
        >>> result = is_subschema_with_reason(s1, s2)
        >>> if not result.is_subtype:
        ...     for reason in result.reasons:
        ...         print(reason)
    """

    is_subtype: bool
    reasons: List[str] = field(default_factory=list)

    def __bool__(self) -> bool:
        """Allow using result directly in boolean context."""
        return self.is_subtype


class ExplainContext:
    """
    Thread-local context for collecting failure reasons during subschema checks.

    This uses a thread-local storage pattern to avoid modifying existing method
    signatures while still collecting failure information.

    Usage:
        ctx = ExplainContext()
        ExplainContext.set_current(ctx)
        try:
            # ... perform subschema check ...
            result = s1.isSubtype(s2)
        finally:
            ExplainContext.set_current(None)

        # Access collected reasons
        for reason in ctx.reasons:
            print(reason)
    """

    _local = threading.local()

    @classmethod
    def get_current(cls) -> Optional["ExplainContext"]:
        """Get the current thread's ExplainContext, or None if not set."""
        return getattr(cls._local, "context", None)

    @classmethod
    def set_current(cls, ctx: Optional["ExplainContext"]) -> None:
        """Set the current thread's ExplainContext."""
        cls._local.context = ctx

    def __init__(self):
        """Initialize an empty explain context."""
        self.reasons: List[str] = []
        self.path: List[str] = []

    def push_path(self, segment: str) -> None:
        """Push a path segment onto the current path stack."""
        self.path.append(segment)

    def pop_path(self) -> Optional[str]:
        """Pop the last path segment from the path stack."""
        if self.path:
            return self.path.pop()
        return None

    def get_path_str(self) -> str:
        """Get the current path as a string."""
        return "/" + "/".join(self.path) if self.path else "/"

    def add_reason(self, code: str, message: str) -> None:
        """
        Add a failure reason to the context.

        Args:
            code: Short identifier for the failure type (e.g., "num__01")
            message: Human-readable description of the failure
        """
        path_str = self.get_path_str()
        self.reasons.append(f"[{code}] {message} (at {path_str})")

    def add_reason_raw(self, message: str) -> None:
        """
        Add a raw failure reason without code formatting.

        Args:
            message: The raw failure message
        """
        self.reasons.append(message)
