"""
Tests for the utility functions
"""
import pytest
from ..src.utils import *


# Each element is a tuple containing:
#   - a list of tuples to add together
#   - what that sum should be
ADD_TUPLES_CASES = [
    # Empty cases
    ([tuple()], tuple()),
    ([tuple(), tuple(), tuple()], tuple()),
    # Single input case
    ([(1,)], (1,)),
    ([(1, 2, 3)], (1, 2, 3)),
    # Two tuples
    ([(1,), (2,)], (3,)),
    ([(1, 2, 3), (4, 5, 6)], (5, 7, 9)),
    # Many tuples
    ([(1, 2, 3), (4, 5, 6), (2, 4, 6), (1, 7, 4)], (8, 18, 19)),
    ([(1, 2, 3, 4, 5, 6), (6, 5, 4, 3, 2, 1), (10, 20, 10, 20, 10, 20),
      (1, 1, 2, 1, 1, 2)], (18, 28, 19, 28, 18, 29)),
    # Negative
    ([(1, 2, 3), (-1, -2, -3)], (0, 0, 0)),
    ([(-1, -2, -3), (-4, -5, -6)], (-5, -7, -9)),
    ([(1, 2, 3), (-4, -5, -6)], (-3, -3, -3)),
]


ADD_FLOAT_TUPLES_CASES = [
    # Single input case
    ([(1.,)], (1.,)),
    ([(0.1, 0.2, 0.3)], (0.1, 0.2, 0.3)),
    # Two tuples
    ([(0.1,), (0.2,)], (0.3,)),
    ([(0.1, 0.2, 0.3), (0.4, 0.5, 0.6)], (0.5, 0.7, 0.9)),
    # Many tuples
    ([(0.1, 0.2, 0.3), (0.4, 0.5, 0.6), (0.2, 0.4, 0.6), (0.1, 0.7, 0.4)],
     (0.8, 1.8, 1.9)),
    ([(2.1, 2.2, 2.3, 2.4, 2.5, 2.6), (1.6, 1.5, 1.4, 1.3, 1.2, 1.1),
      (4.0, 2.0, 1.0, 2.0, 1.0, 2.0), (0.1, 0.1, 0.2, 0.1, 0.1, 0.2)],
     (7.8, 5.8, 4.9, 5.8, 4.8, 5.9)),
]


# Each element is a list of tuples which are not all the same length
ADD_TUPLES_DIFF_LENGTHS_CASES = [
    # Mostly zeros
    [tuple(), tuple(), (1,)],
    [tuple(), (1,), tuple()],
    # One zero
    [(1, 2), (3, 4), (4, 5), tuple()],
    [tuple(), (1, 2), (2, 3), (3, 4)],
    [(1, 2), tuple(), (2, 3), (3, 4)],
    # One different
    [(1, 2), (3, 4), (5, 6), (7, 8, 9)],
    [(1, 2, 3), (4, 5), (6, 7)],
    [(1, 2), (3, 4, 5, 6, 7), (8, 9), (10, 11)],
    # All different
    [(1, 2), (3, 4, 5), (5, 6, 7, 8)],
    [(1, 2), (3, 4, 5, 6, 7), (8, 9, 10)]
]


# Each element is a tuple containing:
#   - a tuple to scale
#   - a float, the scale factor
#   - the tuple scaled by that factor
SCALE_TUPLE_CASES = [
    # Empty cases
    (tuple(), 2, tuple()),
    (tuple(), 0.5, tuple()),
    # Scale by zero
    ((1, 2, 3), 0, (0, 0, 0)),
    # Scale by 1
    ((4, 5, 6), 1, (4, 5, 6)),
    # Scale up, whole number
    ((1, 2, 3), 2, (2, 4, 6)),
    ((4, 5, 6), 3, (12, 15, 18)),
    # Scale up, fraction
    ((2, 4, 6), 1.5, (3, 6, 9)),
    ((4, 8, 12), 2.25, (9, 18, 27)),
    # Scale down
    ((10, 20, 30), 0.1, (1, 2, 3)),
    # Negative
    ((-1, -2, 3), 2, (-2, -4, 6)),
    ((-10, 20, -30), 0.5, (-5, 10, -15)),
    # Negative scale
    ((1, 2, 3), -2, (-2, -4, -6)),
    # Rounding for ints
    ((1, 2, 3, 4, 5), 1.5, (1, 3, 4, 6, 7)),
    ((20, 21, 22, 23, 24, 25, 26), 0.25, (5, 5, 5, 5, 6, 6, 6)),
]


SCALE_FLOAT_TUPLE_CASES = [
    # Float inputs
    ((1.0, 2.0, 3.0), 2.0, (2.0, 4.0, 6.0)),
    # Floats don't round
    ((1.0, 2.0, 3.0), 0.5, (0.5, 1.0, 1.5)),
]

