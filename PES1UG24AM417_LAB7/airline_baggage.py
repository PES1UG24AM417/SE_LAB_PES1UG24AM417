import math


# ==========================================
# 1. PARSE BOOKING
# ==========================================

def parse_booking(code):

    if not isinstance(code, str):
        raise ValueError("Booking code must be a string")

    parts = code.strip().split("-")

    if len(parts) != 3:
        raise ValueError("Invalid booking format")

    airline, flight, seat = parts

    if not airline.isalpha():
        raise ValueError("Invalid airline code")

    if not flight.isdigit():
        raise ValueError("Invalid flight number")

    if len(seat) < 2:
        raise ValueError("Invalid seat number")

    if not seat[:-1].isdigit() or not seat[-1].isalpha():
        raise ValueError("Invalid seat format")

    return airline.upper(), int(flight), seat[-1].upper()


# ==========================================
# 2. TOTAL WEIGHT
# ==========================================

def total_weight(weights_csv):

    if not isinstance(weights_csv, str):
        raise ValueError("Weights must be a string")

    if not weights_csv.strip():
        raise ValueError("Weight list cannot be empty")

    try:
        weights = [
            float(w.strip())
            for w in weights_csv.split(",")
        ]

    except ValueError:
        raise ValueError("Invalid weight value")

    if not all(math.isfinite(w) and w >= 0 for w in weights):
        raise ValueError("Weights must be finite and non-negative")

    return sum(weights)


# ==========================================
# 3. TAG LABEL
# ==========================================

def tag_label(name):

    if not isinstance(name, str):
        raise ValueError("Passenger name must be a string")

    parts = name.split()

    if len(parts) < 2:
        raise ValueError("Enter first and last name")

    return parts[0][0].upper() + ". " + parts[1].upper()


# ==========================================
# MAIN APPLICATION
# ==========================================

def main():

    print("==== Running parse_booking ====")

    user_input = input(
        "Enter a booking code (e.g. AI-203-12A): "
    )

    try:
        result = parse_booking(user_input)
        print("Airline, Flight and Seat Letter:", result)

    except ValueError as e:
        print("Invalid booking:", e)


    print("\n==== Running total_weight ====")

    user_input = input(
        "Enter bag weights in kg as CSV (e.g. 12.5,7,23): "
    )

    try:
        result = total_weight(user_input)
        print("Total Weight:", result)

    except ValueError as e:
        print("Invalid weights:", e)


    print("\n==== Running tag_label ====")

    user_input = input(
        "Enter a passenger name (first and last): "
    )

    try:
        result = tag_label(user_input)
        print("Tag Label:", result)

    except ValueError as e:
        print("Invalid passenger name:", e)


if __name__ == "__main__":
    main()