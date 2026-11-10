-- ========================================================================
-- SMART BUILD – AI-Powered Construction Material Ordering System
-- Database Schema (MySQL 8.0+)
-- Architecture: 24 Normalized Tables with Foreign Keys and Indexes
-- ========================================================================

CREATE DATABASE IF NOT EXISTS `smart_build` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `smart_build`;

SET FOREIGN_KEY_CHECKS = 0;

-- 1. Users Table
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(150) NOT NULL,
    `email` VARCHAR(255) NOT NULL UNIQUE,
    `hashed_password` VARCHAR(255) NOT NULL,
    `phone` VARCHAR(20) NULL,
    `role` ENUM('customer', 'supplier', 'admin', 'delivery_partner') NOT NULL DEFAULT 'customer',
    `is_active` BOOLEAN NOT NULL DEFAULT TRUE,
    `is_verified` BOOLEAN NOT NULL DEFAULT FALSE,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX `idx_users_email` (`email`),
    INDEX `idx_users_role` (`role`)
) ENGINE=InnoDB;

-- 2. Customer Profiles
DROP TABLE IF EXISTS `customer_profiles`;
CREATE TABLE `customer_profiles` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL UNIQUE,
    `avatar_url` VARCHAR(500) NULL,
    `company_name` VARCHAR(200) NULL,
    `gst_number` VARCHAR(50) NULL,
    `preferences` TEXT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `fk_cust_profile_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 3. Supplier Profiles
DROP TABLE IF EXISTS `supplier_profiles`;
CREATE TABLE `supplier_profiles` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL UNIQUE,
    `company_name` VARCHAR(200) NOT NULL,
    `business_license` VARCHAR(100) NULL,
    `tax_id` VARCHAR(100) NULL,
    `address` VARCHAR(255) NOT NULL,
    `city` VARCHAR(100) NOT NULL,
    `state` VARCHAR(100) NOT NULL,
    `postal_code` VARCHAR(20) NOT NULL,
    `approval_status` ENUM('pending', 'approved', 'rejected') NOT NULL DEFAULT 'pending',
    `rejection_reason` TEXT NULL,
    `rating` FLOAT NOT NULL DEFAULT 0.0,
    `total_reviews` INT NOT NULL DEFAULT 0,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX `idx_supplier_city` (`city`),
    INDEX `idx_supplier_approval` (`approval_status`),
    CONSTRAINT `fk_supp_profile_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 4. Delivery Partner Profiles
DROP TABLE IF EXISTS `delivery_partner_profiles`;
CREATE TABLE `delivery_partner_profiles` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL UNIQUE,
    `vehicle_type` VARCHAR(50) NOT NULL,
    `vehicle_number` VARCHAR(50) NOT NULL,
    `license_number` VARCHAR(100) NOT NULL,
    `is_available` BOOLEAN NOT NULL DEFAULT TRUE,
    `current_location` VARCHAR(255) NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX `idx_deliv_avail` (`is_available`),
    CONSTRAINT `fk_deliv_partner_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 5. Categories
DROP TABLE IF EXISTS `categories`;
CREATE TABLE `categories` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL UNIQUE,
    `slug` VARCHAR(120) NOT NULL UNIQUE,
    `description` TEXT NULL,
    `image_url` VARCHAR(500) NULL,
    `is_active` BOOLEAN NOT NULL DEFAULT TRUE,
    `display_order` INT NOT NULL DEFAULT 0,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX `idx_cat_slug` (`slug`),
    INDEX `idx_cat_name` (`name`)
) ENGINE=InnoDB;

-- 6. Products
DROP TABLE IF EXISTS `products`;
CREATE TABLE `products` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `supplier_id` INT NOT NULL,
    `category_id` INT NOT NULL,
    `name` VARCHAR(200) NOT NULL,
    `slug` VARCHAR(220) NOT NULL,
    `description` TEXT NULL,
    `brand` VARCHAR(100) NULL,
    `price` DECIMAL(10, 2) NOT NULL,
    `unit` VARCHAR(50) NOT NULL,
    `min_order_quantity` INT NOT NULL DEFAULT 1,
    `is_approved` BOOLEAN NOT NULL DEFAULT FALSE,
    `approval_status` ENUM('pending', 'approved', 'rejected') NOT NULL DEFAULT 'pending',
    `rejection_reason` TEXT NULL,
    `is_active` BOOLEAN NOT NULL DEFAULT TRUE,
    `rating` FLOAT NOT NULL DEFAULT 0.0,
    `total_reviews` INT NOT NULL DEFAULT 0,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX `idx_prod_name` (`name`),
    INDEX `idx_prod_brand` (`brand`),
    INDEX `idx_prod_approval` (`approval_status`),
    INDEX `idx_prod_active` (`is_active`),
    CONSTRAINT `fk_prod_supplier` FOREIGN KEY (`supplier_id`) REFERENCES `supplier_profiles` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_prod_category` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB;

