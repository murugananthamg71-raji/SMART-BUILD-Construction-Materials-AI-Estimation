<div align="center">
  <img src="frontend/public/images/smart-build-logo.png" alt="SMART BUILD Logo" width="220"/>

  <h1>⚡ SMART BUILD</h1>
  <h3>AI-Powered Construction Materials Ordering & Estimation Platform</h3>

  <p>
    <a href="https://smart-build-online.vercel.app"><img src="https://img.shields.io/badge/🌐_Live_App-smart--build--online.vercel.app-0EA5E9?style=for-the-badge&logo=vercel" alt="Live App"/></a>
    &nbsp;
    <a href="https://smart-build-backend.onrender.com/api/docs"><img src="https://img.shields.io/badge/📡_API_Docs-smart--build--backend.onrender.com-10B981?style=for-the-badge&logo=fastapi" alt="API Docs"/></a>
  </p>

  <p>
    <img src="https://img.shields.io/badge/React-19-61DAFB?style=flat-square&logo=react" />
    <img src="https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi" />
    <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python" />
    <img src="https://img.shields.io/badge/Tailwind_CSS-3.4-06B6D4?style=flat-square&logo=tailwindcss" />
    <img src="https://img.shields.io/badge/MySQL-8.0-4479A1?style=flat-square&logo=mysql" />
    <img src="https://img.shields.io/badge/Deployed-Vercel_%2B_Render-black?style=flat-square" />
  </p>
</div>

---

## 🏗️ System Architecture

> Full-stack cloud-deployed marketplace with AI estimation engine, role-based access, and real-time order management.

![SMART BUILD System Architecture](docs/architecture.png)

| Layer | Technology | Hosting |
|-------|-----------|---------|
| **Frontend** | React 19 + Vite + Tailwind CSS | ▲ Vercel CDN (Global Edge) |
| **API Gateway** | Vercel Rewrite Proxy (`vercel.json`) | ▲ Vercel Serverless |
| **Backend** | Python FastAPI + Uvicorn | 🟣 Render (Auto-deploy) |
| **Database** | SQLite (dev) / MySQL 8.0+ (prod) | ☁️ Cloud Managed DB |
| **AI / ML** | Civil Engineering Rules Engine | Embedded in Backend |
| **Auth** | JWT Bearer Token + bcrypt | Stateless / Role-based |
| **CI/CD** | GitHub → Render + Vercel auto-deploy | 🐙 GitHub `main` branch |

---

## 🚀 Live Deployment

