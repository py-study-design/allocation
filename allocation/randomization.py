"""
Randomization is a module that provides functions to create random group
assignments to be used in clinical trials
"""

import random
import numbers


def cumsum(numbers):
    """Calculates the cumulative sum of a numeric list.

    This function operates on the list *in place*.

    Args:
        numbers: a list of numbers.

    Examples:
        >>> numbers = [1, 2, 3]
        >>> cumsum(numbers)
        >>> print(numbers)
        [1, 3, 6]
    """
    if len(numbers) >= 2:
        for i in range(1, len(numbers)):
            numbers[i] += numbers[i - 1]
    # If the length of numbers is less than 2, nothing happens.


def max_deviation(lst, values):
    """Calculate the maximum devation of a list of values

    Maximum deviation for group :math:`g`: at the :math:`i^{th}` assignment
    is defined as:

    .. math::
        \\frac{|n_g(i) - E[n_g(i)]|}{n_i}

    where :math:`n_g(i)` is the number of assignments to group :math:`g` at the
    :math:`i^{th}` assignment, :math:`E[n_g(i)]` is the expected number of
    assignments to group :math:`g` at the :math:`i^{th}` assignment and
    :math:`n_i` is the total that will be assigned to `n_i`
    """
    totals = {value: 0 for value in values}
    counts = {value: 0 for value in values}

    # First pass we get the counts of values
    for l in lst:
        totals[l] += 1

    expected_percents = {value: totals[value] / len(lst) for value in values}

    max_deviation = 0
    for idx, l in enumerate(lst):
        counts[l] += 1
        for value in values:
            # The inner loop calculates deviance at the current point in the
            # list and sees if it is the new maximum

            # Plus one to account for zero-indexing
            deviation = counts[value] - (idx + 1) * expected_percents[value]
            deviation = abs(deviation) / totals[value]
            if deviation > max_deviation:
                max_deviation = deviation
    return max_deviation


def simple(n_subjects, n_groups, p=None, seed=None):
    """Create a randomization list using simple randomization.

    Simple randomization randomly assigns each new subject to a group
    independent of the assignment of the previous members.

    Args:
        n_subjects: The number of subjects to randomize.
        n_groups: The number of groups to randomize subjects to.
        p: (optional) The probability that a subject will be randomized to a
            group.  The length of p must be equal to n_groups.
        seed: (optional) The seed to provide to the RNG.

    Raises:
        ValueError: If the length of `p` is not equal to `n_groups`.

    Returns:
        list: a list of length `n_subjects` of integers representing the
            groups each subject is assigned to.

    Notes:
        Simple Randomization is prone to long runs of a single group and
        may yield highly unbalanced lists.

    References:
        To be added
    """

    random.seed(seed)
    groups = []
    if p is None:
        for _ in range(0, n_subjects):
            groups.append(random.randint(1, n_groups))
    else:
        if len(p) is not n_groups:
            raise ValueError("The length of `p` must be equal to `n_groups`.")
        # Normalize p to 1
        p = [x / sum(p) for x in p]
        cumsum(p)
        for _ in range(0, n_subjects):
            test = random.random()
            # Find which group the next obs should be assigned to.
            # HACKY - Let's make this better
            group = 0
            for elem in p:
                if elem < test:
                    group += 1
            groups.append(group + 1)
    return groups


def simple_max_deviation(n_subjects, max_allowed_deviation=None,
                         max_iterations=None, seed=None):
    """Create a randomization list using simple randomization.


    Simple randomization randomly assigns each new subject to a group
    independent of the assignment of the previous members.

    This function performs simple randomization but ensures that the deviation
    is kept below a specified limit (between 0 and 1).

    Args:
        subjects: A list of group labels to randomize.
        max_allowed_deviation: (optional) The maximum deviation allowed. The
            default is 0.20 (20%).
        max_iterations: (optional) The maximum number of tries to find a
            list that satisfies the `max_deviation` criteria.  The default
            is 100.
        seed: (optional) The seed to provide to the RNG.

    Returns:
        list: a list of length `len(subjects)` of the group labels of the
            subjects.

    Raises:
        ValueError: If the length of `max_deviation` is not in [0, 1].
        ValueError: If the length of `max_iterations` is not an integer.

    Notes:
        Complete Randomization is prone to long runs of a single group.  By
        setting a maximum deviation, you can avoid that.  However, the lower
        the maximum deviation and the greated the number of subjects
    """

    random.seed(seed)

    if max_allowed_deviation is None:
        max_allowed_deviation = 0.20
    elif max_allowed_deviation >= 1 or max_allowed_deviation <= 0:
        raise ValueError("`max_allowed_deviation` must be in (0, 1).")

    if max_iterations is None:
        max_iterations = 100
    elif not isinstance(max_iterations, int) or max_iterations <= 0:
        raise ValueError("`max_iterations` must be a postive integer.")

    for _ in range(max_iterations):
        groups = simple(n_subjects, 2)

        candidate_max_deviation = max_deviation(groups, [1, 2])
        if candidate_max_deviation < max_allowed_deviation:
            return groups
    return None


