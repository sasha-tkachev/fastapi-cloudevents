from cloudevents.pydantic import CloudEvent# fastapi-cloudevents
[FastAPI](https://fastapi.tiangolo.com/) [Middleware](https://fastapi.tiangolo.com/tutorial/middleware/) for [CloudEvents](https://cloudevents.io/) Integration

install:

```
pip install fastapi-cloudevents
```
   
example:

```python
import uvicorn
from fastapi import FastAPI

from fastapi_cloudevents.middleware import CloudEventsMiddleware
from cloudevents.pydantic import CloudEvent

app = FastAPI()

app.add_middleware(CloudEventsMiddleware)


@app.post("/api/my-endpoint")
async def on_event(event: CloudEvent) -> CloudEvent:
    return event

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