-- 7. Product Images
DROP TABLE IF EXISTS `product_images`;
CREATE TABLE `product_images` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `product_id` INT NOT NULL,
    `image_url` VARCHAR(500) NOT NULL,
    `is_primary` BOOLEAN NOT NULL DEFAULT FALSE,
    `display_order` INT NOT NULL DEFAULT 0,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_prod_img_prod` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 8. Inventory
DROP TABLE IF EXISTS `inventory`;
CREATE TABLE `inventory` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `product_id` INT NOT NULL UNIQUE,
    `stock` INT NOT NULL DEFAULT 0,
    `reserved_stock` INT NOT NULL DEFAULT 0,
    `low_stock_threshold` INT NOT NULL DEFAULT 10,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `fk_inv_prod` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 9. Carts
DROP TABLE IF EXISTS `carts`;
CREATE TABLE `carts` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL UNIQUE,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `fk_cart_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 10. Cart Items
DROP TABLE IF EXISTS `cart_items`;
CREATE TABLE `cart_items` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `cart_id` INT NOT NULL,
    `product_id` INT NOT NULL,
    `quantity` INT NOT NULL DEFAULT 1,
    `unit_price` DECIMAL(10, 2) NOT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY `uq_cart_prod` (`cart_id`, `product_id`),
    CONSTRAINT `fk_ci_cart` FOREIGN KEY (`cart_id`) REFERENCES `carts` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_ci_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 11. Addresses
DROP TABLE IF EXISTS `addresses`;
CREATE TABLE `addresses` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL,
    `title` VARCHAR(50) NOT NULL DEFAULT 'Home',
    `recipient_name` VARCHAR(150) NOT NULL,
    `recipient_phone` VARCHAR(20) NOT NULL,
    `street_address` VARCHAR(255) NOT NULL,
    `landmark` VARCHAR(100) NULL,
    `city` VARCHAR(100) NOT NULL,
    `state` VARCHAR(100) NOT NULL,
    `postal_code` VARCHAR(20) NOT NULL,
    `address_type` ENUM('shipping', 'billing') NOT NULL DEFAULT 'shipping',
    `is_default` BOOLEAN NOT NULL DEFAULT FALSE,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `fk_addr_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 12. Orders
DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `order_number` VARCHAR(50) NOT NULL UNIQUE,
    `user_id` INT NOT NULL,
    `delivery_address_id` INT NULL,
    `total_amount` DECIMAL(12, 2) NOT NULL,
    `tax_amount` DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    `delivery_fee` DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    `discount_amount` DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    `net_amount` DECIMAL(12, 2) NOT NULL,
    `status` ENUM('pending', 'confirmed', 'processing', 'ready_for_dispatch', 'shipped', 'out_for_delivery', 'delivered', 'cancelled', 'failed') NOT NULL DEFAULT 'pending',
    `payment_status` ENUM('pending', 'paid', 'failed', 'refunded') NOT NULL DEFAULT 'pending',
    `payment_method` VARCHAR(50) NOT NULL DEFAULT 'cod',
    `notes` TEXT NULL,
    `ordered_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX `idx_order_status` (`status`),
    INDEX `idx_order_payment_status` (`payment_status`),
    CONSTRAINT `fk_ord_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT,
    CONSTRAINT `fk_ord_addr` FOREIGN KEY (`delivery_address_id`) REFERENCES `addresses` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB;

-- 13. Order Items
DROP TABLE IF EXISTS `order_items`;
CREATE TABLE `order_items` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `order_id` INT NOT NULL,
    `product_id` INT NOT NULL,
    `supplier_id` INT NOT NULL,
    `quantity` INT NOT NULL DEFAULT 1,
    `unit_price` DECIMAL(10, 2) NOT NULL,
    `total_price` DECIMAL(12, 2) NOT NULL,
    `status` ENUM('pending', 'confirmed', 'processing', 'ready_for_dispatch', 'shipped', 'out_for_delivery', 'delivered', 'cancelled', 'failed') NOT NULL DEFAULT 'pending',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_oi_order` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_oi_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE RESTRICT,
    CONSTRAINT `fk_oi_supplier` FOREIGN KEY (`supplier_id`) REFERENCES `supplier_profiles` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB;

