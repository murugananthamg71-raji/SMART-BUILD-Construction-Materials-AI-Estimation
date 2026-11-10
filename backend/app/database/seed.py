import logging
from decimal import Decimal
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.core.security import get_password_hash
from app.models.enums import UserRole, ApprovalStatus, OrderStatus, DeliveryStatus, PaymentStatus
from app.models.user import User
from app.models.profile import CustomerProfile, SupplierProfile, DeliveryPartnerProfile
from app.models.category import Category
from app.models.product import Product, ProductImage
from app.models.inventory import Inventory
from app.models.cart import Cart
from app.models.wishlist import Wishlist
from app.models.address import Address
from app.models.order import Order, OrderItem
from app.models.delivery import Delivery
from app.models.payment import Payment

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("seed")

def seed_database():
    db: Session = SessionLocal()
    try:
        logger.info("Checking if database already has seed data...")
        admin_check = db.query(User).filter(User.email == "admin@smartbuild.com").first()
        if admin_check:
            logger.info("Database already seeded with demo users. Skipping re-seed.")
            return

        logger.info("Seeding demo users...")
        demo_password = get_password_hash("Demo1234!")

        # 1. Admin
        admin = User(
            name="Platform Administrator",
            email="admin@smartbuild.com",
            hashed_password=demo_password,
            phone="+91 90000 00001",
            role=UserRole.ADMIN,
            is_active=True,
            is_verified=True
        )
        db.add(admin)

        # 2. Customer
        customer = User(
            name="Rahul Sharma (Builder)",
            email="customer@smartbuild.com",
            hashed_password=demo_password,
            phone="+91 98888 11111",
            role=UserRole.CUSTOMER,
            is_active=True,
            is_verified=True
        )
        db.add(customer)
        db.flush()

        customer_profile = CustomerProfile(
            user_id=customer.id,
            company_name="Sharma Construction Projects",
            gst_number="29ABCDE1234F1Z5"
        )
        cart = Cart(user_id=customer.id)
        wishlist = Wishlist(user_id=customer.id)
        cust_address = Address(
            user_id=customer.id,
            title="Bangalore Construction Site #1",
            recipient_name="Rahul Sharma",
            recipient_phone="+91 98888 11111",
            street_address="Plot 104, Outer Ring Road, Bellandur",
            landmark="Near Tech Park Gate 2",
            city="Bangalore",
            state="Karnataka",
            postal_code="560103",
            is_default=True
        )
        db.add_all([customer_profile, cart, wishlist, cust_address])

        # 3. Supplier 1
        supplier1_user = User(
            name="Suresh Patel",
            email="supplier@smartbuild.com",
            hashed_password=demo_password,
            phone="+91 97777 22222",
            role=UserRole.SUPPLIER,
            is_active=True,
            is_verified=True
        )
        db.add(supplier1_user)
        db.flush()

        supplier1 = SupplierProfile(
            user_id=supplier1_user.id,
            company_name="Apex Infrastructure & Steel Supplies",
            business_license="BL-KA-2024-9988",
            tax_id="29AAACA9999P1Z1",
            address="Yard 12, Peenya Industrial Area 2nd Stage",
            city="Bangalore",
            state="Karnataka",
            postal_code="560058",
            approval_status=ApprovalStatus.APPROVED,
            rating=4.85,
            total_reviews=142
        )
        db.add(supplier1)

        # Supplier 2
        supplier2_user = User(
            name="Vikram Verma",
            email="cement.hub@smartbuild.com",
            hashed_password=demo_password,
            phone="+91 96666 33333",
            role=UserRole.SUPPLIER,
            is_active=True,
            is_verified=True
        )
        db.add(supplier2_user)
        db.flush()

        supplier2 = SupplierProfile(
            user_id=supplier2_user.id,
            company_name="Bharat Cement & Aggregates Corp",
            business_license="BL-KA-2023-7721",
            tax_id="29BBBCB8888Q1Z2",
            address="Plot 45, Hosur Main Road",
            city="Bangalore",
            state="Karnataka",
            postal_code="560068",
            approval_status=ApprovalStatus.APPROVED,
            rating=4.90,
            total_reviews=98
        )
        db.add(supplier2)

        # 4. Delivery Partner
        delivery_user = User(
            name="Rajesh Gounder",
            email="delivery@smartbuild.com",
            hashed_password=demo_password,
            phone="+91 95555 44444",
            role=UserRole.DELIVERY_PARTNER,
            is_active=True,
            is_verified=True
        )
        db.add(delivery_user)
        db.flush()

        delivery_profile = DeliveryPartnerProfile(
            user_id=delivery_user.id,
            vehicle_type="Heavy Commercial Eicher 1095 Truck (10 Ton)",
            vehicle_number="KA-01-MJ-4592",
            license_number="DL-0420210088992",
            is_available=True,
            current_location="Electronic City, Bangalore"
        )
        db.add(delivery_profile)
        db.flush()

        logger.info("Seeding 9 construction material categories...")
        categories_data = [
            {"name": "Cement", "slug": "cement", "description": "OPC, PPC, and rapid-hardening structural cements from certified plants.", "image_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=500&auto=format&fit=crop&q=60", "display_order": 1},
            {"name": "Steel", "slug": "steel", "description": "High-ductility Fe550D TMT reinforcement rebars and structural angles.", "image_url": "https://images.unsplash.com/photo-1504917599217-d4dc5ebe6122?w=500&auto=format&fit=crop&q=60", "display_order": 2},
            {"name": "Bricks & Blocks", "slug": "bricks", "description": "Red clay kiln-fired bricks, AAC thermal blocks, and concrete solid blocks.", "image_url": "https://images.unsplash.com/photo-1589939705384-5185137a7f0f?w=500&auto=format&fit=crop&q=60", "display_order": 3},
            {"name": "Sand", "slug": "sand", "description": "Manufactured M-Sand for masonry, P-Sand for plastering, and washed river sand.", "image_url": "https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?w=500&auto=format&fit=crop&q=60", "display_order": 4},
            {"name": "Gravel & Aggregates", "slug": "gravel", "description": "Graded 10mm, 20mm blue metal granite aggregates and GSB sub-base rock.", "image_url": "https://images.unsplash.com/photo-1541888946425-d0fbb18086f7?w=500&auto=format&fit=crop&q=60", "display_order": 5},
            {"name": "Tiles & Flooring", "slug": "tiles", "description": "Double-charged vitrified floor tiles, ceramic wall dado, and anti-skid pavers.", "image_url": "https://images.unsplash.com/photo-1584467541268-b040f83be3fd?w=500&auto=format&fit=crop&q=60", "display_order": 6},
            {"name": "Paint & Finishes", "slug": "paint", "description": "Weather-proof exterior coatings, interior luxury acrylic emulsions, and primers.", "image_url": "https://images.unsplash.com/photo-1589939705384-5185137a7f0f?w=500&auto=format&fit=crop&q=60", "display_order": 7},
            {"name": "Plumbing & Drainage", "slug": "plumbing", "description": "CPVC hot/cold water pressure pipes, SWR drainage fittings, and ball valves.", "image_url": "https://images.unsplash.com/photo-1585704032915-c3400ca199e7?w=500&auto=format&fit=crop&q=60", "display_order": 8},
            {"name": "Electrical & Wiring", "slug": "electrical", "description": "FR-LSH copper domestic cables, industrial conduits, and modular switchgear.", "image_url": "https://images.unsplash.com/photo-1544724569-5f546fd6f2b5?w=500&auto=format&fit=crop&q=60", "display_order": 9}
        ]

        cat_map = {}
        for cdata in categories_data:
            cat = Category(**cdata)
            db.add(cat)
            db.flush()
            cat_map[cat.slug] = cat.id

        logger.info("Seeding 22 realistic construction products with stock & imagery...")
        products_data = [
            # Cement
            {
                "name": "UltraTech Super Cement 53 Grade OPC",
                "category_id": cat_map["cement"],
                "supplier_id": supplier2.id,
                "price": Decimal("385.00"),
                "unit": "bag",
                "brand": "UltraTech",
                "description": "Premium 53 Grade Ordinary Portland Cement ideal for high-strength RCC structural casting, slabs, columns, and heavy civil foundations.",
                "stock": 500,
                "image_url": "https://images.unsplash.com/photo-1589939705384-5185137a7f0f?w=600&auto=format&fit=crop&q=80"
            },
            {
                "name": "Ambuja Kawach Waterproof Cement",
                "category_id": cat_map["cement"],
                "supplier_id": supplier2.id,
                "price": Decimal("410.00"),
                "unit": "bag",
                "brand": "Ambuja",
                "description": "Engineered water-repellent cement with active silane technology preventing efflorescence and water seepage in roof slabs and retaining walls.",
                "stock": 350,
                "image_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=600&auto=format&fit=crop&q=80"
            },
            {
                "name": "ACC Concrete Plus Composite PPC Cement",
                "category_id": cat_map["cement"],
                "supplier_id": supplier2.id,
                "price": Decimal("375.00"),
                "unit": "bag",
                "brand": "ACC",
                "description": "Portland Pozzolana Cement formulated with spherical mineral admixtures for ultra-dense, cohesive concrete and reduced thermal cracking.",
                "stock": 420,
                "image_url": "https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=600&auto=format&fit=crop&q=80"
            },
            # Steel
            {
                "name": "Tata Tiscon 550D TMT Rebar (12mm)",
                "category_id": cat_map["steel"],
                "supplier_id": supplier1.id,
                "price": Decimal("74.50"),
                "unit": "kg",
                "brand": "Tata Tiscon",
                "description": "Fe550D grade primary steel reinforcement with superior elongation and earthquake-resistant energy absorption for multistory residential frames.",
                "stock": 2500,
                "image_url": "https://images.unsplash.com/photo-1504917599217-d4dc5ebe6122?w=600&auto=format&fit=crop&q=80"
            },
            {
                "name": "Tata Tiscon 550D TMT Rebar (16mm)",
                "category_id": cat_map["steel"],
                "supplier_id": supplier1.id,
                "price": Decimal("73.80"),
                "unit": "kg",
                "brand": "Tata Tiscon",
                "description": "Heavy-duty 16mm ribbed thermo-mechanically treated bar engineered for ground beam and structural column cages.",
                "stock": 3200,
                "image_url": "https://images.unsplash.com/photo-1535813547-99c456a41d4a?w=600&auto=format&fit=crop&q=80"
            },
            {
                "name": "JSW Neosteel Fe550D TMT Bar (10mm)",
                "category_id": cat_map["steel"],
                "supplier_id": supplier1.id,
                "price": Decimal("71.50"),
                "unit": "kg",
                "brand": "JSW",
                "description": "Pure steel manufactured from virgin iron ore with lowest sulfur-phosphorus impurity levels, providing high fatigue strength.",
                "stock": 1800,
                "image_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=600&auto=format&fit=crop&q=80"
            },
            # Bricks
            {
                "name": "Wienerberger Porotherm Clay Hollow Bricks",
                "category_id": cat_map["bricks"],
                "supplier_id": supplier1.id,
                "price": Decimal("48.00"),
                "unit": "piece",
                "brand": "Wienerberger",
                "description": "Precision perforated clay blocks offering 60% weight reduction compared to red bricks and exceptional thermal insulation for external walls.",
                "stock": 3000,
                "image_url": "https://images.unsplash.com/photo-1589939705384-5185137a7f0f?w=600&auto=format&fit=crop&q=80"
            },
            {
                "name": "Standard Red Clay Table-Moulded Bricks",
                "category_id": cat_map["bricks"],
                "supplier_id": supplier1.id,
                "price": Decimal("9.50"),
                "unit": "piece",
                "brand": "Standard Clay",
                "description": "Kiln-baked first-class red clay bricks with sharp arrises and high compressive crushing strength (> 3.5 N/mm2).",
                "stock": 15000,
                "image_url": "https://images.unsplash.com/photo-1589939705384-5185137a7f0f?w=600&auto=format&fit=crop&q=80"
            },
            {
                "name": "Birla Aerocon AAC Lightweight Blocks (600x200x150mm)",
                "category_id": cat_map["bricks"],
                "supplier_id": supplier2.id,
                "price": Decimal("62.00"),
                "unit": "piece",
                "brand": "Birla Aerocon",
                "description": "Autoclaved aerated concrete block delivering non-combustible 4-hour fire rating and rapid structural wall installation speed.",
                "stock": 1200,
                "image_url": "https://images.unsplash.com/photo-1541888946425-d0fbb18086f7?w=600&auto=format&fit=crop&q=80"
            },
            # Sand
            {
                "name": "Washed M-Sand for Concrete Casting (Zone-II)",
                "category_id": cat_map["sand"],
                "supplier_id": supplier2.id,
                "price": Decimal("1450.00"),
                "unit": "ton",
                "brand": "RoboSand",
                "description": "Triple-washed manufactured granite sand free from silt and clay contamination, matching IS:383 grading specifications.",
                "stock": 120,
                "image_url": "https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?w=600&auto=format&fit=crop&q=80"
            },
            {
                "name": "Super-Fine Plastering P-Sand",
                "category_id": cat_map["sand"],
                "supplier_id": supplier2.id,
                "price": Decimal("1650.00"),
                "unit": "ton",
                "brand": "RoboSand",
                "description": "Air-classified fine plaster sand achieving zero-crack mirror finish for interior wall rendering and ceiling putty prep.",
                "stock": 80,
                "image_url": "https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?w=600&auto=format&fit=crop&q=80"
            },
            # Gravel
            {
                "name": "20mm Blue Metal Granite Aggregate",
                "category_id": cat_map["gravel"],
                "supplier_id": supplier2.id,
                "price": Decimal("980.00"),
                "unit": "ton",
                "brand": "Apex Quarry",
                "description": "Machine-crushed angular hard blue granite stone aggregate providing structural interlock in M20 and M25 design mixes.",
                "stock": 150,
                "image_url": "https://images.unsplash.com/photo-1541888946425-d0fbb18086f7?w=600&auto=format&fit=crop&q=80"
            },
            {
                "name": "12mm Down Fine Aggregate Chips",
                "category_id": cat_map["gravel"],
                "supplier_id": supplier2.id,
                "price": Decimal("1020.00"),
                "unit": "ton",
                "brand": "Apex Quarry",
                "description": "Granite screenings used for beam consolidation and precast lintel fabrication.",
                "stock": 90,
                "image_url": "https://images.unsplash.com/photo-1541888946425-d0fbb18086f7?w=600&auto=format&fit=crop&q=80"
            },
            # Tiles
            {
                "name": "Kajaria Double Charged Vitrified Floor Tiles (600x600mm)",
                "category_id": cat_map["tiles"],
                "supplier_id": supplier1.id,
                "price": Decimal("68.00"),
                "unit": "sqft",
                "brand": "Kajaria",
                "description": "Nano-polished stain-resistant vitrified tiles engineered with 3-4mm double layer pattern for high-traffic living rooms.",
                "stock": 2400,
                "image_url": "https://images.unsplash.com/photo-1584467541268-b040f83be3fd?w=600&auto=format&fit=crop&q=80"
            },
            {
                "name": "Somany Anti-Skid Matte Bathroom Ceramic Tiles (300x300mm)",
                "category_id": cat_map["tiles"],
                "supplier_id": supplier1.id,
                "price": Decimal("46.00"),
                "unit": "sqft",
                "brand": "Somany",
                "description": "Textured wet-area floor tile offering R10 slip-resistance rating and chemical detergent resistance.",
                "stock": 1600,
                "image_url": "https://images.unsplash.com/photo-1584467541268-b040f83be3fd?w=600&auto=format&fit=crop&q=80"
            },
            # Paint
            {
                "name": "Asian Paints Apex Ultima Weatherproof Exterior Emulsion",
                "category_id": cat_map["paint"],
                "supplier_id": supplier1.id,
                "price": Decimal("340.00"),
                "unit": "liter",
                "brand": "Asian Paints",
                "description": "Advanced silicone-additive exterior wall paint with colour-stay technology and 7-year comprehensive anti-fungal warranty.",
                "stock": 250,
                "image_url": "https://images.unsplash.com/photo-1589939705384-5185137a7f0f?w=600&auto=format&fit=crop&q=80"
            },
            {
                "name": "Asian Paints Royale Luxury Interior Matt Emulsion",
                "category_id": cat_map["paint"],
                "supplier_id": supplier1.id,
                "price": Decimal("420.00"),
                "unit": "liter",
                "brand": "Asian Paints",
                "description": "Teflon-surface-protected ultra-smooth interior wall paint with stain repellent properties and zero VOC formulation.",
                "stock": 180,
                "image_url": "https://images.unsplash.com/photo-1589939705384-5185137a7f0f?w=600&auto=format&fit=crop&q=80"
            },
            # Plumbing
            {
                "name": "Ashirvad FlowGuard Plus CPVC Hot & Cold Pipe (1 inch x 3m)",
                "category_id": cat_map["plumbing"],
                "supplier_id": supplier2.id,
                "price": Decimal("380.00"),
                "unit": "piece",
                "brand": "Ashirvad",
                "description": "NSF-certified chlorate polyvinyl chloride potable water line capable of withstanding temperatures up to 93°C.",
                "stock": 300,
                "image_url": "https://images.unsplash.com/photo-1585704032915-c3400ca199e7?w=600&auto=format&fit=crop&q=80"
            },
            {
                "name": "Astral Silencio 4-Inch SWR Soundproof Drainage Pipe",
                "category_id": cat_map["plumbing"],
                "supplier_id": supplier2.id,
                "price": Decimal("1150.00"),
                "unit": "piece",
                "brand": "Astral",
                "description": "Three-layer mineral-reinforced acoustic drainage pipe engineered to minimize plumbing rush noise through vertical ducts.",
                "stock": 140,
                "image_url": "https://images.unsplash.com/photo-1585704032915-c3400ca199e7?w=600&auto=format&fit=crop&q=80"
            },
            # Electrical
            {
                "name": "Havells LifeLine Plus 2.5 sq mm FR-LSH Copper Wire (90m Roll)",
                "category_id": cat_map["electrical"],
                "supplier_id": supplier1.id,
                "price": Decimal("2450.00"),
                "unit": "piece",
                "brand": "Havells",
                "description": "100% electrolytic oxygen-free copper building wire insulated with flame-retardant low-smoke zero-halogen compound.",
                "stock": 110,
                "image_url": "https://images.unsplash.com/photo-1544724569-5f546fd6f2b5?w=600&auto=format&fit=crop&q=80"
            },
            {
                "name": "Polycab 4.0 sq mm Heavy Appliance Cable (90m Coil)",
                "category_id": cat_map["electrical"],
                "supplier_id": supplier1.id,
                "price": Decimal("3850.00"),
                "unit": "piece",
                "brand": "Polycab",
                "description": "Heavy-duty power cable rated for 32 Amp continuous AC units, commercial geysers, and welding points.",
                "stock": 85,
                "image_url": "https://images.unsplash.com/photo-1544724569-5f546fd6f2b5?w=600&auto=format&fit=crop&q=80"
            },
            {
                "name": "Schneider Electric EasyPact Double Pole MCB (32 Amp)",
                "category_id": cat_map["electrical"],
                "supplier_id": supplier1.id,
                "price": Decimal("680.00"),
                "unit": "piece",
                "brand": "Schneider",
                "description": "Thermal magnetic trip curve C miniature circuit breaker ensuring protection against overload and short circuits up to 10kA.",
                "stock": 95,
                "image_url": "https://images.unsplash.com/photo-1544724569-5f546fd6f2b5?w=600&auto=format&fit=crop&q=80"
            }
        ]

        for pdata in products_data:
            slug = f"{pdata['name'].lower().replace(' ', '-').replace('/', '-').replace('(', '').replace(')', '')[:50]}"
            stock = pdata.pop("stock")
            img_url = pdata.pop("image_url")

            p = Product(
                supplier_id=pdata["supplier_id"],
                category_id=pdata["category_id"],
                name=pdata["name"],
                slug=slug,
                description=pdata["description"],
                brand=pdata["brand"],
                price=pdata["price"],
                unit=pdata["unit"],
                min_order_quantity=1,
                is_approved=True,
                approval_status=ApprovalStatus.APPROVED,
                is_active=True,
                rating=4.8,
                total_reviews=15
            )
            db.add(p)
            db.flush()

            inv = Inventory(product_id=p.id, stock=stock, low_stock_threshold=20)
            img = ProductImage(product_id=p.id, image_url=img_url, is_primary=True, display_order=1)
            db.add_all([inv, img])

        # Create one initial sample order for the customer
        sample_prod1 = db.query(Product).first()
        order = Order(
            order_number="SB-20261110-INIT01",
            user_id=customer.id,
            delivery_address_id=cust_address.id,
            total_amount=Decimal("19250.00"),
            tax_amount=Decimal("3465.00"),
            delivery_fee=Decimal("500.00"),
            discount_amount=Decimal("0.00"),
            net_amount=Decimal("23215.00"),
            status=OrderStatus.SHIPPED,
            payment_status=PaymentStatus.PAID,
            payment_method="razorpay",
            notes="Please unload near Tower B foundation"
        )
        db.add(order)
        db.flush()

        order_item = OrderItem(
            order_id=order.id,
            product_id=sample_prod1.id,
            supplier_id=sample_prod1.supplier_id,
            quantity=50,
            unit_price=sample_prod1.price,
            total_price=Decimal("19250.00"),
            status=OrderStatus.SHIPPED
        )
        db.add(order_item)

        delivery = Delivery(
            order_id=order.id,
            delivery_partner_id=delivery_profile.id,
            tracking_number="TRK-SB-INIT9988",
            address="Plot 104, Outer Ring Road, Bellandur, Bangalore - 560103",
            status=DeliveryStatus.PICKED_UP,
            pickup_time=customer.created_at,
            estimated_delivery_time=customer.created_at
        )
        db.add(delivery)

        payment = Payment(
            order_id=order.id,
            user_id=customer.id,
            payment_method="razorpay",
            transaction_id="TXN-INIT-SAMPLE001",
            amount=Decimal("23215.00"),
            status=PaymentStatus.PAID
        )
        db.add(payment)

        db.commit()
        logger.info("Database successfully seeded with 4 demo accounts, 9 categories, 22 products, and initial order!")
    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding database: {e}", exc_info=True)
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
