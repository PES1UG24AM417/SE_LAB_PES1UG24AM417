
import pytest
from airline_baggage import baggage_fee, carry_on_ok, check_in_status


# =====================================
# 1. BAGGAGE FEE TEST CASES
# =====================================

def test_within_allowance():
    assert baggage_fee("economy", 10, "domestic", False) == 0


def test_unknown_cabin():
    with pytest.raises(ValueError):
        baggage_fee("first", 10, "domestic", False)


def test_negative_weight():
    with pytest.raises(ValueError):
        baggage_fee("economy", -5, "domestic", False)


def test_member_extra_allowance():
    assert baggage_fee("economy", 25, "domestic", True) == 0


def test_business_member_no_extra_allowance():
    assert baggage_fee("business", 41, "domestic", True) == 20


def test_domestic_excess_baggage():
    assert baggage_fee("economy", 20, "domestic", False) == 100


def test_international_excess_baggage():
    assert baggage_fee("economy", 20, "international", False) == 225


def test_domestic_excess_above_20():
    assert baggage_fee("economy", 36, "domestic", False) == 840


def test_international_excess_above_20():
    assert baggage_fee("economy", 36, "international", False) == 2100


def test_other_route_excess_above_20():
    assert baggage_fee("economy", 36, "regional", False) == 1890


# =====================================
# 2. CARRY-ON BAGGAGE TEST CASES
# =====================================

def test_carry_on_ok():
    assert carry_on_ok(5, 1, False) is True


def test_infant_two_items():
    assert carry_on_ok(12, 2, True) is True


def test_infant_more_than_two_items():
    assert carry_on_ok(5, 3, True) is False


def test_weight_above_limit():
    assert carry_on_ok(8, 1, False) is False


def test_weight_at_limit():
    assert carry_on_ok(7, 1, False) is True


def test_non_infant_multiple_items():
    assert carry_on_ok(5, 2, False) is False


# =====================================
# 3. CHECK-IN STATUS TEST CASES
# =====================================

def test_domestic_baggage_open():
    assert check_in_status(60, True, False) == "open"


def test_domestic_baggage_late():
    assert check_in_status(45, True, False) == "late"


def test_domestic_baggage_closed():
    assert check_in_status(44, True, False) == "closed"


def test_domestic_without_baggage_open():
    assert check_in_status(45, False, False) == "open"


def test_domestic_without_baggage_late():
    assert check_in_status(30, False, False) == "late"


def test_international_baggage_open():
    assert check_in_status(120, True, True) == "open"


def test_international_baggage_late():
    assert check_in_status(105, True, True) == "late"


def test_international_without_baggage_closed():
    assert check_in_status(89, False, True) == "closed"
