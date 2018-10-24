"""
Randomization is a module that provides functions to create random group
assignments to be used in clinical trials
"""

import math
import random
import scipy.stats as stats


# A Response addaptive randomization technique
def double_biased_coin_minimize(control_success, control_trials,
                                treatment_success, treatment_trials,
                                control_name=None, treatment_name=None,
                                seed=None):
    """ Returns a group assignment for adaptive trials using the Double Biased
    Coin Minimization method.

    Suppose that :math:`N_{c}` is the number of controls, of which
    :math:`S_{c}` were successes and :math:`N_{t}` is the number of treatments,
    of which :math:`S_{t}` were successes.  We can define the probability of
    success as:

    .. math::
        p_{c} = \\frac{S_{c}}{N_{c}}
        p_{t} = \\frac{S_{t}}{N_{t}}

    The next subject will be randomized to the control group with probability:

    .. math::
        \\frac{\sqrt{p_{c}}}{\\sqrt{p_{c}} + \\sqrt{p_{t}}}

    Args:
        control_success: The number of successfull trials in the control group.
        control_trials: The number of trials in the control group.
        treatment_success: The number of successfull trials in the treatment
            group.
        treatment_trials: The number of trials in the treatment group.
        control_name: (optional) The name of the control group.  The default
            is 'C'
        treatment_name: (optional) The name of the treatment group.  The
            default is 'T'
        seed: (optional) The seed to provide to the RNG.

    Returns:
        list: the name (either `control_name` or `treatment_name`) of the group
            the subject is assigned to.
    """
    if control_trials < control_success:
        raise ValueError('`control_trials` must be greater than or equal '
                         'to `control_success`')
    if treatment_trials < treatment_success:
        raise ValueError('`treatment_trials` must be greater than or equal '
                         'to `treatment_success`')

    if control_name is None:
        control_name = "Control"
    if treatment_name is None:
        treatment_name = "Treatment"

    if seed is not None:
        # This ensures a new seed for each selection
        seed = seed + 10 * (control_trials + treatment_trials)

    random.seed(seed)

    if control_trials > 1:
        pC = float(control_success) / control_trials
    else:
        pC = 0.5
    if treatment_trials > 1:
        pT = float(treatment_success) / treatment_trials
    else:
        pT = 0.5

    cut = math.sqrt(pC) / (math.sqrt(pC) + math.sqrt(pT))
    test = random.random()

    if test < cut:
        group = control_name
    else:
        group = treatment_name
    return group


# A Response addaptive randomization technique
def double_biased_coin_urn(control_success, control_trials,
                           treatment_success, treatment_trials,
                           control_name=None, treatment_name=None,
                           seed=None):
    """ Returns a group assignment for adaptive trials using the Double Biased
    Coin Minimization method.

    Suppose that :math:`N_{c}` is the number of controls, of which
    :math:`S_{c}` were successes and :math:`N_{t}` is the number of treatments,
    of which :math:`S_{t}` were successes.  We can define the probability of
    success as:

    .. math::
        p_{c} = \\frac{S_{c}}{N_{c}}
        p_{t} = \\frac{S_{t}}{N_{t}}

    The next subject will be randomized to the control group with probability:

    .. math::
        \\frac{1 - p_{t}}{(1 - p_{c}) + (1 - p_{t})}

    Args:
        control_success: The number of successfull trials in the control group.
        control_trials: The number of trials in the control group.
        treatment_success: The number of successfull trials in the treatment
            group.
        treatment_trials: The number of trials in the treatment group.
        control_name: (optional) The name of the control group.  The default
            is 'C'
        treatment_name: (optional) The name of the treatment group.  The
            default is 'T'
        seed: (optional) The seed to provide to the RNG.

    Returns:
        list: the name (either `control_name` or `treatment_name`) of the group
            the subject is assigned to.
    """
    if control_trials < control_success:
        raise ValueError('`control_trials` must be greater than or equal '
                         'to `control_success`')
    if treatment_trials < treatment_success:
        raise ValueError('`treatment_trials` must be greater than or equal '
                         'to `treatment_success`')

    if control_name is None:
        control_name = "Control"
    if treatment_name is None:
        treatment_name = "Treatment"

    if seed is not None:
        # This ensures a new seed for each selection
        seed = seed + 10 * (control_trials + treatment_trials)
    random.seed(seed)
    if control_trials > 1:
        pC = float(control_success) / control_trials
    else:
        pC = 0.5
    if treatment_trials > 1:
        pT = float(treatment_success) / treatment_trials
    else:
        pT = 0.5
    cut = (1 - pT) / ((1 - pT) + (1 - pC))
    test = random.random()
    if test < cut:
        group = control_name
    else:
        group = treatment_name
    return group


def multi_arm_bandit(k, successes, failures, t=None, T=None, prior_alpha=None, prior_beta=None, seed=None, method=None):
    if prior_alpha is None:
        prior_alpha = 0.5
    if prior_beta is None:
        prior_beta = 0.5
    if seed is None:
        seed = 79461734
    if method is None:
        method = "Current Belief"
    if t is None:
        t = sum(successes) + sum(failures)
    random.seed(seed)

    posterior_alphas = [prior_alpha + s for s in successes]
    posterior_betas = [prior_beta + f for f in failures]

    if method == 'Current Belief':
        post_means = [a / (a + b) for a, b in zip(posterior_alphas, posterior_betas)]
        max_value = max(post_means)
        groups = [i for i, j in enumerate(post_means) if j == max_value]
        if len(groups) > 1:
            group = random.choice(groups)
        else:
            group = groups[0]
    elif method == "Thompson":
        c = t / 2 * T
    elif method == "UCB":
        if t == 0:
            groups = list(range(k))
        else:
            idxs = [None] * k
            for group in range(k):
                num = prior_alpha + successes[group]
                denom = prior_alpha + prior_beta + successes[group] + failures[group]
                idx = num / denom + math.sqrt((2 * math.log(t)) / denom)
                idxs[group] = idx
            max_value = max(idxs)
            groups = [i for i, j in enumerate(idxs) if j == max_value]
        if len(groups) > 1:
            group = random.choice(groups)
        else:
            group = groups[0]
    return group
