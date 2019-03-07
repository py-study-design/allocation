import math
import random

from .. import CONTROL, TREATMENT


class DoubleBiasedCoin(object):
    def __init__(
        self,
        control_success,
        control_trials,
        treatment_success,
        treatment_trials,
        control_name=None,
        treatment_name=None,
        seed=None,
    ):
        if control_trials < control_success:
            raise ValueError(
                "'control_trials' must be greater than or equal to 'control_success'"
            )
        if treatment_trials < treatment_success:
            raise ValueError(
                "'treatment_trials' must be greater than or equal "
                "to 'treatment_success'"
            )

        self.control_name = control_name or CONTROL
        self.treatment_name = treatment_name or TREATMENT

        self.seed = seed + 10 * control_trials + treatment_trials if seed else None
        random.seed(seed)

        if control_trials > 1:
            self.p_c = float(control_success) / control_trials
        else:
            self.p_c = 0.5
        if treatment_trials > 1:
            self.p_t = float(treatment_success) / treatment_trials
        else:
            self.p_t = 0.5

    def minimize(self):
        cut = math.sqrt(self.p_c) / (math.sqrt(self.p_c) + math.sqrt(self.p_t))
        return self.get_group(cut)

    def urn(self):
        cut = (1 - self.p_t) / ((1 - self.p_t) + (1 - self.p_c))
        return self.get_group(cut)

    def get_group(self, cut):
        test = random.random()
        if test < cut:
            group = self.control_name
        else:
            group = self.treatment_name
        return group


def double_biased_coin_minimize(*args, **kwargs):
    dbc = DoubleBiasedCoin(*args, **kwargs)
    return dbc.minimize()


def double_biased_coin_urn(*args, **kwargs):
    dbc = DoubleBiasedCoin(*args, **kwargs)
    return dbc.urn()
