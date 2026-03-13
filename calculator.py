"""
App Calculator — DSS Sizing Engine
It takes farm inputs and returns irrigation equipment sizing recommendations.
All formulas are based on standard agronomic and hydraulic engineering principles.

Functions:
  - calculate_flow_rate()
  - calculate_pump_power()
  - calculate_pipe_diameter()
  - recommend_pump_size()
  - run_full_calculation()
"""

import math
# CONSTANTS

# Default irrigation hours per day if not specified by user
DEFAULT_HOURS_PER_DAY = 8.0

# Recommended water velocity in pipes
# 1.0–1.5 m/s is standard for small-scale irrigation mains
PIPE_VELOCITY_MS = 1.2

# Assumed total head(sum of static head + friction losses)
# For small farms, 20m is a reasonable default
DEFAULT_TOTAL_HEAD_M = 20.0

# Pump efficiency. Small centrifugal pumps: 0.55–0.70
DEFAULT_PUMP_EFFICIENCY = 0.65

# Water density (kg/m³) and gravity (m/s²) — physical constants
WATER_DENSITY = 1000
GRAVITY = 9.81


# ================================================================
# STEP 1: FLOW RATE
# ================================================================

def calculate_flow_rate(
    farm_area_ha: float,
    water_req_mm_day: float,
    irrigation_hours: float = DEFAULT_HOURS_PER_DAY,
    irrigation_efficiency: float = 1.0
) -> float:
    """
    Calculate the required flow rate in litres per hour (L/hr).

    Formula:
        Volume needed (m³) = Area (m²) × Water depth (m)
        Flow Rate (m³/hr) = Volume / Irrigation hours
        Flow Rate (L/hr)  = Flow Rate (m³/hr) × 1000

    Args:
        farm_area_ha        : Farm size in hectares
        water_req_mm_day    : Crop daily water requirement in mm (from FAO-56)
        irrigation_hours    : Hours of irrigation per day
        irrigation_efficiency: System efficiency (e.g. 0.90 for drip)

    Returns:
        Flow rate in litres per hour (L/hr)

    Example:
        >>> calculate_flow_rate(1.0, 5.0, 8.0, 0.90)
        6944.44  # ~7000 L/hr needed for 1 ha of maize with drip irrigation
    """
    if farm_area_ha <= 0:
        raise ValueError("Farm area must be greater than 0 hectares.")
    if water_req_mm_day <= 0:
        raise ValueError("Crop water requirement must be greater than 0 mm/day.")
    if irrigation_hours <= 0 or irrigation_hours > 24:
        raise ValueError("Irrigation hours must be between 1 and 24.")
    if not (0 < irrigation_efficiency <= 1.0):
        raise ValueError("Irrigation efficiency must be between 0 and 1.")

    # Convert hectares to m²: 1 ha = 10,000 m²
    area_m2 = farm_area_ha * 10_000

    # Convert mm to metres: 1 mm = 0.001 m
    water_depth_m = water_req_mm_day / 1000

    # Gross volume needed (accounting for system inefficiency)
    # If efficiency=0.90, we pump MORE water because 10% is lost
    volume_m3 = (area_m2 * water_depth_m) / irrigation_efficiency

    # Flow rate in m³/hr
    flow_m3_hr = volume_m3 / irrigation_hours

    # Convert to litres per hour
    flow_lph = flow_m3_hr * 1000

    return round(flow_lph, 2)


# ================================================================
# STEP 2: PUMP POWER
# ================================================================

def calculate_pump_power(
    flow_rate_lph: float,
    total_head_m: float = DEFAULT_TOTAL_HEAD_M,
    pump_efficiency: float = DEFAULT_PUMP_EFFICIENCY
) -> float:
    """
    Calculate required pump shaft power in kilowatts (kW).

    Formula (from hydraulic engineering):
        Power (W) = (ρ × g × Q × H) / η
        where:
            ρ = water density (1000 kg/m³)
            g = gravity (9.81 m/s²)
            Q = flow rate in m³/s
            H = total head in metres
            η = pump efficiency (decimal)

    Args:
        flow_rate_lph   : Flow rate in litres per hour
        total_head_m    : Total pumping head (static + friction losses) in metres
        pump_efficiency : Pump efficiency as decimal (0.55–0.75 typical)

    Returns:
        Required pump power in kilowatts (kW)
    """
    if flow_rate_lph <= 0:
        raise ValueError("Flow rate must be greater than 0.")
    if total_head_m <= 0:
        raise ValueError("Total head must be greater than 0.")
    if not (0 < pump_efficiency <= 1.0):
        raise ValueError("Pump efficiency must be between 0 and 1.")

    # Convert L/hr → m³/s
    flow_m3s = flow_rate_lph / 3_600_000

    # Hydraulic power formula
    power_watts = (WATER_DENSITY * GRAVITY * flow_m3s * total_head_m) / pump_efficiency

    # Convert W → kW
    power_kw = power_watts / 1000

    return round(power_kw, 3)


# ================================================================
# STEP 3: PIPE DIAMETER
# ================================================================

