import yaml
from main import app

openapi_schema = app.openapi()

with open("openapi.yaml", "w", encoding="utf-8") as f:
    yaml.dump(openapi_schema, f, sort_keys=False, allow_unicode=True)