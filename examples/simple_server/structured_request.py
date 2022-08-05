import requests
from cloudevents.http import CloudEvent, to_structured

headers, data = to_structured(
    CloudEvent(
        attributes={"type": "com.your-corp.response.v1", "source": "your:source"}
    )
)
print(requests.post("http://localhost:8000", headers=headers, data=data).content)
