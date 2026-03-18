from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import User, Supplier
from app import db
from flask import Blueprint, render_template, redirect, url_for, flash, request

admin = Blueprint('admin', __name__)

@admin.route('/admin/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        flash('Access denied.')
        return redirect(url_for('auth.login'))
    users = User.query.all()
    pending = Supplier.query.filter_by(is_approved=False).all()
    return render_template('dashboard_admin.html', users=users, pending=pending)

@admin.route('/admin/approve-seller/<int:supplier_id>')
@login_required
def approve_seller(supplier_id):
    if current_user.role != 'admin':
        flash('Access denied.')
        return redirect(url_for('auth.login'))
    supplier = Supplier.query.get_or_404(supplier_id)
    supplier.is_approved = True
    db.session.commit()
    flash('Supplier approved successfully.')
    return redirect(url_for('admin.dashboard'))

@admin.route('/admin/deactivate-user/<int:user_id>')
@login_required
def deactivate_user(user_id):
    if current_user.role != 'admin':
        flash('Access denied.')
        return redirect(url_for('auth.login'))
    user = User.query.get_or_404(user_id)
    user.is_approved = False
    db.session.commit()
    flash(f'{user.name} has been deactivated.')
    return redirect(url_for('admin.dashboard'))

@admin.route('/admin/activate-user/<int:user_id>')
@login_required
def activate_user(user_id):
    if current_user.role != 'admin':
        flash('Access denied.')
        return redirect(url_for('auth.login'))
    user = User.query.get_or_404(user_id)
    user.is_approved = True
    db.session.commit()
    flash(f'{user.name} has been activated.')
    return redirect(url_for('admin.dashboard'))

from app.models import User, Supplier, SizingRule

@admin.route('/admin/sizing-rules')
@login_required
def sizing_rules():
    if current_user.role != 'admin':
        flash('Access denied.')
        return redirect(url_for('auth.login'))
    rules = SizingRule.query.order_by(SizingRule.crop_type, SizingRule.irrigation_method).all()
    return render_template('sizing_rules.html', rules=rules)

@admin.route('/admin/sizing-rules/edit/<int:rule_id>', methods=['POST'])
@login_required
def edit_sizing_rule(rule_id):
    if current_user.role != 'admin':
        flash('Access denied.')
        return redirect(url_for('auth.login'))
    rule = SizingRule.query.get_or_404(rule_id)
    rule.water_req_mm_day = float(request.form.get('water_req_mm_day'))
    rule.efficiency = float(request.form.get('efficiency'))
    db.session.commit()
    flash(f'Rule for {rule.crop_type} / {rule.irrigation_method} updated.')
    return redirect(url_for('admin.sizing_rules'))