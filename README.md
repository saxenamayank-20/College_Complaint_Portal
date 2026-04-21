# Complaint Portal

A simple complaint management portal built with Streamlit and MySQL.

This project is meant to make complaint handling easier for three kinds of users:
- Students can register, log in, and submit complaints.
- Grievance managers can review assigned complaints and update progress.
- Admins can monitor the full system and close complaints officially.

The app includes role-based dashboards, complaint tracking, timeline history, and an optional FastAPI layer.

## Features

- Student login and registration
- Complaint submission with category-based routing
- Separate dashboards for students, grievance managers, and admins
- Complaint status tracking and timeline history
- MySQL-backed data storage
- Optional FastAPI API

## Tech Stack

- Python
- Streamlit
- MySQL
- FastAPI

## Getting Started

### 1. Clone the project

```bash
git clone https://github.com/YOUR_USERNAME/Complaint_Complaint_Portal.git
cd Complaint_Complaint_Portal
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the MySQL database

Run this in MySQL:

```sql
CREATE DATABASE complaint_portal CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Add your environment variables

Copy `.env.example` to `.env`, then update it with your local values:

```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=complaint_portal

ADMIN_SEED_PASSWORD=change-me-admin
MANAGER_SEED_PASSWORD=change-me-manager
```

`.env` is already ignored by Git, so your local passwords will not be pushed.

### 6. Run the app

```bash
streamlit run main.py
```

The app usually opens at:

`http://localhost:8501`

## Optional API

If you also want to run the FastAPI backend:

```bash
uvicorn api.routes:app --reload --port 8000
```

API docs will be available at:

`http://localhost:8000/docs`

## Project Structure

```text
Complaint_Complaint_Portal/
|-- main.py
|-- README.md
|-- requirements.txt
|-- .env.example
|-- config/
|   `-- settings.py
|-- database/
|   |-- connection.py
|   `-- models.py
|-- app/
|   |-- components/
|   |   `-- ui.py
|   `-- pages/
|       |-- auth.py
|       |-- student.py
|       |-- manager.py
|       `-- admin.py
|-- api/
|   `-- routes.py
`-- tests/
```

## Notes

- Keep your real database password only in `.env`.
- Keep `.venv` local and do not push it to GitHub.
- If you plan to publish this project, avoid committing personal credentials or machine-specific settings.

## License

This project is for educational and personal use unless you choose to add a separate license.
