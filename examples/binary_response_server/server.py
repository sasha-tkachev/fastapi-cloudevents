import uvicorn
from fastapi import FastAPI

from fastapi_cloudevents import (BinaryCloudEventResponse, CloudEvent,
                                 CloudEventRoute)

app = FastAPI()
app.router.route_class = CloudEventRoute


@app.post("/", response_class=BinaryCloudEventResponse)
async def on_event(event: CloudEvent) -> CloudEvent:
    return CloudEvent(
        type="com.my-corp.response.v1", source="my:source", data=event.data,
        datacontenttype=event.datacontenttype
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)