# Each element is a tuple containing:
# - range 1
# - range 2
# - a bool, whether range 1 and range 2 overlap
DO_RANGES_OVERLAP_CASES = [
    # range1 < range2
    (range(-10, -5), range(5, 10), False),
    (range(5, 10), range(11, 20), False),
    # range1.start < range2.start < range1.stop < range2.stop
    (range(-10, 0), range(-5, 15), True),
    # range1 fully within range2
    (range(20, 30), range(10, 500), True),
    # range2.start < range1.start < range2.stop < range1.stop
    (range(-5, 15), range(-10, 0), True),
    # range1 > range2
    (range(5, 10), range(-10, -5), False),
    (range(11, 20), range(5, 10), False),
    # range2 fully within range1
    (range(100), range(40, 75), True),
    # one stop == other start
    (range(5, 10), range(10, 20), True),
    (range(-50, 0), range(10), True),
    (range(10, 20), range(5, 10), True),
    (range(10), range(-50, 0), True),
    # start at same place
    (range(10, 20), range(10, 30), True),
    (range(10, 30), range(10, 20), True),
    # End at same place
    (range(10, 30), range(20, 30), True),
    (range(20, 30), range(10, 30), True),
    # Same range
    (range(10, 20), range(10, 20), True),
    # Size 1
    (range(1, 1), range(10), True),
    (range(1, 1), range(1, 10), True)
]

