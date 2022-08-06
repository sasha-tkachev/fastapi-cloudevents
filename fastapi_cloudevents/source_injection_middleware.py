from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class BinarySourceInjectionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        source = response.headers.get("ce-source")
        if source is not None:
            response.headers["ce-source"] = source.replace("{url}", str(request.url))
        return response


class StructuredSourceInjectionMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
    ):
        super(StructuredSourceInjectionMiddleware, self).__init__(app)
        raise NotImplementedError(
            "Structured CloudEvent source injection is not supported yet"
        )

    async def dispatch(self, request: Request, call_next):
        # do something with the request object, for example
        raise NotImplementedError(
            "Structured CloudEvent source injection is not supported yet"
        )
