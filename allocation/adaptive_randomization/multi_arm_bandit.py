import math
import random


def multi_arm_bandit(
    k,
    successes,
    failures,
    t=None,
    T=None,
    prior_alpha=None,
    prior_beta=None,
    seed=None,
    method=None,
):
    prior_alpha = prior_alpha or 0.5
    prior_beta = prior_beta or 0.5
    seed = seed or 79461734
    method = method or "Current Belief"
    t = t or sum(successes) + sum(failures)

    random.seed(seed)

    posterior_alphas = [prior_alpha + s for s in successes]
    posterior_betas = [prior_beta + f for f in failures]

    if method == "Current Belief":
        post_means = [a / (a + b) for a, b in zip(posterior_alphas, posterior_betas)]
        max_value = max(post_means)
        groups = [i for i, j in enumerate(post_means) if j == max_value]
        if len(groups) > 1:
            group = random.choice(groups)
        else:
            group = groups[0]
    elif method == "Thompson":
        group = t / 2 * T
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
