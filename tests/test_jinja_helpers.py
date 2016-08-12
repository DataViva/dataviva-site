#coding: utf-8

from dataviva.utils.jinja_helpers import max_digits
from flask import g
from test_base import BaseTestCase


class MaxDigitsPTTests(BaseTestCase):

    def setUp(self):
        g.locale = 'en'

    def test_max_digits_3_for_1_is_1(self):
        assert '1.00' == max_digits(1, 3)

    def test_max_digits_3_for_10_is_10(self):
        assert '10.0' == max_digits(10, 3)

    def test_max_digits_3_for_100_is_100(self):
        assert '100' == max_digits(100, 3)

    def test_max_digits_3_for_1000_is_1000(self):
        assert '1.00' == max_digits(1000, 3)

    def test_max_digits_3_for_10000_is_10000(self):
        assert '10.0' == max_digits(10000, 3)

    def test_max_digits_3_for_100000_is_100000(self):
        assert '100' == max_digits(100000, 3)

    def test_max_digits_3_for_001_is_001(self):
        assert '0.01' == max_digits(0.01, 3)

    def test_max_digits_3_for_decimal_0001_is_000(self):
        assert '0.00' == max_digits(0.001, 3)

    def test_max_digits_3_for_decimal_0009_is_001(self):
        assert '0.01' == max_digits(0.009, 3)

    def test_max_digits_3_for_decimal_0005_is_001(self):
        assert '0.01' == max_digits(0.005, 3)

    def test_max_digits_3_for_decimal_0003_is_001(self):
        assert '0.00' == max_digits(0.003, 3)

    def test_max_digits_3_for_decimal_50_600_is_50_6(self):
        assert '50.6' == max_digits(50.600, 3)

    def test_max_digits_3_for_decimal_100001000100_00_is_100(self):
        assert '100' == max_digits(100001000100.00, 3)

    def test_max_digits_3_for_decimal_10000100010_00_is_10_0(self):
        assert '10.0' == max_digits(10000100010.00, 3)

    def test_max_digits_3_for_decimal_0_4_is_10_0_40(self):
        assert '0.40' == max_digits(0.4, 3)

    def test_max_digits_3_for_decimal__0_4_is_10__0_40(self):
        assert '-0.40' == max_digits(-0.4, 3)

    def test_max_digits_3_for_decimal__2319086130_00_is_10__0_40(self):
        assert '-2.31' == max_digits(-2319086130.00, 3)