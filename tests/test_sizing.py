import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from calculator import (
    calculate_flow_rate,
    calculate_pump_power,
    calculate_pipe_diameter,
    recommend_pump_size,
    run_full_calculation
)

# ================================================================
# FLOW RATE TESTS
# ================================================================

def test_flow_rate_basic():
    """1 ha of maize with drip irrigation, 8 hours"""
    result = calculate_flow_rate(1.0, 5.0, 8.0, 0.90)
    assert result > 0
    assert isinstance(result, float)

def test_flow_rate_increases_with_area():
    """Larger farm needs more water"""
    small = calculate_flow_rate(1.0, 5.0, 8.0, 0.90)
    large = calculate_flow_rate(2.0, 5.0, 8.0, 0.90)
    assert large > small

def test_flow_rate_increases_with_water_req():
    """Higher crop water requirement = higher flow rate"""
    low = calculate_flow_rate(1.0, 3.0, 8.0, 0.90)
    high = calculate_flow_rate(1.0, 7.0, 8.0, 0.90)
    assert high > low

def test_flow_rate_efficiency_impact():
    """Lower efficiency = more water needed"""
    efficient = calculate_flow_rate(1.0, 5.0, 8.0, 0.90)
    inefficient = calculate_flow_rate(1.0, 5.0, 8.0, 0.60)
    assert inefficient > efficient

def test_flow_rate_invalid_area():
    """Zero or negative area should raise error"""
    try:
        calculate_flow_rate(0, 5.0, 8.0, 0.90)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass

def test_flow_rate_invalid_water_req():
    """Zero water requirement should raise error"""
    try:
        calculate_flow_rate(1.0, 0, 8.0, 0.90)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass

def test_flow_rate_invalid_hours():
    """More than 24 hours should raise error"""
    try:
        calculate_flow_rate(1.0, 5.0, 25.0, 0.90)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass

def test_flow_rate_invalid_efficiency():
    """Efficiency above 1.0 should raise error"""
    try:
        calculate_flow_rate(1.0, 5.0, 8.0, 1.5)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


# ================================================================
# PUMP POWER TESTS
# ================================================================

def test_pump_power_basic():
    """Basic pump power calculation returns positive kW"""
    result = calculate_pump_power(5000.0, 20.0, 0.65)
    assert result > 0
    assert isinstance(result, float)

def test_pump_power_increases_with_flow():
    """Higher flow rate = more power needed"""
    low = calculate_pump_power(3000.0, 20.0, 0.65)
    high = calculate_pump_power(6000.0, 20.0, 0.65)
    assert high > low

def test_pump_power_increases_with_head():
    """Higher head = more power needed"""
    low_head = calculate_pump_power(5000.0, 10.0, 0.65)
    high_head = calculate_pump_power(5000.0, 30.0, 0.65)
    assert high_head > low_head

def test_pump_power_efficiency_impact():
    """Less efficient pump needs more power"""
    efficient = calculate_pump_power(5000.0, 20.0, 0.75)
    inefficient = calculate_pump_power(5000.0, 20.0, 0.55)
    assert inefficient > efficient

def test_pump_power_invalid_flow():
    """Zero flow rate should raise error"""
    try:
        calculate_pump_power(0, 20.0, 0.65)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


# ================================================================
# PIPE DIAMETER TESTS
# ================================================================

def test_pipe_diameter_basic():
    """Basic pipe diameter calculation returns positive mm"""
    result = calculate_pipe_diameter(5000.0)
    assert result > 0
    assert isinstance(result, float)

def test_pipe_diameter_increases_with_flow():
    """Higher flow needs wider pipe"""
    small = calculate_pipe_diameter(2000.0)
    large = calculate_pipe_diameter(8000.0)
    assert large > small

def test_pipe_diameter_invalid_flow():
    """Zero flow should raise error"""
    try:
        calculate_pipe_diameter(0)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


# ================================================================
# PUMP RECOMMENDATION TESTS
# ================================================================

def test_recommend_small_pump():
    """Very small power gets 0.5 HP recommendation"""
    result = recommend_pump_size(0.2)
    assert result['recommended_hp'] == 0.5

def test_recommend_medium_pump():
    """Medium power gets 2 HP recommendation"""
    result = recommend_pump_size(1.0)
    assert result['recommended_hp'] == 2.0

def test_recommend_returns_all_fields():
    """Recommendation always returns all required fields"""
    result = recommend_pump_size(1.5)
    assert 'recommended_kw' in result
    assert 'recommended_hp' in result
    assert 'pump_type' in result
    assert 'notes' in result

def test_recommend_safety_margin():
    """Recommended size should always be >= calculated power"""
    power = 1.0
    result = recommend_pump_size(power)
    assert result['recommended_kw'] >= power


# ================================================================
# FULL CALCULATION TESTS
# ================================================================

def test_full_calculation_drip():
    """Full calculation for drip irrigation returns all keys"""
    result = run_full_calculation(
        farm_area_ha=1.0,
        water_req_mm_day=5.0,
        irrigation_efficiency=0.90
    )
    assert 'flow_rate_lph' in result
    assert 'pump_power_kw' in result
    assert 'pipe_diameter_mm' in result
    assert 'pump_recommendation' in result
    assert 'inputs_summary' in result

def test_full_calculation_surface():
    """Full calculation for surface irrigation"""
    result = run_full_calculation(
        farm_area_ha=2.0,
        water_req_mm_day=6.0,
        irrigation_efficiency=0.60
    )
    assert result['flow_rate_lph'] > 0
    assert result['pipe_diameter_mm'] > 0
    assert result['pump_power_kw'] > 0

def test_full_calculation_larger_farm_needs_more():
    """Larger farm always needs higher flow rate"""
    small = run_full_calculation(1.0, 5.0, 0.90)
    large = run_full_calculation(3.0, 5.0, 0.90)
    assert large['flow_rate_lph'] > small['flow_rate_lph']

def test_full_calculation_inputs_summary():
    """Inputs summary correctly reflects what was passed in"""
    result = run_full_calculation(
        farm_area_ha=1.5,
        water_req_mm_day=5.5,
        irrigation_efficiency=0.75
    )
    summary = result['inputs_summary']
    assert summary['farm_area_ha'] == 1.5
    assert summary['water_req_mm_day'] == 5.5
    assert summary['irrigation_efficiency_pct'] == 75