def complete(subjects, seed=None):
    """Create a randomization list using complete randomization.

    Complete randomization randomly shuffles a list of group labels.  This
    ensures that the resultant list is retains the exact balance desired.
    This randomization is done in place.

    Args:
        subjects: A list of group labels to randomize.
        seed: (optional) The seed to provide to the RNG.

    Notes:
        Complete Randomization is prone to long runs of a single group.

    Returns:
        list: a list of length `len(subjects)` of the group labels of the
            subjects.

    Examples:
        >>> subjects = ["a", "a", "a", "b", "b", "b"]
        >>> complete(subjects)
        ["a", "b", "b", a", "a", "b"]
    """

    random.seed(seed)
    # We do not want to do the shuffle in place because it would break with
    # the pattern of the rest of the randomization functions
    groups = subjects[:]
    random.shuffle(groups)
    return groups


def complete_max_deviation(subjects, max_allowed_deviation=None,
                           max_iterations=None, seed=None):
    """Create a randomization list using complete randomization.

    Complete randomization randomly shuffles a list of group labels.
    This ensures that the resultant list is retains the exact balance
    desired. This randomization is done in place.

    This function performs complete randomization but ensures that
    the deviation is kept below a specified limit (between 0 and 1).

    Args:
        subjects: A list of group labels to randomize.
        max_allowed_deviation: (optional) The maximum deviation
            allowed. The default is 0.20 (20%).
        max_iterations: (optional) The maximum number of tries to find
            a list that satisfies the `max_deviation` criteria.  The
            default is 100.
        seed: (optional) The seed to provide to the RNG.

    Returns:
        list: a list of length `len(subjects)` of the group labels of
            the subjects.

    Raises:
        ValueError: If the length of `max_deviation` is not in [0, 1].
        ValueError: If the length of `max_iterations` is not an integer.

    Notes:
        Complete Randomization is prone to long runs of a single group.
        By setting a maximum deviation, you can avoid that.  However,
        the lower the maximum deviation and the greated the number of
        subjects
    """

    random.seed(seed)

    if max_allowed_deviation is None:
        max_allowed_deviation = 0.20
    elif max_allowed_deviation >= 1 or max_allowed_deviation <= 0:
        raise ValueError("`max_allowed_deviation` must be in (0, 1).")

    if max_iterations is None:
        max_iterations = 100
    elif not isinstance(max_iterations, int) or max_iterations <= 0:
        raise ValueError("`max_iterations` must be a postive integer.")

    group_labels = set(subjects)

    # We do not want to do the shuffle in place because it would break with
    # the pattern of the rest of the randomization functions
    for _ in range(max_iterations):
        groups = subjects[:]
        random.shuffle(groups)

        candidate_max_deviation = max_deviation(groups, group_labels)
        if candidate_max_deviation < max_allowed_deviation:
            return groups
    return None


def block(n_subjects, n_groups, block_length, seed=None):
    """Create a randomization list using block randomization.

    Block randomization takes blocks of group labels of length `block_length`,
    shuffles them and adds them to the randomization list.  This is done to
    prevent long runs of a single group. Usually `block_length` is equal
    to 4 or 6.

    Args:
        n_subjects: The number of subjects to randomize.
        n_groups: The number of groups to randomize subjects to.
        block_length: The length of the blocks.  `block` should be equal to
            :math:`k * n_{groups}, k > 1`.
        seed: (optional) The seed to provide to the RNG.

    Returns:
        list: a list of length `n_subjects` of integers representing the
            groups each subject is assigned to.

    Notes:
        The value of `block_length` should be a multiple of `n_groups` to
        ensure proper balance.
    """

    random.seed(seed)
    block_form = []
    for i in range(0, block_length):
        # If n_groups is not a factor of block_length, there will be unbalance.
        block_form.append(i % n_groups + 1)

    count = 0
    groups = []

    while count < n_subjects:
        random.shuffle(block_form)
        groups.extend(block_form)
        count += block_length

    # If `n_subjects` is not a multiple of `block_length`, only return the
    # first `n_subjects` elements of `groups`
    return groups[:n_subjects]


