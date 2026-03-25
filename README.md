# Inventory Management System (IMS)

A Python CLI application for managing warehouse inventory, built with MySQL.

![CI](https://github.com/<your-username>/ims/actions/workflows/ci.yml/badge.svg)

---

## Project Structure

```
ims-project/
├── backend/
│   ├── main.py          # Entry point — menus and app flow
│   ├── db_connect.py    # MySQL connection (reads from .env)
│   ├── login.py         # Authentication with bcrypt
│   ├── register.py      # New user registration
│   ├── inventory.py     # CRUD for inventory items
│   ├── transactions.py  # Transaction log
│   └── admin.py         # User management (admin only)
├── tests/
│   └── test_ims.py      # Pytest unit tests (fully mocked)
├── db/
│   └── schema.sql       # MySQL schema (auto-loaded by Docker)
├── .github/
│   └── workflows/
│       └── ci.yml       # GitHub Actions — lint, test, deploy
├── .env.example         # Template for environment variables
├── .gitignore
├── .flake8
├── pytest.ini
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

---

## Quick Start (Docker — recommended)

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/ims.git
cd ims

# 2. Create your .env file
cp .env.example .env
# Edit .env and set a real DB_PASSWORD

# 3. Start the app + MySQL
docker compose up --build
```

## Quick Start (Local)

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Fill in your DB credentials in .env

# 4. Run the app
cd src
python main.py
```

---

## Running Tests

```bash
pytest
```

Tests use mocks — no live database required.

---

## CI/CD Pipeline (GitHub Actions)

Every push and pull request automatically:
1. **Lints** the code with `flake8`
2. **Tests** on Python 3.10, 3.11, and 3.12 with a real MySQL service container
3. **Deploys** via FTP to the host server on merge to `main`

### Required GitHub Secrets

| Secret | Description |
|---|---|
| `DB_PASSWORD` | MySQL root password used in the CI service container |
| `FTP_SERVER` | Hostname of your deployment server |
| `FTP_USERNAME` | FTP username |
| `FTP_PASSWORD` | FTP password |

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `DB_HOST` | `localhost` | MySQL host |
| `DB_USER` | `root` | MySQL user |
| `DB_PASSWORD` | _(none)_ | MySQL password — **required** |
| `DB_NAME` | `warehouse` | Database name |
