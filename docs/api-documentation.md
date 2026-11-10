# SMART BUILD – API Documentation

The SMART BUILD backend is constructed using **Python FastAPI**, delivering high-performance, asynchronous REST APIs with automatic OpenAPI (Swagger UI) documentation.

Interactive Swagger UI: `http://localhost:8000/api/docs`  
ReDoc UI: `http://localhost:8000/api/redoc`

---

## 1. System & Health Endpoints

### GET `/api/health`
Returns system status, service name, version, and running environment.

**Response:**
```json
{
  "status": "healthy",
  "service": "SMART BUILD - AI-Powered Construction Material Ordering System",
  "version": "1.0.0",
  "environment": "development"
}
```

### GET `/api/db-check`
Runs a live query against the active database engine (MySQL with SQLite local fallback) and confirms registration and schema integrity across all 24 database tables.

**Response:**
```json
{
  "status": "connected",
  "database": "online",
  "test_query": 1,
  "registered_tables_count": 24,
  "tables": [
    "users", "customer_profiles", "supplier_profiles", "delivery_partner_profiles",
    "categories", "products", "product_images", "inventory",
    "carts", "cart_items", "addresses", "orders",
    "order_items", "payments", "deliveries", "reviews",
    "wishlists", "wishlist_items", "notifications", "complaints",
    "price_history", "ai_estimations", "ai_predictions", "audit_logs"
  ]
}
```

---

## 2. API Route Modules (Architecture Spec)

| Router Prefix | Primary Responsibility | Target Actors |
| :--- | :--- | :--- |
| `/api/auth` | User registration, login, token refresh, and profile retrieval | All Users |
| `/api/users` | Profile updates, password changes, notification management | Authenticated Users |
| `/api/categories` | Catalog category listing, creation, and updates | Public / Admin |
| `/api/products` | Material discovery, search, filtering, and CRUD operations | Public / Supplier / Admin |
| `/api/inventory` | Real-time stock status, low-stock alerts, restock updates | Supplier / Admin |
| `/api/cart` | Shopping cart manipulation, quantity updates, total calculation | Customer |
| `/api/orders` | Checkout, order creation, transaction status tracking | Customer / Supplier / Admin |
| `/api/payments` | Razorpay sandbox order generation and cryptographic verification | Customer |
| `/api/deliveries` | Shipment assignment, status transitions, driver confirmation | Delivery Partner / Customer |
| `/api/reviews` | Rating submissions and verified customer feedback | Customer / Public |
| `/api/wishlist` | Saved favorite materials management | Customer |
| `/api/estimator` | AI construction material calculations and estimation history | Customer / Admin |
| `/api/admin` | User moderation, supplier vetting, product approvals, and reports | Administrator |
| `/api/analytics` | Sales performance, revenue trends, and inventory metrics | Supplier / Admin |
