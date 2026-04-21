import os
from dotenv import load_dotenv

_ = load_dotenv()

ADMIN_SEED_PASSWORD = os.getenv("ADMIN_SEED_PASSWORD", "change-me-admin")
MANAGER_SEED_PASSWORD = os.getenv("MANAGER_SEED_PASSWORD", "change-me-manager")

# ─── MYSQL ────────────────────────────────────────────────────────────────────
DB_CONFIG = {
    "host":     os.getenv("MYSQL_HOST",     "localhost"),
    "port":     int(os.getenv("MYSQL_PORT", "3306")),
    "user":     os.getenv("MYSQL_USER",     "root"),
    # Support either MYSQL_PASSWORD or DB_PASSWORD from local .env files.
    "password": os.getenv("MYSQL_PASSWORD") or os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("MYSQL_DB",       "complaint_portal"),
}

# ─── PREDEFINED USERS (Admin + 4 Grievance Managers) ─────────────────────────
# Format: (user_id, full_name, email, password, role, department, category)
# Seed passwords come from environment variables so they do not need to live in Git.

PREDEFINED_USERS = [
    # ── ADMIN ──────────────────────────────────────────────────────────────────
    ("ADMIN001", "Super Admin",       "admin@college.edu",   ADMIN_SEED_PASSWORD,   "admin",            "Administration",  None),

    # ── GRIEVANCE MANAGERS ──────────────────────────────────────────────────────
    ("GM001",    "Dr. Rajesh Kumar",  "rajesh@college.edu",  MANAGER_SEED_PASSWORD, "grievance_manager", "Academics",       "Academic"),
    ("GM002",    "Ms. Priya Sharma",  "priya@college.edu",   MANAGER_SEED_PASSWORD, "grievance_manager", "Infrastructure",  "Infrastructure"),
    ("GM003",    "Mr. Anil Verma",    "anil@college.edu",    MANAGER_SEED_PASSWORD, "grievance_manager", "Student Affairs", "Hostel/Canteen"),
    ("GM004",    "Ms. Sunita Rao",    "sunita@college.edu",  MANAGER_SEED_PASSWORD, "grievance_manager", "Finance & Admin", "Administrative/Finance"),
]

# ─── CATEGORY → MANAGER MAPPING ───────────────────────────────────────────────
CATEGORY_MANAGER_MAP = {
    "Academic":              "GM001",
    "Examination":           "GM001",
    "Library":               "GM001",
    "Infrastructure":        "GM002",
    "IT/Internet":           "GM002",
    "Hostel":                "GM003",
    "Canteen":               "GM003",
    "Sports":                "GM003",
    "Ragging":               "GM003",
    "Fee/Finance":           "GM004",
    "Administrative":        "GM004",
    "Scholarship":           "GM004",
    "Other":                 "GM002",
}

CATEGORIES  = list(dict.fromkeys(CATEGORY_MANAGER_MAP.keys()))
STATUS_FLOW = ["Pending", "Assigned", "In Progress", "Resolved", "Closed"]

# ─── PRIORITY AUTO-DETECTION ──────────────────────────────────────────────────
PRIORITY_KEYWORDS = {
    "Critical": ["ragging","harassment","assault","threat","violence","emergency",
                 "critical","danger","safety","abuse","suicide","mental health"],
    "High":     ["exam","result","fees","scholarship","deadline","not working",
                 "broken","failed","error","blocked","urgent","immediately"],
    "Medium":   ["internet","wifi","library","hostel","canteen","maintenance",
                 "repair","issue","problem","concern"],
}
DEFAULT_PRIORITY = "Low"

# ─── GOOGLE MEET (Critical complaints) ───────────────────────────────────────
# Opens a new Meet session. Replace with fixed room links if preferred.
MANAGER_MEET_LINKS = {
    "GM001": "https://meet.google.com/new",
    "GM002": "https://meet.google.com/new",
    "GM003": "https://meet.google.com/new",
    "GM004": "https://meet.google.com/new",
}

APP_TITLE   = "College Complaint Portal"
INSTITUTION = "GLA University — CDOE"
