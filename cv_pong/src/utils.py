"""
Module containing utility functions for Pong
"""


def add_tuples(*tuples: tuple[float | int, ...]) -> tuple[float | int, ...]:
    """
    Add the elements of multiple tuples together

    All given tuples need to be the same length

    :param tuples: a collection of at least one tuple of integers, the tuple(s)
        to add together
    :return: a tuple the same length of the input tuple(s), giving the
        element-wise sum of the tuples
    """
    if len(tuples) == 0:
        raise ValueError('Need at least one tuple to add, given 0')
    ans = tuple(0 for _ in tuples[0])
    for tup in tuples:
        if len(tup) != len(ans):
            raise ValueError(f'All tuples must be of same length. Found length '
                             f'{len(ans)} and {len(tup)}')
        ans = tuple(a + tup[i] for i, a in enumerate(ans))
    return ans


def scale_tuple(tup: tuple[float | int, ...], scale_factor: float) \
        -> tuple[float | int, ...]:
    """
    Scale a tuple by the given scale factor

    The elements of the resulting tuple will be integers. If a non-integer value
    is found while scaling, the result will be that value rounded down

    :param tup: a tuple of ints to scale
    :param scale_factor: a float, the amount to scale by
    :return: a tuple of ints, the given tuple multiplied by the given scale
        factor
    """
    return tuple(type(val)(val * scale_factor) for val in tup)


def do_ranges_overlap(range1: range, range2: range) -> bool:
    """
    Calculate if two ranges overlap

    For the purposes of this function, both bounds of ranges are inclusive;
    i.e. if only the only intersection is at the stop, an overlap is still
    counted. The ranges are assumed to be increasing (i.e. start < stop)

    :param range1: a range, the first range to detect overlap of
    :param range2: a range, the second range to detect overlap of
    :return: True if the ranges overlap, False otherwise
    """
    return range1.start <= range2.start <= range1.stop \
        or range1.start <= range2.stop <= range1.stop \
        or range2.start <= range1.start <= range1.stop <= range2.stop


RectTuple = tuple[int, int, int, int]


def do_rects_intersect(rect1: RectTuple, rect2: RectTuple) -> bool:
    """
    Determine whether two rectangles intersect

    A rectangle is defined as a tuple of four integers, giving (in order):
    - left position coordinate (positive to right)
    - top position (positive down)
    - width
    - height
    An intersection occurs when the intersection of the two rectangles is
    nonempty. An intersection is detected even if just the borders touch

    :param rect1: the first rectangle to check for intersection with
    :param rect2: the second rectangle to check for intersection with
    :return: True if the rectangles intersect, False otherwise
    """
    rect1x = range(rect1[0], rect1[0] + rect1[2])
    rect1y = range(rect1[1], rect1[1] + rect1[3])
    rect2x = range(rect2[0], rect2[0] + rect2[2])
    rect2y = range(rect2[1], rect2[1] + rect2[3])
    return do_ranges_overlap(rect1x, rect2x) \
        and do_ranges_overlap(rect1y, rect2y)
