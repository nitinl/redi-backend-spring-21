# Unit testing examples
import pytest


def square(number):
    # return number * number
    result = 0
    for i in range(number):
        result += number
    return result


def test_square():
    output = square(4)
    assert output == 16


def test_square_negative():
    assert square(-4) == 16


def divide(numerator, denominator):
    if denominator == 0:
        raise ZeroDivisionError('cant divide by zero')
    return numerator/denominator


def test_divide():
    assert divide(4, 2) == 2


def test_divide_by_zero():
    pytest.raises(ZeroDivisionError, divide, 4, 0)


# example of a bad test. Failure of this test does not point to the exact part of the code which has a problem.
def test_math():
    assert square(4) == 16
    assert square(-4) == 16
    assert divide(4, 2) == 2
