# SMART BUILD – AI-Powered Construction Material Ordering System

**SMART BUILD** is an intelligent online marketplace connecting customers, construction material suppliers, delivery partners, and administrators. It features an automated AI material estimation engine, price comparisons, dynamic inventory management, and transaction-safe order execution.

---

## Architecture Reference

Built according to the system specification and architectural blueprint:
- **Frontend Layer**: React 19, Vite, Tailwind CSS, Lucide React, Axios, React Router, PWA
- **Backend Layer**: Python, FastAPI, SQLAlchemy 2.0, Pydantic v2, JWT Auth, PyMySQL
- **Database Layer**: MySQL 8.0+ (with SQLite local fallback), 24 normalized tables, Alembic migrations
- **AI/ML Layer**: Civil engineering structural estimation rules engine, Pandas, NumPy, Scikit-learn
- **Deployment Ready**: Vercel (Frontend), Render (Backend), Managed MySQL (Cloud DB)

---

## Project Structure

```
smart-build-web-app/
├── backend/
│   ├── alembic/              # Database version migrations
│   │   └── versions/
│   ├── app/
│   │   ├── ai/               # AI estimation & ML services
│   │   ├── core/             # Configuration, security & dependencies
│   │   ├── database/         # Session management & declarative Base
│   │   ├── models/           # 24 Normalized SQLAlchemy models & enums
│   │   ├── routers/          # FastAPI REST endpoints
│   │   ├── schemas/          # Pydantic validation models
│   │   ├── services/         # Business logic services
│   │   └── main.py           # Application entry point & middleware
│   ├── tests/                # Automated pytest test suites
│   ├── alembic.ini
│   ├── pytest.ini
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── public/               # Static assets & PWA manifest
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   ├── pages/            # Role-based dashboard & marketplace pages
│   │   ├── services/         # Axios API client & endpoints
│   │   ├── App.jsx           # Application root & diagnostics
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── .env.example
├── database/
│   └── smart_build.sql       # Raw MySQL 8.0+ DDL schema with 24 tables
├── docs/
│   ├── architecture.md       # High-level & detailed architecture
│   ├── database-erd.md       # Entity-Relationship diagram & table specifications
│   ├── api-documentation.md  # Endpoints & payload documentation
│   └── setup-guide.md        # Local development setup instructions
└── README.md
```

---

## Database Schema (24 Tables)

1. `users`
2. `customer_profiles`
3. `supplier_profiles`
4. `delivery_partner_profiles`
5. `categories`
6. `products`
7. `product_images`
8. `inventory`
9. `carts`
10. `cart_items`
11. `addresses`
12. `orders`
13. `order_items`
14. `payments`
15. `deliveries`
16. `reviews`
17. `wishlists`
18. `wishlist_items`
19. `notifications`
20. `complaints`
21. `price_history`
22. `ai_estimations`
23. `ai_predictions`
24. `audit_logs`

---

## Quick Start

### 1. Backend
```powershell
cd backend
.\venv\Scripts\Activate.ps1
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```
Swagger UI: `http://localhost:8000/api/docs`

### 2. Frontend
```powershell
cd frontend
npm install
npm run dev
```
Web App: `http://localhost:5173`

### 3. Automated Tests
```powershell
cd backend
.\venv\Scripts\pytest -v
```
