# 🎨 Frontend - Player Dashboard

This is the graphical user interface of the application. It is an interactive web dashboard built with **Streamlit**, designed to consume the backend API.

## 🚀 Run the application

- [ ] Install all dependencies: `uv sync --project frontend --all-extras`

Then you have to be in the *frontend* folder to launch:

- [ ] `cd frontend`
- [ ] `uv run --project . streamlit run src/app.py --server.port=8000 --server.address=0.0.0.0`


## 🏛️ Architecture

The frontend follows a modular structure to separate UI components from API interaction:

- **Entry point** (`app.py`) : Configures the app and builds the navigation menu depending on whether the user is logged in
- **Pages** (`pages/`) : Individual views (Home and login, Projects, New audit, Audit result, Audits history, Public key, Certificate verification)
- **API Client** (`utils/api_client.py`) : Centralized logic for communicating with the FastAPI backend (adds the `X-Auth-Token` header to every request)
- **Access guard** (`utils/auth_guard.py`) : Redirects to the home page when no access token is stored in the session (the token itself is validated by the backend)
- **Utilities** (`utils/`) : Helpers for logging and environment variables

Here is the structure of the code:

```
frontend/
├── Dockerfile
├── logging_config.yml
├── pyproject.toml
├── README.md
└── src/
    ├── app.py
    ├── assets/
    │   └── logo_cleanops.png
    ├── pages/
    │   ├── home.py
    │   ├── projects.py
    │   ├── new_audit.py
    │   ├── audit_result.py
    │   ├── audits.py
    │   ├── public_key.py
    │   └── verify_certificate.py
    └── utils/
        ├── api_client.py
        ├── auth_guard.py
        ├── env_variables.py
        ├── log_init.py
        └── signature.py
```


## ⚒️ Debugging & Logs

### Logs

The frontend has its own logging system, initialized once per session in `app.py` (`utils/log_init.py`).

- Every call to the backend is logged by `utils/api_client.py`: HTTP method, URL, then status code and reason.
- Logs are written both to the console and to `frontend/logs/frontend.log` (a new file every day at midnight).
- The path is relative: launch Streamlit **from the `frontend/` folder**, otherwise the log file cannot be created.
- The format and the level (`INFO`) are configured in `logging_config.yml`.
- Response bodies are only logged at `DEBUG` level, and never for sensitive requests (login, secret keys, signatures).

### Code quality

The **format on save** with [Ruff](https://docs.astral.sh/ruff/) is enabled by default in the workspace (cf. *.vscode/settings.json*).

To run it manually:

```bash
uv run --project frontend ruff format frontend/
uv run --project frontend ruff check --fix frontend/
```
