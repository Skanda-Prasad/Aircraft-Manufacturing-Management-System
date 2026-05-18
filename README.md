# Aircraft Management (Streamlit)

Refactored Streamlit app for managing aircraft models, components, suppliers, customers, and orders.

Quick start

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Configure database connection via environment variables (optional):

```bash
export DB_HOST=localhost
export DB_USER=dbms
export DB_PASSWORD=1234
export DB_NAME=dbms_project
```

3. Run the app with Streamlit:

```bash
streamlit run frontend.py
```

Files

- `frontend.py`: small launcher that runs the app (keeps original entry filename)
- `app.py`: main Streamlit app (menu + wiring)
- `db.py`: DB connection and `execute_query`
- `auth.py`: authentication helpers
- `aircraft_models.py`, `suppliers.py`, `customers.py`, `orders.py`: feature modules
- `tables.sql`: provided SQL schema (unchanged)

Notes

- The DB credentials default to the values found in the original script. Override with environment variables for production.
- This refactor splits functionality into modules for easier maintenance and GitHub upload.

CI and Container

- A GitHub Actions workflow is included at `.github/workflows/ci.yml` to run the test suite on push and PRs.
- A `Dockerfile` is provided to run the app in a container. Build and run with:

```bash
docker build -t aircraft-mgmt .
docker run -p 8501:8501 aircraft-mgmt
```
