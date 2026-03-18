from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Supplier
from app import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            if not user.is_approved:
                flash('Your account has been deactivated. Please contact admin.')
                return redirect(url_for('auth.login'))
            login_user(user)
            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif user.role == 'seller':
                return redirect(url_for('seller.dashboard'))
            else:
                return redirect(url_for('farmer.dashboard'))
        flash('Invalid email or password.')
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        if User.query.filter_by(email=email).first():
            flash('Email already registered.')
            return redirect(url_for('auth.register'))

        user = User(name=name, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.flush()

        if role == 'seller':
            business_name = request.form.get('business_name')
            phone = request.form.get('phone')
            location = request.form.get('location')

            if not business_name:
                flash('Please provide your business name.')
                return redirect(url_for('auth.register'))

            supplier = Supplier(
                business_name=business_name,
                contact_email=email,
                phone=phone,
                location=location,
                is_approved=False,
                user_id=user.id
            )
            db.session.add(supplier)
            flash('Seller account created! Please wait for admin approval before your products appear to farmers.')
        else:
            flash('Account created! Please log in.')

        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))