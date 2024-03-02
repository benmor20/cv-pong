"""
Module containing utility functions for Pong
"""


def add_tuples(*tuples: tuple[int, ...]) -> tuple[int, ...]:
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
            raise ValueError(f'All tuples must be of same length. Found length'
                             f'{len(ans)} and {len(tup)}')
        ans = tuple(a + tup[i] for i, a in enumerate(ans))
    return ans


def scale_tuple(tup: tuple[int, ...], scale_factor: float) -> tuple[int, ...]:
    """
    Scale a tuple by the given scale factor

    The elements of the resulting tuple will be integers. If a non-integer value
    is found while scaling, the result will be that value rounded down

    :param tup: a tuple of ints to scale
    :param scale_factor: a float, the amount to scale by
    :return: a tuple of ints, the given tuple multiplied by the given scale
        factor
    """
    return tuple(int(val * scale_factor) for val in tup)
