""" Test Cases for Adaptive Allocation module
"""

from ..adaptive_allocation import minimization


def test_minimization():
    """ Test Cases for minimization """
    counts = [[10, 9], [2, 2]]
    names = ['Treatment 1', 'Treatment 2']

    result = minimization(counts)
    assert result == 2

    result = minimization(counts, group_labels=names)
    assert result == 'Treatment 2'
