# EdgeGuard

Final interactive project build for:

**EdgeGuard: An Adaptive Privacy-Preserving Gateway for Secure Industrial LLM Integration**

## Run

```powershell
cd C:\Users\nisar\Documents\Codex\EdgeGuard
C:\Users\nisar\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe run_edgeguard_app.py
```

Then open:

```text
http://127.0.0.1:8080
```

## Online fallback

This build supports:

- primary live backend via `OPENAI_*`
- secondary online fallback via `ONLINE_FALLBACK_*`
- final offline grounded fallback

Example Ollama config lives in `.env`.
