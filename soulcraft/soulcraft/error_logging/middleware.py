from .models import ErrorLog


class ErrorLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code in [500, 403]:
            ErrorLog.objects.create(
                path=request.path,
                status_code=response.status_code,
                method=request.method,
                error_message=response.content.decode("utf-8")[
                    :1024
                ],  # Truncate to fit the model
            )
        return response
