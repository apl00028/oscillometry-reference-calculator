import unittest

from equations import (
    calculate_bmi,
    gochicoa_r5r20,
    gochicoa_x5,
    gochicoa_fres,
    gochicoa_ax,
)


class TestGochicoaEquations(unittest.TestCase):

    def assert_close(self, observed, expected):
        self.assertAlmostEqual(observed, expected, places=10)

    def test_bmi(self):
        self.assert_close(
            calculate_bmi(65, 165),
            23.875114784205696,
        )

    def test_r5r20_adult(self):
        result = gochicoa_r5r20(
            60, "M", 165, 65, 0.08
        )

        self.assert_close(
            result["predicted"],
            0.05751370675291377,
        )
        self.assert_close(
            result["uln"],
            0.11475622675291378,
        )
        self.assert_close(
            result["z_score"],
            0.6461578519277653,
        )
        self.assertFalse(result["abnormal"])

    def test_r5r20_young(self):
        result = gochicoa_r5r20(
            10, "H", 140, 35, 0.10
        )

        self.assert_close(
            result["predicted"],
            0.14949269342857144,
        )

    def test_x5_adult(self):
        result = gochicoa_x5(
            60, "M", 165, 65, -0.15
        )

        self.assert_close(
            result["predicted"],
            -0.10428259396503495,
        )
        self.assert_close(
            result["lln"],
            -0.17139451396503497,
        )
        self.assertFalse(result["abnormal"])

    def test_x5_group_1(self):
        result = gochicoa_x5(
            4, "M", 105, 17, -0.20
        )

        self.assert_close(
            result["predicted"],
            -0.3969827134873949,
        )

    def test_x5_group_2(self):
        result = gochicoa_x5(
            10, "H", 140, 35, -0.15
        )

        self.assert_close(
            result["predicted"],
            -0.18286666457142858,
        )

    def test_fres_adult(self):
        result = gochicoa_fres(
            60, "M", 165, 65, 20
        )

        self.assert_close(
            result["predicted"],
            16.429633648496505,
        )
        self.assert_close(
            result["uln"],
            22.828294648496506,
        )
        self.assertFalse(result["abnormal"])

    def test_fres_group_1(self):
        result = gochicoa_fres(
            5, "M", 110, 20, 25
        )

        self.assert_close(
            result["predicted"],
            23.637503674090908,
        )

    def test_fres_group_2(self):
        result = gochicoa_fres(
            15, "H", 160, 50, 20
        )

        self.assert_close(
            result["predicted"],
            16.044237191,
        )


    def test_ax_group_1(self):
        result = gochicoa_ax(
            5, "M", 110, 20, 1.0
        )

        self.assert_close(
            result["predicted"],
            2.4725228348427755,
        )
        self.assert_close(
            result["uln"],
            4.514400597377983,
        )
        self.assertFalse(result["abnormal"])

    def test_ax_group_2(self):
        result = gochicoa_ax(
            15, "H", 160, 50, 1.0
        )

        self.assert_close(
            result["predicted"],
            0.49687817085447067,
        )
        self.assert_close(
            result["uln"],
            1.0606569581665997,
        )
        self.assertFalse(result["abnormal"])

    def test_ax_adult(self):
        result = gochicoa_ax(
            60, "M", 165, 65, 1.0
        )

        self.assert_close(
            result["predicted"],
            0.4927265194429299,
        )
        self.assert_close(
            result["uln"],
            1.3684543809200072,
        )
        self.assertFalse(result["abnormal"])

    def test_ax_must_be_positive(self):
        with self.assertRaises(ValueError):
            gochicoa_ax(
                60, "M", 165, 65, 0
            )


    def test_r5r20_adult_has_both_reference_limits(self):
        result = gochicoa_r5r20(
            60, "M", 165, 65, 0.08
        )

        self.assert_close(
            result["lln"],
            0.00027118675291377264,
        )
        self.assert_close(
            result["uln"],
            0.11475622675291378,
        )

    def test_x5_adult_has_both_reference_limits(self):
        result = gochicoa_x5(
            60, "M", 165, 65, -0.15
        )

        self.assert_close(
            result["lln"],
            -0.17139451396503497,
        )
        self.assert_close(
            result["uln"],
            -0.03717067396503494,
        )

    def test_fres_adult_has_both_reference_limits(self):
        result = gochicoa_fres(
            60, "M", 165, 65, 20
        )

        self.assert_close(
            result["lln"],
            10.030972648496505,
        )
        self.assert_close(
            result["uln"],
            22.828294648496506,
        )


if __name__ == "__main__":
    unittest.main()

