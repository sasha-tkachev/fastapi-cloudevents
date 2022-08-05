# fastapi-cloudevents
[FastAPI](https://fastapi.tiangolo.com/) [Middleware](https://fastapi.tiangolo.com/tutorial/middleware/) for [CloudEvents](https://cloudevents.io/) Integration

install:

```
pip install fastapi-cloudevents
```
   
## Examples

### [Simple Example](examples/simple_server)
```python
import uvicorn
from fastapi import FastAPI

from fastapi_cloudevents import CloudEvent, CloudEventRoute

app = FastAPI()
app.router.route_class = CloudEventRoute


@app.post("/")
async def on_event(event: CloudEvent) -> CloudEvent:
    return CloudEvent(
        type="com.my-corp.response.v1", source="my:source", data=event.data
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

This simple accepts both structured cloudevents (whole event is passed in the
 body) 
```python
import requests
from cloudevents.http import CloudEvent, to_structured

headers, data = to_structured(
    CloudEvent(
        attributes={"type": "com.your-corp.response.v1", "source": "your:source"},
        data={"hello": "world"},
    )
)
print(requests.post("http://localhost:8000", headers=headers, data=data).content)
```
```json
{
  "type":"com.my-corp.response.v1",
  "data":{"hello":"world"},
  "source":"my:source",
  "id":"265b4053-efd6-4f6a-885e-9867dbc80b2a",
  "specversion":"1.0",
  "time":"2022-08-05T21:28:27.675355+00:00"
}
```
And binary cloudevents (only data in passed in the body, while the attributes are
 passed in the header)
```python
import requests
from cloudevents.http import CloudEvent, to_structured

headers, data = to_structured(
    CloudEvent(
        attributes={"type": "com.your-corp.response.v1", "source": "your:source"},
        data={"hello": "world"},
    )
)
print(requests.post("http://localhost:8000", headers=headers, data=data).content)

```

### Binary Responses
To send the response in the http CloudEvent binary format, you MAY use the
 `BinaryCloudEventResponse` class
 
```python
import uvicorn
from fastapi import FastAPI

from fastapi_cloudevents import (BinaryCloudEventResponse, CloudEvent,
                                 CloudEventRoute)

app = FastAPI()
app.router.route_class = CloudEventRoute


@app.post("/", response_class=BinaryCloudEventResponse)
async def on_event(event: CloudEvent) -> CloudEvent:
    return CloudEvent(
        type="com.my-corp.response.v1", source="my:source", data=event.data
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
``` 


```python
import requests
from cloudevents.http import CloudEvent, to_structured

headers, data = to_structured(
    CloudEvent(
        attributes={"type": "com.your-corp.response.v1", "source": "your:source"},
        data={"hello": "world"},
    )
)

response = requests.post("http://localhost:8001", headers=headers, data=data)
print(response.content)
print(response.headers)
```

```json
{"hello": "world"}
```
```json
{
  "ce-source": "your:source", 
  "ce-type": "com.your-corp.response.v1", 
  "ce-time": "2022-08-05T21:56:43.613658+00:00",
  "ce-id": "b4b47632-9d6e-4de2-8415-1533c3e58f27" 
}
```
