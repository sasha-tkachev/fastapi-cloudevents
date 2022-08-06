# fastapi-cloudevents
[FastAPI](https://fastapi.tiangolo.com/) [Middleware](https://fastapi.tiangolo.com/tutorial/middleware/) for [CloudEvents](https://cloudevents.io/) Integration


### Install
This package currently cannot be installed directly from pypi. 
The reason for it is because it requires the unreleased [pydantic feature](https://github.com/cloudevents/sdk-python/issues/181) in the
 [cloudevents python sdk](https://github.com/cloudevents/sdk-python)  

If you wish to try out the beta version use
```
pip install fastapi-cloudevents --no-deps
```
and install the [development branch of the pydantic feature](https://github.com/cloudevents/sdk-python/pull/182)


   
## Examples

### [Simple Example](examples/simple_server)
```python
import uvicorn
from fastapi import FastAPI

from fastapi_cloudevents import CloudEvent, install_fastapi_cloudevents

app = FastAPI()
app = install_fastapi_cloudevents(app)


@app.post("/")
async def on_event(event: CloudEvent) -> CloudEvent:
    return CloudEvent(
        type="my.response-type.v1",
        data=event.data,
        datacontenttype=event.datacontenttype,
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
date: Fri, 05 Aug 2022 23:50:52 GMT
server: uvicorn
content-length: 13
content-type: application/json
ce-specversion: 1.0
ce-id: 25cd28f0-0605-4a76-b1d8-cffbe3375413
ce-source: http://localhost:8000/
ce-type: my.response-type.v1
ce-time: 2022-08-05T23:50:52.809697+00:00

"Hello World"
```

### [CloudEvent Type Routing](examples/type_routing)
```python
from typing import Literal, Union

import uvicorn
from fastapi import FastAPI
from pydantic import Field
from typing_extensions import Annotated

from fastapi_cloudevents import (CloudEvent, StructuredCloudEventResponse,
                                 install_fastapi_cloudevents)

app = FastAPI()
app = install_fastapi_cloudevents(
    app, default_response_class=StructuredCloudEventResponse
)


class MyEvent(CloudEvent):
    type: Literal["my.type.v1"]


class YourEvent(CloudEvent):
    type: Literal["your.type.v1"]


OurEvent = Annotated[Union[MyEvent, YourEvent], Field(discriminator="type")]

_source = "dummy:source"


@app.post("/")
async def on_event(event: OurEvent) -> CloudEvent:
    if isinstance(event, MyEvent):
        return CloudEvent(
            type="my.response-type.v1",
            data=f"got {event.data} from my event!",
            datacontenttype="text/plain",
        )
    else:
        return CloudEvent(
            type="your.response-type.v1",
            data=f"got {event.data} from your event!",
            datacontenttype="text/plain",
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
```

### [Structured Response Example](examples/structured_response_server)
To send the response in the http CloudEvent structured format, you MAY use the
 `BinaryCloudEventResponse` class
 
```python
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
date: Fri, 05 Aug 2022 23:51:26 GMT
server: uvicorn
content-length: 247
content-type: application/json

{"data":"Hello World!","source":"http://localhost:8001/","id":"3412321f-85b3-4f7f-a551-f4c23a05de3a","type":"com.my-corp.response.v1","specversion":"1.0","time":"2022-08-05T23:51:26.878723+00:00","datacontenttype":"text/plain"}
```

## More Examples
* [Custom Source Tags](examples/custom_source_tag)