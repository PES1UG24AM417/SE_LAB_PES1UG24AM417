import pytest
from hypothesis import given, settings, strategies as st

from airline_baggage import parse_booking, total_weight, tag_label


# 1. Booking code fuzz testing

@settings(max_examples=100)
@given(st.one_of(st.text(), st.none()))
def test_parse_booking_no_unhandled_crash(code):
    try:
        parse_booking(code)
    except (ValueError, TypeError):
        pass


# 2. Weight fuzz testing

@settings(max_examples=100)
@given(st.one_of(st.text(), st.none()))
def test_total_weight_no_unhandled_crash(weights):
    try:
        total_weight(weights)
    except (ValueError, TypeError):
        pass


# 3. Passenger name fuzz testing

@settings(max_examples=100)
@given(st.one_of(st.text(), st.none()))
def test_tag_label_no_unhandled_crash(name):
    try:
        tag_label(name)
    except (ValueError, TypeError):
        pass


# 4. Valid booking

def test_valid_booking():
    assert parse_booking("AI-203-12A") == ("AI", 203, "A")


# 5. Valid weight

def test_valid_weight():
    assert total_weight("10,20,15") == 45.0


# 6. Valid passenger name

def test_valid_tag():
    assert tag_label("vivek d") == "V. D"

@given(st.one_of(st.none(), st.just(""), st.just("vivek")))
def test_invalid_passenger_name(name):
    with pytest.raises(ValueError):
        tag_label(name)