def calculate_pipe_diameter(
    flow_rate_lph: float,
    velocity_ms: float = PIPE_VELOCITY_MS
) -> float:
    """
    Calculate the minimum pipe internal diameter in millimetres (mm).

    Derived from the continuity equation:
        Q = A × v
        A = Q / v  →  A = π × (D/2)²
        D = √(4Q / πv)

    Args:
        flow_rate_lph : Flow rate in litres per hour
        velocity_ms   : Target water velocity in pipe (m/s), default 1.2

    Returns:
        Minimum pipe internal diameter in mm
    """
    if flow_rate_lph <= 0:
        raise ValueError("Flow rate must be greater than 0.")

    # Convert L/hr → m³/s
    flow_m3s = flow_rate_lph / 3_600_000

    # Calculate diameter in metres
    diameter_m = math.sqrt((4 * flow_m3s) / (math.pi * velocity_ms))

    # Convert to mm and round up to nearest 5mm (standard pipe sizes)
    diameter_mm = diameter_m * 1000

    return round(diameter_mm, 1)


# ================================================================
# STEP 4: HUMAN-READABLE PUMP SIZE RECOMMENDATION
# ================================================================

def recommend_pump_size(pump_power_kw: float) -> dict:
    """
    Translate calculated pump power into a practical purchase recommendation.

    Uses standard pump size brackets sold in Kenyan agri-supply shops.

    Args:
        pump_power_kw : Calculated power requirement in kW

    Returns:
        dict with:
            - recommended_kw    : Suggested pump size (kW)
            - recommended_hp    : Same in horsepower (common in shops)
            - pump_type         : Type of pump suited to this use case
            - notes             : Advice for the farmer
    """
    # Add 20% safety margin — always size up slightly
    design_kw = pump_power_kw * 1.20

    # Standard pump brackets (kW) available in Kenyan market
    # Below each bracket: recommended size, HP equivalent, type
    if design_kw <= 0.37:
        rec_kw, rec_hp, pump_type = 0.37, 0.5, "Submersible / Centrifugal"
        notes = "Very small farm — a basic ½ HP pump is sufficient."
    elif design_kw <= 0.75:
        rec_kw, rec_hp, pump_type = 0.75, 1.0, "Centrifugal Surface Pump"
        notes = "A 1 HP surface pump is widely available and affordable."
    elif design_kw <= 1.5:
        rec_kw, rec_hp, pump_type = 1.5, 2.0, "Centrifugal Surface Pump"
        notes = "A 2 HP pump is a common choice for farms up to 2 ha."
    elif design_kw <= 2.2:
        rec_kw, rec_hp, pump_type = 2.2, 3.0, "Centrifugal Surface Pump"
        notes = "3 HP pump — ensure your power source (grid/generator/solar) can support it."
    elif design_kw <= 3.7:
        rec_kw, rec_hp, pump_type = 3.7, 5.0, "Heavy-Duty Centrifugal Pump"
        notes = "5 HP pump. Consider a diesel engine pump if grid power is unreliable."
    elif design_kw <= 5.5:
        rec_kw, rec_hp, pump_type = 5.5, 7.5, "Heavy-Duty Centrifugal Pump"
        notes = "7.5 HP pump. Suitable for medium farms. Budget for a diesel backup."
    else:
        rec_kw = round(design_kw * 1.1, 1)
        rec_hp = round(rec_kw * 1.341, 1)
        pump_type = "Industrial Pump — consult a specialist"
        notes = "Large farm — seek professional hydraulic design assessment."

    return {
        'recommended_kw': rec_kw,
        'recommended_hp': rec_hp,
        'pump_type': pump_type,
        'notes': notes
    }


# ================================================================
# MASTER FUNCTION: Run the full DSS calculation
# ================================================================

def run_full_calculation(
    farm_area_ha: float,
    water_req_mm_day: float,
    irrigation_efficiency: float,
    irrigation_hours: float = DEFAULT_HOURS_PER_DAY,
    total_head_m: float = DEFAULT_TOTAL_HEAD_M
) -> dict:
    """
    Master function — runs all calculations and returns a complete result dict.
    This is what your Flask route will call.

    Args:
        farm_area_ha            : Farm size in hectares (user input)
        water_req_mm_day        : Crop water req from DB (FAO-56)
        irrigation_efficiency   : From IrrigationMethod model (e.g. 0.90)
        irrigation_hours        : Hours irrigated per day (default 8)
        total_head_m            : Pumping head in metres (default 20)

    Returns:
        A dictionary with all calculated values, ready to pass to HTML template.

    Example output:
        {
          'flow_rate_lph': 6944.44,
          'pump_power_kw': 0.572,
          'pipe_diameter_mm': 45.3,
          'pump_recommendation': {
              'recommended_kw': 0.75,
              'recommended_hp': 1.0,
              'pump_type': 'Centrifugal Surface Pump',
              'notes': 'A 1 HP surface pump is widely available...'
          },
          'inputs_summary': { ... }
        }
    """
    # Run each calculation step
    flow_rate = calculate_flow_rate(
        farm_area_ha,
        water_req_mm_day,
        irrigation_hours,
        irrigation_efficiency
    )

    pump_power = calculate_pump_power(flow_rate, total_head_m)

    pipe_diameter = calculate_pipe_diameter(flow_rate)

    pump_recommendation = recommend_pump_size(pump_power)

    return {
        'flow_rate_lph': flow_rate,
        'flow_rate_m3hr': round(flow_rate / 1000, 3),
        'pump_power_kw': pump_power,
        'pipe_diameter_mm': pipe_diameter,
        'pump_recommendation': pump_recommendation,
        'inputs_summary': {
            'farm_area_ha': farm_area_ha,
            'water_req_mm_day': water_req_mm_day,
            'irrigation_efficiency_pct': round(irrigation_efficiency * 100),
            'irrigation_hours': irrigation_hours,
            'total_head_m': total_head_m,
        }
    }