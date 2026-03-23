# Irrigation DSS — Decision Support System for Irrigation Equipment Sizing

A web-based decision support system that helps small-scale farmers in Kenya select correctly sized irrigation equipment before purchasing. Built as a Diploma in Business Information Technology project at Strathmore University.

---

## What It Does

This system takes four simple inputs from the farmer and returns accurate equipment recommendations based on real agronomic and hydraulic engineering standards (FAO-56).

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
├── .env               
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
    └── test_sizing.py      # 
```

---

