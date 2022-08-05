import uvicorn
from fastapi import FastAPI

from fastapi_cloudevents import CloudEvent, CloudEventRoute

app = FastAPI()
app.router.route_class = CloudEventRoute


@app.post("/")
async def on_event(event: CloudEvent) -> CloudEvent:
    return CloudEvent(
        type="my.response-type.v1", source="my:source", data=event.data,
        datacontenttype=event.datacontenttype
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