-- 14. Payments
DROP TABLE IF EXISTS `payments`;
CREATE TABLE `payments` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `order_id` INT NOT NULL,
    `user_id` INT NOT NULL,
    `payment_method` VARCHAR(50) NOT NULL,
    `transaction_id` VARCHAR(100) NULL UNIQUE,
    `gateway_order_id` VARCHAR(100) NULL,
    `gateway_signature` VARCHAR(255) NULL,
    `amount` DECIMAL(12, 2) NOT NULL,
    `currency` VARCHAR(10) NOT NULL DEFAULT 'INR',
    `status` ENUM('pending', 'paid', 'failed', 'refunded') NOT NULL DEFAULT 'pending',
    `raw_response` TEXT NULL,
    `paid_at` DATETIME NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_pay_order` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_pay_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB;

-- 15. Deliveries
DROP TABLE IF EXISTS `deliveries`;
CREATE TABLE `deliveries` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `order_id` INT NOT NULL UNIQUE,
    `delivery_partner_id` INT NULL,
    `tracking_number` VARCHAR(100) NOT NULL UNIQUE,
    `address` VARCHAR(500) NOT NULL,
    `status` ENUM('assigned', 'picked_up', 'out_for_delivery', 'delivered', 'failed', 'cancelled') NOT NULL DEFAULT 'assigned',
    `pickup_time` DATETIME NULL,
    `estimated_delivery_time` DATETIME NULL,
    `actual_delivery_time` DATETIME NULL,
    `failure_reason` TEXT NULL,
    `notes` TEXT NULL,
    `delivered_at` DATETIME NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX `idx_del_status` (`status`),
    CONSTRAINT `fk_del_order` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_del_partner` FOREIGN KEY (`delivery_partner_id`) REFERENCES `delivery_partner_profiles` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB;

-- 16. Reviews
DROP TABLE IF EXISTS `reviews`;
CREATE TABLE `reviews` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `product_id` INT NOT NULL,
    `user_id` INT NOT NULL,
    `rating` INT NOT NULL,
    `title` VARCHAR(150) NULL,
    `comment` TEXT NOT NULL,
    `is_verified_purchase` BOOLEAN NOT NULL DEFAULT FALSE,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `fk_rev_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_rev_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 17. Wishlists
DROP TABLE IF EXISTS `wishlists`;
CREATE TABLE `wishlists` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL UNIQUE,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `fk_wish_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 18. Wishlist Items
DROP TABLE IF EXISTS `wishlist_items`;
CREATE TABLE `wishlist_items` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `wishlist_id` INT NOT NULL,
    `product_id` INT NOT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY `uq_wish_prod` (`wishlist_id`, `product_id`),
    CONSTRAINT `fk_wi_wishlist` FOREIGN KEY (`wishlist_id`) REFERENCES `wishlists` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_wi_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 19. Notifications
