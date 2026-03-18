from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Farm, Recommendation, Equipment, Supplier, Rating
from app.sizing import calculate
from app import db
from sqlalchemy import func

farmer = Blueprint('farmer', __name__)

@farmer.route('/')
def home():
    return redirect(url_for('auth.login'))

@farmer.route('/dashboard')
@login_required
def dashboard():
    past_recs = db.session.query(Recommendation, Farm).join(
        Farm, Recommendation.farm_id == Farm.id
    ).filter(Farm.user_id == current_user.id).order_by(
        Recommendation.created_at.desc()
    ).all()
    return render_template('dashboard_farmer.html', user=current_user, past_recs=past_recs)

@farmer.route('/farm-input', methods=['GET', 'POST'])
@login_required
def farm_input():
    if request.method == 'POST':
        farm = Farm(
            farm_size=float(request.form.get('farm_size')),
            crop_type=request.form.get('crop_type'),
            irrigation_method=request.form.get('irrigation_method'),
            water_source=request.form.get('water_source'),
            user_id=current_user.id
        )
        db.session.add(farm)
        db.session.commit()
        result = calculate(farm)
        rec = Recommendation(
            pump_capacity=result['pump_capacity'],
            pump_hp=result['pump_hp'],
            pump_type=result['pump_type'],
            pump_notes=result['pump_notes'],
            pipe_diameter=result['pipe_diameter'],
            flow_rate=result['flow_rate'],
            flow_rate_m3hr=result['flow_rate_m3hr'],
            pump_power_kw=result['pump_power_kw'],
            farm_id=farm.id
        )
        db.session.add(rec)
        db.session.commit()
        return redirect(url_for('farmer.recommendation', rec_id=rec.id))
    return render_template('farm_input.html')

@farmer.route('/recommendation/<int:rec_id>')
@login_required
def recommendation(rec_id):
    rec = Recommendation.query.get_or_404(rec_id)
    farm = Farm.query.get(rec.farm_id)

    # Security check — farmer can only view their own recommendations
    if farm.user_id != current_user.id:
        flash('Access denied.')
        return redirect(url_for('farmer.dashboard'))

    matched_equipment = Equipment.query.join(Supplier).filter(
        Equipment.irrigation_method == farm.irrigation_method,
        Equipment.is_active == True,
        Supplier.is_approved == True
    ).all()

    suppliers_dict = {}
    for item in matched_equipment:
        sup = Supplier.query.get(item.supplier_id)
        if sup.id not in suppliers_dict:
            avg = db.session.query(func.avg(Rating.score)).filter_by(supplier_id=sup.id).scalar()
            count = Rating.query.filter_by(supplier_id=sup.id).count()
            suppliers_dict[sup.id] = {
                'supplier': sup,
                'items': [],
                'avg_rating': round(avg, 1) if avg else None,
                'rating_count': count
            }
        suppliers_dict[sup.id]['items'].append(item)

    return render_template('recommendation.html',
                           rec=rec,
                           farm=farm,
                           suppliers=list(suppliers_dict.values()))

@farmer.route('/rate-supplier/<int:supplier_id>', methods=['POST'])
@login_required
def rate_supplier(supplier_id):
    score = int(request.form.get('score'))
    comment = request.form.get('comment')

    existing = Rating.query.filter_by(
        farmer_id=current_user.id,
        supplier_id=supplier_id
    ).first()

    if existing:
        existing.score = score
        existing.comment = comment
        flash('Your rating has been updated.')
    else:
        rating = Rating(
            score=score,
            comment=comment,
            farmer_id=current_user.id,
            supplier_id=supplier_id
        )
        db.session.add(rating)
        flash('Thank you for your rating!')

    db.session.commit()
    return redirect(request.referrer or url_for('farmer.dashboard'))