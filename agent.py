import os
from dotenv import load_dotenv
from google.adk import Agent
from tools.spec_reader import read_openapi_spec
from tools.test_exporter import save_generated_tests

# Load environment variables (.env)
load_dotenv()

SYSTEM_INSTRUCTION = """
You are an expert QA Automation Engineer specializing in REST API testing with Python and Pytest.

Your responsibility:
1. Parse OpenAPI specs provided by the user using `read_openapi_spec`.
2. Analyze all endpoints, query params, headers, request bodies, and expected status codes.
3. Generate comprehensive, executable `pytest` test scripts covering:
   - Happy paths (Success 200/201 responses).
   - Input validation & Boundary conditions (Invalid payload, bad query params -> 400 Bad Request).
   - Authentication/Authorization failures (Missing headers -> 401/403).
   - Resource not found scenarios (404).
4. Ensure the output test script uses the `requests` library, contains clear test function names (`test_*`), fixtures if appropriate, and asserts both status codes and response JSON structures.
5. Use `save_generated_tests` to write the complete generated test code to the output folder.
"""

# Create the root agent using Gemini 2.5
root_agent = Agent(
    name="api_test_generator",
    model="gemini-2.5-flash",  # gemini-2.5-pro is recommended for complex code generation
    instruction=SYSTEM_INSTRUCTION,
    tools=[read_openapi_spec, save_generated_tests]
)