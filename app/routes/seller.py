from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Equipment, Supplier
from app import db

seller = Blueprint('seller', __name__)

@seller.route('/seller/dashboard')
@login_required
def dashboard():
    equipment = Equipment.query.filter_by(supplier_id=current_user.id).all()
    return render_template('dashboard_seller.html', equipment=equipment)

@seller.route('/seller/add-equipment', methods=['GET', 'POST'])
@login_required
def add_equipment():
    if request.method == 'POST':
        item = Equipment(
            name=request.form.get('name'),
            equipment_type=request.form.get('equipment_type'),
            irrigation_method=request.form.get('irrigation_method'),
            price=float(request.form.get('price')),
            supplier_id=current_user.id
        )
        db.session.add(item)
        db.session.commit()
        flash('Equipment added successfully.')
        return redirect(url_for('seller.dashboard'))
    return render_template('dashboard_seller.html')

@seller.route('/seller/delete-equipment/<int:item_id>')
@login_required
def delete_equipment(item_id):
    item = Equipment.query.get_or_404(item_id)
    item.is_active = False
    db.session.commit()
    flash('Equipment removed.')
    return redirect(url_for('seller.dashboard'))