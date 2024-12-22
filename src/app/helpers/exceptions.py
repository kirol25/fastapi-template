from fastapi import HTTPException, status


class ResourceNotFoundException(HTTPException):
    def __init__(self, detail: dict):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class InvalidInputException(HTTPException):
    def __init__(self, detail: dict | str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class RateLimitException(HTTPException):
    def __init__(self, detail: dict):
        super().__init__(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=detail)


class UnauthorizedException(HTTPException):
    def __init__(self, detail: dict):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)
