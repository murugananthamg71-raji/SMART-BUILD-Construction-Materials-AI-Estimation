import math
from typing import Dict, Any, List
from decimal import Decimal

# Standard civil engineering average market rates in INR (configurable)
BASE_UNIT_PRICES = {
    "cement_bag": Decimal("390.00"),    # per 50kg bag (OPC/PPC 53/43 grade)
    "steel_kg": Decimal("72.00"),       # per kg of Fe550D TMT rebar
    "brick_piece": Decimal("9.50"),     # per standard clay brick / fly ash block
    "sand_ton": Decimal("1450.00"),     # per metric ton of manufactured / river sand
    "gravel_ton": Decimal("980.00"),    # per metric ton of 20mm blue metal aggregate
    "tiles_sqft": Decimal("65.00"),     # per sq.ft vitrified double-charged tiles
    "paint_liter": Decimal("280.00")    # per liter premium acrylic emulsion
}

QUALITY_COST_MULTIPLIERS = {
    "Budget": Decimal("0.88"),
    "Standard": Decimal("1.00"),
    "Premium": Decimal("1.35")
}

CONSTRUCTION_TYPE_MULTIPLIERS = {
    "Residential": 1.0,
    "Commercial": 1.18,
    "Industrial": 1.32
}

def calculate_material_estimates(
    length: float,
    width: float,
    floors: int = 1,
    floor_height: float = 10.0,
    construction_type: str = "Residential",
    building_type: str = "Individual House",
    location: str = "Bangalore",
    quality: str = "Standard"
) -> Dict[str, Any]:
    """
    Computes structural construction material quantities and budgetary projections
    based on IS civil engineering rules of thumb.
    """
    plot_footprint = length * width
    built_up_area_sqft = plot_footprint * floors

    # Load factor based on structural category
    load_factor = CONSTRUCTION_TYPE_MULTIPLIERS.get(construction_type, 1.0)
    # Adjustment for floor height variance (> 10 ft)
    height_factor = max(1.0, floor_height / 10.0)
    effective_factor = load_factor * height_factor

    # 1. Cement: standard 0.42 bags / sq.ft
    cement_bags = math.ceil(built_up_area_sqft * 0.42 * effective_factor)

    # 2. Steel: standard 3.8 kg / sq.ft
    steel_kg = round(built_up_area_sqft * 3.8 * effective_factor, 1)

    # 3. Bricks: standard 8.5 bricks / sq.ft
    bricks_count = math.ceil(built_up_area_sqft * 8.5 * effective_factor)

    # 4. Sand: ~0.075 ton / sq.ft
    sand_ton = round(built_up_area_sqft * 0.075 * effective_factor, 2)

    # 5. Coarse Gravel / Aggregate: ~0.062 ton / sq.ft
    gravel_ton = round(built_up_area_sqft * 0.062 * effective_factor, 2)

    # 6. Tiles: ~1.25 sq.ft per sq.ft of built-up area
    tiles_sqft = round(built_up_area_sqft * 1.25, 1)

    # 7. Paint: ~0.18 liter per sq.ft (primer + 2 finish coats)
    paint_liter = round(built_up_area_sqft * 0.18 * height_factor, 1)

    # Calculate Material Costs
    q_mult = QUALITY_COST_MULTIPLIERS.get(quality, Decimal("1.00"))

    cost_cement = (Decimal(str(cement_bags)) * BASE_UNIT_PRICES["cement_bag"] * q_mult).quantize(Decimal("0.01"))
    cost_steel = (Decimal(str(steel_kg)) * BASE_UNIT_PRICES["steel_kg"] * q_mult).quantize(Decimal("0.01"))
    cost_bricks = (Decimal(str(bricks_count)) * BASE_UNIT_PRICES["brick_piece"] * q_mult).quantize(Decimal("0.01"))
    cost_sand = (Decimal(str(sand_ton)) * BASE_UNIT_PRICES["sand_ton"] * q_mult).quantize(Decimal("0.01"))
    cost_gravel = (Decimal(str(gravel_ton)) * BASE_UNIT_PRICES["gravel_ton"] * q_mult).quantize(Decimal("0.01"))
    cost_tiles = (Decimal(str(tiles_sqft)) * BASE_UNIT_PRICES["tiles_sqft"] * q_mult).quantize(Decimal("0.01"))
    cost_paint = (Decimal(str(paint_liter)) * BASE_UNIT_PRICES["paint_liter"] * q_mult).quantize(Decimal("0.01"))

    total_budget = cost_cement + cost_steel + cost_bricks + cost_sand + cost_gravel + cost_tiles + cost_paint

    breakdown = [
        {
            "material": "Cement",
            "quantity": cement_bags,
            "unit": "Bags (50kg)",
            "unit_price": float(BASE_UNIT_PRICES["cement_bag"] * q_mult),
            "estimated_cost": float(cost_cement),
            "specification": "53 Grade OPC / PPC for columns, slabs & brick masonry"
        },
        {
            "material": "Structural Steel",
            "quantity": steel_kg,
            "unit": "kg",
            "unit_price": float(BASE_UNIT_PRICES["steel_kg"] * q_mult),
            "estimated_cost": float(cost_steel),
            "specification": "Fe550D High-Ductility TMT Rebar (8mm, 10mm, 12mm, 16mm)"
        },
        {
            "material": "Bricks / Blocks",
            "quantity": bricks_count,
            "unit": "Pieces",
            "unit_price": float(BASE_UNIT_PRICES["brick_piece"] * q_mult),
            "estimated_cost": float(cost_bricks),
            "specification": "Red Clay Table-Moulded Bricks / Autoclaved Aerated Blocks"
        },
        {
            "material": "River / M-Sand",
            "quantity": sand_ton,
            "unit": "Tons",
            "unit_price": float(BASE_UNIT_PRICES["sand_ton"] * q_mult),
            "estimated_cost": float(cost_sand),
            "specification": "Washed Plastering & Concreting Grade M-Sand"
        },
        {
            "material": "Gravel (Coarse Aggregate)",
            "quantity": gravel_ton,
            "unit": "Tons",
            "unit_price": float(BASE_UNIT_PRICES["gravel_ton"] * q_mult),
            "estimated_cost": float(cost_gravel),
            "specification": "20mm & 12mm Blue Metal Granular Aggregate"
        },
        {
            "material": "Flooring & Wall Tiles",
            "quantity": tiles_sqft,
            "unit": "sq.ft",
            "unit_price": float(BASE_UNIT_PRICES["tiles_sqft"] * q_mult),
            "estimated_cost": float(cost_tiles),
            "specification": "Double-Charged Vitrified Ceramic & Anti-Skid Floor Tiles"
        },
        {
            "material": "Protective Paint & Primer",
            "quantity": paint_liter,
            "unit": "Liters",
            "unit_price": float(BASE_UNIT_PRICES["paint_liter"] * q_mult),
            "estimated_cost": float(cost_paint),
            "specification": "Interior Acrylic Emulsion + Exterior Weather-Coat"
        }
    ]

    return {
        "built_up_area_sqft": built_up_area_sqft,
        "cement_bags": cement_bags,
        "steel_kg": steel_kg,
        "bricks_count": bricks_count,
        "sand_ton": sand_ton,
        "gravel_ton": gravel_ton,
        "tiles_sqft": tiles_sqft,
        "paint_liter": paint_liter,
        "estimated_total_budget": float(total_budget),
        "breakdown": breakdown,
        "quality_tier": quality,
        "construction_type": construction_type,
        "building_type": building_type,
        "location": location,
        "disclaimer": "These are preliminary planning estimates calculated via rule-based civil engineering guidelines. Actual quantities depend on structural drawings, soil bearing capacity, architectural plans, site wastage, and professional structural engineer sign-off."
    }