# Each element is a tuple containing:
# - a tuple defining left, top, width, height of rect 1
# - a tuple defining left, top, width, height of rect 2
# - a bool, whether the two rectangles overlap
DO_RECTS_INTERSECT_CASES = [
    ((-10, -10, 5, 5), (5, 5, 5, 5), False),
    ((-10, -10, 5, 10), (5, -5, 5, 20), False),
    ((-10, 20, 5, 10), (5, 10, 5, 490), False),
    ((-10, -5, 5, 20), (5, -10, 5, 10), False),
    ((-10, 5, 5, 5), (5, -10, 5, 5), False),
    ((-10, 0, 5, 100), (5, 40, 5, 35), False),
    ((-10, 5, 5, 5), (5, 10, 5, 10), False),
    ((-10, 0, 5, 10), (5, -50, 5, 50), False),
    ((-10, 10, 5, 10), (5, 10, 5, 20), False),
    ((-10, 20, 5, 10), (5, 10, 5, 20), False),
    ((-10, 10, 5, 10), (5, 10, 5, 10), False),
    ((-10, -10, 10, 5), (-5, 5, 20, 5), False),
    ((-10, -10, 10, 10), (-5, -5, 20, 20), True),
    ((-10, 20, 10, 10), (-5, 10, 20, 490), True),
    ((-10, -5, 10, 20), (-5, -10, 20, 10), True),
    ((-10, 5, 10, 5), (-5, -10, 20, 5), False),
    ((-10, 0, 10, 100), (-5, 40, 20, 35), True),
    ((-10, 5, 10, 5), (-5, 10, 20, 10), True),
    ((-10, 0, 10, 10), (-5, -50, 20, 50), True),
    ((-10, 10, 10, 10), (-5, 10, 20, 20), True),
    ((-10, 20, 10, 10), (-5, 10, 20, 20), True),
    ((-10, 10, 10, 10), (-5, 10, 20, 10), True),
    ((20, -10, 10, 5), (10, 5, 490, 5), False),
    ((20, -10, 10, 10), (10, -5, 490, 20), True),
    ((20, 20, 10, 10), (10, 10, 490, 490), True),
    ((20, -5, 10, 20), (10, -10, 490, 10), True),
    ((20, 5, 10, 5), (10, -10, 490, 5), False),
    ((20, 0, 10, 100), (10, 40, 490, 35), True),
    ((20, 5, 10, 5), (10, 10, 490, 10), True),
    ((20, 0, 10, 10), (10, -50, 490, 50), True),
    ((20, 10, 10, 10), (10, 10, 490, 20), True),
    ((20, 20, 10, 10), (10, 10, 490, 20), True),
    ((20, 10, 10, 10), (10, 10, 490, 10), True),
    ((-5, -10, 20, 5), (-10, 5, 10, 5), False),
    ((-5, -10, 20, 10), (-10, -5, 10, 20), True),
    ((-5, 20, 20, 10), (-10, 10, 10, 490), True),
    ((-5, -5, 20, 20), (-10, -10, 10, 10), True),
    ((-5, 5, 20, 5), (-10, -10, 10, 5), False),
    ((-5, 0, 20, 100), (-10, 40, 10, 35), True),
    ((-5, 5, 20, 5), (-10, 10, 10, 10), True),
    ((-5, 0, 20, 10), (-10, -50, 10, 50), True),
    ((-5, 10, 20, 10), (-10, 10, 10, 20), True),
    ((-5, 20, 20, 10), (-10, 10, 10, 20), True),
    ((-5, 10, 20, 10), (-10, 10, 10, 10), True),
    ((5, -10, 5, 5), (-10, 5, 5, 5), False),
    ((5, -10, 5, 10), (-10, -5, 5, 20), False),
    ((5, 20, 5, 10), (-10, 10, 5, 490), False),
    ((5, -5, 5, 20), (-10, -10, 5, 10), False),
    ((5, 5, 5, 5), (-10, -10, 5, 5), False),
    ((5, 0, 5, 100), (-10, 40, 5, 35), False),
    ((5, 5, 5, 5), (-10, 10, 5, 10), False),
    ((5, 0, 5, 10), (-10, -50, 5, 50), False),
    ((5, 10, 5, 10), (-10, 10, 5, 20), False),
    ((5, 20, 5, 10), (-10, 10, 5, 20), False),
    ((5, 10, 5, 10), (-10, 10, 5, 10), False),
    ((0, -10, 100, 5), (40, 5, 35, 5), False),
    ((0, -10, 100, 10), (40, -5, 35, 20), True),
    ((0, 20, 100, 10), (40, 10, 35, 490), True),
    ((0, -5, 100, 20), (40, -10, 35, 10), True),
    ((0, 5, 100, 5), (40, -10, 35, 5), False),
    ((0, 0, 100, 100), (40, 40, 35, 35), True),
    ((0, 5, 100, 5), (40, 10, 35, 10), True),
    ((0, 0, 100, 10), (40, -50, 35, 50), True),
    ((0, 10, 100, 10), (40, 10, 35, 20), True),
    ((0, 20, 100, 10), (40, 10, 35, 20), True),
    ((0, 10, 100, 10), (40, 10, 35, 10), True),
    ((5, -10, 5, 5), (10, 5, 10, 5), False),
    ((5, -10, 5, 10), (10, -5, 10, 20), True),
    ((5, 20, 5, 10), (10, 10, 10, 490), True),
    ((5, -5, 5, 20), (10, -10, 10, 10), True),
    ((5, 5, 5, 5), (10, -10, 10, 5), False),
    ((5, 0, 5, 100), (10, 40, 10, 35), True),
    ((5, 5, 5, 5), (10, 10, 10, 10), True),
    ((5, 0, 5, 10), (10, -50, 10, 50), True),
    ((5, 10, 5, 10), (10, 10, 10, 20), True),
    ((5, 20, 5, 10), (10, 10, 10, 20), True),
    ((5, 10, 5, 10), (10, 10, 10, 10), True),
    ((0, -10, 10, 5), (-50, 5, 50, 5), False),
    ((0, -10, 10, 10), (-50, -5, 50, 20), True),
    ((0, 20, 10, 10), (-50, 10, 50, 490), True),
    ((0, -5, 10, 20), (-50, -10, 50, 10), True),
    ((0, 5, 10, 5), (-50, -10, 50, 5), False),
    ((0, 0, 10, 100), (-50, 40, 50, 35), True),
    ((0, 5, 10, 5), (-50, 10, 50, 10), True),
    ((0, 0, 10, 10), (-50, -50, 50, 50), True),
    ((0, 10, 10, 10), (-50, 10, 50, 20), True),
    ((0, 20, 10, 10), (-50, 10, 50, 20), True),
    ((0, 10, 10, 10), (-50, 10, 50, 10), True),
    ((10, -10, 10, 5), (10, 5, 20, 5), False),
    ((10, -10, 10, 10), (10, -5, 20, 20), True),
    ((10, 20, 10, 10), (10, 10, 20, 490), True),
    ((10, -5, 10, 20), (10, -10, 20, 10), True),
    ((10, 5, 10, 5), (10, -10, 20, 5), False),
    ((10, 0, 10, 100), (10, 40, 20, 35), True),
    ((10, 5, 10, 5), (10, 10, 20, 10), True),
    ((10, 0, 10, 10), (10, -50, 20, 50), True),
    ((10, 10, 10, 10), (10, 10, 20, 20), True),
    ((10, 20, 10, 10), (10, 10, 20, 20), True),
    ((10, 10, 10, 10), (10, 10, 20, 10), True),
    ((20, -10, 10, 5), (10, 5, 20, 5), False),
    ((20, -10, 10, 10), (10, -5, 20, 20), True),
    ((20, 20, 10, 10), (10, 10, 20, 490), True),
    ((20, -5, 10, 20), (10, -10, 20, 10), True),
    ((20, 5, 10, 5), (10, -10, 20, 5), False),
    ((20, 0, 10, 100), (10, 40, 20, 35), True),
    ((20, 5, 10, 5), (10, 10, 20, 10), True),
    ((20, 0, 10, 10), (10, -50, 20, 50), True),
    ((20, 10, 10, 10), (10, 10, 20, 20), True),
    ((20, 20, 10, 10), (10, 10, 20, 20), True),
    ((20, 10, 10, 10), (10, 10, 20, 10), True),
    ((10, -10, 10, 5), (10, 5, 10, 5), False),
    ((10, -10, 10, 10), (10, -5, 10, 20), True),
    ((10, 20, 10, 10), (10, 10, 10, 490), True),
    ((10, -5, 10, 20), (10, -10, 10, 10), True),
    ((10, 5, 10, 5), (10, -10, 10, 5), False),
    ((10, 0, 10, 100), (10, 40, 10, 35), True),
    ((10, 5, 10, 5), (10, 10, 10, 10), True),
    ((10, 0, 10, 10), (10, -50, 10, 50), True),
    ((10, 10, 10, 10), (10, 10, 10, 20), True),
    ((10, 20, 10, 10), (10, 10, 10, 20), True),
    ((10, 10, 10, 10), (10, 10, 10, 10), True),
]  # Yes, they were auto-generated, but with 121 different cases I wasn't about
# to write it myself. the code to auto-generate I did write though


