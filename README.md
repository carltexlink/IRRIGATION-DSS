# IRRIGATION-DSS
### Decision Support System for Correct Sizing of Irrigation Equipment for Small-Scale Farmers

A web-based application developed as an Information Systems project at Strathmore Institute of Management and Technology.

---

## 📌 Project Overview

Small-scale farmers often purchase incorrectly sized irrigation equipment due to limited technical knowledge, relying on guesswork or vendor advice. This system helps farmers select the right pump capacity, pipe diameter, and water flow rate based on their specific farm details — without needing any engineering background.

---

## 🎯 Objectives

- Evaluate gaps in existing irrigation sizing tools
- Analyse current irrigation practices among small-scale farmers
- Design a user-friendly Decision Support System (DSS)
- Develop and test the solution

---

## 👥 Users & Roles

| Role | Description |
|------|-------------|
| **Farmer** | Inputs farm details and receives equipment recommendations |
| **Seller** | Lists and manages verified irrigation equipment |
| **Admin** | Manages users, approves suppliers, configures sizing rules |

---

## ⚙️ System Inputs

- Farm size
- Crop type
- Irrigation method (drip, sprinkler, surface)
- Water source

## 📤 System Outputs

- Recommended pump capacity
- Pipe diameter
- Estimated water flow rate
- List of verified local suppliers

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python (Flask) |
| Database | MySQL |
| Testing | pytest |
| IDE | VS Code |

---

## 🗂️ System Modules

1. **User Authentication** – Login and role management
2. **Farm Input** – Capture and store farm details
3. **Decision Support** – Calculate and generate equipment recommendations
4. **Supplier Information** – Browse verified equipment suppliers
5. **Reporting** – Generate PDF recommendation summaries

---

## 🚀 Getting Started

# Clone the repository
git clone git@github.com:carltexlink/IRRIGATION-DSS.git
cd IRRIGATION-DSS

# Install dependencies
pip install -r requirements.txt

# Run the app
flask run


---

## 👨‍💻 Contributors

- Carlton (carltexlink)
- Ahadi