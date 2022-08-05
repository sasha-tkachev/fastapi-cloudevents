from starlette.middleware.base import (BaseHTTPMiddleware)
from starlette.requests import Request


class CloudEventsMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        # do something with the request object, for example
        content_type = request.headers.get("Content-Type")
        print(content_type)

        # process the request and get the response
        response = await call_next(request)

        return response