@pytest.mark.parametrize("tuple_list, answer", ADD_TUPLES_CASES)
def test_add_tuples(tuple_list: list[tuple[int, ...]], answer: tuple[int, ...]):
    """
    Test the default behavior of the add_tuples function

    :param tuple_list: the list of tuples to add together
    :param answer: the tuple that is the desired result of the tuples added
    """
    assert add_tuples(*tuple_list) == answer


@pytest.mark.parametrize("tuple_list, answer", ADD_FLOAT_TUPLES_CASES)
def test_add_float_tuples(tuple_list: list[tuple[float, ...]],
                          answer: tuple[float, ...]):
    """
    Test the default behavior of the add_tuples function

    :param tuple_list: the list of tuples to add together
    :param answer: the tuple that is the desired result of the tuples added
    """
    for ele, ans in zip(add_tuples(*tuple_list), answer):
        assert pytest.approx(ele) == ans


def test_add_tuples_no_input():
    """
    Test that add_tuples raises a value error when no tuples are given
    """
    with pytest.raises(ValueError):
        add_tuples()


@pytest.mark.parametrize("tuple_list", ADD_TUPLES_DIFF_LENGTHS_CASES)
def test_add_tuple_wrong_length(tuple_list: list[tuple[float | int, ...]]):
    """
    Test that add_tuples throws a value error when the inputs are not all the
        same length.

    :param tuple_list: the list of tuples to give to add_tuples, at least one
        of which is a different length
    """
    with pytest.raises(ValueError):
        add_tuples(*tuple_list)


@pytest.mark.parametrize("to_scale, scale_factor, answer", SCALE_TUPLE_CASES)
def test_scale_tuple(to_scale: tuple[int, ...], scale_factor: float,
                     answer: tuple[int, ...]):
    """
    Test the scale_tuple function

    :param to_scale: the tuple of integers to scale
    :param scale_factor: a float, the factor to scale the tuple by
    :param answer: the tuple of ints that should result from scaling to_scale
        by scale_factor
    """
    assert scale_tuple(to_scale, scale_factor) == answer


@pytest.mark.parametrize("to_scale, scale_factor, answer", SCALE_TUPLE_CASES)
def test_scale_float_tuple(to_scale: tuple[float, ...], scale_factor: float,
                     answer: tuple[float, ...]):
    """
    Test the scale_tuple function

    :param to_scale: the tuple of floats to scale
    :param scale_factor: a float, the factor to scale the tuple by
    :param answer: the tuple of floats that should result from scaling to_scale
        by scale_factor
    """
    for ele, ans in zip(scale_tuple(to_scale, scale_factor), answer):
        assert pytest.approx(ele) == ans


@pytest.mark.parametrize("range1, range2, overlap", DO_RANGES_OVERLAP_CASES)
def test_do_ranges_overlap(range1: range, range2: range, overlap: bool):
    """
    Test do_ranges_overlap function

    :param range1: one range to test overlap with
    :param range2: another range to test overlap with
    :param overlap: a bool, whether the ranges overlap
    """
    assert do_ranges_overlap(range1, range2) == overlap


@pytest.mark.parametrize("rect1, rect2, intersect", DO_RECTS_INTERSECT_CASES)
def test_do_rects_intersect(rect1: RectTuple, rect2: RectTuple,
                            intersect: bool):
    """
    Test do_rects_intersect function

    :param rect1: one rect represented as (left, top, width, height)
    :param rect2: another rect represented as (left, top, width, height)
    :param intersect: whether the two rectangles intersect each other
    """
    assert do_rects_intersect(rect1, rect2) == intersect
