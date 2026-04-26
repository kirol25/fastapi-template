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
