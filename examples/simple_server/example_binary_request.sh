curl http://localhost:8000 -i -X POST -d "Hello World!" \
  -H "Content-Type: text/plain" \
  -H "ce-specversion: 1.0" \
  -H "ce-type: my.request-type.v1" \
  -H "ce-id: 123" \
  -H "ce-source: my-source"
