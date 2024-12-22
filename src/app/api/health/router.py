from fastapi import APIRouter, status

from app.api.health.schemas import HealthResponse

router = APIRouter(tags=["Monitoring"], prefix="/monitoring")


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    response_model=HealthResponse,
    summary="Health Check",
    description="Check the health status of the service.",
)
async def health() -> HealthResponse:
    """
    Endpoint to check the health status of the service.

    This endpoint is used to verify that the service is operational and healthy.
    It returns a simple JSON response with a status message.

    Returns:
        HealthResponse: A dictionary containing a status message indicating that the service is healthy.
    """
    return HealthResponse(status="healthy")
