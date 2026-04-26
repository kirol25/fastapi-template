import enum


class StrEnum(enum.StrEnum):
    @classmethod
    def list_values(cls) -> list[str]:
        """Return a list of all values in the enum."""
        return [e.value for e in cls]


class Environment(StrEnum):
    """Application deployment environments."""
    dev = "dev"
    sandbox = "sandbox"


class SentByEnum(StrEnum):
    """Identifies the sender of a message."""
    client = "client"
    server = "server"


class MessageTypeEnum(StrEnum):
    """Types of messages in the system."""
    text = "text"
    status = "status"
    result = "result"
    suggestions = "suggestions"
