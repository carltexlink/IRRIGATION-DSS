from flask import Blueprint, make_response
from flask_login import login_required, current_user
from app.models import Recommendation, Farm, Supplier, Equipment
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
import io

reports = Blueprint('reports', __name__)

@reports.route('/report/<int:rec_id>')
@login_required
def generate_pdf(rec_id):
    rec = Recommendation.query.get_or_404(rec_id)
    farm = Farm.query.get(rec.farm_id)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)

    styles = getSampleStyleSheet()
    green = colors.HexColor('#198754')
    elements = []

    # Title
    title_style = ParagraphStyle('title', parent=styles['Title'],
                                  textColor=green, fontSize=18, spaceAfter=6)
    sub_style = ParagraphStyle('sub', parent=styles['Normal'],
                                textColor=colors.grey, fontSize=10, spaceAfter=20)
    elements.append(Paragraph('Irrigation Equipment Recommendation', title_style))
    elements.append(Paragraph(f'Generated for: {current_user.name}', sub_style))
    elements.append(Spacer(1, 0.3*cm))

    # Farm inputs section
    elements.append(Paragraph('Farm Details', styles['Heading2']))
    farm_data = [
        ['Field', 'Value'],
        ['Farm Size', f'{farm.farm_size} acres'],
        ['Crop Type', farm.crop_type.title()],
        ['Irrigation Method', farm.irrigation_method.title()],
        ['Water Source', farm.water_source.title()],
    ]
    farm_table = Table(farm_data, colWidths=[6*cm, 10*cm])
    farm_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), green),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(farm_table)
    elements.append(Spacer(1, 0.5*cm))

    # Pump recommendation section
    elements.append(Paragraph('Pump Recommendation', styles['Heading2']))
    pump_data = [
        ['Field', 'Value'],
        ['Recommended Size', f'{rec.pump_capacity} kW / {rec.pump_hp} HP'],
        ['Pump Type', rec.pump_type],
        ['Calculated Power', f'{rec.pump_power_kw} kW (before safety margin)'],
        ['Advice', rec.pump_notes],
    ]
    pump_table = Table(pump_data, colWidths=[6*cm, 10*cm])
    pump_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), green),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('WORDWRAP', (0, 0), (-1, -1), True),
    ]))
    elements.append(pump_table)
    elements.append(Spacer(1, 0.5*cm))

    # Pipe and flow section
    elements.append(Paragraph('Pipe & Flow', styles['Heading2']))
    pipe_data = [
        ['Field', 'Value'],
        ['Pipe Diameter', f'{rec.pipe_diameter} mm'],
        ['Flow Rate', f'{rec.flow_rate} L/hr  /  {rec.flow_rate_m3hr} m³/hr'],
    ]
    pipe_table = Table(pipe_data, colWidths=[6*cm, 10*cm])
    pipe_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), green),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(pipe_table)
    elements.append(Spacer(1, 0.5*cm))

    # Verified suppliers section
    matched = Equipment.query.join(Supplier).filter(
        Equipment.irrigation_method == farm.irrigation_method,
        Equipment.is_active == True,
        Supplier.is_approved == True
    ).all()

    if matched:
        elements.append(Paragraph('Verified Suppliers', styles['Heading2']))
        supplier_data = [['Supplier', 'Equipment', 'Type', 'Price (KES)']]
        for item in matched:
            sup = Supplier.query.get(item.supplier_id)
            supplier_data.append([
                sup.business_name,
                item.name,
                item.equipment_type.title(),
                f'{item.price:,.0f}'
            ])
        supplier_table = Table(supplier_data, colWidths=[4*cm, 6*cm, 3*cm, 3*cm])
        supplier_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), green),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(supplier_table)
        elements.append(Spacer(1, 0.5*cm))

    # Footer note
    note_style = ParagraphStyle('note', parent=styles['Normal'],
                                 textColor=colors.grey, fontSize=8, spaceAfter=0)
    elements.append(Paragraph(
        'This recommendation is generated by the Irrigation DSS. '
        'It assists decision-making but does not replace expert judgment.',
        note_style
    ))

    doc.build(elements)
    buffer.seek(0)
    response = make_response(buffer.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=irrigation_recommendation_{rec_id}.pdf'
    return response