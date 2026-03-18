from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'farmer', 'seller', 'admin'
    is_approved = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    farms = db.relationship('Farm', backref='farmer', lazy=True)
    supplier_profile = db.relationship('Supplier', backref='user', uselist=False, lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Farm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    farm_size = db.Column(db.Float, nullable=False)             # in acres
    crop_type = db.Column(db.String(100), nullable=False)
    irrigation_method = db.Column(db.String(50), nullable=False)  # drip, sprinkler, surface
    water_source = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    recommendation = db.relationship('Recommendation', backref='farm', lazy=True)

class Recommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pump_capacity = db.Column(db.Float)       # recommended kW
    pump_hp = db.Column(db.Float)             # horsepower
    pump_type = db.Column(db.String(100))     # e.g. Centrifugal Surface Pump
    pump_notes = db.Column(db.String(255))    # advice for farmer
    pipe_diameter = db.Column(db.Float)       # mm
    flow_rate = db.Column(db.Float)           # litres/hour
    flow_rate_m3hr = db.Column(db.Float)      # m³/hour
    pump_power_kw = db.Column(db.Float)       # calculated power before safety margin
    farm_id = db.Column(db.Integer, db.ForeignKey('farm.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_name = db.Column(db.String(150), nullable=False)
    contact_email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    location = db.Column(db.String(150))
    is_approved = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    equipment = db.relationship('Equipment', backref='supplier', lazy=True)
    ratings = db.relationship('Rating', backref='supplier', lazy=True)

class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    equipment_type = db.Column(db.String(50), nullable=False)  # pump, pipe, valve
    irrigation_method = db.Column(db.String(50))
    price = db.Column(db.Float)
    is_active = db.Column(db.Boolean, default=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)       # 1 to 5
    comment = db.Column(db.String(255))
    farmer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Enforce one rating per farmer per supplier at database level
    __table_args__ = (
        db.UniqueConstraint('farmer_id', 'supplier_id', name='unique_farmer_supplier_rating'),
    )

class SizingRule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crop_type = db.Column(db.String(100), nullable=False)
    water_req_mm_day = db.Column(db.Float, nullable=False)
    irrigation_method = db.Column(db.String(50), nullable=False)
    efficiency = db.Column(db.Float, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Enforce one rule per crop + method combination
    __table_args__ = (
        db.UniqueConstraint('crop_type', 'irrigation_method', name='unique_crop_method_rule'),
    )