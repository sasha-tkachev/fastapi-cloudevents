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