| Service | URL | Status |
|---------|-----|--------|
| 🌐 **Frontend** | [smart-build-online.vercel.app](https://smart-build-online.vercel.app) | ✅ Live |
| 📡 **Backend API** | [smart-build-backend.onrender.com](https://smart-build-backend.onrender.com) | ✅ Live |
| 📖 **Swagger Docs** | [/api/docs](https://smart-build-backend.onrender.com/api/docs) | ✅ Live |
| ❤️ **Health Check** | [/health](https://smart-build-backend.onrender.com/health) | ✅ Healthy |

---

## 🎯 What is SMART BUILD?

**SMART BUILD** is an intelligent full-stack online marketplace that connects:

- 🏗️ **Customers / Builders** — Browse 66+ construction materials, compare prices, place orders, track deliveries, get AI-powered material estimates for their construction projects.
- 🏪 **Material Suppliers** — List products, manage inventory, fulfill orders, view analytics via a dedicated vendor portal.
- 🚚 **Delivery Partners** — Accept delivery assignments, update delivery status in real time.
- 🛡️ **Administrators** — Manage users, approve suppliers, oversee the marketplace, view audit logs.

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🤖 **AI BOQ Estimator** | Input project area & type → AI calculates exact quantities & costs for 66+ materials using civil engineering rules |
| 🛒 **Smart Marketplace** | Browse, filter, and compare products by category, price, supplier rating |
| 📦 **Order Management** | End-to-end order lifecycle: cart → checkout → payment → fulfillment → delivery |
| 🔐 **Role-Based Auth** | Separate portals for Customer, Material Supplier, Delivery Partner, Admin with strict routing |
| 💳 **Payment Integration** | Secure transaction-safe payment processing |
| ⭐ **Reviews & Ratings** | Customer reviews on products and supplier performance ratings |
| 🔔 **Notifications** | Real-time order status and system notifications |
| 🗺️ **Delivery Tracking** | Live delivery status tracking for customers |
| 📊 **Admin Dashboard** | Full marketplace oversight, user management, approval workflows |
| 🏪 **Supplier Portal** | Dedicated vendor dashboard for product listing, inventory, and order fulfillment |

---

## 🗂️ Project Structure

```
smart-build-web-app/
├── backend/                          # Python FastAPI backend
│   ├── alembic/                      # Database version migrations
│   │   └── versions/
│   ├── app/
│   │   ├── ai/                       # AI BOQ estimation engine
│   │   │   ├── estimator.py          # Civil engineering rules engine
│   │   │   └── material_calculator.py
│   │   ├── core/                     # App config, security, dependencies
│   │   │   ├── config.py
│   │   │   ├── security.py           # JWT + bcrypt
│   │   │   └── dependencies.py
│   │   ├── database/                 # DB session, base, seeder
│   │   │   ├── session.py
│   │   │   ├── base.py
│   │   │   └── seed.py               # Auto-seeds 66 materials on startup
│   │   ├── models/                   # 24 SQLAlchemy ORM models
│   │   ├── routers/                  # FastAPI REST endpoints (24 routes)
│   │   │   ├── auth.py
│   │   │   ├── products.py
│   │   │   ├── orders.py
│   │   │   ├── cart.py
│   │   │   ├── ai_estimation.py
│   │   │   └── ...
│   │   ├── schemas/                  # Pydantic v2 request/response schemas
│   │   ├── services/                 # Business logic layer
│   │   └── main.py                   # App entry point, lifespan, CORS
│   ├── tests/                        # pytest test suites
│   ├── requirements.txt
│   ├── alembic.ini
│   └── .env.example
│
├── frontend/                         # React 19 + Vite frontend
│   ├── public/
│   │   ├── images/
│   │   │   ├── smart-build-logo.png  # Official logo
│   │   │   └── materials/            # 66 material images
│   │   └── manifest.json             # PWA manifest
│   ├── src/
│   │   ├── components/               # Reusable UI components
│   │   │   ├── layout/               # Navbar, Footer, Sidebar
│   │   │   └── ui/                   # Cards, Modals, Buttons
│   │   ├── context/
│   │   │   └── AuthContext.jsx       # Global auth state (JWT + roles)
│   │   ├── pages/
│   │   │   ├── auth/
│   │   │   │   ├── LoginPage.jsx     # Role-selector: Customer | Supplier
│   │   │   │   └── RegisterPage.jsx  # Role-based registration form
│   │   │   ├── customer/             # Customer dashboard & marketplace
│   │   │   ├── supplier/             # Material Supplier vendor portal
│   │   │   ├── admin/                # Admin control panel
│   │   │   └── delivery/             # Delivery partner portal
│   │   ├── services/
│   │   │   └── api.js                # Axios instance with JWT interceptors
│   │   ├── App.jsx                   # Route definitions + protected routes
│   │   └── main.jsx
│   ├── vercel.json                   # API proxy rewrite rules
│   ├── vite.config.js
│   └── package.json
│
├── database/
│   └── smart_build.sql               # MySQL 8.0+ DDL — 24 tables
│
├── docs/
│   ├── architecture.png              # System architecture diagram
│   ├── architecture.md               # Detailed architecture notes
│   ├── database-erd.md               # ERD & table specifications
│   ├── api-documentation.md          # Endpoint reference
│   └── setup-guide.md                # Local dev setup guide
│
├── render.yaml                       # Render cloud deployment blueprint
└── README.md
```

---

## 🗄️ Database Schema — 24 Normalized Tables

```
┌─────────────────────┬──────────────────────────┬──────────────────────────┐
│   USERS & PROFILES  │   PRODUCTS & INVENTORY   │   ORDERS & PAYMENTS      │
├─────────────────────┼──────────────────────────┼──────────────────────────┤
│ users               │ categories               │ orders                   │
│ customer_profiles   │ products                 │ order_items              │
│ supplier_profiles   │ product_images           │ payments                 │
│ delivery_profiles   │ inventory                │ deliveries               │
│                     │ price_history            │ complaints               │
├─────────────────────┼──────────────────────────┼──────────────────────────┤
│   CART & WISHLIST   │   AI & ANALYTICS         │   ENGAGEMENT             │
├─────────────────────┼──────────────────────────┼──────────────────────────┤
│ carts               │ ai_estimations           │ reviews                  │
│ cart_items          │ ai_predictions           │ notifications            │
│ addresses           │ audit_logs               │ wishlists                │
│                     │                          │ wishlist_items           │
└─────────────────────┴──────────────────────────┴──────────────────────────┘
```

---

## 🤖 AI BOQ Estimation Engine

The AI engine estimates **Bill of Quantities (BOQ)** for construction projects:

```
Input:
  ├── Project Type  → Residential / Commercial / Industrial
  ├── Built-up Area → sq.ft or sq.m
  ├── No. of Floors
  └── Location      → Coimbatore, Tamil Nadu

Output (66+ Materials):
  ├── 🧱 Cement        (bags)   — OPC 53 Grade
  ├── 🏗️ Steel TMT     (kg)     — Fe500D
  ├── 🏜️ River Sand    (cft)
  ├── 🪨 Blue Metal    (cft)    — 20mm & 12mm
  ├── 🧱 Red Bricks    (nos)
  ├── 🏠 Roofing Tiles (sq.ft)
  ├── 🚰 PVC Pipes     (mtr)
  └── ... 60 more materials with quantities & estimated costs
```

---

## 🔐 Authentication & Role Routing

```
Login Flow:
  ┌──────────────┐     ┌──────────────────────┐
  │ Login Page   │────▶│ Select Role Tab       │
  │ /login       │     │  Customer / Builder   │
  └──────────────┘     │  Material Supplier    │
                       └──────────┬───────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              ▼                   ▼                   ▼
     /customer/dashboard   /supplier/dashboard   /admin/dashboard
     (Customers only)      (Suppliers only)      (Admins only)
              │
     ⛔ Supplier account trying
        to access Customer portal
        → Blocked + Warning shown
```

**Demo Credentials:**

| Role | Email | Password |
|------|-------|----------|
| 🏪 Material Supplier | `supplier@smartbuild.com` | `Demo1234!` |
| 👷 Customer | `customer@smartbuild.com` | `Demo1234!` |

---

## 🛠️ Local Development Setup

### Prerequisites
- Node.js 18+ and npm
- Python 3.11+
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/murugananthamg71-raji/SMART-BUILD-Construction-Materials-AI-Estimation.git
cd SMART-BUILD-Construction-Materials-AI-Estimation
```

### 2. Backend Setup
```powershell
cd backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database credentials

# Run database migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload --port 8000
```

📖 Swagger UI: [http://localhost:8000/api/docs](http://localhost:8000/api/docs)

### 3. Frontend Setup
```powershell
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env.local
# Set VITE_API_BASE_URL=http://localhost:8000

# Start dev server
npm run dev
```

🌐 Web App: [http://localhost:5173](http://localhost:5173)

### 4. Run Tests
```powershell
cd backend
.\venv\Scripts\Activate.ps1
pytest -v
```

---

## ☁️ Cloud Deployment

### Frontend → Vercel
```bash
cd frontend
npx vercel --prod
```

### Backend → Render
The `render.yaml` blueprint at the repository root configures automatic deployment.

Push to `main` branch → Render auto-deploys the backend.

```yaml
# render.yaml (blueprint)
services:
  - type: web
    name: smart-build-backend
    runtime: python
    buildCommand: pip install -r backend/requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Environment Variables

**Backend (Render → Environment):**
```env
SECRET_KEY=your-jwt-secret-key-here
DATABASE_URL=mysql+pymysql://user:pass@host/dbname
ENVIRONMENT=production
```

**Frontend (Vercel → Environment):**
```env
VITE_API_BASE_URL=https://smart-build-backend.onrender.com
```

---

## 📡 API Reference

Base URL: `https://smart-build-backend.onrender.com`

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `POST` | `/api/auth/register` | Register new user (customer/supplier) | — |
| `POST` | `/api/auth/login` | Login & get JWT token | — |
| `GET` | `/api/auth/me` | Get current user profile | 🔒 JWT |
| `GET` | `/api/products/` | List all products (paginated) | — |
| `GET` | `/api/products/{id}` | Get product details | — |
| `POST` | `/api/cart/items` | Add item to cart | 🔒 JWT |
| `GET` | `/api/cart/` | Get cart contents | 🔒 JWT |
| `POST` | `/api/orders/` | Place an order | 🔒 JWT |
| `GET` | `/api/orders/` | List user orders | 🔒 JWT |
| `POST` | `/api/ai/estimate` | AI BOQ estimation | 🔒 JWT |
| `GET` | `/api/supplier/products` | Supplier's product list | 🔒 Supplier |
| `GET` | `/api/admin/users` | All users (admin only) | 🔒 Admin |

📖 Full interactive docs: [https://smart-build-backend.onrender.com/api/docs](https://smart-build-backend.onrender.com/api/docs)

---

## 👨‍💻 Developer

<div align="center">

**Muruganantham G**  
Full Stack Developer | AI/ML Engineer  
📍 Coimbatore, Tamil Nadu, India

[![GitHub](https://img.shields.io/badge/GitHub-murugananthamg71--raji-181717?style=flat-square&logo=github)](https://github.com/murugananthamg71-raji)

</div>

---

## 📄 License

This project is built for educational and portfolio purposes.  
© 2024 Muruganantham G — SMART BUILD. All rights reserved.

---

<div align="center">
  <sub>Built with ❤️ in Coimbatore · Powered by React, FastAPI, and AI</sub>
</div>
