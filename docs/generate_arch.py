"""Generate SMART BUILD architecture diagram image."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1400, 900
img = Image.new("RGB", (W, H), "#0F172A")
draw = ImageDraw.Draw(img)

# ── helpers ──────────────────────────────────────────────────────────────────
def rr(d, x0, y0, x1, y1, r=12, fill=None, outline=None, width=2):
    d.rounded_rectangle([x0, y0, x1, y1], radius=r, fill=fill, outline=outline, width=width)

def txt(d, x, y, text, size=14, color="#FFFFFF", anchor="mm"):
    try:
        f = ImageFont.truetype("arial.ttf", size)
    except Exception:
        f = ImageFont.load_default()
    d.text((x, y), text, font=f, fill=color, anchor=anchor)

def bold(d, x, y, text, size=14, color="#FFFFFF", anchor="mm"):
    try:
        f = ImageFont.truetype("arialbd.ttf", size)
    except Exception:
        try:
            f = ImageFont.truetype("arial.ttf", size)
        except Exception:
            f = ImageFont.load_default()
    d.text((x, y), text, font=f, fill=color, anchor=anchor)

def arrow(d, x1, y1, x2, y2, color="#64748B", w=2):
    d.line([(x1, y1), (x2, y2)], fill=color, width=w)
    # arrowhead
    dx, dy = x2 - x1, y2 - y1
    length = (dx**2 + dy**2) ** 0.5
    if length == 0:
        return
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    size = 8
    d.polygon([
        (x2, y2),
        (x2 - ux*size + px*size//2, y2 - uy*size + py*size//2),
        (x2 - ux*size - px*size//2, y2 - uy*size - py*size//2),
    ], fill=color)

# ── TITLE ─────────────────────────────────────────────────────────────────────
rr(draw, 350, 18, 1050, 58, r=10, fill="#1E293B", outline="#F59E0B", width=2)
bold(draw, 700, 38, "⚡  SMART BUILD — System Architecture", size=22, color="#F59E0B")

# ════════════════════════════════════════════════════════════════════════
# LAYER LABELS (left side)
# ════════════════════════════════════════════════════════════════════════
layers = [
    (80, "USERS",        "#64748B"),
    (200, "FRONTEND",    "#0EA5E9"),
    (350, "API GATEWAY", "#8B5CF6"),
    (500, "BACKEND",     "#10B981"),
    (650, "DATABASE",    "#F59E0B"),
    (790, "AI / ML",     "#EC4899"),
]
for cy, label, col in layers:
    bold(draw, 55, cy + 40, label, size=11, color=col, anchor="mm")

# ════════════════════════════════════════════════════════════════════════
# ROW 1 — USERS
# ════════════════════════════════════════════════════════════════════════
users = [
    (180,  70, "👷 Customer\n/ Builder",    "#0EA5E9"),
    (380,  70, "🏪 Material\nSupplier",     "#10B981"),
    (580,  70, "🚚 Delivery\nPartner",      "#F59E0B"),
    (780,  70, "🛡️ Admin",                 "#EC4899"),
]
for cx, cy, label, col in users:
    rr(draw, cx-70, cy, cx+70, cy+70, r=10, fill="#1E293B", outline=col, width=2)
    lines = label.split("\n")
    bold(draw, cx, cy + 20, lines[0], size=13, color=col)
    if len(lines) > 1:
        txt(draw, cx, cy + 38, lines[1], size=12, color="#CBD5E1")

# ════════════════════════════════════════════════════════════════════════
# ROW 2 — FRONTEND (Vercel)
# ════════════════════════════════════════════════════════════════════════
rr(draw, 115, 185, 920, 290, r=14, fill="#0C1A30", outline="#0EA5E9", width=2)
bold(draw, 170, 198, "▲ FRONTEND — Vercel  (smart-build-online.vercel.app)", size=13, color="#0EA5E9", anchor="lm")

fe_boxes = [
    (175, "React 19\n+ Vite",         "#1D4ED8"),
    (340, "Tailwind CSS\n+ Lucide UI", "#0369A1"),
    (505, "React Router\n(Role-based Routes)", "#0891B2"),
    (670, "Axios\nAPI Client",         "#6366F1"),
    (835, "PWA\nManifest",             "#7C3AED"),
]
for cx, label, col in fe_boxes:
    rr(draw, cx-70, 215, cx+70, 280, r=10, fill="#1E3A5F", outline=col, width=2)
    lines = label.split("\n")
    bold(draw, cx, 235, lines[0], size=12, color="#E2E8F0")
    if len(lines) > 1:
        txt(draw, cx, 254, lines[1], size=10, color="#94A3B8")

# ════════════════════════════════════════════════════════════════════════
# ROW 3 — API Gateway / Vercel Proxy
# ════════════════════════════════════════════════════════════════════════
rr(draw, 115, 320, 920, 390, r=14, fill="#1A0A2E", outline="#8B5CF6", width=2)
bold(draw, 180, 340, "🔀 API GATEWAY — Vercel Rewrite Proxy", size=13, color="#A78BFA", anchor="lm")
txt(draw, 180, 362, "vercel.json  ·  /api/(*) → https://smart-build-backend.onrender.com/api/$1", size=12, color="#C4B5FD", anchor="lm")
rr(draw, 680, 330, 910, 380, r=8, fill="#2E1065", outline="#7C3AED", width=1)
bold(draw, 795, 345, "HTTPS + CORS", size=11, color="#DDD6FE")
txt(draw, 795, 362, "JWT Bearer Token", size=10, color="#A78BFA")

# ════════════════════════════════════════════════════════════════════════
# ROW 4 — BACKEND (Render)
# ════════════════════════════════════════════════════════════════════════
rr(draw, 115, 420, 920, 540, r=14, fill="#061A0F", outline="#10B981", width=2)
bold(draw, 180, 435, "⚙️  BACKEND — Render  (smart-build-backend.onrender.com)", size=13, color="#10B981", anchor="lm")

be_boxes = [
    (175, "FastAPI\n+ Uvicorn",        "#059669"),
    (340, "SQLAlchemy 2\n+ Pydantic v2","#0D9488"),
    (505, "JWT Auth\n+ bcrypt",         "#0369A1"),
    (670, "24 REST API\nEndpoints",     "#7C3AED"),
    (835, "Alembic\nMigrations",        "#B45309"),
]
for cx, label, col in be_boxes:
    rr(draw, cx-70, 455, cx+70, 530, r=10, fill="#052E16", outline=col, width=2)
    lines = label.split("\n")
    bold(draw, cx, 474, lines[0], size=12, color="#D1FAE5")
    if len(lines) > 1:
        txt(draw, cx, 495, lines[1], size=10, color="#6EE7B7")

# ════════════════════════════════════════════════════════════════════════
# ROW 5 — DATABASE
# ════════════════════════════════════════════════════════════════════════
rr(draw, 115, 570, 660, 670, r=14, fill="#1C0A00", outline="#F59E0B", width=2)
bold(draw, 175, 585, "🗄️  DATABASE LAYER", size=13, color="#F59E0B", anchor="lm")

db_boxes = [
    (195, "SQLite\n(Dev / Auto-seed)",  "#92400E"),
    (390, "MySQL 8.0+\n(Production)",   "#B45309"),
    (585, "24 Normalized\nTables",      "#D97706"),
]
for cx, label, col in db_boxes:
    rr(draw, cx-85, 608, cx+85, 660, r=10, fill="#2D1600", outline=col, width=2)
    lines = label.split("\n")
    bold(draw, cx, 625, lines[0], size=12, color="#FDE68A")
    if len(lines) > 1:
        txt(draw, cx, 643, lines[1], size=10, color="#FCD34D")

# ════════════════════════════════════════════════════════════════════════
# ROW 5 — AI / ML
# ════════════════════════════════════════════════════════════════════════
rr(draw, 680, 570, 920, 670, r=14, fill="#1F0028", outline="#EC4899", width=2)
bold(draw, 800, 585, "🤖 AI / ML", size=13, color="#F472B6")
ai_items = ["BOQ Estimator", "Civil Rules Engine", "Pandas • NumPy", "Scikit-learn"]
for i, item in enumerate(ai_items):
    txt(draw, 800, 603 + i * 16, item, size=11, color="#FBCFE8")

# ════════════════════════════════════════════════════════════════════════
# ROW 6 — FEATURES summary bar
# ════════════════════════════════════════════════════════════════════════
rr(draw, 115, 695, 920, 780, r=14, fill="#0F172A", outline="#334155", width=1)
bold(draw, 517, 710, "🚀  KEY FEATURES", size=13, color="#94A3B8")
features = [
    "🛒 Marketplace",
    "📦 Order Mgmt",
    "💳 Payments",
    "🤖 AI BOQ Estimator",
    "⭐ Reviews",
    "🔔 Notifications",
    "🗺️ Delivery Track",
    "🛡️ Role-based Auth",
]
cols_feat = [160, 285, 410, 560, 710, 820, 940, 1070]  # limit to width
feat_x = [160, 275, 390, 530, 660, 775, 900, 1030]
# only 6 fit nicely
for i, (feat, fx) in enumerate(zip(features[:6], [175, 310, 445, 600, 740, 870])):
    rr(draw, fx-65, 724, fx+65, 764, r=8, fill="#1E293B", outline="#475569", width=1)
    txt(draw, fx, 744, feat, size=11, color="#CBD5E1")

# ════════════════════════════════════════════════════════════════════════
# VERTICAL ARROWS between layers
# ════════════════════════════════════════════════════════════════════════
arrow_x = 960
# Users → Frontend
arrow(draw, arrow_x - 870, 140, arrow_x - 870, 185, color="#0EA5E9", w=3)
# Frontend → Gateway
arrow(draw, arrow_x - 870, 290, arrow_x - 870, 320, color="#8B5CF6", w=3)
# Gateway → Backend
arrow(draw, arrow_x - 870, 390, arrow_x - 870, 420, color="#10B981", w=3)
# Backend → DB
arrow(draw, arrow_x - 870, 540, arrow_x - 870, 570, color="#F59E0B", w=3)
# Backend → AI
arrow(draw, arrow_x - 50, 540, arrow_x - 50, 570, color="#EC4899", w=3)

# ════════════════════════════════════════════════════════════════════════
# RIGHT SIDEBAR — DEPLOYMENT STACK
# ════════════════════════════════════════════════════════════════════════
rr(draw, 950, 70, 1365, 780, r=16, fill="#111827", outline="#374151", width=1)
bold(draw, 1157, 90, "☁️  DEPLOYMENT STACK", size=15, color="#E2E8F0")

deploy_items = [
    ("▲ Vercel",          "Frontend Hosting",          "CDN edge network, global",    "#0EA5E9"),
    ("🟣 Render",          "Backend Hosting",           "Auto-deploy from GitHub",     "#10B981"),
    ("🐙 GitHub",          "Source Control",            "main branch CI/CD",           "#6366F1"),
    ("🔑 JWT Auth",        "Stateless Authentication",  "Role-based access control",   "#F59E0B"),
    ("🗄️ SQLite / MySQL", "Database Options",          "Dev local / Prod cloud",      "#EC4899"),
    ("🤖 AI Engine",       "BOQ Estimation",            "66+ construction materials",  "#A78BFA"),
    ("🛡️ FastAPI Docs",   "Swagger UI",                "/api/docs — live API docs",   "#34D399"),
]
for i, (title, sub1, sub2, col) in enumerate(deploy_items):
    y0 = 115 + i * 94
    rr(draw, 965, y0, 1350, y0 + 80, r=10, fill="#1F2937", outline=col, width=2)
    bold(draw, 985, y0 + 18, title, size=14, color=col, anchor="lm")
    txt(draw, 985, y0 + 40, sub1, size=12, color="#CBD5E1", anchor="lm")
    txt(draw, 985, y0 + 58, sub2, size=11, color="#6B7280", anchor="lm")

# ════════════════════════════════════════════════════════════════════════
# FOOTER
# ════════════════════════════════════════════════════════════════════════
rr(draw, 115, 800, 920, 858, r=10, fill="#0F172A", outline="#1E293B", width=1)
bold(draw, 517, 818, "SMART BUILD — by Muruganantham G  •  Coimbatore, Tamil Nadu", size=12, color="#475569")
txt(draw, 517, 840, "Frontend: smart-build-online.vercel.app  •  Backend: smart-build-backend.onrender.com", size=11, color="#334155")

# Save
out = os.path.join(os.path.dirname(__file__), "architecture.png")
img.save(out, "PNG")
print(f"Saved → {out}")
