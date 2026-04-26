import enum


class StrEnum(str, enum.Enum):
    def __str__(self) -> str:
        return self.value

    @classmethod
    def list_values(cls) -> list[str]:
        """
        Returns a list of all values in the enum.

        This method iterates over all enum members and collects their values into a list.

        Returns:
            list[str]: A list of string values representing all members of the enum.
        """
        return [enum.value for enum in cls]


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