def random_block(n_subjects, n_groups, block_lengths, seed=None):
    """Create a randomization list by block randomization with random blocks.

    Block randomization takes blocks of group labels of length `block_length`,
    shuffles them and adds them to the randomization list.  This is done to
    prevent long runs of a single group. Usually `block_length` is equal
    to 4 or 6.

    Block randomization with random blocks adds an extra layer of randomness by
    changing the length of each new block added.  This is done in order to
    hide patterns that may arise if the block length becomes known.

    Args:
        n_subjects: The number of subjects to randomize.
        n_groups: The number of groups to randomize subjects to.
        block_lengths: A list of the length of the blocks.
        seed: (optional) The seed to provide to the RNG.

    Returns:
        list: a list of length `n_subjects` of integers representing the
            groups each subject is assigned to.

    Notes:
        Each value in `block_lengths` should be a multiple of `n_groups`
        to ensure proper balance.

    Todo:
        - Implement weights for block lengths
    """
    random.seed(seed)
    n_block_lengths = len(block_lengths)
    blocks = []
    for block_length in block_lengths:
        block_form = []
        for i in range(0, block_length):
            block_form.append(i % n_groups + 1)
        blocks.append(block_form)
    count = 0
    groups = []
    while count < n_subjects:
        this_block = blocks[random.randint(0, n_block_lengths - 1)]
        random.shuffle(this_block)
        groups.extend(this_block)
        count += len(this_block)
    # Due to the random selection of block lengths, you cannot guarentee that
    # `len(groups) is n_subjects` therefore we only return the first
    # `n_subjects` elements of `groups`
    return groups[:n_subjects]


def random_treatment_order(n_subjects, n_treatments, seed=None):
    """Create a randomization list for studies where the subject recieves
    multiple treatments.

    If a subject will recieve multiple treatments, those treatments should be
    randomized.

    Args:
        n_subjects: The number of subjects to randomize.
        n_treatments: The number of treatments a subject will
        seed: (optional) The seed to provide to the RNG.

    Returns:
        list: a list of length `n_subjects` of lists of length `n_treatments`.
            Each sublist is treatment order of the subject.
    """

    random.seed(seed)
    treatment = []
    for i in range(0, n_treatments):
        treatment.append(i + 1)
    groups = []
    for i in range(0, n_subjects):
        random.shuffle(treatment)
        groups.append(treatment[:])
    return groups


def efrons_biased_coin(n_subjects, bias=None, seed=None):
    """Create a randomization list using Efron's Biased Coin

    Efron's Biased Coin weights the assignment of a new subject by adjusting
    the probability of the Bernoulli random variable used to determine the next
    group according to which group is under represented.  The adjusted
    probability is a fixed value determined by `bias`.
    This method is only approriate for 2 groups.

    Args:
        n_subjects: The number of subjects to randomize.
        bias: (optional) The probability the new subject will be assigned to
            the under represented group.  The default is 0.67.
        seed: (optional) The seed to provide to the RNG.

    Returns:
        list: a list of length `n_subjects` of integers representing the
            groups each subject is assigned to.

    Raises:
        ValueError: If the length of `bias` is not in [0, 1].

    Notes:
        Exact balance between groups is not guaranteed when using Efron's
        Biased Coin, but it is usually very close to balanced.
    """
    random.seed(seed)
    if bias is None:
        bias = 0.67
    else:
        if bias >= 1 or bias <= 0:
            raise ValueError("`bias` must be in [0, 1].")
    group_0_count = 0.0
    groups = []
    for i in range(0, n_subjects):
        if (group_0_count / (i + 1)) == 0.5 or i == 0:
            # Balance
            cut = 0.5
        elif group_0_count / (i + 1) < 0.5:
            # Too few from Group 0
            cut = 1 - bias
        else:
            # Too few from Group 1
            cut = bias
        test = random.random()
        if test > cut:
            group = 1
        else:
            group = 2
        groups.append(group)
        if group == 1:
            group_0_count += 1
    return groups


