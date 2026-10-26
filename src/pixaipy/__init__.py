"""pixaipy — client for the PixAI.art GraphQL/REST API.

Unofficial, not affiliated with PixAI. Token auth, quota checks,
generation task submission/polling and a generic ``graphql()`` escape
hatch. See the project README for details.
"""

from .errors import PixAIError
from .client import PixAI

__all__ = ["PixAI", "PixAIError"]
__version__ = "0.1.0"
