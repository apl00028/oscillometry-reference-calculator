import sys
import unittest
from pathlib import Path

tool_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(tool_dir))

from validation import (
    parse_number,
    parse_optional_number,
    validate_demographics,
    validate_oscillometry_value,
)


class TestValidation(unittest.TestCase):

    def test_valid_demographics(self):
        result = validate_demographics(
            sex="Mujer",
            age=60,
            height_cm=165,
            weight_kg=65,
        )

        self.assertEqual(result["errors"], [])
        self.assertEqual(result["warnings"], [])
        self.assertAlmostEqual(
            result["bmi"],
            23.875114784205696,
            places=10,
        )

    def test_comma_decimal(self):
        self.assertEqual(
            parse_number("1,25", "Valor"),
            1.25,
        )

    def test_height_in_metres_is_error(self):
        result = validate_demographics(
            sex="Mujer",
            age=60,
            height_cm="1,65",
            weight_kg=65,
        )

        self.assertTrue(result["errors"])
        self.assertTrue(
            any(
                "metros" in error
                for error in result["errors"]
            )
        )

    def test_age_outside_reference_range_is_error(self):
        result = validate_demographics(
            sex="Hombre",
            age=91,
            height_cm=175,
            weight_kg=80,
        )

        self.assertTrue(
            any(
                "2,7-90" in error
                for error in result["errors"]
            )
        )

    def test_extreme_weight_generates_warning(self):
        result = validate_demographics(
            sex="Hombre",
            age=60,
            height_cm=180,
            weight_kg=260,
        )

        self.assertEqual(result["errors"], [])
        self.assertTrue(result["warnings"])

    def test_optional_empty_value(self):
        self.assertIsNone(
            parse_optional_number("", "AX")
        )

    def test_optional_numeric_value(self):
        self.assertEqual(
            parse_optional_number("0,75", "AX"),
            0.75,
        )

    def test_ax_must_be_positive(self):
        with self.assertRaises(ValueError):
            validate_oscillometry_value(
                "AX",
                0,
            )

    def test_missing_parameter_is_allowed(self):
        self.assertIsNone(
            validate_oscillometry_value(
                "X5",
                "",
            )
        )


if __name__ == "__main__":
    unittest.main()
