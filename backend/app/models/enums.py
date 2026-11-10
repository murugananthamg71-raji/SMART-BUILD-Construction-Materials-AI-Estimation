import enum

class UserRole(str, enum.Enum):
    CUSTOMER = "customer"
    SUPPLIER = "supplier"
    ADMIN = "admin"
    DELIVERY_PARTNER = "delivery_partner"

class ApprovalStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    READY_FOR_DISPATCH = "ready_for_dispatch"
    SHIPPED = "shipped"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    FAILED = "failed"

class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"

class DeliveryStatus(str, enum.Enum):
    ASSIGNED = "assigned"
    PICKED_UP = "picked_up"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    FAILED = "failed"
    CANCELLED = "cancelled"

class AddressType(str, enum.Enum):
    SHIPPING = "shipping"
    BILLING = "billing"

class NotificationType(str, enum.Enum):
    ORDER = "order"
    DELIVERY = "delivery"
    SYSTEM = "system"
    ALERT = "alert"
    PROMOTION = "promotion"

class ComplaintStatus(str, enum.Enum):
    OPEN = "open"
    IN_INVESTIGATION = "in_investigation"
    RESOLVED = "resolved"
    CLOSED = "closed"
