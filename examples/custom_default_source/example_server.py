import random

import uvicorn
from fastapi import FastAPI

from fastapi_cloudevents import CloudEvent, install_fastapi_cloudevents
from fastapi_cloudevents.settings import CloudEventSettings

app = FastAPI()
app = install_fastapi_cloudevents(
    app, settings=CloudEventSettings(default_source="my-source",
                                     create_events_on_behalf_of_the_client=True,
                                     response_mode="structured")
)


@app.get("/")
async def index(event: CloudEvent) -> CloudEvent:
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
