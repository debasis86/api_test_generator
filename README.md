# API Test Generator

> Generate comprehensive **pytest** test suites from an OpenAPI specification using a Gemini LLM agent.

---

## Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Configuration](#configuration)
- [Running the Agent](#running-the-agent)
- [Generated Tests](#generated-tests)
- [Continuous Integration (GitHub Actions)](#continuous-integration-github-actions)
- [Troubleshooting](#troubleshooting)

---

## Overview

The repository contains a **Google Antigravity (ADK) agent** that:
1. Reads an OpenAPI spec (JSON or YAML) via `tools/spec_reader.py`.
2. Generates a concise JSON summary of the API.
3. Passes the summary to a Gemini LLM (`gemini-1.5-flash` by default) to create full‑featured pytest test files.
4. Saves the generated tests to the `output_tests/` folder via `tools/test_exporter.py`.

The workflow is orchestrated by `agent.py` – a thin wrapper that defines the system prompt, the model, and the tools.

---

## Project Structure
```
api_test_generator/
├─ .env                # GEMINI_API_KEY (do not commit)
├─ .gitignore          # ignores venv, __pycache__, .adk, etc.
├─ .github/
│   └─ ci.yml         # GitHub Actions workflow
├─ output_tests/       # Generated pytest files (created at runtime)
├─ specs/              # Example OpenAPI specs
│   └─ petstore_openapi.json
├─ tools/
│   ├─ __init__.py    # (optional) makes tools a package
│   ├─ spec_reader.py  # reads & summarizes OpenAPI specs
│   └─ test_exporter.py# writes generated Python test code
├─ agent.py            # ADK entry point – defines the agent
├─ requirements.txt    # Python dependencies
└─ README.md           # <-- this file
```

---

## Prerequisites
- **macOS / Linux** (the CI runs on Ubuntu)
- **Python 3.11** (required for the `google-generativeai` client)
- A valid **Gemini API key** with access to the chosen model (`gemini-1.5-flash`).

---

## Setup
```bash
# 1. Clone the repository (if you haven't already)
git clone https://github.com/debasis86/api_test_generator.git
cd api_test_generator

# 2. Create a virtual environment using Python 3.11
python3.11 -m venv venv
source venv/bin/activate

# 3. Upgrade pip and install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt
```
> **Note:** The CI workflow uses the same commands.

---

## Configuration
Create a `.env` file at the project root (already present in the repo) and add your Gemini key:
```
# .env
GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
```
The `dotenv` package automatically loads this variable when you run the agent.

---

## Running the Agent
The agent can be invoked in two ways. The **recommended** way is to point ADK at the **project folder**, which ensures the `tools` package is on the import path.

```bash
# From the repository root (venv must be activated)
adk run .
```
You will be dropped into an interactive CLI. Example query:
```
> Generate pytest tests for the OpenAPI spec at specs/petstore_openapi.json
```
The LLM will produce a `test_petstore_api.py` file inside `output_tests/`.

If you prefer a one‑shot non‑interactive run, you can pipe a query:
```bash
echo "Generate pytest tests for specs/petstore_openapi.json" | adk run .
```

---

## Generated Tests
- All test files are placed under `output_tests/`.
- Each file follows the pattern `test_<service>_api.py` and uses the **requests** library.
- You can run the tests with `pytest output_tests/`.

---

## Continuous Integration (GitHub Actions)
The repository ships a CI workflow (`.github/ci.yml`) that:
1. Checks out the code.
2. Sets up Python 3.11.
3. Creates a virtual environment and installs dependencies.
4. Executes the agent (`adk run agent.py`).

> **Important:** The workflow expects a secret named `GEMINI_API_KEY` to be added in the repository settings.

---

## Troubleshooting
| Issue | Fix |
|-------|-----|
| `ImportError: cannot import name 'read_openapi_spec'` | Ensure `tools/spec_reader.py` contains the correct `read_openapi_spec` function (the file is already fixed). |
| `Model not available` | Update `agent.py` to use a supported model, e.g. `gemini-1.5-flash` (already done). |
| `adk run .` says *directory is a file* | Run the command from the **project root** and pass `.` (the folder), not `agent.py`. |
| Missing GEMINI_API_KEY | Add it to `.env` locally or as a secret in GitHub Actions. |
| Dependencies failing | Re‑install with `pip install -r requirements.txt` inside the active venv. |

---

