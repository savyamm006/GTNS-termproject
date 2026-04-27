from collections import deque


def resident_optimal(n_res, n_hosp, res_prefs, hosp_prefs, capacities=None):
    if capacities is None:
        capacities = [1] * n_hosp

    hosp_rank = [{r: i for i, r in enumerate(hosp_prefs[h])} for h in range(n_hosp)]

    free       = deque(range(n_res))
    next_prop  = [0] * n_res
    res_match  = {r: None for r in range(n_res)}
    hosp_match = {h: []   for h in range(n_hosp)}
    proposals  = [0] * n_res

    while free:
        r = free.popleft()
        if next_prop[r] >= len(res_prefs[r]):
            continue
        h = res_prefs[r][next_prop[r]]
        next_prop[r] += 1
        proposals[r] += 1

        hosp_match[h].append(r)
        hosp_match[h].sort(key=lambda x: hosp_rank[h][x])

        if len(hosp_match[h]) > capacities[h]:
            dropped = hosp_match[h].pop()
            res_match[dropped] = None
            free.append(dropped)

        res_match[r] = h

    return res_match, hosp_match, proposals


def hospital_optimal(n_res, n_hosp, res_prefs, hosp_prefs, capacities=None):
    if capacities is None:
        capacities = [1] * n_hosp

    res_rank   = [{h: i for i, h in enumerate(res_prefs[r])} for r in range(n_res)]
    next_prop  = [0] * n_hosp
    hosp_match = {h: []   for h in range(n_hosp)}
    res_match  = {r: None for r in range(n_res)}

    def has_vacancy(h):
        return len(hosp_match[h]) < capacities[h] and next_prop[h] < len(hosp_prefs[h])

    free = deque(range(n_hosp))
    while free:
        h = free.popleft()
        if not has_vacancy(h):
            continue
        r = hosp_prefs[h][next_prop[h]]
        next_prop[h] += 1

        if res_match[r] is None:
            hosp_match[h].append(r)
            res_match[r] = h
        else:
            cur = res_match[r]
            if res_rank[r][h] < res_rank[r][cur]:
                hosp_match[cur].remove(r)
                hosp_match[h].append(r)
                res_match[r] = h
                if has_vacancy(cur):
                    free.append(cur)

        if has_vacancy(h):
            free.append(h)

    return res_match, hosp_match
