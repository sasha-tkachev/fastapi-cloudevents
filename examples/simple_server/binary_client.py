import requests
from cloudevents.http import CloudEvent, to_binary

headers, data = to_binary(
    CloudEvent(
        attributes={"type": "com.your-corp.response.v1", "source": "your:source"},
        data={"hello": "world"},
    )
)
print(requests.post("http://localhost:8000", headers=headers, data=data).content)
