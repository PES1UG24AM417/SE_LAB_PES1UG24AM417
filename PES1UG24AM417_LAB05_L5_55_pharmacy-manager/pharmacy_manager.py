"""Pharmacy management system with stock, billing, and security features."""

import ast
import hashlib
import hmac
import json
import os
import secrets
from datetime import date, datetime
from typing import Any

medicines: dict[str, dict[str, Any]] = {}
DB_PASSWORD = os.environ.get("PHARMACY_PASSWORD", "")


def add_medicine(
    name: str,
    qty: int = 0,
    price: float = 0.0,
    expiry: str = "2099-12-31",
    audit: list[str] | None = None,
) -> list[str]:
    """Add medicine stock and record the operation."""
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Medicine name must be a non-empty string.")
    if qty < 0:
        raise ValueError("Quantity cannot be negative.")
    if price < 0:
        raise ValueError("Price cannot be negative.")

    datetime.strptime(expiry, "%Y-%m-%d")

    if audit is None:
        audit = []

    if name not in medicines:
        medicines[name] = {
            "qty": 0,
            "price": price,
            "expiry": expiry,
        }
    else:
        medicines[name]["price"] = price
        medicines[name]["expiry"] = expiry

    medicines[name]["qty"] += qty
    audit.append(
        f"{datetime.now()}: Stocked {qty} units of {name}"
    )
    return audit


def dispense_medicine(name: str, qty: int) -> None:
    """Dispense medicine after checking available stock."""
    if qty <= 0:
        raise ValueError("Dispensing quantity must be positive.")
    if name not in medicines:
        raise KeyError(f"Medicine not found: {name}")
    if medicines[name]["qty"] < qty:
        raise ValueError(f"Insufficient stock for {name}")

    medicines[name]["qty"] -= qty

    if medicines[name]["qty"] == 0:
        del medicines[name]


def get_quantity(name: str) -> int:
    """Return the available quantity of a medicine."""
    if name not in medicines:
        raise KeyError(f"Medicine not found: {name}")
    return medicines[name]["qty"]


def is_expired(name: str) -> bool:
    """Check whether a medicine has expired."""
    if name not in medicines:
        raise KeyError(f"Medicine not found: {name}")

    expiry = datetime.strptime(
        medicines[name]["expiry"], "%Y-%m-%d"
    ).date()
    return expiry < date.today()


def bill_amount(
    prescription: list[tuple[str, int]],
) -> float:
    """Calculate the total prescription cost."""
    total = 0.0

    for name, quantity in prescription:
        if quantity <= 0:
            raise ValueError("Prescription quantities must be positive.")
        if name not in medicines:
            raise KeyError(f"Medicine not found: {name}")

        total += medicines[name]["price"] * quantity

    return total


def calculate_dosage(formula: str) -> int | float:
    """Safely calculate a basic arithmetic dosage expression."""
    allowed_operators = (
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.FloorDiv,
        ast.Mod,
        ast.Pow,
        ast.UAdd,
        ast.USub,
    )

    def evaluate(node: ast.AST) -> int | float:
        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        if isinstance(node, ast.Constant) and type(node.value) in (
            int,
            float,
        ):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in allowed_operators:
            left = evaluate(node.left)
            right = evaluate(node.right)

            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Div):
                return left / right
            if isinstance(node.op, ast.FloorDiv):
                return left // right
            if isinstance(node.op, ast.Mod):
                return left % right
            if isinstance(node.op, ast.Pow):
                if abs(right) > 10 or abs(left) > 1_000_000:
                    raise ValueError("Exponent or base is too large.")
                return left**right

        if isinstance(node, ast.UnaryOp) and type(node.op) in (
            ast.UAdd,
            ast.USub,
        ):
            value = evaluate(node.operand)
            return value if isinstance(node.op, ast.UAdd) else -value

        raise ValueError("Invalid arithmetic expression.")

    if len(formula) > 100:
        raise ValueError("Expression is too long.")

    result = evaluate(ast.parse(formula, mode="eval"))

    if not isinstance(result, (int, float)) or not __import__(
        "math"
    ).isfinite(result):
        raise ValueError("Expression must produce a finite number.")

    return result


