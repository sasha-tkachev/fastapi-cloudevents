import uvicorn
from fastapi import FastAPI

from fastapi_cloudevents import (CloudEvent, StructuredCloudEventResponse,
                                 install_fastapi_cloudevents)

app = FastAPI()
app = install_fastapi_cloudevents(app)


@app.post("/", response_class=StructuredCloudEventResponse)
async def on_event(event: CloudEvent) -> CloudEvent:
    return CloudEvent(
        type="com.my-corp.response.v1",
        data=event.data,
        datacontenttype=event.datacontenttype,
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
