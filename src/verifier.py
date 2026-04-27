def build_rank(prefs):
    return [{agent: idx for idx, agent in enumerate(lst)} for lst in prefs]


def _worst_rank_per_hospital(hosp_match, hosp_rank, capacities, n_hosp):
    worst = []
    for h in range(n_hosp):
        if len(hosp_match[h]) < capacities[h]:
            worst.append(-1)
        elif not hosp_match[h]:
            worst.append(-1)
        else:
            worst.append(max(hosp_rank[h][r] for r in hosp_match[h]))
    return worst


def find_blocking_pairs(n_res, n_hosp, res_prefs, hosp_prefs,
                        res_match, hosp_match, capacities=None,
                        res_rank=None, hosp_rank=None):
    if capacities is None:
        capacities = [1] * n_hosp
    if res_rank is None:
        res_rank = build_rank(res_prefs)
    if hosp_rank is None:
        hosp_rank = build_rank(hosp_prefs)

    worst = _worst_rank_per_hospital(hosp_match, hosp_rank, capacities, n_hosp)
    blocking = []

    for r in range(n_res):
        cur_h = res_match[r]
        cur_rank = res_rank[r][cur_h] if cur_h is not None else len(res_prefs[r])

        for h in res_prefs[r]:
            if res_rank[r][h] >= cur_rank:
                break
            if worst[h] == -1 or hosp_rank[h][r] < worst[h]:
                blocking.append((r, h))

    return blocking


def has_blocking_pair(n_res, n_hosp, res_prefs, hosp_prefs,
                      res_match, hosp_match, capacities=None,
                      res_rank=None, hosp_rank=None):
    if capacities is None:
        capacities = [1] * n_hosp
    if res_rank is None:
        res_rank = build_rank(res_prefs)
    if hosp_rank is None:
        hosp_rank = build_rank(hosp_prefs)

    worst = _worst_rank_per_hospital(hosp_match, hosp_rank, capacities, n_hosp)

    for r in range(n_res):
        cur_h = res_match[r]
        cur_rank = res_rank[r][cur_h] if cur_h is not None else len(res_prefs[r])
        for h in res_prefs[r]:
            if res_rank[r][h] >= cur_rank:
                break
            if worst[h] == -1 or hosp_rank[h][r] < worst[h]:
                return True
    return False


def is_stable(n_res, n_hosp, res_prefs, hosp_prefs,
              res_match, hosp_match, capacities=None,
              res_rank=None, hosp_rank=None):
    return not has_blocking_pair(n_res, n_hosp, res_prefs, hosp_prefs,
                                 res_match, hosp_match, capacities,
                                 res_rank, hosp_rank)
