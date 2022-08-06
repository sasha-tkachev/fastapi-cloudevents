import uvicorn
from fastapi import FastAPI
from pydantic.main import BaseModel

from fastapi_cloudevents import CloudEvent, install_fastapi_cloudevents

app = FastAPI()
app = install_fastapi_cloudevents(app)


class MyModel(BaseModel):
    my_value: str


@app.post("/event-response")
async def on_event(value: MyModel) -> CloudEvent:
    return CloudEvent(
        type="my.model-acknowledged.v1",
        data=value,
    )


@app.post("/model-response")
async def on_event(value: MyModel) -> MyModel:
    return value

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004)
