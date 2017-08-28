""" Test Cases for Adaptive Allocation module
"""

import pytest
import allocation.adaptive_allocation as alloc


def test_minimization():
    """ Test Cases for minimization """
    counts = [[10, 9], [2, 2]]
    names = ['Treatment 1', 'Treatment 2']

    result = alloc.minimization(counts)
    assert result == 2

    result = alloc.minimization(counts, group_labels=names)
    assert result == 'Treatment 2'
