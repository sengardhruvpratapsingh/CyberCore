# CyberCore

CyberCore is a local-first cyber-fraud investigation platform for organizing cases, processing evidence, and reviewing risk signals, timelines, entity relationships, and investigation reports.

## Requirements

- Python 3.11 or later
- A modern web browser
- Optional: Ollama for local Copilot tool selection

## Run locally

Start the backend from the repository root:

```powershell
cd backend
..\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Serve the static frontend in a second terminal:

```powershell
python -m http.server 5500 --bind 127.0.0.1 --directory frontend
```

Open <http://127.0.0.1:5500/>. The API and interactive documentation are available at <http://127.0.0.1:8000/> and <http://127.0.0.1:8000/docs>.

The backend creates a local SQLite database at `backend/cybercore.db`; uploaded evidence and generated reports are stored locally under `backend/uploads/` and `backend/reports/`.

## Local Copilot

Start Ollama and load the configured local model:

```powershell
ollama serve
ollama pull qwen3.5:9b-q4_K_M
```

The backend uses these environment variables:

```powershell
$env:CYBERCORE_SLM_ENABLED = "true"
$env:CYBERCORE_SLM_MODEL = "qwen3.5:9b-q4_K_M"
$env:OLLAMA_BASE_URL = "http://localhost:11434"
```

Set `CYBERCORE_SLM_ENABLED` to `false` to use the deterministic offline Copilot directly. If Ollama is unavailable, times out, or returns invalid tool JSON, Copilot falls back automatically.

## Tests

Run the backend tests from the repository root:

```powershell
cd backend
..\.venv\Scripts\python.exe -m unittest discover -s tests
```

## Deploy to Render

The root `render.yaml` Blueprint defines separate `cybercore-api` and
`cybercore-frontend` services. In Render, create a new Blueprint from this
repository and deploy the `main` branch. The frontend build receives the API
hostname from the backend service and writes it into `api-config.js`.

The free backend is for demos with synthetic data only. It has no application
authentication, its filesystem is ephemeral, and uploaded evidence, reports,
and the SQLite database can be lost when the service restarts or spins down.
Do not upload real or sensitive case data.
