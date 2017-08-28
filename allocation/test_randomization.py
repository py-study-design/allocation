""" Test Cases for Randomization module
"""

import pytest
import allocation as r


def run_length(result):
    """ Calculates the number of repeatd values in a row.
    """
    max_run = 0
    current_run = 0
    for i in range(1, len(result)):
        if result[i] == result[i - 1]:
            current_run += 1
            if current_run > max_run:
                max_run = current_run
        else:
            current_run = 0
    return max_run


def test_cumsum():
    """ Test cases for cumsum function """
    numbers = [1, 2, 3]
    one_as_list = [1]
    empty_list = []
    letters = ['a', 'b']
    r.cumsum(numbers)
    r.cumsum(one_as_list)
    r.cumsum(empty_list)
    r.cumsum(letters)
    assert numbers == [1, 3, 6]
    assert one_as_list == [1]
    assert empty_list == []
    assert letters == ['a', 'ba']


def test_max_deviation():
    """ Test cases for max_deviation function """
    labels = ['a', 'b', 'c']
    subjects = ['c', 'a', 'b', 'c', 'c', 'a', 'c', 'b', 'a', 'b',
                'a', 'a', 'a', 'c', 'b', 'b', 'c', 'c', 'b', 'a',
                'c', 'a', 'a', 'b', 'c', 'b', 'c', 'b', 'a', 'b']
    max_dev = r.max_deviation(subjects, labels)
    assert abs(max_dev - 0.167) < 0.01

    labels = [1, 2, 3]
    subjects = [3, 1, 2, 3, 3, 1, 3, 2, 1, 2,
                1, 1, 1, 3, 2, 2, 3, 3, 2, 1,
                3, 1, 1, 2, 3, 2, 3, 2, 1, 2]
    max_dev = r.max_deviation(subjects, labels)
    assert abs(max_dev - 0.167) < 0.01


def test_simple():
    """ Test Cases for Simple Randomization"""
    result = r.simple(100, 2)
    assert len(result) == 100
    assert len(set(result)) == 2

    # Test Case to ensure the distribution of groups is close to uniform.

    # Note: This test MAY fail.  It is entirely possible, with a probability
    # of :math:`2^{-n}` where :math:`n` is the number of subjects to randomize
    result = r.simple(100000, 2)
    percent_group_1 = (float(sum([value == 1 for value in result])) /
                       float(len(result)))
    assert percent_group_1 < 0.52
    assert percent_group_1 > 0.48

    result = r.simple(100000, 2, p=[0.3, 0.7])
    percent_group_1 = (float(sum([value == 1 for value in result])) /
                       float(len(result)))
    assert percent_group_1 < 0.32
    assert percent_group_1 > 0.28

    result = r.simple(100000, 2, p=[0.2, 0.4])
    percent_group_1 = (float(sum([value == 1 for value in result])) /
                       float(len(result)))
    assert percent_group_1 < 0.35
    assert percent_group_1 > 0.31

    result = r.simple(100000, 2, p=[1, 2])
    percent_group_1 = (float(sum([value == 1 for value in result])) /
                       float(len(result)))
    assert percent_group_1 < 0.35
    assert percent_group_1 > 0.31


def test_complete():
    """ Test Cases for Complete Ranomization

    Note:
        These tests may fail due to a list being randomly permuted to itself.
    """

    # First we test for numeric lists.
    groups = [1, 2, 1, 1, 2, 1, 2, 1, 2, 1, 2, 2, 2, 1, 1, 1, 2, 2, 2, 1, 1, 2, 2]
    result = r.complete(groups)
    assert not groups == result

    # Second we test for character list.
    groups = ['1', '2', '1', '1', '2', '1', '2' '1', '2']
    result = r.complete(groups)
    assert not groups == result

    # Third we test for mixed list.
    groups = [1, 2, 1, 'a', 'b', 'a', [1, 2]]
    result = r.complete(groups)
    assert not groups == result


def test_complete_max_deviation():
    """ Test Cases for Complete Ranomization with max-deviation """
    # Make it long enough such that the probability of failure is tiny
    groups = [1, 2, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2]
    groups.extend(groups)
    groups.extend(groups)
    result = r.complete_max_deviation(groups)
    assert not groups == result

    groups = [1, 2, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2]
    groups.extend(groups)
    groups.extend(groups)
    result = r.complete_max_deviation(groups,
                                                  max_allowed_deviation=0.5)
    assert not groups == result

    with pytest.raises(ValueError):
        r.complete_max_deviation(groups, max_allowed_deviation=1.5)
    with pytest.raises(ValueError):
        r.complete_max_deviation(groups, max_allowed_deviation=1)
    with pytest.raises(ValueError):
        r.complete_max_deviation(groups, max_allowed_deviation=0)
    with pytest.raises(ValueError):
        r.complete_max_deviation(groups,
                                             max_allowed_deviation=-0.2)

    with pytest.raises(ValueError):
        r.complete_max_deviation(groups,
                                             max_iterations=10.2)
    with pytest.raises(ValueError):
        r.complete_max_deviation(groups,
                                             max_iterations=0)
    with pytest.raises(ValueError):
        r.complete_max_deviation(groups,
                                             max_iterations=-10)


