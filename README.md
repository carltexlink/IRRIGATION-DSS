# Irrigation DSS — Decision Support System for Irrigation Equipment Sizing

A web-based decision support system that helps small-scale farmers in Kenya select correctly sized irrigation equipment before purchasing. Built as a Diploma in Business Information Technology project at Strathmore University.

---

## What It Does

Small-scale farmers often buy wrongly sized pumps and pipes due to limited technical knowledge. This system takes four simple inputs from the farmer and returns accurate equipment recommendations based on real agronomic and hydraulic engineering standards (FAO-56).

**Inputs:**
- Farm size (acres)
- Crop type
- Irrigation method (drip, sprinkler, surface)
- Water source

**Outputs:**
- Recommended pump capacity (kW and HP)
- Pipe diameter (mm)
- Flow rate (L/hr and m³/hr)
- List of verified local suppliers selling relevant equipment
- Downloadable PDF report

---

## System Roles

| Role | What They Can Do |
|------|-----------------|
| Farmer | Register, enter farm details, get recommendations, view history, view suppliers, rate suppliers |
| Seller | Register with business details, manage equipment listings after admin approval |
| Admin | Approve sellers, manage users, configure FAO-56 sizing rules |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML, CSS, Bootstrap 5, Jinja2 |
| Backend | Python, Flask |
| Database | MySQL, SQLAlchemy |
| Auth | Flask-Login, Werkzeug |
| PDF | ReportLab |
| Testing | pytest |

---

## Project Structure
```
IRRIGATION-DSS/
├── run.py                  # Entry point
├── config.py               # App configuration
├── calculator.py           # Core sizing engine (FAO-56 formulas)
├── setup.py                # One-command database setup
├── seed.py                 # Optional sample supplier data
├── requirements.txt
├── .env                    # Environment variables (not committed)
├── app/
│   ├── __init__.py         # App factory
│   ├── models.py           # Database models
│   ├── sizing.py           # Connects calculator to database rules
│   ├── routes/
│   │   ├── auth.py         # Login, register, logout
│   │   ├── farmer.py       # Farm input, recommendations, history, ratings
│   │   ├── seller.py       # Equipment listings management
│   │   ├── admin.py        # User management, seller approval, sizing rules
│   │   └── reports.py      # PDF generation
│   ├── templates/          # HTML templates
│   └── static/             # CSS and JS
└── tests/
    └── test_sizing.py      # 24 pytest unit tests
```

---

## Quick Start (After Cloning)

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd IRRIGATION-DSS
```

### 2. Create and activate a virtual environment

On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

On Mac/Linux:
```bash
python -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal line.

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Start MySQL

**Using XAMPP:**
- Open XAMPP Control Panel
- Click **Start** next to MySQL
- Click **Admin** to open phpMyAdmin
- Click **New** on the left sidebar
- Type `irrigation_dss` and click **Create**

**Using MySQL directly:**
```sql
CREATE DATABASE irrigation_dss;
```

### 5. Create your `.env` file

Create a file called `.env` in the project root — this is not committed to git for security:

**If using XAMPP (no password):**
```
SECRET_KEY=supersecretkey123
DATABASE_URL=mysql+pymysql://root:@localhost/irrigation_dss
```

**If using MySQL with a password:**
```
SECRET_KEY=supersecretkey123
DATABASE_URL=mysql+pymysql://root:yourpassword@localhost/irrigation_dss
```

### 6. Run the setup script

This creates all tables, the admin account and seeds the FAO-56 sizing rules:
```bash
python setup.py
```

You should see:
```
✓ All tables created
  ✓ user
  ✓ farm
  ✓ recommendation
  ✓ supplier
  ✓ equipment
  ✓ rating
  ✓ sizing_rule
✓ Admin user created
✓ 15 sizing rules seeded

All done! Run: python run.py
```

### 7. Run the app
```bash
python run.py
```

Visit `http://127.0.0.1:5000`

---

## Default Admin Account

| Field | Value |
|-------|-------|
| Email | admin@irrigation.com |
| Password | admin123 |

> Change the password after first login in a production environment.

---

## Daily Startup

Once set up, every time you want to run the project:

1. Open XAMPP → click **Start** next to MySQL
2. Open your project in VS Code
3. Activate your virtual environment: `venv\Scripts\activate`
4. Run: `python run.py`
5. Visit `http://127.0.0.1:5000`

---

## Running Tests
```bash
pytest tests/test_sizing.py -v
```

24 unit tests covering flow rate, pump power, pipe diameter, pump recommendations and full calculations.

---

## Sizing Engine

The core calculation engine (`calculator.py`) is based on:

- **FAO-56** crop water requirement standards for East Africa
- **Continuity equation** for pipe diameter sizing: D = √(4Q / πv)
- **Hydraulic pump power formula**: P = (ρgQH) / η
- **20% safety margin** on all pump recommendations
- Standard Kenyan market pump size brackets (0.5 HP to 7.5 HP)

Sizing rules (crop water requirements and irrigation efficiencies) are stored in the database and can be updated by the admin without touching code.

---

## Security Features

- Password hashing with Werkzeug
- Role-based access control (farmer / seller / admin)
- Session-based authentication with Flask-Login
- Deactivated users cannot log in
- Farmers can only view their own recommendations
- Sellers can only manage their own equipment listings
- Only admin-approved suppliers appear to farmers
- Database-level unique constraints on ratings and sizing rules

---

## Authors

- 223011
- 221293

Strathmore Institute of Management and Technology
Diploma in Business Information Technology — February 2026