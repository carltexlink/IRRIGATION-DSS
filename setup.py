from app import create_app, db
from app.models import User, SizingRule, Supplier, Equipment, Farm, Recommendation, Rating

app = create_app()

with app.app_context():

    # Drop all and recreate cleanly
    db.drop_all()
    db.create_all()
    print('✓ All tables created')

    # Verify all tables exist
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    expected = ['user', 'farm', 'recommendation', 'supplier', 'equipment', 'rating', 'sizing_rule']
    for table in expected:
        if table in tables:
            print(f'  ✓ {table}')
        else:
            print(f'  ✗ MISSING: {table}')

    # Create admin
    existing_admin = User.query.filter_by(email='admin@irrigation.com').first()
    if not existing_admin:
        admin = User(name='Admin', email='admin@irrigation.com', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print('✓ Admin user created')
    else:
        print('✓ Admin already exists')

    # Seed sizing rules
    if SizingRule.query.count() == 0:
        rules = [
            ('maize',      5.5, 'drip',      0.90),
            ('maize',      5.5, 'sprinkler', 0.75),
            ('maize',      5.5, 'surface',   0.60),
            ('beans',      4.5, 'drip',      0.90),
            ('beans',      4.5, 'sprinkler', 0.75),
            ('beans',      4.5, 'surface',   0.60),
            ('tomatoes',   6.0, 'drip',      0.90),
            ('tomatoes',   6.0, 'sprinkler', 0.75),
            ('tomatoes',   6.0, 'surface',   0.60),
            ('vegetables', 5.0, 'drip',      0.90),
            ('vegetables', 5.0, 'sprinkler', 0.75),
            ('vegetables', 5.0, 'surface',   0.60),
            ('other',      5.0, 'drip',      0.90),
            ('other',      5.0, 'sprinkler', 0.75),
            ('other',      5.0, 'surface',   0.60),
        ]
        for crop, water, method, eff in rules:
            db.session.add(SizingRule(
                crop_type=crop,
                water_req_mm_day=water,
                irrigation_method=method,
                efficiency=eff
            ))
        db.session.commit()
        print(f'✓ {len(rules)} sizing rules seeded')
    else:
        print(f'✓ Sizing rules already exist ({SizingRule.query.count()} rules)')

    print('\nAll done! Run: python run.py')