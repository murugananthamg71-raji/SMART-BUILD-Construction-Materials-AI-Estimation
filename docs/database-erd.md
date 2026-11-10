# SMART BUILD – Database Entity-Relationship Specification

## 1. Relational Schema Structure (24 Tables)

```mermaid
erDiagram
    users ||--o| customer_profiles : has
    users ||--o| supplier_profiles : has
    users ||--o| delivery_partner_profiles : has
    users ||--o{ addresses : owns
    users ||--o| carts : possesses
    users ||--o| wishlists : possesses
    users ||--o{ orders : places
    users ||--o{ reviews : writes
    users ||--o{ notifications : receives
    users ||--o{ complaints : files
    users ||--o{ ai_estimations : creates
    users ||--o{ audit_logs : logs

    categories ||--o{ products : categorizes
    supplier_profiles ||--o{ products : supplies
    products ||--o| inventory : tracks
    products ||--o{ product_images : has
    products ||--o{ price_history : logs
    products ||--o{ reviews : receives

    carts ||--o{ cart_items : contains
    products ||--o{ cart_items : referenced_in

    wishlists ||--o{ wishlist_items : contains
    products ||--o{ wishlist_items : referenced_in

    orders ||--o{ order_items : contains
    orders ||--o{ payments : processed_by
    orders ||--o| deliveries : dispatched_via
    orders ||--o{ complaints : linked_to
    addresses ||--o{ orders : delivers_to

    products ||--o{ order_items : ordered_as
    supplier_profiles ||--o{ order_items : fulfills
    delivery_partner_profiles ||--o{ deliveries : executes
```

## 2. Table Summary

| Table | Description | Primary Key | Foreign Keys |
| :--- | :--- | :--- | :--- |
| `users` | Base identity, role-based auth & status | `id` | - |
| `customer_profiles` | Additional profile data for retail & contractor buyers | `id` | `user_id` -> `users.id` |
| `supplier_profiles` | Verified seller information, tax & approval state | `id` | `user_id` -> `users.id` |
| `delivery_partner_profiles` | Courier details, vehicle type & availability | `id` | `user_id` -> `users.id` |
| `categories` | Material classification hierarchy | `id` | - |
| `products` | Construction materials catalog | `id` | `supplier_id`, `category_id` |
| `product_images` | Gallery & primary asset URLs | `id` | `product_id` -> `products.id` |
| `inventory` | Real-time stock, reserved inventory, thresholds | `id` | `product_id` -> `products.id` |
| `carts` | User active shopping carts | `id` | `user_id` -> `users.id` |
| `cart_items` | Quantity & unit price snapshots | `id` | `cart_id`, `product_id` |
| `addresses` | Multi-address book (billing/shipping/site) | `id` | `user_id` -> `users.id` |
| `orders` | Transaction master records | `id` | `user_id`, `delivery_address_id` |
| `order_items` | Line items with quantity & unit price | `id` | `order_id`, `product_id`, `supplier_id` |
| `payments` | Gateway transactions, signatures & statuses | `id` | `order_id`, `user_id` |
| `deliveries` | Real-time shipment status, tracking & POD | `id` | `order_id`, `delivery_partner_id` |
| `reviews` | Verified product feedback & 1-5 ratings | `id` | `product_id`, `user_id` |
| `wishlists` | Customer saved items | `id` | `user_id` -> `users.id` |
| `wishlist_items` | Wishlist product entries | `id` | `wishlist_id`, `product_id` |
| `notifications` | Targeted event alerts & status updates | `id` | `user_id` -> `users.id` |
| `complaints` | Customer support tickets & disputes | `id` | `user_id`, `order_id` |
| `price_history` | Audit log of supplier price adjustments | `id` | `product_id`, `changed_by_user_id` |
| `ai_estimations` | User estimation history, inputs & computed quantities | `id` | `user_id` -> `users.id` |
| `ai_predictions` | Predictive ML cache (price trend, demand forecast) | `id` | `product_id`, `category_id` |
| `audit_logs` | Admin action audits for security & compliance | `id` | `user_id` -> `users.id` |
