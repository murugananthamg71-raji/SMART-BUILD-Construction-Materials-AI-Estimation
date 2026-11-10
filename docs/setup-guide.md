# SMART BUILD – Setup and Installation Guide

This guide walks you through running SMART BUILD locally on Windows 11 with VS Code and PowerShell.

---

## Prerequisites

- **Python**: 3.10 to 3.14+
- **Node.js**: v18.0.0+ (Tested on v26+)
- **MySQL Server**: 8.0+ (Optional for local development; system seamlessly falls back to SQLite `smart_build.db` if MySQL is unavailable)

---

## 1. Backend Setup

1. Open PowerShell and navigate to the `backend` folder:
   ```powershell
   cd backend
   ```

2. Activate the virtual environment:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

3. Ensure dependencies are installed:
   ```powershell
   pip install -r requirements.txt
   ```

4. Configure environment variables in `backend/.env`:
   ```ini
   ENVIRONMENT=development
   DEBUG=true
   SECRET_KEY=smart_build_jwt_secret_key_change_in_production_2026_xyz!
   DATABASE_URL=mysql+pymysql://root:password@localhost:3306/smart_build
   USE_SQLITE_FALLBACK=true
   ```

5. Run database migrations:
   ```powershell
   alembic upgrade head
   ```

6. Start the FastAPI backend server:
   ```powershell
   uvicorn app.main:app --reload --port 8000
   ```
   Interactive Swagger documentation will be available at: `http://localhost:8000/api/docs`

---

## 2. Frontend Setup

1. Open a second PowerShell window and navigate to the `frontend` directory:
   ```powershell
   cd frontend
   ```

2. Install frontend dependencies:
   ```powershell
   npm install
   ```

3. Start the Vite React development server:
   ```powershell
   npm run dev
   ```
   The application will be accessible at: `http://localhost:5173`

---

## 3. Running Automated Tests

Run backend tests using Pytest:
```powershell
cd backend
.\venv\Scripts\pytest -v
```
