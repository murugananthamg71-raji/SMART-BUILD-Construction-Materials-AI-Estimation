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
from app.models.cart import Cart, CartItem
from app.models.wishlist import Wishlist
from app.models.address import Address
from app.models.order import Order, OrderItem
from app.models.delivery import Delivery
from app.models.payment import Payment

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("seed")

def seed_database(force_refresh=True):
    db: Session = SessionLocal()
    try:
        logger.info("Initializing full Construction Materials dataset...")

        if force_refresh:
            logger.info("Clearing existing products, images, inventory & categories...")
            db.query(CartItem).delete()
            db.query(OrderItem).delete()
            db.query(Delivery).delete()
            db.query(Payment).delete()
            db.query(Order).delete()
            db.query(ProductImage).delete()
            db.query(Inventory).delete()
            db.query(Product).delete()
            db.query(Category).delete()
            db.commit()

        # Ensure demo users exist
        demo_password = get_password_hash("Demo1234!")

        admin = db.query(User).filter(User.email == "admin@smartbuild.com").first()
        if not admin:
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

        customer = db.query(User).filter(User.email == "customer@smartbuild.com").first()
        if not customer:
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
            cust_profile = CustomerProfile(user_id=customer.id, company_name="Sharma Construction Projects")
            cart = Cart(user_id=customer.id)
            wishlist = Wishlist(user_id=customer.id)
            db.add_all([cust_profile, cart, wishlist])

        cust_address = db.query(Address).filter(Address.user_id == customer.id).first()
        if not cust_address:
            cust_address = Address(
                user_id=customer.id,
                title="Bangalore Construction Site #1",
                recipient_name="Rahul Sharma",
                recipient_phone="+91 98888 11111",
                street_address="Plot 104, Outer Ring Road, Bellandur",
                city="Bangalore",
                state="Karnataka",
                postal_code="560103",
                is_default=True
            )
            db.add(cust_address)
            db.flush()

        supplier1_user = db.query(User).filter(User.email == "supplier@smartbuild.com").first()
        if not supplier1_user:
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
                rating=4.90,
                total_reviews=168
            )
            db.add(supplier1)
        else:
            supplier1 = supplier1_user.supplier_profile

        supplier2_user = db.query(User).filter(User.email == "cement.hub@smartbuild.com").first()
        if not supplier2_user:
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
                company_name="Bharat Cement, Quarry & Aggregates Corp",
                business_license="BL-KA-2023-7721",
                tax_id="29BBBCB8888Q1Z2",
                address="Plot 45, Hosur Main Road",
                city="Bangalore",
                state="Karnataka",
                postal_code="560068",
                approval_status=ApprovalStatus.APPROVED,
                rating=4.88,
                total_reviews=142
            )
            db.add(supplier2)
        else:
            supplier2 = supplier2_user.supplier_profile

        delivery_user = db.query(User).filter(User.email == "delivery@smartbuild.com").first()
        if not delivery_user:
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
            deliv_prof = DeliveryPartnerProfile(
                user_id=delivery_user.id,
                vehicle_type="Heavy Commercial Eicher 1095 Tipper (10 Ton)",
                vehicle_number="KA-01-MJ-4592",
                license_number="DL-0420210088992",
                is_available=True,
                current_location="Electronic City, Bangalore"
            )
            db.add(deliv_prof)

        db.commit()

        # 9 EXACT CATEGORIES with bilingual Tamil + English titles & user's images
        categories_data = [
            {
                "name": "Cement (சிமெண்ட்)",
                "slug": "cement",
                "description": "OPC 43, OPC 53, PPC, PSC, White Cement, and Ready Mix Concrete from certified plants.",
                "image_url": "/images/materials/cat_cement.png",
                "display_order": 1
            },
            {
                "name": "Steel (இரும்பு)",
                "slug": "steel",
                "description": "TMT Rebars, MS Rods, Steel Angles, Channels, Sheets, Binding Wires, and Steel Pipes.",
                "image_url": "/images/materials/cat_steel.png",
                "display_order": 2
            },
            {
                "name": "Bricks & Blocks (செங்கல்)",
                "slug": "bricks",
                "description": "Red Clay Bricks, Fly Ash Bricks, AAC Blocks, Solid Concrete Blocks, Hollow & Paver Blocks.",
                "image_url": "/images/materials/cat_bricks.png",
                "display_order": 3
            },
            {
                "name": "Sand (மணல்)",
                "slug": "sand",
                "description": "Government Approved River Sand, M-Sand, P-Sand, Plastering Sand, and Filter Sand.",
                "image_url": "/images/materials/cat_sand.png",
                "display_order": 4
            },
            {
                "name": "Gravel & Aggregates (ஜல்லி)",
                "slug": "gravel",
                "description": "6mm, 10mm, 12mm, 20mm, 40mm Granite Jelly, Stone Dust, and Machine-Crushed Stone.",
                "image_url": "/images/materials/cat_gravel.png",
                "display_order": 5
            },
            {
                "name": "Tiles & Flooring (டைல்ஸ்)",
                "slug": "tiles",
                "description": "Ceramic, Vitrified, Porcelain Tiles, Granite Slabs, Italian Marble, Parking & Anti-Skid Tiles.",
                "image_url": "/images/materials/cat_tiles.png",
                "display_order": 6
            },
            {
                "name": "Paint & Finishes (பெயிண்ட்)",
                "slug": "paint",
                "description": "Interior & Exterior Paints, Primers, Wall Putty, Enamel, Texture Paints, and Waterproofing.",
                "image_url": "/images/materials/cat_paint.png",
                "display_order": 7
            },
            {
                "name": "Plumbing & Drainage (பிளம்பிங்)",
                "slug": "plumbing",
                "description": "PVC, CPVC, UPVC, HDPE Pipes, Fittings, Elbows, Tees, Water Taps, Valves, Traps & Tanks.",
                "image_url": "/images/materials/cat_plumbing.png",
                "display_order": 8
            },
            {
                "name": "Electrical & Wiring (எலக்ட்ரிக்கல்)",
                "slug": "electrical",
                "description": "Electrical Wires, Armoured Cables, Switches, Sockets, MCBs, Distribution Boards, LED, Conduits.",
                "image_url": "/images/materials/cat_electrical.png",
                "display_order": 9
            }
        ]

        cat_map = {}
        for cdata in categories_data:
            cat = Category(**cdata)
            db.add(cat)
            db.flush()
            cat_map[cat.slug] = cat.id

        logger.info("Seeding full construction materials list (all 66 items)...")

        # Full exhaustive list requested by user
        full_materials_list = [
            # 1. CEMENT (சிமெண்ட்)
            {
                "name": "OPC 43 Grade Cement (UltraTech / Dalmia)",
                "category_id": cat_map["cement"],
                "supplier_id": supplier2.id,
                "price": Decimal("375.00"),
                "unit": "bag",
                "brand": "UltraTech",
                "description": "Ordinary Portland Cement 43 Grade suitable for general RCC structures, plastering, non-structural precast and brick masonry.",
                "stock": 800,
                "image_url": "/images/materials/opc_43_grade.png"
            },
            {
                "name": "OPC 53 Grade Cement (UltraTech / Chettinad)",
                "category_id": cat_map["cement"],
                "supplier_id": supplier2.id,
                "price": Decimal("395.00"),
                "unit": "bag",
                "brand": "UltraTech",
                "description": "High-strength 53 Grade OPC with early 28-day characteristic compressive strength exceeding 53 MPa for columns, heavy beams & multistory slabs.",
                "stock": 1200,
                "image_url": "/images/materials/opc_53_grade.png"
            },
            {
                "name": "PPC Cement (Portland Pozzolana Cement - Ambuja Kawach / Ramco)",
                "category_id": cat_map["cement"],
                "supplier_id": supplier2.id,
                "price": Decimal("380.00"),
                "unit": "bag",
                "brand": "Ambuja",
                "description": "Water-repellent pozzolana cement offering superior resistance to chemical and sulfate attacks, damp-proofing foundations and roof slabs.",
                "stock": 650,
                "image_url": "/images/materials/ppc_cement.png"
            },
            {
                "name": "PSC Cement (Portland Slag Cement - JSW Concreel HD)",
                "category_id": cat_map["cement"],
                "supplier_id": supplier2.id,
                "price": Decimal("365.00"),
                "unit": "bag",
                "brand": "JSW",
                "description": "Slag cement manufactured by grinding clinker and granulated blast-furnace slag, providing highest impermeability against groundwater dampness.",
                "stock": 500,
                "image_url": "/images/materials/psc_cement.png"
            },
            {
                "name": "White Cement (Birla White / JK White 50kg Bag)",
                "category_id": cat_map["cement"],
                "supplier_id": supplier2.id,
                "price": Decimal("850.00"),
                "unit": "bag",
                "brand": "Birla White",
                "description": "Superior whiteness (> 89% Hunter scale) cement for terrazzo flooring, ornamental architectural precast work, tile grouting, and marble setting.",
                "stock": 250,
                "image_url": "/images/materials/white_cement.png"
            },
            {
                "name": "Ready Mix Cement Concrete (RMC M20 / M25 Grade Transit Mix)",
                "category_id": cat_map["cement"],
                "supplier_id": supplier2.id,
                "price": Decimal("4200.00"),
                "unit": "cubic_meter",
                "brand": "UltraTech RMC",
                "description": "Automated computerized batching plant mixed concrete delivered via transit mixer truck directly pumped to floor slab levels.",
                "stock": 100,
                "image_url": "/images/materials/ready_mix_cement.png"
            },

            # 2. STEEL (இரும்பு)
            {
                "name": "TMT Bars (Tata Tiscon / JSW Neosteel Fe550D 12mm)",
                "category_id": cat_map["steel"],
                "supplier_id": supplier1.id,
                "price": Decimal("74.50"),
                "unit": "kg",
                "brand": "Tata Tiscon",
                "description": "Primary high-ductility Fe550D thermo-mechanically treated rebar with seismic resistance for residential and commercial RCC framing.",
                "stock": 6000,
                "image_url": "/images/materials/tmt_bars.png"
            },
            {
                "name": "MS Rods (Mild Steel Round Bars 10mm / 12mm)",
                "category_id": cat_map["steel"],
                "supplier_id": supplier1.id,
                "price": Decimal("68.00"),
                "unit": "kg",
                "brand": "Kamdhenu",
                "description": "Plain circular mild steel rods for fabrication, window grills, structural stirrups, and miscellaneous anchor ties.",
                "stock": 3500,
                "image_url": "/images/materials/ms_rods.png"
            },
            {
                "name": "Steel Angles (MS Equal Angles 50x50x5mm)",
                "category_id": cat_map["steel"],
                "supplier_id": supplier1.id,
                "price": Decimal("72.00"),
                "unit": "kg",
                "brand": "SAIL",
                "description": "L-shaped structural mild steel angles for roof trusses, support purlins, shed fabrication, and industrial mezzanines.",
                "stock": 2400,
                "image_url": "/images/materials/steel_angles.png"
            },
            {
                "name": "Steel Channels (ISMC 100 / 150 Structural C-Channel)",
                "category_id": cat_map["steel"],
                "supplier_id": supplier1.id,
                "price": Decimal("73.50"),
                "unit": "kg",
                "brand": "Jindal Steel",
                "description": "Hot-rolled C-shaped structural steel sections used as heavy load-bearing purlins, lintels, and bridge stringers.",
                "stock": 2000,
                "image_url": "/images/materials/steel_channels.png"
            },
            {
                "name": "Steel Sheets (Galvanized Plain GP / CR Sheet 1.2mm)",
                "category_id": cat_map["steel"],
                "supplier_id": supplier1.id,
                "price": Decimal("78.00"),
                "unit": "kg",
                "brand": "Tata Shaktee",
                "description": "Corrosion-resistant zinc-galvanized flat steel sheets for shuttering plates, ducting, and weather barrier cladding.",
                "stock": 1800,
                "image_url": "/images/materials/steel_sheets.png"
            },
            {
                "name": "Binding Wire (18 Gauge Annealed GI Binding Wire)",
                "category_id": cat_map["steel"],
                "supplier_id": supplier1.id,
                "price": Decimal("85.00"),
                "unit": "kg",
                "brand": "Apex Steel",
                "description": "Soft annealed galvanized iron wire for tightly binding reinforcement rebar intersections prior to slab casting.",
                "stock": 900,
                "image_url": "/images/materials/binding_wire.png"
            },
            {
                "name": "Steel Pipes (MS Round & Square Hollow Sections 2-Inch)",
                "category_id": cat_map["steel"],
                "supplier_id": supplier1.id,
                "price": Decimal("76.00"),
                "unit": "kg",
                "brand": "APL Apollo",
                "description": "High torsional resistance hollow structural pipe for staircase railings, boundary gates, canopy framing, and scaffolding poles.",
                "stock": 2200,
                "image_url": "/images/materials/steel_pipes.png"
            },

            # 3. BRICKS & BLOCKS (செங்கல்)
            {
                "name": "Red Clay Bricks (First Class Kiln-Fired Red Chamber Bricks)",
                "category_id": cat_map["bricks"],
                "supplier_id": supplier1.id,
                "price": Decimal("9.50"),
                "unit": "piece",
                "brand": "Standard Clay",
                "description": "First-class table-moulded kiln-fired red clay bricks with uniform cherry color, sharp edges, and high crushing resistance (> 3.5 MPa).",
                "stock": 25000,
                "image_url": "/images/materials/red_clay_bricks.png"
            },
            {
                "name": "Fly Ash Bricks (Machine-Pressed Cement Fly Ash)",
                "category_id": cat_map["bricks"],
                "supplier_id": supplier1.id,
                "price": Decimal("7.80"),
                "unit": "piece",
                "brand": "EcoBricks",
                "description": "Eco-friendly uniform industrial bricks requiring 30% less mortar plastering with zero water absorption efflorescence.",
                "stock": 20000,
                "image_url": "/images/materials/fly_ash_bricks.png"
            },
            {
                "name": "AAC Blocks (Birla Aerocon / Magicrete 600x200x150mm)",
                "category_id": cat_map["bricks"],
                "supplier_id": supplier2.id,
                "price": Decimal("62.00"),
                "unit": "piece",
                "brand": "Birla Aerocon",
                "description": "Autoclaved Aerated Concrete lightweight thermal blocks cutting dead load by 50% with superior thermal insulation and fire safety.",
                "stock": 2500,
                "image_url": "/images/materials/aac_blocks.png"
            },
            {
                "name": "Solid Concrete Blocks (8-Inch Heavy Duty)",
                "category_id": cat_map["bricks"],
                "supplier_id": supplier2.id,
                "price": Decimal("44.00"),
                "unit": "piece",
                "brand": "BuildStone",
                "description": "High-density vibrated solid concrete blocks for load-bearing external perimeter walls, basement retaining and boundary walls.",
                "stock": 4000,
                "image_url": "/images/materials/solid_concrete_blocks.png"
            },
            {
                "name": "Hollow Concrete Blocks (8-Inch 2-Hole Acoustic)",
                "category_id": cat_map["bricks"],
                "supplier_id": supplier2.id,
                "price": Decimal("38.00"),
                "unit": "piece",
                "brand": "BuildStone",
                "description": "Precast hollow cavity masonry blocks providing thermal cooling and conduits for concealed electrical plumbing runs.",
                "stock": 3500,
                "image_url": "/images/materials/hollow_blocks.png"
            },
            {
                "name": "Paver Blocks (60mm Zig-Zag Heavy Duty Interlocking Tiles)",
                "category_id": cat_map["bricks"],
                "supplier_id": supplier1.id,
                "price": Decimal("18.50"),
                "unit": "piece",
                "brand": "UltraPaver",
                "description": "Interlocking hydraulic-pressed concrete block for car parking bays, factory driveways, and garden pedestrian pathways.",
                "stock": 6000,
                "image_url": "/images/materials/paver_blocks.png"
            },

            # 4. SAND (மணல்)
            {
                "name": "River Sand (Government Approved Natural Washed River Sand)",
                "category_id": cat_map["sand"],
                "supplier_id": supplier2.id,
                "price": Decimal("2400.00"),
                "unit": "ton",
                "brand": "Cauvery River Sand",
                "description": "Natural screened river bed sand certified zero-silt for high-grade finish plastering and historic lime-surkhi masonry.",
                "stock": 150,
                "image_url": "/images/materials/river_sand.png"
            },
            {
                "name": "M-Sand (Manufactured Concrete Sand Zone-II)",
                "category_id": cat_map["sand"],
                "supplier_id": supplier2.id,
                "price": Decimal("1450.00"),
                "unit": "ton",
                "brand": "RoboSand",
                "description": "VSI-crushed granite sand graded strictly to IS:383 Zone II for dense void-free structural RCC concrete slabs and columns.",
                "stock": 300,
                "image_url": "/images/materials/m_sand.png"
            },
            {
                "name": "P-Sand (Plastering Manufactured Sand Zone-IV)",
                "category_id": cat_map["sand"],
                "supplier_id": supplier2.id,
                "price": Decimal("1650.00"),
                "unit": "ton",
                "brand": "RoboSand",
                "description": "Air-classified fine washed sand under 150 microns for smooth interior wall rendering without shrinkage micro-cracks.",
                "stock": 250,
                "image_url": "/images/materials/p_sand.png"
            },
            {
                "name": "Plastering Sand (Ultra-Fine Washed Silica Plaster Sand)",
                "category_id": cat_map["sand"],
                "supplier_id": supplier2.id,
                "price": Decimal("1750.00"),
                "unit": "ton",
                "brand": "SilicaPlast",
                "description": "Screened fine-grain silica sand engineered specifically for ceiling plaster skim coats and decorative cornice mouldings.",
                "stock": 120,
                "image_url": "/images/materials/plastering_sand.png"
            },
            {
                "name": "Filter Sand (Graded Coarse Filtration & Drainage Sand)",
                "category_id": cat_map["sand"],
                "supplier_id": supplier2.id,
                "price": Decimal("1300.00"),
                "unit": "ton",
                "brand": "HydroFilter",
                "description": "Coarse round-grain quartz sand for rainwater harvesting recharge pits, drainage French drains, and water treatment filter beds.",
                "stock": 100,
                "image_url": "/images/materials/filter_sand.png"
            },

            # 5. GRAVEL & AGGREGATES (ஜல்லி)
            {
                "name": "6mm Jelly (6mm Granite Aggregate Chips)",
                "category_id": cat_map["gravel"],
                "supplier_id": supplier2.id,
                "price": Decimal("1050.00"),
                "unit": "ton",
                "brand": "Apex Quarry",
                "description": "Fine 6mm granite chips used for solid block manufacturing, thin mosaic flooring base, and precast window lintels.",
                "stock": 150,
                "image_url": "/images/materials/6mm_jelly.png"
            },
            {
                "name": "10mm Jelly (10mm Graded Concrete Coarse Jelly)",
                "category_id": cat_map["gravel"],
                "supplier_id": supplier2.id,
                "price": Decimal("1020.00"),
                "unit": "ton",
                "brand": "Apex Quarry",
                "description": "Clean machine-crushed 10mm aggregate essential for dense congested rebar beam consolidation and pumpable concrete.",
                "stock": 200,
                "image_url": "/images/materials/10mm_jelly.png"
            },
            {
                "name": "12mm Jelly (12mm Intermediate Blue Metal Aggregate)",
                "category_id": cat_map["gravel"],
                "supplier_id": supplier2.id,
                "price": Decimal("1000.00"),
                "unit": "ton",
                "brand": "Apex Quarry",
                "description": "Intermediate blue metal granite aggregate for floor screeds, compound wall beams, and precast drainage channels.",
                "stock": 180,
                "image_url": "/images/materials/12mm_jelly.png"
            },
            {
                "name": "20mm Jelly (20mm High-Strength Structural RCC Aggregate Jelly)",
                "category_id": cat_map["gravel"],
                "supplier_id": supplier2.id,
                "price": Decimal("980.00"),
                "unit": "ton",
                "brand": "Apex Quarry",
                "description": "Prime structural angular 20mm granite stone aggregate meeting IS 383 specifications for M20, M25, and M30 grade RCC slabs and columns.",
                "stock": 400,
                "image_url": "/images/materials/20mm_jelly.png"
            },
            {
                "name": "40mm Jelly (40mm Sub-Base & Foundation Heavy Jelly Stone)",
                "category_id": cat_map["gravel"],
                "supplier_id": supplier2.id,
                "price": Decimal("890.00"),
                "unit": "ton",
                "brand": "Apex Quarry",
                "description": "Large 40mm broken blue metal stone for Plain Cement Concrete (PCC) footing bed foundation, road metalling, and railway ballast.",
                "stock": 350,
                "image_url": "/images/materials/40mm_jelly.png"
            },
            {
                "name": "Stone Dust (Granite Crusher Dust for Masonry Bedding)",
                "category_id": cat_map["gravel"],
                "supplier_id": supplier2.id,
                "price": Decimal("650.00"),
                "unit": "ton",
                "brand": "Apex Quarry",
                "description": "Granite crusher screenings for paver tile leveling bedding, sub-base compaction, and trench pipe surround cushion.",
                "stock": 250,
                "image_url": "/images/materials/stone_dust.png"
            },
            {
                "name": "Crushed Stone (Machine-Crushed Hard Blue Granite Stone GSB)",
                "category_id": cat_map["gravel"],
                "supplier_id": supplier2.id,
                "price": Decimal("820.00"),
                "unit": "ton",
                "brand": "Apex Quarry",
                "description": "Graded wet-mix Granular Sub-Base (GSB) crushed rock mixture for solid pavement bases and driveway stabilization.",
                "stock": 300,
                "image_url": "/images/materials/crushed_stone.png"
            },

            # 6. TILES & FLOORING (டைல்ஸ்)
            {
                "name": "Ceramic Tiles (Digital Glazed Bathroom Wall Tiles 300x450mm)",
                "category_id": cat_map["tiles"],
                "supplier_id": supplier1.id,
                "price": Decimal("42.00"),
                "unit": "sqft",
                "brand": "Kajaria",
                "description": "Gloss-finish stain-resistant ceramic wall tiles for bathroom dado and kitchen splashbacks.",
                "stock": 4000,
                "image_url": "/images/materials/ceramic_tiles.png"
            },
            {
                "name": "Vitrified Tiles (Double Charged High-Gloss 600x600mm)",
                "category_id": cat_map["tiles"],
                "supplier_id": supplier1.id,
                "price": Decimal("68.00"),
                "unit": "sqft",
                "brand": "Kajaria",
                "description": "Nano-sealed 3-4mm double layer vitrified floor tiles with high abrasion resistance for living rooms and bedrooms.",
                "stock": 5000,
                "image_url": "/images/materials/vitrified_tiles.png"
            },
            {
                "name": "Porcelain Tiles (Full Body Matt Porcelain Slabs 600x1200mm)",
                "category_id": cat_map["tiles"],
                "supplier_id": supplier1.id,
                "price": Decimal("95.00"),
                "unit": "sqft",
                "brand": "Somany",
                "description": "Commercial-grade full body porcelain tile for luxury villas, office lobbies, and outdoor terraces.",
                "stock": 3200,
                "image_url": "/images/materials/porcelain_tiles.png"
            },
            {
                "name": "Granite (Black Galaxy / Tan Brown Polished Slabs)",
                "category_id": cat_map["tiles"],
                "supplier_id": supplier1.id,
                "price": Decimal("145.00"),
                "unit": "sqft",
                "brand": "Apex Granite",
                "description": "Mirror-polished 18mm natural granite slabs for kitchen counters, staircase treads, door thresholds, and vanity tops.",
                "stock": 2800,
                "image_url": "/images/materials/granite.png"
            },
            {
                "name": "Marble (Makrana Pure White Indian Marble Slabs)",
                "category_id": cat_map["tiles"],
                "supplier_id": supplier1.id,
                "price": Decimal("220.00"),
                "unit": "sqft",
                "brand": "Royal Marble",
                "description": "Classic cool natural crystalline calcium marble for temple rooms, luxury halls, and heritage floorings.",
                "stock": 1500,
                "image_url": "/images/materials/marble.png"
            },
            {
                "name": "Parking Tiles (Heavy-Duty Anti-Skid 300x300x12mm Paver Tiles)",
                "category_id": cat_map["tiles"],
                "supplier_id": supplier1.id,
                "price": Decimal("48.00"),
                "unit": "sqft",
                "brand": "Nitco",
                "description": "Heavy vehicular weight-rated parking floor tiles with punching relief pattern for vehicle garages and driveways.",
                "stock": 3500,
                "image_url": "/images/materials/parking_tiles.png"
            },
            {
                "name": "Wooden Flooring (Water-Resistant Laminated HDF AC4 Planks)",
                "category_id": cat_map["tiles"],
                "supplier_id": supplier1.id,
                "price": Decimal("110.00"),
                "unit": "sqft",
                "brand": "Action TESA",
                "description": "Click-lock acoustic German-technology interlocking wood flooring for master bedrooms and home theaters.",
                "stock": 2000,
                "image_url": "/images/materials/wooden_flooring.png"
            },
            {
                "name": "Anti-Skid Tiles (Matte R10 Textured Wet-Area Floor Tiles)",
                "category_id": cat_map["tiles"],
                "supplier_id": supplier1.id,
                "price": Decimal("45.00"),
                "unit": "sqft",
                "brand": "Somany",
                "description": "High friction textured ceramic tiles preventing slips in shower cubicles, swimming pool decks, and utility balconies.",
                "stock": 3000,
                "image_url": "/images/materials/anti_skid_tiles.png"
            },

            # 7. PAINT & FINISHES (பெயிண்ட்)
            {
                "name": "Interior Paint (Asian Paints Royale Luxury Interior Matt)",
                "category_id": cat_map["paint"],
                "supplier_id": supplier1.id,
                "price": Decimal("420.00"),
                "unit": "liter",
                "brand": "Asian Paints",
                "description": "Teflon-protected luxury acrylic interior wall paint with anti-fungal shield and washable stain-resistance.",
                "stock": 450,
                "image_url": "/images/materials/interior_paint.png"
            },
            {
                "name": "Exterior Paint (Asian Paints Apex Ultima Weatherproof)",
                "category_id": cat_map["paint"],
                "supplier_id": supplier1.id,
                "price": Decimal("340.00"),
                "unit": "liter",
                "brand": "Asian Paints",
                "description": "Silicone-infused exterior wall coating offering 7 years weather protection against tropical rain, UV bleaching, and algae.",
                "stock": 500,
                "image_url": "/images/materials/exterior_paint.png"
            },
            {
                "name": "Primer (Berger WeatherCoat Water-Based Exterior/Interior Wall Primer)",
                "category_id": cat_map["paint"],
                "supplier_id": supplier1.id,
                "price": Decimal("160.00"),
                "unit": "liter",
                "brand": "Berger",
                "description": "Deep-penetrating acrylic primer binding loose plaster dust and reducing topcoat paint consumption by 25%.",
                "stock": 400,
                "image_url": "/images/materials/primer.png"
            },
            {
                "name": "Wall Putty (Birla White Polymer-Modified Waterproof Putty 40kg)",
                "category_id": cat_map["paint"],
                "supplier_id": supplier1.id,
                "price": Decimal("920.00"),
                "unit": "bag",
                "brand": "Birla White",
                "description": "White cement-based fine polymer putty providing an ultra-smooth silk finish and water repellency prior to priming.",
                "stock": 350,
                "image_url": "/images/materials/wall_putty.png"
            },
            {
                "name": "Enamel Paint (Asian Paints Apcolite Premium Gloss Enamel)",
                "category_id": cat_map["paint"],
                "supplier_id": supplier1.id,
                "price": Decimal("380.00"),
                "unit": "liter",
                "brand": "Asian Paints",
                "description": "Oil-based mirror-gloss enamel paint for steel grills, window frames, wooden doors, and exterior gate protection.",
                "stock": 300,
                "image_url": "/images/materials/enamel_paint.png"
            },
            {
                "name": "Texture Paint (Exterior Heritage Granular Flake Texture Coating)",
                "category_id": cat_map["paint"],
                "supplier_id": supplier1.id,
                "price": Decimal("1250.00"),
                "unit": "bucket",
                "brand": "Asian Paints",
                "description": "Architectural high-build quartz sand finish creating textured patterns on building facade elevations.",
                "stock": 180,
                "image_url": "/images/materials/texture_paint.png"
            },
            {
                "name": "Waterproof Coating (Dr. Fixit Fastflex 2K Acrylic Flexible Polymer)",
                "category_id": cat_map["paint"],
                "supplier_id": supplier1.id,
                "price": Decimal("2450.00"),
                "unit": "bucket",
                "brand": "Dr. Fixit",
                "description": "Elastomeric 2-component membrane for terrace waterproofing, sunken toilet waterproofing, and underground water sumps.",
                "stock": 200,
                "image_url": "/images/materials/waterproof_coating.png"
            },
            {
                "name": "Wood Polish (Asian Paints Touchwood PU Clear Gloss Wood Varnish)",
                "category_id": cat_map["paint"],
                "supplier_id": supplier1.id,
                "price": Decimal("460.00"),
                "unit": "liter",
                "brand": "Asian Paints",
                "description": "Scratch-resistant polyurethane wood finish highlighting natural teakwood grain on front doors and banisters.",
                "stock": 150,
                "image_url": "/images/materials/wood_polish.png"
            },

            # 8. PLUMBING & DRAINAGE (பிளம்பிங்)
            {
                "name": "PVC Pipes (Supreme 4-Inch SWR Drainage & Rainwater Pipe 3m)",
                "category_id": cat_map["plumbing"],
                "supplier_id": supplier2.id,
                "price": Decimal("680.00"),
                "unit": "piece",
                "brand": "Supreme",
                "description": "Rigid polyvinyl chloride drainage pipe with rubber ring socket for storm water, sewage, and rainwater down-take stacks.",
                "stock": 400,
                "image_url": "/images/materials/pvc_pipes.png"
            },
            {
                "name": "CPVC Pipes (Ashirvad FlowGuard Plus SDR 11 Hot & Cold Pipe 1-Inch)",
                "category_id": cat_map["plumbing"],
                "supplier_id": supplier2.id,
                "price": Decimal("420.00"),
                "unit": "piece",
                "brand": "Ashirvad",
                "description": "Chlorinated polyvinyl chloride potable drinking water line withstanding temperatures up to 93°C for geyser connections.",
                "stock": 500,
                "image_url": "/images/materials/cpvc_pipes.png"
            },
            {
                "name": "UPVC Pipes (Astral Aquarius Lead-Free Plumbing Pipe 3/4-Inch)",
                "category_id": cat_map["plumbing"],
                "supplier_id": supplier2.id,
                "price": Decimal("310.00"),
                "unit": "piece",
                "brand": "Astral",
                "description": "Lead-free cold water distribution line resistant to corrosion and chemical calcification over 50 years lifespan.",
                "stock": 450,
                "image_url": "/images/materials/upvc_pipes.png"
            },
            {
                "name": "HDPE Pipes (High-Density Polyethylene Underground Coil 50m)",
                "category_id": cat_map["plumbing"],
                "supplier_id": supplier2.id,
                "price": Decimal("3200.00"),
                "unit": "coil",
                "brand": "Finolex",
                "description": "Flexible tough underground black HDPE pipe for main municipal water connection and borewell submersibles.",
                "stock": 80,
                "image_url": "/images/materials/hdpe_pipes.png"
            },
            {
                "name": "Pipe Elbows (Ashirvad CPVC 90-Degree Brass Threaded Elbows 1-Inch)",
                "category_id": cat_map["plumbing"],
                "supplier_id": supplier2.id,
                "price": Decimal("95.00"),
                "unit": "piece",
                "brand": "Ashirvad",
                "description": "Heavy brass insert female elbow ensuring leak-free transition to chrome-plated taps and shower arms.",
                "stock": 1200,
                "image_url": "/images/materials/pipe_elbows.png"
            },
            {
                "name": "Pipe Tees (Astral UPVC Equal Branch Plumbing Tee 1-Inch)",
                "category_id": cat_map["plumbing"],
                "supplier_id": supplier2.id,
                "price": Decimal("48.00"),
                "unit": "piece",
                "brand": "Astral",
                "description": "T-junction directional flow divider for balancing water supply into multiple bathroom lines.",
                "stock": 900,
                "image_url": "/images/materials/pipe_tees.png"
            },
            {
                "name": "Water Taps (Jaquar Solid Brass Chrome Plated Quarter-Turn Bib Tap)",
                "category_id": cat_map["plumbing"],
                "supplier_id": supplier2.id,
                "price": Decimal("950.00"),
                "unit": "piece",
                "brand": "Jaquar",
                "description": "Heavy forged solid brass construction with ceramic disc cartridge tested to 500,000 operation cycles.",
                "stock": 350,
                "image_url": "/images/materials/water_taps.png"
            },
            {
                "name": "Valves (Zoloto Heavy Duty Full Bore Brass Ball Valve 1-Inch)",
                "category_id": cat_map["plumbing"],
                "supplier_id": supplier2.id,
                "price": Decimal("680.00"),
                "unit": "piece",
                "brand": "Zoloto",
                "description": "Full bore flow isolation valve with PTFE packing seats for main water meter and tank shut-off lines.",
                "stock": 250,
                "image_url": "/images/materials/valves.png"
            },
            {
                "name": "Floor Traps (Jindal SS-304 Anti-Foul Cockroach Proof Trap 150mm)",
                "category_id": cat_map["plumbing"],
                "supplier_id": supplier2.id,
                "price": Decimal("240.00"),
                "unit": "piece",
                "brand": "Jindal",
                "description": "Stainless steel square drain grating with water seal trap blocking sewer gas odors and insect entry.",
                "stock": 600,
                "image_url": "/images/materials/floor_traps.png"
            },
            {
                "name": "Water Tanks (Sintex 1000 Liter Triple-Layer Antibacterial Overhead Tank)",
                "category_id": cat_map["plumbing"],
                "supplier_id": supplier2.id,
                "price": Decimal("7800.00"),
                "unit": "piece",
                "brand": "Sintex",
                "description": "FDA approved virgin food-grade plastic water storage tank with UV stabilization shield and anti-algae inner layer.",
                "stock": 45,
                "image_url": "/images/materials/water_tanks.png"
            },

            # 9. ELECTRICAL & WIRING (எலக்ட்ரிக்கல்)
            {
                "name": "Electrical Wires (Havells LifeLine Plus 2.5 sq mm FR Copper Wire 90m)",
                "category_id": cat_map["electrical"],
                "supplier_id": supplier1.id,
                "price": Decimal("2450.00"),
                "unit": "coil",
                "brand": "Havells",
                "description": "100% electrolytic annealed copper wire with flame-retardant low smoke insulation for lighting and power circuits.",
                "stock": 180,
                "image_url": "/images/materials/electrical_wires.png"
            },
            {
                "name": "Cables (Polycab 4-Core 6.0 sq mm Aluminium Armoured Power Cable 50m)",
                "category_id": cat_map["electrical"],
                "supplier_id": supplier1.id,
                "price": Decimal("8500.00"),
                "unit": "coil",
                "brand": "Polycab",
                "description": "Steel-tape armoured underground service cable connecting EB electric meter to main distribution panel.",
                "stock": 60,
                "image_url": "/images/materials/cables.png"
            },
            {
                "name": "Switches (Legrand Arteor / Anchor Roma 6A Modular Switch 10-Pack)",
                "category_id": cat_map["electrical"],
                "supplier_id": supplier1.id,
                "price": Decimal("480.00"),
                "unit": "box",
                "brand": "Legrand",
                "description": "Ultra-smooth soft click modular switches with silver cadmium oxide contacts for spark-free performance.",
                "stock": 500,
                "image_url": "/images/materials/switches.png"
            },
            {
                "name": "Sockets (Legrand 6/16A Universal 3-Pin Modular Power Socket)",
                "category_id": cat_map["electrical"],
                "supplier_id": supplier1.id,
                "price": Decimal("140.00"),
                "unit": "piece",
                "brand": "Legrand",
                "description": "Child-safe safety shutter power socket for ACs, refrigerators, water heaters, and power tools.",
                "stock": 700,
                "image_url": "/images/materials/sockets.png"
            },
            {
                "name": "MCB (Schneider Electric EasyPact 32A C-Curve Miniature Circuit Breaker)",
                "category_id": cat_map["electrical"],
                "supplier_id": supplier1.id,
                "price": Decimal("680.00"),
                "unit": "piece",
                "brand": "Schneider",
                "description": "10kA breaking capacity double pole circuit breaker tripping on short circuits and power overloads.",
                "stock": 350,
                "image_url": "/images/materials/mcb.png"
            },
            {
                "name": "Distribution Board (Havells 8-Way Double Door Metal Clad DB)",
                "category_id": cat_map["electrical"],
                "supplier_id": supplier1.id,
                "price": Decimal("1850.00"),
                "unit": "piece",
                "brand": "Havells",
                "description": "IP43 dust-protected cold-rolled steel consumer unit with copper busbar and neutral link.",
                "stock": 120,
                "image_url": "/images/materials/distribution_board.png"
            },
            {
                "name": "LED Lights (Philips 15W Concealed Round Ceiling Downlight Panel 5-Pack)",
                "category_id": cat_map["electrical"],
                "supplier_id": supplier1.id,
                "price": Decimal("1650.00"),
                "unit": "box",
                "brand": "Philips",
                "description": "Warm white / Cool daylight 1500 lumen energy-saving LED slim recessed ceiling panels.",
                "stock": 250,
                "image_url": "/images/materials/led_lights.png"
            },
            {
                "name": "Conduits (VIP Heavy Mechanical 25mm Fire-Retardant PVC Conduit Pipes 3m)",
                "category_id": cat_map["electrical"],
                "supplier_id": supplier1.id,
                "price": Decimal("85.00"),
                "unit": "piece",
                "brand": "VIP",
                "description": "High impact resistant electrical conduit pipe cast inside RCC concrete slabs and chased into brick walls.",
                "stock": 1500,
                "image_url": "/images/materials/conduits.png"
            },
            {
                "name": "Junction Boxes (Precast Metal Galvanized 4-Way Wall Box)",
                "category_id": cat_map["electrical"],
                "supplier_id": supplier1.id,
                "price": Decimal("45.00"),
                "unit": "piece",
                "brand": "VIP",
                "description": "Deep stamped metal enclosure with grounding screw for wire pulling and branch connections.",
                "stock": 1000,
                "image_url": "/images/materials/junction_boxes.png"
            }
        ]

        logger.info(f"Adding {len(full_materials_list)} products to database...")
        for pdata in full_materials_list:
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
                rating=4.85,
                total_reviews=28
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

        deliv_partner_prof = db.query(DeliveryPartnerProfile).first()
        delivery = Delivery(
            order_id=order.id,
            delivery_partner_id=deliv_partner_prof.id if deliv_partner_prof else None,
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
        logger.info(f"Database successfully populated with all {len(categories_data)} categories and all {len(full_materials_list)} products!")
    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding database: {e}", exc_info=True)
    finally:
        db.close()

if __name__ == "__main__":
    seed_database(force_refresh=True)
