import json
import os
import yaml

def read_openapi_spec(file_path: str) -> str:
    """Read an OpenAPI specification (JSON or YAML) and return a concise JSON summary.

    The summary includes title, version, servers, endpoints, and schemas.

    Args:
        file_path: Path to the OpenAPI spec file.

    Returns:
        A JSON-formatted string containing the summary.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Specification file not found: {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            if file_path.lower().endswith((".yaml", ".yml")):
                spec_dict = yaml.safe_load(file)
            else:
                spec_dict = json.load(file)

        paths = spec_dict.get("paths", {})
        components = spec_dict.get("components", {}).get("schemas", {})

        summary = {
            "title": spec_dict.get("info", {}).get("title", "API Spec"),
            "version": spec_dict.get("info", {}).get("version", "1.0.0"),
            "servers": spec_dict.get("servers", []),
            "endpoints": paths,
            "schemas": components,
        }

        return json.dumps(summary, indent=2)
    except Exception as e:
        return f"Error parsing OpenAPI spec: {str(e)}"