def test_simple_max_deviation():
    """ Test Cases for Simple Ranomization with max-deviation """
    n_subjects = 100
    result = r.simple_max_deviation(n_subjects, max_allowed_deviation=0.5)
    dev = r.max_deviation(result, [1, 2])
    assert dev < 0.5

    with pytest.raises(ValueError):
        r.simple_max_deviation(n_subjects, max_allowed_deviation=1.5)
    with pytest.raises(ValueError):
        r.simple_max_deviation(n_subjects, max_allowed_deviation=1)
    with pytest.raises(ValueError):
        r.simple_max_deviation(n_subjects, max_allowed_deviation=0)
    with pytest.raises(ValueError):
        r.simple_max_deviation(n_subjects,
                                           max_allowed_deviation=-0.2)

    with pytest.raises(ValueError):
        r.simple_max_deviation(n_subjects,
                                           max_iterations=10.2)
    with pytest.raises(ValueError):
        r.simple_max_deviation(n_subjects,
                                           max_iterations=0)
    with pytest.raises(ValueError):
        r.simple_max_deviation(n_subjects,
                                           max_iterations=-10)


def test_block():
    """ Test Cases for Block Ranomization """

    result = r.block(100, 2, 4)
    assert len(result) == 100

    # Make sure that if the number of subjects is not divisible by the
    # block length, the result is of the correct length
    result = r.block(98, 2, 4)
    assert len(result) == 98

    result = r.block(100, 2, 6)
    max_run = run_length(result)
    assert max_run <= 6


def test_random_block():
    """ Test Cases for Block Ranomization with Random Block Lengths"""
    result = r.random_block(100, 2, [2, 4])
    assert len(result) == 100

    # Make sure that if the number of subjects is not divisible by the
    # block length, the result is of the correct length
    result = r.random_block(99, 2, [2, 4])
    assert len(result) == 99

    result = r.random_block(100, 2, [4, 6])
    max_run = run_length(result)
    assert max_run <= 6


def test_random_treatment_order():
    """ Test Cases for Random Treatment Order """
    result = r.random_treatment_order(100, 2)
    assert len(result) == 100
    assert len(set(result[24])) == 2


def test_efrons_biased_coin():
    """ Test Cases for Efron's Biased Coin Randomization """

    # Test without bias set
    result = r.efrons_biased_coin(10000)
    percent_group_1 = (float(sum([value == 1 for value in result])) /
                       float(len(result)))
    assert len(result) == 10000
    assert len(set(result)) == 2
    assert percent_group_1 < 0.52
    assert percent_group_1 > 0.48

    # Test with bias set
    result = r.efrons_biased_coin(10000, 0.8)
    percent_group_1 = (float(sum([value == 1 for value in result])) /
                       float(len(result)))
    assert len(result) == 10000
    assert len(set(result)) == 2
    assert percent_group_1 < 0.52
    assert percent_group_1 > 0.48

    with pytest.raises(ValueError):
        r.efrons_biased_coin(100000, -1)
    with pytest.raises(ValueError):
        r.efrons_biased_coin(100000, 0)
    with pytest.raises(ValueError):
        r.efrons_biased_coin(100000, 1)
    with pytest.raises(ValueError):
        r.efrons_biased_coin(100000, -1.5)


def test_smiths_exponent():
    """ Test Cases for Smith's Exponent Randomization """
    result = r.smiths_exponent(10000)
    percent_group_1 = (float(sum([value == 1 for value in result])) /
                       float(len(result)))
    assert len(result) == 10000
    assert len(set(result)) == 2
    assert percent_group_1 < 0.52
    assert percent_group_1 > 0.48

    result = r.smiths_exponent(10000, exponent=2)
    percent_group_1 = (float(sum([value == 1 for value in result])) /
                       float(len(result)))
    assert len(result) == 10000
    assert len(set(result)) == 2
    assert percent_group_1 < 0.52
    assert percent_group_1 > 0.48

    with pytest.raises(ValueError):
        r.smiths_exponent(100, exponent='a')


def test_weis_urn():
    """ Test Cases for Wei's Urn Randomization """
    result = r.weis_urn(10000)
    percent_group_1 = (float(sum([value == 1 for value in result])) /
                       float(len(result)))
    assert len(result) == 10000
    assert len(set(result)) == 2
    assert percent_group_1 < 0.52
    assert percent_group_1 > 0.48


def test_stratification():
    """ Test Cases for Stratified Randomization """
    result = r.stratification([10, 12], 2)
    assert len(result) == 2
    assert len(result[0]) == 10
    assert len(result[1]) == 12
