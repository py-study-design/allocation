"""
Randomization is a module that provides functions to create random group
assignments to be used in clinical trials
"""

import math
import random

# import scipy.stats as stats


# A Response adaptive randomization technique
def double_biased_coin_minimize(
    control_success,
    control_trials,
    treatment_success,
    treatment_trials,
    control_name=None,
    treatment_name=None,
    seed=None,
):
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
        raise ValueError(
            "`control_trials` must be greater than or equal " "to `control_success`"
        )
    if treatment_trials < treatment_success:
        raise ValueError(
            "`treatment_trials` must be greater than or equal " "to `treatment_success`"
        )

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


# A Response adaptive randomization technique
def double_biased_coin_urn(
    control_success,
    control_trials,
    treatment_success,
    treatment_trials,
    control_name=None,
    treatment_name=None,
    seed=None,
):
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
        raise ValueError(
            "`control_trials` must be greater than or equal " "to `control_success`"
        )
    if treatment_trials < treatment_success:
        raise ValueError(
            "`treatment_trials` must be greater than or equal " "to `treatment_success`"
        )

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
