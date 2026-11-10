# SMART BUILD – System Architecture Documentation

**SMART BUILD** is a production-grade, responsive, full-stack online marketplace for construction materials powered by AI estimation engines.

---

## 1. High-Level Architecture Overview

```
                                  +-----------------------+
                                  |      User Layer       |
                                  | Customer | Supplier   |
                                  | Admin    | Delivery   |
                                  +-----------+-----------+
                                              |
                                     (HTTPS / REST JSON)
                                              v
                      +-----------------------------------------------+
                      |          Frontend Layer (React 19 + Vite)     |
                      |  - Pages, Tailwind UI, React Router           |
                      |  - Context API State Management               |
                      |  - Axios Services with JWT Interceptors       |
                      |  - Progressive Web App (PWA) Manifest         |
                      +-----------------------+-----------------------+
                                              |
                                     (REST API / JSON)
                                              v
                      +-----------------------------------------------+
                      |           Backend Layer (Python FastAPI)      |
                      |  - API Gateway & Routers                      |
                      |  - Pydantic v2 Request/Response Validation    |
                      |  - JWT Authentication & Bcrypt Hashing        |
                      |  - Rule-based & ML AI Material Estimator      |
                      |  - Background Tasks & Audit Logger            |
                      +-----------------------+-----------------------+
                                              |
                                       (SQLAlchemy ORM)
                                              v
                      +-----------------------------------------------+
                      |             Database Layer (MySQL 8.0+)       |
                      |  - 24 Normalized Tables                       |
                      |  - Foreign Key Constraints & Cascades         |
                      |  - Composite & Indexed Search Fields          |
                      |  - Alembic Version-controlled Migrations      |
                      +-----------------------------------------------+
                                              |
                               +--------------+--------------+
                               | External Integrations       |
                               | - Razorpay Sandbox Payments |
                               | - Cloud Storage             |
                               | - Maps & Location API       |
                               +-----------------------------+
```

---

## 2. Core Modules

1. **Authentication & Authorization**:
   - Role-based Access Control (RBAC) with 4 discrete roles: `customer`, `supplier`, `admin`, `delivery_partner`.
   - Signed JWT Bearer token authentication with configurable TTL.

2. **Product & Catalog Management**:
   - Tiered hierarchy: Categories -> Products -> Product Images & Inventory.
   - Moderation workflow: Supplier submissions require Admin approval before being publicly indexable.

3. **Cart & Transaction-Safe Order Pipeline**:
   - Stock reservation & optimistic verification on checkout.
   - Server-side tax, delivery fee, and net price re-calculation.

4. **AI Construction Material Estimator**:
   - Deterministic structural civil engineering rule formulas for:
     - Built-up area (Length x Width x Floors)
     - Cement bags (OPC/PPC)
     - TMT Rebar Steel (kg)
     - Standard kiln bricks
     - River/M-sand (tons)
     - Coarse aggregate gravel (tons)
     - Vitrified flooring tiles (sq.ft)
     - Emulsion paint (liters)
   - Quality tiers: Budget, Standard, Premium multipliers.
   - Direct "Add Estimated Materials to Cart" integration.

5. **Delivery Tracking**:
   - Status state-machine: `Assigned` -> `Picked Up` -> `Out for Delivery` -> `Delivered` / `Failed`.
   - Authorized privacy masks for customer contact details.

6. **Admin Dashboard & Business Intelligence**:
   - Platform metrics, approval queues, transaction oversight, user management, and audit trails.
