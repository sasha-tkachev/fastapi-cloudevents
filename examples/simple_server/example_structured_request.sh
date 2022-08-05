curl http://localhost:8000 -i -X POST -H "Content-Type: application/json" \
  -d '{"data":"Hello World", "source":"my-source", "id":"123", "type":"my.request-type.v1","specversion":"1.0"}'
