from ..main import simple_result
import unittest

def test_roll_zero_dices():
    result = simple_result(0)
    assert len(result) == 0

def test_roll_two_dices():
    result = simple_result(2)
    assert len(result) == 2

def test_roll_five_dices():
    assert len(simple_result(15)) == 15


if __name__ == '__main__':
    unittest.main()