from fastapi import HTTPException, status


class ResourceNotFoundException(HTTPException):
    """Raised when a requested resource does not exist."""

    def __init__(self, detail: dict) -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class InvalidInputException(HTTPException):
    """Raised when the request input is invalid."""

    def __init__(self, detail: dict | str) -> None:
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class RateLimitException(HTTPException):
    """Raised when the rate limit is exceeded."""

    def __init__(self, detail: dict) -> None:
        super().__init__(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=detail)


class UnauthorizedException(HTTPException):
    """Raised when the request is not authorized."""

    def __init__(self, detail: dict) -> None:
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)
