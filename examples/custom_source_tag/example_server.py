import random

import uvicorn
from fastapi import FastAPI

from fastapi_cloudevents import (BinaryCloudEventResponse, CloudEvent,
                                 CloudEventRoute)

app = FastAPI(default_response_class=BinaryCloudEventResponse)
app.router.route_class = CloudEventRoute


@app.post(
    "/",
    tags=[
        # this tag will cause all events produced by this route to have a "my-source"
        # as their event source if no source is given
        "ce-source:my-source",
    ],
)
async def index() -> CloudEvent:
    i = random.randint(0, 3)
    if i == 0:
        # will have "my-source" as the source
        return CloudEvent(type="my.event.v1")
    if i == 1:
        # will have "my-source" as the source
        return CloudEvent(type="my.other-event.v1")
    else:
        # will have "his-source" as the source
        return CloudEvent(type="his.event.v1", source="his-source")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)
