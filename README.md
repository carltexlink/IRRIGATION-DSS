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
| Farmer | Register, enter farm details, get recommendations, view suppliers, rate suppliers |
| Seller | Register with business details, manage equipment listings (add/edit/delete) |
| Admin | Approve sellers, manage users, configure sizing rules |

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
├── requirements.txt
├── .env                    # Environment variables (not committed)
├── seed.py                 # Sample data for development
├── app/
│   ├── __init__.py         # App factory
│   ├── models.py           # Database models
│   ├── sizing.py           # Connects calculator to database rules
│   ├── routes/
│   │   ├── auth.py         # Login, register, logout
│   │   ├── farmer.py       # Farm input, recommendations, ratings
│   │   ├── seller.py       # Equipment listings
│   │   ├── admin.py        # User management, sizing rules
│   │   └── reports.py      # PDF generation
│   ├── templates/          # HTML templates
│   └── static/             # CSS and JS
└── tests/
    └── test_sizing.py      # 25 pytest unit tests
```

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd IRRIGATION-DSS
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create the database

Open MySQL and run:
```sql
CREATE DATABASE irrigation_dss;
```

### 4. Configure environment variables

Create a `.env` file in the root directory:
```
SECRET_KEY=your-secret-key
DATABASE_URL=mysql+pymysql://root:yourpassword@localhost/irrigation_dss
```

### 5. Create tables
```bash
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
```

### 6. Create admin account
```bash
python -c "
from app import create_app, db
from app.models import User
app = create_app()
with app.app_context():
    admin = User(name='Admin', email='admin@irrigation.com', role='admin')
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
"
```

### 7. Seed sizing rules
```bash
python -c "
from app import create_app, db
from app.models import SizingRule
app = create_app()
with app.app_context():
    rules = [
        ('maize', 5.5, 'drip', 0.90), ('maize', 5.5, 'sprinkler', 0.75), ('maize', 5.5, 'surface', 0.60),
        ('beans', 4.5, 'drip', 0.90), ('beans', 4.5, 'sprinkler', 0.75), ('beans', 4.5, 'surface', 0.60),
        ('tomatoes', 6.0, 'drip', 0.90), ('tomatoes', 6.0, 'sprinkler', 0.75), ('tomatoes', 6.0, 'surface', 0.60),
        ('vegetables', 5.0, 'drip', 0.90), ('vegetables', 5.0, 'sprinkler', 0.75), ('vegetables', 5.0, 'surface', 0.60),
        ('other', 5.0, 'drip', 0.90), ('other', 5.0, 'sprinkler', 0.75), ('other', 5.0, 'surface', 0.60),
    ]
    for crop, water, method, eff in rules:
        db.session.add(SizingRule(crop_type=crop, water_req_mm_day=water, irrigation_method=method, efficiency=eff))
    db.session.commit()
    print('Done!')
"
```

### 8. Run the app
```bash
python run.py
```

Visit `http://127.0.0.1:5000`

---

## Running Tests
```bash
pytest tests/test_sizing.py -v
```

25 unit tests covering flow rate, pump power, pipe diameter, pump recommendations and full calculations.

---

## Sizing Engine

The core calculation engine (`calculator.py`) is based on:

- **FAO-56** crop water requirement standards for East Africa
- **Continuity equation** for pipe diameter sizing
- **Hydraulic pump power formula** — P = (ρgQH) / η
- **20% safety margin** on all pump recommendations
- Standard Kenyan market pump size brackets (0.5 HP to 7.5 HP)

Sizing rules (crop water requirements and irrigation efficiencies) are stored in the database and can be updated by the admin without touching code.

---

## Authors

- 223011
- 221293

Strathmore Institute of Management and Technology
Diploma in Business Information Technology — February 2026