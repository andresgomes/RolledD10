from ..main import simple_result, right_result
import unittest

def test_should_return_list_with_no_elements_when_roll_no_dice():
    result = simple_result(0)
    assert len(result) == 0

def test_should_return_list_with_two_elements_when_roll_2_dices():
    result = simple_result(2)
    assert len(result) == 2

def test_should_return_list_with_fifteen_elements_when_roll_fiftenn_dice():
    assert len(simple_result(15)) == 15

def test_first_list_element_should_be_between_one_and_10():
    result = simple_result(1)
    r = range(1, 11)
    assert result[0] in r

def test_last_list_element_should_be_between_one_and_10():
    result = simple_result(10)
    r = range(1, 11)
    assert result[-1] in r

if __name__ == '__main__':
    unittest.main()