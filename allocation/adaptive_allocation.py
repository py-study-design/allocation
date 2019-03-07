import random


class Minimization(object):

    """Minimization attempts to minimize imbalance within a set of factors between
    a group of treatments.

    Suppose you are interested in sex and race a prognostic factors in a
    clinical trial.  So far, you have the following counts:

    Prognostic Factor | Level    | Treatment 1 | Treatment 2
    ------------------+--------  +-------------+------------
    Sex               | Male     | 8           | 9
                      | Female   | 10          | 9
    ------------------+--------  +-------------+------------
    Race              | AA       | 3           | 4
                      | Asian    | 2           | 0
                      | Hispanic | 2           | 2
                      | White    | 11          | 12
    ------------------+--------  +-------------+------------

    The next person to be assigned to a treatment is an Hispanic Female.  To
    perform the minimization, we add up the number of Hispanic and Females
    assigned to each treatment.  Treatment 1 has 10 + 2 = 12.  Treatment 2 has
    9 + 2 = 11.  Since 11 < 12, we assign the new subject to Treatment 2.

    Arguments:
        current_tally: a list whose length is equal to the number of
            treatments whose elements are lists whose length is the
            number of factors to minimize over whose elements are
            the subject counts for that treatment with that factor.
            Each count should be the count for the level of the factor
            that the prospective subject has.
        group_labels: (optional) a list of labels corresponding to each
            element in current_tally.  If not provided, it defaults to
            [1, ... len(current_tally)]

    Return:
        group: the group label for the next allocation

    """

    def __init__(self, current_tally=None, group_labels=None, seed=None):
        self.current_tally = current_tally
        if group_labels is not None:
            if len(group_labels) != self.target_length:
                raise ValueError(
                    "group_labels must be {} long".format(self.target_length)
                )
        self.group_labels = group_labels
        self.seed = seed or random.seed(seed)

    @property
    def group(self):
        """ Returns a group assignment for adaptive trials using the
        Minimization.

        """
        sums = [0] * self.n_treatments
        for idx, tally in enumerate(self.current_tally):
            sums[idx] = sum(tally)
        if sum(sums) == 0:
            # No assignment made yet, so make one at random
            idx = random.randint(0, self.n_treatments - 1)
        else:
            min_value = min(sums)
            groups = [i for i, j in enumerate(sums) if j == min_value]
            if len(groups) > 1:
                idx = random.choice(groups)
            else:
                idx = groups[0]

        if self.group_labels:
            print(self.group_labels)
            group = self.group_labels[idx]
        else:
            group = idx + 1
        print(group)
        return group

    @property
    def target_length(self):
        target_length = None
        for tally in self.current_tally:
            if target_length is None:
                target_length = len(tally)
            else:
                if target_length != len(tally):
                    raise ValueError(
                        "Each list in current_tally must be the same length."
                    )
        return target_length

    @property
    def n_treatments(self):
        n_treatments = len(self.current_tally)
        if n_treatments < 2:
            raise ValueError(
                "current_tally must be a list of lists whose length is "
                "greater than 2."
            )
        return n_treatments


def minimization(current_tally, group_labels=None, seed=None):
    minimization = Minimization(
        current_tally=current_tally, group_labels=group_labels, seed=seed
    )
    return minimization.group