DROP TABLE IF EXISTS `notifications`;
CREATE TABLE `notifications` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL,
    `title` VARCHAR(200) NOT NULL,
    `message` TEXT NOT NULL,
    `notification_type` ENUM('order', 'delivery', 'system', 'alert', 'promotion') NOT NULL DEFAULT 'system',
    `is_read` BOOLEAN NOT NULL DEFAULT FALSE,
    `metadata_json` TEXT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_notif_read` (`is_read`),
    CONSTRAINT `fk_notif_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 20. Complaints
DROP TABLE IF EXISTS `complaints`;
CREATE TABLE `complaints` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL,
    `order_id` INT NULL,
    `subject` VARCHAR(200) NOT NULL,
    `description` TEXT NOT NULL,
    `category` VARCHAR(100) NOT NULL DEFAULT 'General',
    `status` ENUM('open', 'in_investigation', 'resolved', 'closed') NOT NULL DEFAULT 'open',
    `resolution_notes` TEXT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX `idx_comp_status` (`status`),
    CONSTRAINT `fk_comp_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_comp_order` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB;

-- 21. Price History
DROP TABLE IF EXISTS `price_history`;
CREATE TABLE `price_history` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `product_id` INT NOT NULL,
    `old_price` DECIMAL(10, 2) NOT NULL,
    `new_price` DECIMAL(10, 2) NOT NULL,
    `changed_by_user_id` INT NULL,
    `change_reason` VARCHAR(255) NULL,
    `changed_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_ph_prod` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_ph_user` FOREIGN KEY (`changed_by_user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB;

-- 22. AI Estimations
DROP TABLE IF EXISTS `ai_estimations`;
CREATE TABLE `ai_estimations` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NULL,
    `building_length` FLOAT NOT NULL,
    `building_width` FLOAT NOT NULL,
    `no_of_floors` INT NOT NULL DEFAULT 1,
    `floor_height` FLOAT NOT NULL DEFAULT 10.0,
    `construction_type` VARCHAR(50) NOT NULL,
    `building_type` VARCHAR(50) NOT NULL,
    `location` VARCHAR(100) NOT NULL,
    `quality_preference` VARCHAR(50) NOT NULL DEFAULT 'Standard',
    `built_up_area_sqft` FLOAT NOT NULL,
    `estimated_cement_bags` INT NOT NULL,
    `estimated_steel_kg` FLOAT NOT NULL,
    `estimated_bricks_count` INT NOT NULL,
    `estimated_sand_ton` FLOAT NOT NULL,
    `estimated_gravel_ton` FLOAT NOT NULL,
    `estimated_tiles_sqft` FLOAT NOT NULL,
    `estimated_paint_liter` FLOAT NOT NULL,
    `estimated_total_budget` DECIMAL(14, 2) NOT NULL,
    `detailed_breakdown_json` TEXT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_ae_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB;

-- 23. AI Predictions
DROP TABLE IF EXISTS `ai_predictions`;
CREATE TABLE `ai_predictions` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `product_id` INT NULL,
    `category_id` INT NULL,
    `prediction_type` VARCHAR(50) NOT NULL,
    `predicted_value` FLOAT NOT NULL,
    `confidence_score` FLOAT NOT NULL,
    `metadata_json` TEXT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_ap_prod` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_ap_cat` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 24. Audit Logs
DROP TABLE IF EXISTS `audit_logs`;
CREATE TABLE `audit_logs` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NULL,
    `action` VARCHAR(100) NOT NULL,
    `entity_type` VARCHAR(50) NOT NULL,
    `entity_id` INT NULL,
    `ip_address` VARCHAR(50) NULL,
    `user_agent` VARCHAR(255) NULL,
    `details_json` TEXT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_audit_action` (`action`),
    CONSTRAINT `fk_audit_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB;

SET FOREIGN_KEY_CHECKS = 1;
