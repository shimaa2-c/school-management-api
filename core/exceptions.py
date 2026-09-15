from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    request = context.get("request")

    request_id = getattr(
        request,
        "request_id",
        None,
    )

    if response is None:
        return Response(
            {
                "success": False,
                "message": "Internal server error.",
                "data": None,
                "errors": {
                    "detail": "An unexpected error occurred."
                },
                "meta": {
                    "request_id": request_id,
                },
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    if response.status_code == status.HTTP_400_BAD_REQUEST:
        message = "Validation failed."

    elif response.status_code == status.HTTP_401_UNAUTHORIZED:
        message = "Authentication failed."

    elif response.status_code == status.HTTP_403_FORBIDDEN:
        message = "Permission denied."

    elif response.status_code == status.HTTP_404_NOT_FOUND:
        message = "Resource not found."

    else:
        message = "Request failed."

    return Response(
        {
            "success": False,
            "message": message,
            "data": None,
            "errors": response.data,
            "meta": {
                "request_id": request_id,
            },
        },
        status=response.status_code,
        headers=response.headers,
    )