def smiths_exponent(n_subjects, exponent=None, seed=None):
    """Create a randomization list using Smith's Exponent

    Smith's Exponent weights the assignment of a new subject by adjusting
    the probability of the Bernoulli random variable used to determine the next
    group according to which group is under represented.  The probablity that
    subject :math:`j`, give an exponent :math:`\\rho`, will be assigned to
    group 1 is:

    .. math::
        p_{ij} = \\frac{n_2}{n_1 + n_2} (j - 1)^{\\rho}

    Args:
        n_subjects: The number of subjects to randomize.
        exponent: (optional) Smith's Exponent (:math:`\\rho`).
            The default is 1.
        seed: (optional) The seed to provide to the RNG.

    Raises:
        ValueError: If `exponent` is not a number.

    Returns:
        list: a list of length `n_subjects` of integers representing the
            groups each subject is assigned to.

    Notes:
        Exact balance between groups is not guaranteed when using Smith's
        Exponent, but it is usually very close to balanced (assuming a non-
        negative exponent).

        Though you can theoretically choose any value for the exponent, it is
        best to choose a non-negative number.  A zero exponent reduces to
        simple randomization and a negative exponent will cause one group to be
        over-represented in the list.
    """
    random.seed(seed)
    if exponent is None:
        exponent = 1
    else:
        if not isinstance(exponent, numbers.Number):
            raise ValueError("`exponent` must be a number.")
    group_0_count = 0.0
    groups = []
    for i in range(0, n_subjects):
        # The plus one is to account for zero indexing.
        denom = group_0_count**exponent + (i + 1 - group_0_count)**exponent
        cut = group_0_count**exponent / denom

        test = random.random()
        if test > cut:
            group = 1
        else:
            group = 2
        groups.append(group)
        if group == 1:
            group_0_count += 1
    return groups


def weis_urn(n_subjects, seed=None):
    """Create a randomization list using Wei's Urn.

    Wei's Urn weights the assignment of a new subject by adjusting the
    probability of the Bernoulli random variable used to determine the next
    group according to which group is under represented.  The adjusted
    probability is a dynamic value.

    Suppose that :math:`N_{r}` is the total number of subjects already
    randomize and :math:`N_{r0}` is the number of subjects already randomized
    that were randomized to Group 0.  The probability that the next subject
    will be randomized to Group 0 is:

    .. math::
        p_{0} = 1 - \\frac{N_{r0}}{N_{r}}

    This method is only approriate for 2 groups.

    Args:
        n_subjects: The number of subjects to randomize.
        seed: (optional) The seed to provide to the RNG.

    Returns:
        list: a list of length `n_subjects` of integers representing the
            groups each subject is assigned to.

    Notes:
        Exact balance between groups is not guaranteed when using Wei's
        Urn, but it is usually very close to balanced.
    """

    random.seed(seed)
    group_0_count = 0.0
    groups = []
    for i in range(0, n_subjects):
        if i > 0:
            cut = 1 - group_0_count / (i + 1)
        else:
            cut = 0.5
        test = random.random()
        if test < cut:
            group = 1
        else:
            group = 2
        groups.append(group)
        if group == 1:
            group_0_count += 1
    return groups


def stratification(n_subjects_per_strata, n_groups, block_length=4, seed=None):
    """Create a randomization list for each strata using Block Randomization.

    If a study has several strata, each strata is seperately randomized using
    block randomization.

    Args:
        n_subjects_per_strata: A list of the number of subjects for each
            strata.
        n_groups: The number of groups to randomize subjects to.
        block_length: The length of the blocks.
        seed: (optional) The seed to provide to the RNG.

    Returns:
        list: a list of length `len(n_subjects_per_strata)` of lists of length
            `n_subjects_per_strata`.  Each sublist is the strata specific
            randomization list.

    Notes:
        The value of `block_length` should be a multiple of `n_groups`
        to ensure proper balance.

    Todo:
        Allow for multiple randomization techniques to be used.
    """

    groups = []
    for n_subjects_per_stratum in n_subjects_per_strata:
        # Adding 52490, a dummy value, to the seed ensures a different list
        # per strata.  The use of a 'magic number' here allows for
        # reproducibility
        if seed is not None:
            seed = seed + 52490
        groups.append(block(n_subjects_per_stratum, n_groups,
                            block_length, seed))
    return groups
