from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Equipment, Supplier
from app import db

seller = Blueprint('seller', __name__)

@seller.route('/seller/dashboard')
@login_required
def dashboard():
    supplier = Supplier.query.filter_by(user_id=current_user.id).first()
    if not supplier:
        flash('No supplier profile found. Please contact admin.')
        return redirect(url_for('auth.login'))
    if not supplier.is_approved:
        flash('Your account is pending admin approval. You cannot manage listings yet.')
        return render_template('dashboard_seller.html', equipment=[], supplier=supplier)
    equipment = Equipment.query.filter_by(supplier_id=supplier.id, is_active=True).all()
    return render_template('dashboard_seller.html', equipment=equipment, supplier=supplier)

@seller.route('/seller/add-equipment', methods=['GET', 'POST'])
@login_required
def add_equipment():
    supplier = Supplier.query.filter_by(user_id=current_user.id).first()
    if not supplier:
        flash('No supplier profile found.')
        return redirect(url_for('auth.login'))
    if not supplier.is_approved:
        flash('Your account is pending admin approval.')
        return redirect(url_for('seller.dashboard'))
    if request.method == 'POST':
        item = Equipment(
            name=request.form.get('name'),
            equipment_type=request.form.get('equipment_type'),
            irrigation_method=request.form.get('irrigation_method'),
            price=float(request.form.get('price')),
            supplier_id=supplier.id
        )
        db.session.add(item)
        db.session.commit()
        flash('Equipment added successfully.')
        return redirect(url_for('seller.dashboard'))
    return render_template('dashboard_seller.html', equipment=[], supplier=supplier)

@seller.route('/seller/delete-equipment/<int:item_id>')
@login_required
def delete_equipment(item_id):
    supplier = Supplier.query.filter_by(user_id=current_user.id).first()
    item = Equipment.query.get_or_404(item_id)
    if item.supplier_id != supplier.id:
        flash('You do not have permission to remove this item.')
        return redirect(url_for('seller.dashboard'))
    item.is_active = False
    db.session.commit()
    flash('Equipment removed.')
    return redirect(url_for('seller.dashboard'))