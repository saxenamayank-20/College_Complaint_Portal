"""database/models.py — All database operations (CRUD)."""
import bcrypt, random, string
from datetime import datetime
from database.connection import get_connection
from config.settings import (PREDEFINED_USERS, CATEGORY_MANAGER_MAP,
    STATUS_FLOW, PRIORITY_KEYWORDS, DEFAULT_PRIORITY, MANAGER_MEET_LINKS)


# ─── INIT ────────────────────────────────────────────────────────────────────
def init_db():
    conn = get_connection(); c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id VARCHAR(50) UNIQUE NOT NULL,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(150) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        role ENUM('student','grievance_manager','admin') NOT NULL,
        department VARCHAR(100), category VARCHAR(100),
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP)""")

    c.execute("""CREATE TABLE IF NOT EXISTS complaints (
        id INT AUTO_INCREMENT PRIMARY KEY,
        ticket_id VARCHAR(20) UNIQUE NOT NULL,
        student_id VARCHAR(50) NOT NULL,
        student_name VARCHAR(100), student_email VARCHAR(150), student_dept VARCHAR(100),
        title VARCHAR(200) NOT NULL, description TEXT NOT NULL,
        category VARCHAR(100) NOT NULL,
        priority ENUM('Low','Medium','High','Critical') NOT NULL,
        status ENUM('Pending','Assigned','In Progress','Resolved','Closed') NOT NULL DEFAULT 'Pending',
        assigned_to VARCHAR(50), manager_name VARCHAR(100), manager_email VARCHAR(150),
        student_remarks TEXT, manager_remarks TEXT,
        meet_link VARCHAR(300), close_requested TINYINT(1) DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        resolved_at DATETIME,
        FOREIGN KEY (student_id) REFERENCES users(user_id))""")

    c.execute("""CREATE TABLE IF NOT EXISTS complaint_history (
        id INT AUTO_INCREMENT PRIMARY KEY,
        ticket_id VARCHAR(20) NOT NULL, changed_by VARCHAR(50) NOT NULL,
        action VARCHAR(150) NOT NULL, old_status VARCHAR(50), new_status VARCHAR(50),
        note TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (ticket_id) REFERENCES complaints(ticket_id))""")

    c.execute("""CREATE TABLE IF NOT EXISTS manager_updates (
        id INT AUTO_INCREMENT PRIMARY KEY,
        ticket_id VARCHAR(20) NOT NULL, manager_id VARCHAR(50) NOT NULL,
        manager_name VARCHAR(100), update_text TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP)""")

    conn.commit(); _seed_users(conn); conn.close()


def _hash(pw): return bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()

def _seed_users(conn):
    c = conn.cursor()
    for u in PREDEFINED_USERS:
        c.execute("SELECT 1 FROM users WHERE user_id=%s", (u[0],))
        if not c.fetchone():
            try:
                cat = u[6] if u[6] is not None else None
                c.execute("INSERT INTO users (user_id,name,email,password,role,department,category) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                          (u[0], u[1], u[2], _hash(u[3]), u[4], u[5], cat))
                conn.commit()
            except Exception as e:
                print(f"[SEED] Skipping {u[0]}: {e}")
    conn.commit()


# ─── AUTH ────────────────────────────────────────────────────────────────────
def register_student(user_id, name, email, password, department):
    conn = get_connection(); c = conn.cursor()
    try:
        c.execute("INSERT INTO users (user_id,name,email,password,role,department) VALUES (%s,%s,%s,%s,'student',%s)",
                  (user_id, name, email, _hash(password), department))
        conn.commit(); return True, "Registration successful!"
    except Exception as e:
        err = str(e)
        if "user_id" in err or user_id in err: return False, "Student ID already exists."
        if "email" in err: return False, "Email already registered."
        return False, err
    finally: conn.close()
 

def login_user(user_id, password):
    conn = get_connection(); c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id=%s", (user_id,))
    row = c.fetchone(); conn.close()
    if row and bcrypt.checkpw(password.encode(), row["password"].encode()): return row
    return None


# ─── PRIORITY AUTO-DETECT ────────────────────────────────────────────────────
def auto_detect_priority(title, description, category):
    text = (title + " " + description + " " + category).lower()
    for level in ["Critical", "High", "Medium"]:
        if any(kw in text for kw in PRIORITY_KEYWORDS.get(level, [])):
            return level
    return DEFAULT_PRIORITY


# ─── COMPLAINTS ──────────────────────────────────────────────────────────────
def _gen_ticket():
    return "TKT-" + "".join(random.choices(string.ascii_uppercase, k=3)) + \
           "".join(random.choices(string.digits, k=5))


def submit_complaint(student_id, title, description, category, remarks=""):
    conn = get_connection(); c = conn.cursor()
    priority    = auto_detect_priority(title, description, category)
    manager_uid = CATEGORY_MANAGER_MAP.get(category, "GM002")

    c.execute("SELECT name,email FROM users WHERE user_id=%s", (manager_uid,))
    mgr = c.fetchone()
    mgr_name  = mgr["name"]  if mgr else "Unknown"
    mgr_email = mgr["email"] if mgr else ""

    c.execute("SELECT name,email,department FROM users WHERE user_id=%s", (student_id,))
    stu = c.fetchone()
    stu_name  = stu["name"]       if stu else ""
    stu_email = stu["email"]      if stu else ""
    stu_dept  = stu["department"] if stu else ""

    meet_link = MANAGER_MEET_LINKS.get(manager_uid) if priority == "Critical" else None
    ticket_id = _gen_ticket()

    c.execute("""INSERT INTO complaints
        (ticket_id,student_id,student_name,student_email,student_dept,
         title,description,category,priority,status,
         assigned_to,manager_name,manager_email,student_remarks,meet_link)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,'Assigned',%s,%s,%s,%s,%s)""",
        (ticket_id, student_id, stu_name, stu_email, stu_dept,
         title, description, category, priority,
         manager_uid, mgr_name, mgr_email, remarks, meet_link))

    note = f"Assigned to {mgr_name} | Priority auto-detected: {priority}"
    if priority == "Critical": note += " | CRITICAL: Google Meet link generated"
    c.execute("INSERT INTO complaint_history (ticket_id,changed_by,action,old_status,new_status,note) VALUES (%s,%s,'Complaint Submitted',NULL,'Assigned',%s)",
              (ticket_id, student_id, note))
    conn.commit(); conn.close()
    return ticket_id, mgr_name, priority, meet_link


def get_student_complaints(student_id):
    conn = get_connection(); c = conn.cursor()
    c.execute("SELECT * FROM complaints WHERE student_id=%s ORDER BY created_at DESC", (student_id,))
    rows = c.fetchall(); conn.close(); return rows


def get_manager_complaints(manager_uid, resolved=False):
    conn = get_connection(); c = conn.cursor()
    if resolved:
        c.execute("SELECT * FROM complaints WHERE assigned_to=%s AND status IN ('Resolved','Closed') ORDER BY updated_at DESC", (manager_uid,))
    else:
        c.execute("SELECT * FROM complaints WHERE assigned_to=%s AND status NOT IN ('Resolved','Closed') ORDER BY created_at DESC", (manager_uid,))
    rows = c.fetchall(); conn.close(); return rows


def update_complaint_status(ticket_id, new_status, manager_uid, remark=""):
    conn = get_connection(); c = conn.cursor()
    c.execute("SELECT status FROM complaints WHERE ticket_id=%s", (ticket_id,))
    row = c.fetchone()
    if not row: conn.close(); return False, "Ticket not found."
    old = row["status"]
    resolved_at = datetime.now().isoformat() if new_status in ("Resolved","Closed") else None
    c.execute("UPDATE complaints SET status=%s,manager_remarks=%s,updated_at=CURRENT_TIMESTAMP,resolved_at=%s WHERE ticket_id=%s",
              (new_status, remark, resolved_at, ticket_id))
    c.execute("INSERT INTO complaint_history (ticket_id,changed_by,action,old_status,new_status,note) VALUES (%s,%s,'Status Updated',%s,%s,%s)",
              (ticket_id, manager_uid, old, new_status, remark))
    conn.commit(); conn.close(); return True, "Status updated."


def request_close(ticket_id, manager_uid):
    conn = get_connection(); c = conn.cursor()
    c.execute("UPDATE complaints SET close_requested=1 WHERE ticket_id=%s", (ticket_id,))
    c.execute("INSERT INTO complaint_history (ticket_id,changed_by,action,note) VALUES (%s,%s,'Close Requested','Manager sent close request to Admin')",
              (ticket_id, manager_uid))
    conn.commit(); conn.close()


def admin_close_complaint(ticket_id, admin_id):
    conn = get_connection(); c = conn.cursor()
    c.execute("UPDATE complaints SET status='Closed',close_requested=0,resolved_at=CURRENT_TIMESTAMP,updated_at=CURRENT_TIMESTAMP WHERE ticket_id=%s",
              (ticket_id,))
    c.execute("INSERT INTO complaint_history (ticket_id,changed_by,action,old_status,new_status,note) VALUES (%s,%s,'Admin Closed','Resolved','Closed','Complaint officially closed by Admin')",
              (ticket_id, admin_id))
    conn.commit(); conn.close()


def add_manager_update(ticket_id, manager_id, manager_name, update_text):
    conn = get_connection(); c = conn.cursor()
    c.execute("INSERT INTO manager_updates (ticket_id,manager_id,manager_name,update_text) VALUES (%s,%s,%s,%s)",
              (ticket_id, manager_id, manager_name, update_text))
    conn.commit(); conn.close()


def get_manager_updates():
    conn = get_connection(); c = conn.cursor()
    c.execute("""SELECT mu.*,c.title,c.category,c.priority,c.status
        FROM manager_updates mu JOIN complaints c ON mu.ticket_id=c.ticket_id
        ORDER BY mu.created_at DESC""")
    rows = c.fetchall(); conn.close(); return rows


def get_complaint_timeline(ticket_id):
    conn = get_connection(); c = conn.cursor()
    c.execute("SELECT * FROM complaint_history WHERE ticket_id=%s ORDER BY timestamp ASC", (ticket_id,))
    rows = c.fetchall(); conn.close(); return rows


def get_all_complaints():
    conn = get_connection(); c = conn.cursor()
    c.execute("SELECT * FROM complaints ORDER BY created_at DESC")
    rows = c.fetchall(); conn.close(); return rows


def get_all_complaints_by_category():
    from collections import defaultdict
    conn = get_connection(); c = conn.cursor()
    c.execute("SELECT * FROM complaints WHERE status!='Closed' ORDER BY created_at DESC")
    rows = c.fetchall(); conn.close()
    result = defaultdict(list)
    for r in rows: result[r["category"]].append(r)
    return dict(result)


def get_resolved_complaints():
    conn = get_connection(); c = conn.cursor()
    c.execute("""SELECT * FROM complaints
        WHERE status IN ('Resolved','Closed') OR close_requested=1
        ORDER BY updated_at DESC""")
    rows = c.fetchall(); conn.close(); return rows


def get_all_users(role=None):
    conn = get_connection(); c = conn.cursor()
    if role: c.execute("SELECT * FROM users WHERE role=%s ORDER BY created_at DESC", (role,))
    else: c.execute("SELECT * FROM users ORDER BY created_at DESC")
    rows = c.fetchall(); conn.close(); return rows


def get_stats():
    conn = get_connection(); c = conn.cursor(); stats = {}
    for s in STATUS_FLOW:
        c.execute("SELECT COUNT(*) AS n FROM complaints WHERE status=%s", (s,))
        stats[s] = c.fetchone()["n"]
    c.execute("SELECT COUNT(*) AS n FROM complaints"); stats["Total"] = c.fetchone()["n"]
    c.execute("SELECT COUNT(*) AS n FROM users WHERE role='student'"); stats["Students"] = c.fetchone()["n"]
    c.execute("SELECT COUNT(*) AS n FROM complaints WHERE close_requested=1"); stats["PendingClose"] = c.fetchone()["n"]
    c.execute("SELECT COUNT(*) AS n FROM complaints WHERE priority='Critical' AND status NOT IN ('Resolved','Closed')")
    stats["OpenCritical"] = c.fetchone()["n"]
    conn.close(); return stats
