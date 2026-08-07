import json
import os
import yaml

def read_openai_spec(file_path:str)->str:
    """
    Reads an OpenAPI specification file (JSON or YAML format) and extracts 
    its path, method, schema, parameters, and response structures.

    Args:
        file_path (str): Relative or absolute path to the OpenAPI spec file.

    Returns:
        str: JSON string containing the extracted API endpoints and schemas.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Specification file not found: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            if file_path.endswith(('.yaml','.yml')):
                spec_dict = yaml.safe_load(file)
            else:
                spec_dict = json.load(file)

        # Extract high level summary to prevent overhelming LLM context window
        paths = spec_dict.get("paths",{})
        components = spec_dict.get("components",{}).get("schemas",{})

        summary = {
            "title": spec_dict.get("info", {}).get("title", "API Spec"),
            "version": spec_dict.get("info", {}).get("version", "1.0.0"),
            "servers": spec_dict.get("servers", []),
            "endpoints": paths,
            "schemas": components
        }

        return json.dumps(summary, indent =2)

    except Exception as e:
        return f"Error parsing OpenAPI spec: {str(e)}"

    
    

        
                
                