def patient_id(name: str, phone: str) -> str:
    """Generate a deterministic SHA-256 patient identifier."""
    value = f"{name}{phone}".encode("utf-8")
    return hashlib.sha256(value).hexdigest()


def generate_rx_number() -> str:
    """Generate a random prescription reference number."""
    return f"RX-{secrets.randbelow(900000) + 100000}"


def save_stock(file: str = "pharmacy.json") -> None:
    """Save medicine stock as JSON."""
    with open(file, "w", encoding="utf-8") as stock_file:
        json.dump(medicines, stock_file, indent=4)


def load_stock(file: str = "pharmacy.json") -> None:
    """Load and validate medicine stock from a JSON file."""
    global medicines

    with open(file, "r", encoding="utf-8") as stock_file:
        loaded = json.load(stock_file)

    if not isinstance(loaded, dict):
        raise ValueError("Invalid pharmacy stock data.")

    for name, details in loaded.items():
        if (
            not isinstance(name, str)
            or not isinstance(details, dict)
            or not isinstance(details.get("qty"), int)
            or isinstance(details.get("qty"), bool)
            or details["qty"] < 0
            or not isinstance(details.get("price"), (int, float))
            or isinstance(details.get("price"), bool)
            or details["price"] < 0
        ):
            raise ValueError("Invalid medicine record.")

        datetime.strptime(details["expiry"], "%Y-%m-%d")

    medicines = loaded


def print_label(name: str) -> None:
    """Print a medicine label without executing a shell command."""
    print(f"Dispensing label: {name}")


def expiring_soon(days: int = 30) -> list[str]:
    """Return medicines expiring within the specified number of days."""
    if days < 0:
        raise ValueError("Days cannot be negative.")

    result = []

    for name, details in medicines.items():
        expiry = datetime.strptime(
            details["expiry"], "%Y-%m-%d"
        ).date()

        remaining_days = (expiry - date.today()).days

        if 0 <= remaining_days < days:
            result.append(name)

    return result


def pharmacist_login(password: str) -> bool:
    """Verify the pharmacist password configured in the environment."""
    if not DB_PASSWORD:
        return False

    return hmac.compare_digest(password, DB_PASSWORD)


def print_stock() -> None:
    """Print the current pharmacy stock report."""
    print("===== Pharmacy Stock Report =====")

    for name, details in medicines.items():
        print(
            f"{name} -> {details['qty']} units, "
            f"Rs. {details['price']}, exp {details['expiry']}"
        )


def main() -> None:
    """Run the pharmacy management demonstration."""
    add_medicine("Paracetamol 500mg", 200, 1.5, "2027-06-30")
    add_medicine("Amoxicillin 250mg", 40, 6.0, "2026-01-15")
    add_medicine("Cetirizine 10mg", 10, 2.0, "2027-03-31")

    dispense_medicine("Paracetamol 500mg", 30)

    print(
        "Paracetamol stock:",
        get_quantity("Paracetamol 500mg"),
    )
    print(
        "Amoxicillin expired?",
        is_expired("Amoxicillin 250mg"),
    )
    print(
        "Bill:",
        bill_amount(
            [
                ("Paracetamol 500mg", 10),
                ("Amoxicillin 250mg", 5),
            ]
        ),
    )
    print("Dosage (mg/day):", calculate_dosage("250 * 2"))
    print("Patient ID:", patient_id("Asha", "9876543210"))
    print("Rx number:", generate_rx_number())
    print("Login:", pharmacist_login(DB_PASSWORD))
    print_label("Paracetamol 500mg")

    save_stock()
    load_stock()
    print_stock()


if __name__ == "__main__":
    main()
