from fastapi_tools.middlewares import SimpleBaseMiddleware
from starlette.requests import Request
from starlette.responses import Response


class CloudEventsMiddleware(SimpleBaseMiddleware):
    async def before_request(self, request: Request) -> [Response, None]:
        pass

    async def after_request(self, request: Request):
        pass

    async def send(self, message, send, request):
        pass
