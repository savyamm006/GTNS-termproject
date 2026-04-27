import warnings
import numpy as np


def _validate(n_res, n_hosp, capacities, list_length):
    if n_res < 1:
        raise ValueError(f"n_residents must be >= 1, got {n_res}")
    if n_hosp < 1:
        raise ValueError(f"n_hospitals must be >= 1, got {n_hosp}")
    if len(capacities) != n_hosp:
        raise ValueError(f"len(capacities)={len(capacities)} but n_hospitals={n_hosp}")
    for h, c in enumerate(capacities):
        if c < 1:
            raise ValueError(f"capacities[{h}]={c}, must be >= 1")
    if list_length < 1 or list_length > n_hosp:
        raise ValueError(f"list_length={list_length} must be in [1, {n_hosp}]")
    if sum(capacities) > n_res:
        warnings.warn(f"Total capacity ({sum(capacities)}) > n_residents ({n_res}). "
                      "Some slots will be unfilled.", UserWarning, stacklevel=3)


def generate_uniform(n_res, n_hosp, capacities=None, list_length=None, seed=None):
    if capacities is None:
        capacities = [1] * n_hosp
    if list_length is None:
        list_length = n_hosp
    _validate(n_res, n_hosp, capacities, list_length)

    rng = np.random.default_rng(seed)
    res_prefs = [
        [int(h) for h in rng.choice(n_hosp, size=list_length, replace=False)]
        for _ in range(n_res)
    ]

    if list_length == n_hosp:
        hosp_prefs = [
            [int(r) for r in rng.permutation(n_res)]
            for _ in range(n_hosp)
        ]
    else:
        applicants = {h: [] for h in range(n_hosp)}
        for r, prefs in enumerate(res_prefs):
            for h in prefs:
                applicants[h].append(r)
        hosp_prefs = []
        for h in range(n_hosp):
            app = applicants[h]
            hosp_prefs.append(
                [int(app[i]) for i in rng.permutation(len(app))] if app else []
            )

    return res_prefs, hosp_prefs, capacities


def generate_correlated(n_res, n_hosp, noise_std=1.0, capacities=None,
                        list_length=None, seed=None):
    if capacities is None:
        capacities = [1] * n_hosp
    if list_length is None:
        list_length = n_hosp
    _validate(n_res, n_hosp, capacities, list_length)
    if noise_std <= 0:
        raise ValueError(f"noise_std must be > 0, got {noise_std}")

    rng = np.random.default_rng(seed)
    hosp_quality = rng.standard_normal(n_hosp)
    res_quality  = rng.standard_normal(n_res)

    res_prefs = []
    for _ in range(n_res):
        u = hosp_quality + rng.normal(0, noise_std, n_hosp)
        res_prefs.append([int(h) for h in np.argsort(-u)[:list_length]])

    if list_length == n_hosp:
        hosp_prefs = []
        for _ in range(n_hosp):
            u = res_quality + rng.normal(0, noise_std, n_res)
            hosp_prefs.append([int(r) for r in np.argsort(-u)])
    else:
        applicants = {h: [] for h in range(n_hosp)}
        for r, prefs in enumerate(res_prefs):
            for h in prefs:
                applicants[h].append(r)
        hosp_prefs = []
        for h in range(n_hosp):
            app = applicants[h]
            if not app:
                hosp_prefs.append([])
                continue
            u = res_quality[np.array(app)] + rng.normal(0, noise_std, len(app))
            hosp_prefs.append([int(app[i]) for i in np.argsort(-u)])

    return res_prefs, hosp_prefs, capacities


def build_pref_rank(prefs):
    return [{agent: idx for idx, agent in enumerate(lst)} for lst in prefs]


def match_rank(agent, partner, prefs, rank_lookup=None):
    if partner is None:
        return len(prefs[agent])
    if rank_lookup is not None:
        return rank_lookup[agent].get(partner, len(prefs[agent]))
    try:
        return prefs[agent].index(partner)
    except ValueError:
        return len(prefs[agent])


def average_match_rank(n_agents, match, prefs, rank_lookup=None):
    if rank_lookup is None:
        rank_lookup = build_pref_rank(prefs)
    ranks = [match_rank(a, match[a], prefs, rank_lookup) for a in range(n_agents)]
    return float(np.mean(ranks))
