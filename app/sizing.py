from calculator import run_full_calculation

def calculate(farm):
    from app.models import SizingRule
    from app import db

    # Look up rule from database
    rule = SizingRule.query.filter_by(
        crop_type=farm.crop_type.lower(),
        irrigation_method=farm.irrigation_method.lower()
    ).first()

    # Fall back to safe defaults if rule not found
    water_req = rule.water_req_mm_day if rule else 5.0
    efficiency = rule.efficiency if rule else 0.75

    # Convert acres to hectares
    farm_area_ha = farm.farm_size * 0.4047

    result = run_full_calculation(
        farm_area_ha=farm_area_ha,
        water_req_mm_day=water_req,
        irrigation_efficiency=efficiency
    )

    return {
        'flow_rate': result['flow_rate_lph'],
        'pipe_diameter': result['pipe_diameter_mm'],
        'pump_capacity': result['pump_recommendation']['recommended_kw'],
        'pump_hp': result['pump_recommendation']['recommended_hp'],
        'pump_type': result['pump_recommendation']['pump_type'],
        'pump_notes': result['pump_recommendation']['notes'],
        'flow_rate_m3hr': result['flow_rate_m3hr'],
        'pump_power_kw': result['pump_power_kw'],
    }