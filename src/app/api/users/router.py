from fastapi import APIRouter, Depends, status

from app.api.users import schemas
from app.api.users.services import UserService
from app.helpers.schemas import ApiError

router = APIRouter(tags=["User"], prefix="/users")


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=schemas.UserResponse,
    responses={
        status.HTTP_200_OK: {
            "model": schemas.UserResponse,
            "description": "OK",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ApiError,
            "description": "The User is not authorized",
        },
    },
    description="This endpoint retrieves all information for respectice user from the database.",
    summary="Retrieve user information",
)
async def get_user_profile(
    username: str,
    service: UserService = Depends(),
) -> schemas.UserResponse:
    """
    Retrieve all User information from the database.

    Args:
        username (str): Extracted username from Bearer Token.
        service (FeedbackService): An instance of the FeedbackService used for storing the feedback.

    Raises:
        HTTPException:
            If the storage fails, an appropriate HTTP exception is raised.
    """
    return service.get_user_profile(username)
