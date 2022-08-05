# fastapi-cloudevents
[FastAPI](https://fastapi.tiangolo.com/) [Middleware](https://fastapi.tiangolo.com/tutorial/middleware/) for [CloudEvents](https://cloudevents.io/) Integration


### Install

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
        type="my.response-type.v1", source="my:source", data=event.data,
        datacontenttype=event.datacontenttype
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

```

The rout accepts both binary CloudEvents
```shell script
curl http://localhost:8000 -i -X POST -d "Hello World!" \
  -H "Content-Type: text/plain" \
  -H "ce-specversion: 1.0" \
  -H "ce-type: my.request-type.v1" \
  -H "ce-id: 123" \
  -H "ce-source: my-source"
```

And structured CloudEvents 
```shell script
curl http://localhost:8000 -i -X POST -H "Content-Type: application/json" \
  -d '{"data":"Hello World", "source":"my-source", "id":"123", "type":"my.request-type.v1","specversion":"1.0"}'
```
Both of the requests will yield a response in the same format:
```text
HTTP/1.1 200 OK
date: Fri, 05 Aug 2022 22:48:00 GMT
server: uvicorn
content-length: 235
content-type: application/json

{"data":"Hello World!","source":"my:source","id":"a6318d09-1d89-436b-8b28-a6e56734c050","type":"my.response-type.v1","specversion":"1.0","time":"2022-08-05T22:48:01.492529+00:00","datacontenttype":"text/plain"}
```

### [Binary Response Example](examples/binary_response_server)
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
        type="com.my-corp.response.v1", source="my:source", data=event.data,
        datacontenttype=event.datacontenttype
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
``` 
```shell script
curl http://localhost:8001 -i -X POST -d "Hello World!" \
  -H "Content-Type: text/plain" \
  -H "ce-specversion: 1.0" \
  -H "ce-type: my.request-type.v1" \
  -H "ce-id: 123" \
  -H "ce-source: my-source"

```
```text
HTTP/1.1 200 OK
date: Fri, 05 Aug 2022 22:58:14 GMT
server: uvicorn
content-length: 14
content-type: text/plain
ce-specversion: 1.0
ce-id: 67f30e64-772d-4395-8939-c7d994dba0a4
ce-source: my:source
ce-type: com.my-corp.response.v1
ce-time: 2022-08-05T22:58:14.648649+00:00

"Hello World!"
```
