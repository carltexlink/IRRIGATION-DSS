from app import create_app, db
from app.models import User, Supplier, Equipment

app = create_app()

with app.app_context():

    suppliers_data = [
        {
            'name': 'Amiran Kenya',
            'email': 'sales@amiran.co.ke',
            'password': 'supplier123',
            'business_name': 'Amiran Kenya Ltd',
            'contact_email': 'sales@amiran.co.ke',
            'phone': '+254 20 533 000',
            'location': 'Nairobi, Kenya',
        },
        {
            'name': 'Netafim Kenya',
            'email': 'info@netafim.co.ke',
            'password': 'supplier123',
            'business_name': 'Netafim Kenya',
            'contact_email': 'info@netafim.co.ke',
            'phone': '+254 722 204 050',
            'location': 'Nairobi, Kenya',
        },
        {
            'name': 'Agri-Sol Kenya',
            'email': 'info@agrisol.co.ke',
            'password': 'supplier123',
            'business_name': 'Agri-Sol Kenya',
            'contact_email': 'info@agrisol.co.ke',
            'phone': '+254 733 610 800',
            'location': 'Nakuru, Kenya',
        },
    ]

    supplier_ids = []

    for s in suppliers_data:
        user = User(name=s['name'], email=s['email'], role='seller')
        user.set_password(s['password'])
        db.session.add(user)
        db.session.flush()

        supplier = Supplier(
            business_name=s['business_name'],
            contact_email=s['contact_email'],
            phone=s['phone'],
            location=s['location'],
            is_approved=False,
            user_id=user.id
        )
        db.session.add(supplier)
        db.session.flush()
        supplier_ids.append(supplier.id)

    db.session.commit()

    equipment_data = [
        {'name': 'Grundfos CM 1 HP Pump', 'equipment_type': 'pump', 'irrigation_method': 'drip', 'price': 18500, 'supplier_id': supplier_ids[0]},
        {'name': 'Grundfos CM 2 HP Pump', 'equipment_type': 'pump', 'irrigation_method': 'sprinkler', 'price': 28000, 'supplier_id': supplier_ids[0]},
        {'name': 'Drip Tape 16mm (per metre)', 'equipment_type': 'pipe', 'irrigation_method': 'drip', 'price': 45, 'supplier_id': supplier_ids[0]},
        {'name': 'Drip Emitter Set (100 pcs)', 'equipment_type': 'valve', 'irrigation_method': 'drip', 'price': 1200, 'supplier_id': supplier_ids[0]},
        {'name': 'Netafim 1 HP Surface Pump', 'equipment_type': 'pump', 'irrigation_method': 'drip', 'price': 22000, 'supplier_id': supplier_ids[1]},
        {'name': 'Netafim 3 HP Surface Pump', 'equipment_type': 'pump', 'irrigation_method': 'sprinkler', 'price': 45000, 'supplier_id': supplier_ids[1]},
        {'name': 'uPVC Pipe 50mm (per metre)', 'equipment_type': 'pipe', 'irrigation_method': 'surface', 'price': 320, 'supplier_id': supplier_ids[1]},
        {'name': 'Sprinkler Head (per unit)', 'equipment_type': 'sprinkler', 'irrigation_method': 'sprinkler', 'price': 850, 'supplier_id': supplier_ids[1]},
        {'name': 'Honda WB20 2 HP Pump', 'equipment_type': 'pump', 'irrigation_method': 'surface', 'price': 32000, 'supplier_id': supplier_ids[2]},
        {'name': 'Honda WB30 3 HP Pump', 'equipment_type': 'pump', 'irrigation_method': 'surface', 'price': 48000, 'supplier_id': supplier_ids[2]},
        {'name': 'HDPE Pipe 63mm (per metre)', 'equipment_type': 'pipe', 'irrigation_method': 'surface', 'price': 480, 'supplier_id': supplier_ids[2]},
        {'name': 'Gate Valve 50mm', 'equipment_type': 'valve', 'irrigation_method': 'drip', 'price': 1800, 'supplier_id': supplier_ids[2]},
    ]

    for e in equipment_data:
        item = Equipment(
            name=e['name'],
            equipment_type=e['equipment_type'],
            irrigation_method=e['irrigation_method'],
            price=e['price'],
            is_active=True,
            supplier_id=e['supplier_id']
        )
        db.session.add(item)

    db.session.commit()
    print('Suppliers and equipment seeded successfully!')