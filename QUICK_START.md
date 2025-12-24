# Quick Start Guide

## 1. Start Backend (Terminal 1)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python init_db.py
uvicorn app.main:app --reload
```

Backend: http://localhost:8000

## 2. Start Frontend (Terminal 2)

```bash
cd frontend
./start.sh
```

Frontend: http://localhost:8080

## 3. Access Application

- Dashboard: http://localhost:8080/index.html
- Accounts: http://localhost:8080/accounts.html
- Generator: http://localhost:8080/generator.html
- API Docs: http://localhost:8000/docs

Done! 🚀
