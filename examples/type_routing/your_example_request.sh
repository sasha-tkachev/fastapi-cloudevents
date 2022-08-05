curl http://localhost:8002 -X POST -d "Hello World!" \
  -H "Content-Type: text/plain" \
  -H "ce-specversion: 1.0" \
  -H "ce-type: your.type.v1" \
  -H "ce-id: 123" \
  -H "ce-source: your-source"