"""
Currency-specific rules and formatting for international payments
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List, Any, Optional
from ..core.constants import PaymentCurrency


class CurrencyRules:
    def __init__(self):
        self.currency_data = self._load_currency_data()

    def _load_currency_data(self) -> Dict[str, Dict[str, Any]]:
        """Load currency-specific rules and formatting"""
        return {
            "USD": {
                "symbol": "$",
                "format": "${amount}",
                "decimal_places": 2,
                "thousands_separator": ",",
                "decimal_separator": ".",
                "formatting_rules": "prefix",
                "minimum_amount": Decimal("0.01"),
                "maximum_amount": Decimal("1000000.00"),
                "rounding_method": ROUND_HALF_UP,
                "allowed_denominations": [
                    0.01,
                    0.05,
                    0.10,
                    0.25,
                    1,
                    5,
                    10,
                    20,
                    50,
                    100,
                ],
            },
            "EUR": {
                "symbol": "€",
                "format": "€{amount}",
                "decimal_places": 2,
                "thousands_separator": ".",
                "decimal_separator": ",",
                "formatting_rules": "prefix",
                "minimum_amount": Decimal("0.01"),
                "maximum_amount": Decimal("1000000.00"),
                "rounding_method": ROUND_HALF_UP,
                "allowed_denominations": [
                    0.01,
                    0.02,
                    0.05,
                    0.10,
                    0.20,
                    0.50,
                    1,
                    2,
                    5,
                    10,
                    20,
                    50,
                    100,
                    200,
                    500,
                ],
            },
            "GBP": {
                "symbol": "£",
                "format": "£{amount}",
                "decimal_places": 2,
                "thousands_separator": ",",
                "decimal_separator": ".",
                "formatting_rules": "prefix",
                "minimum_amount": Decimal("0.01"),
                "maximum_amount": Decimal("1000000.00"),
                "rounding_method": ROUND_HALF_UP,
                "allowed_denominations": [
                    0.01,
                    0.02,
                    0.05,
                    0.10,
                    0.20,
                    0.50,
                    1,
                    2,
                    5,
                    10,
                    20,
                    50,
                ],
            },
            "JPY": {
                "symbol": "¥",
                "format": "¥{amount}",
                "decimal_places": 0,  # Japanese Yen typically doesn't use decimals
                "thousands_separator": ",",
                "decimal_separator": ".",
                "formatting_rules": "prefix",
                "minimum_amount": Decimal("1"),
                "maximum_amount": Decimal("100000000"),
                "rounding_method": ROUND_HALF_UP,
                "allowed_denominations": [
                    1,
                    5,
                    10,
                    50,
                    100,
                    500,
                    1000,
                    2000,
                    5000,
                    10000,
                ],
            },
            "KRW": {
                "symbol": "₩",
                "format": "₩{amount}",
                "decimal_places": 0,  # South Korean Won doesn't use decimals
                "thousands_separator": ",",
                "decimal_separator": ".",
                "formatting_rules": "prefix",
                "minimum_amount": Decimal("1"),
                "maximum_amount": Decimal("1000000000"),
                "rounding_method": ROUND_HALF_UP,
                "allowed_denominations": [
                    1,
                    5,
                    10,
                    50,
                    100,
                    500,
                    1000,
                    5000,
                    10000,
                    50000,
                ],
            },
            "RUB": {
                "symbol": "₽",
                "format": "{amount} ₽",
                "decimal_places": 2,
                "thousands_separator": " ",
                "decimal_separator": ",",
                "formatting_rules": "suffix",
                "minimum_amount": Decimal("0.01"),
                "maximum_amount": Decimal("10000000.00"),
                "rounding_method": ROUND_HALF_UP,
                "allowed_denominations": [
                    1,
                    2,
                    5,
                    10,
                    50,
                    100,
                    200,
                    500,
                    1000,
                    2000,
                    5000,
                ],
            },
            "CHF": {
                "symbol": "CHF",
                "format": "CHF {amount}",
                "decimal_places": 2,
                "thousands_separator": "'",
                "decimal_separator": ".",
                "formatting_rules": "prefix_space",
                "minimum_amount": Decimal("0.05"),
                "maximum_amount": Decimal("1000000.00"),
                "rounding_method": ROUND_HALF_UP,
                "allowed_denominations": [
                    0.05,
                    0.10,
                    0.20,
                    0.50,
                    1,
                    2,
                    5,
                    10,
                    20,
                    50,
                    100,
                    200,
                    1000,
                ],
            },
            "ARS": {
                "symbol": "$",
                "format": "${amount}",
                "decimal_places": 2,
                "thousands_separator": ".",
                "decimal_separator": ",",
                "formatting_rules": "prefix",
                "minimum_amount": Decimal("0.01"),
                "maximum_amount": Decimal("100000.00"),
                "rounding_method": ROUND_HALF_UP,
                "allowed_denominations": [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000],
            },
            "MXN": {
                "symbol": "$",
                "format": "${amount}",
                "decimal_places": 2,
                "thousands_separator": ",",
                "decimal_separator": ".",
                "formatting_rules": "prefix",
                "minimum_amount": Decimal("0.01"),
                "maximum_amount": Decimal("500000.00"),
                "rounding_method": ROUND_HALF_UP,
                "allowed_denominations": [
                    0.05,
                    0.10,
                    0.20,
                    0.50,
                    1,
                    2,
                    5,
                    10,
                    20,
                    50,
                    100,
                    200,
                    500,
                    1000,
                ],
            },
            "INR": {
                "symbol": "₹",
                "format": "₹{amount}",
                "decimal_places": 2,
                "thousands_separator": ",",
                "decimal_separator": ".",
                "formatting_rules": "prefix",
                "minimum_amount": Decimal("0.01"),
                "maximum_amount": Decimal("10000000.00"),
                "rounding_method": ROUND_HALF_UP,
                "allowed_denominations": [1, 2, 5, 10, 20, 50, 100, 200, 500, 2000],
            },
        }

    def format_amount(self, amount: Decimal, currency: PaymentCurrency) -> str:
        """Format amount according to currency rules"""
        currency_code = currency.value
        rules = self.currency_data.get(currency_code, self.currency_data["USD"])

        # Round according to currency rules
        rounded_amount = self.round_amount(amount, currency)

        # Format number with proper separators
        formatted_number = self._format_number(rounded_amount, rules)

        # Apply currency formatting
        format_template = rules["format"]
        return format_template.replace("{amount}", formatted_number)

    def _format_number(self, amount: Decimal, rules: Dict[str, Any]) -> str:
        """Format number with proper separators"""
        decimal_places = rules["decimal_places"]
        thousands_sep = rules["thousands_separator"]
        decimal_sep = rules["decimal_separator"]

        # Convert to string with proper decimal places
        if decimal_places == 0:
            number_str = f"{int(amount)}"
        else:
            number_str = f"{amount:.{decimal_places}f}"

        # Split integer and decimal parts
        if decimal_sep in number_str:
            integer_part, decimal_part = number_str.split(".")
        else:
            integer_part, decimal_part = number_str, ""

        # Add thousands separators
        integer_formatted = ""
        for i, digit in enumerate(reversed(integer_part)):
            if i > 0 and i % 3 == 0:
                integer_formatted = thousands_sep + integer_formatted
            integer_formatted = digit + integer_formatted

        # Combine parts
        if decimal_part:
            return f"{integer_formatted}{decimal_sep}{decimal_part}"
        else:
            return integer_formatted

    def round_amount(self, amount: Decimal, currency: PaymentCurrency) -> Decimal:
        """Round amount according to currency rules"""
        currency_code = currency.value
        rules = self.currency_data.get(currency_code, self.currency_data["USD"])

        decimal_places = rules["decimal_places"]
        rounding_method = rules["rounding_method"]

        # Round to specified decimal places
        rounding_format = f"0.{'0' * decimal_places}" if decimal_places > 0 else "0"
        rounded = amount.quantize(Decimal(rounding_format), rounding=rounding_method)

        return rounded

    def validate_amount(
        self, amount: Decimal, currency: PaymentCurrency
    ) -> Dict[str, Any]:
        """Validate amount against currency rules"""
        currency_code = currency.value
        rules = self.currency_data.get(currency_code, self.currency_data["USD"])

        validation_result = {
            "is_valid": True,
            "errors": [],
            "warnings": [],
            "rounded_amount": self.round_amount(amount, currency),
        }

        # Check minimum amount
        if amount < rules["minimum_amount"]:
            validation_result["is_valid"] = False
            validation_result["errors"].append(
                f"Amount below minimum {self.format_amount(rules['minimum_amount'], currency)}"
            )

        # Check maximum amount
        if amount > rules["maximum_amount"]:
            validation_result["is_valid"] = False
            validation_result["errors"].append(
                f"Amount above maximum {self.format_amount(rules['maximum_amount'], currency)}"
            )

        # Check if amount matches allowed denominations
        if not self._is_valid_denomination(amount, rules):
            validation_result["warnings"].append(
                "Amount doesn't match common denominations for this currency"
            )

        # Check decimal precision
        if not self._has_valid_precision(amount, rules):
            validation_result["is_valid"] = False
            validation_result["errors"].append(
                f"Amount has too many decimal places (max {rules['decimal_places']})"
            )

        return validation_result

    def _is_valid_denomination(self, amount: Decimal, rules: Dict[str, Any]) -> bool:
        """Check if amount matches common denominations"""
        allowed_denominations = rules.get("allowed_denominations", [])
        if not allowed_denominations:
            return True

        # For currencies without decimals, check integer amounts
        if rules["decimal_places"] == 0:
            return int(amount) in allowed_denominations

        # For currencies with decimals, this is more complex
        # In practice, you might want to check if the amount is a multiple of the smallest denomination
        smallest_denomination = min(allowed_denominations)
        remainder = amount % Decimal(str(smallest_denomination))

        return remainder == 0

    def _has_valid_precision(self, amount: Decimal, rules: Dict[str, Any]) -> bool:
        """Check if amount has valid decimal precision"""
        decimal_places = rules["decimal_places"]

        if decimal_places == 0:
            return amount == amount.to_integral_value()

        # Check number of decimal places
        amount_str = str(amount)
        if "." in amount_str:
            actual_decimal_places = len(amount_str.split(".")[1])
            return actual_decimal_places <= decimal_places

        return True

    def get_currency_info(self, currency: PaymentCurrency) -> Dict[str, Any]:
        """Get comprehensive currency information"""
        currency_code = currency.value
        rules = self.currency_data.get(currency_code, self.currency_data["USD"])

        return {
            "code": currency_code,
            "symbol": rules["symbol"],
            "name": self._get_currency_name(currency_code),
            "decimal_places": rules["decimal_places"],
            "format_example": self.format_amount(Decimal("1234.56"), currency),
            "minimum_amount": float(rules["minimum_amount"]),
            "maximum_amount": float(rules["maximum_amount"]),
            "formatting_rules": rules["formatting_rules"],
            "is_decimal_currency": rules["decimal_places"] > 0,
        }

    def _get_currency_name(self, currency_code: str) -> str:
        """Get currency name"""
        currency_names = {
            "USD": "US Dollar",
            "EUR": "Euro",
            "GBP": "British Pound",
            "JPY": "Japanese Yen",
            "KRW": "South Korean Won",
            "RUB": "Russian Ruble",
            "CHF": "Swiss Franc",
            "ARS": "Argentine Peso",
            "MXN": "Mexican Peso",
            "INR": "Indian Rupee",
        }
        return currency_names.get(currency_code, currency_code)

    def convert_and_format(
        self,
        amount: Decimal,
        from_currency: PaymentCurrency,
        to_currency: PaymentCurrency,
        exchange_rate: Decimal,
    ) -> Dict[str, Any]:
        """Convert amount and format for both currencies"""
        converted_amount = amount * exchange_rate
        rounded_converted = self.round_amount(converted_amount, to_currency)

        return {
            "original": {
                "amount": float(amount),
                "formatted": self.format_amount(amount, from_currency),
                "currency": from_currency.value,
            },
            "converted": {
                "amount": float(rounded_converted),
                "formatted": self.format_amount(rounded_converted, to_currency),
                "currency": to_currency.value,
            },
            "exchange_rate": float(exchange_rate),
            "is_accurate": converted_amount == rounded_converted,
        }
