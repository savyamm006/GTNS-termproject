# Stable Matching: Python Implementation
**CS-4231-1 Graph Theory and Network Science | Term Paper**

Supplementary code for the paper:
*Stable Matching in Graphs: Gale-Shapley Algorithm — Applications to Hospital Residency Matching and Market Design*

---

## Project Structure

```
stable_matching/
├── src/
│   ├── gale_shapley.py      # Core GS algorithm (both DA variants)
│   ├── verifier.py          # Independent O(n²) blocking-pair verifier
│   └── data_generator.py    # Synthetic preference list generator
├── experiments/
│   ├── exp1_runtime.py      # Fig 1 — Runtime scaling vs O(n²)
│   ├── exp2_bipartite_graph.py  # Fig 2 — Bipartite matching graph
│   ├── exp3_asymmetry.py    # Fig 3 — Proposer-optimality asymmetry
│   ├── exp4_proposals.py    # Fig 4 — Proposals-per-resident distribution
│   └── exp5_stability_check.py  # Stability verification (all trials)
├── plots/                   # Generated figures saved here
├── run_all.py               # Master script — runs all experiments
├── requirements.txt
└── README.md
```

---

## Setup

```bash
# Clone the repo
git clone https://github.com/[your-repo]/stable-matching
cd stable-matching/stable_matching

# Install dependencies
pip install -r requirements.txt
```

---

## Running

### Run all experiments at once
```bash
python run_all.py
```

### Run individual experiments
```bash
python experiments/exp1_runtime.py
python experiments/exp2_bipartite_graph.py
python experiments/exp3_asymmetry.py
python experiments/exp4_proposals.py
python experiments/exp5_stability_check.py
```

All figures are saved to `plots/` as high-resolution PNGs.

---

## Key Results

| Experiment | Key Finding |
|---|---|
| Runtime scaling | Empirical runtime tracks O(n²) closely up to n = 500 |
| Bipartite graph | Matching visualised with match-rank colour coding |
| Asymmetry | Resident-optimal DA gives residents avg rank ~1.6 vs ~4.2 for hospitals |
| Proposals | Right-skewed: most residents match in 1–3 proposals; tail reaches ~n |
| Stability | **Zero blocking pairs** detected across all trials (both DA variants) |

---

## Algorithm Overview

The core Gale-Shapley Deferred Acceptance runs in **O(n²)** time:

```python
while free_residents:
    r = free_residents.popleft()
    h = res_prefs[r][next_proposal[r]]   # propose to next hospital
    next_proposal[r] += 1

    hosp_match[h].append(r)
    hosp_match[h].sort(key=lambda x: hosp_rank[h][x])

    if len(hosp_match[h]) > capacity[h]:
        dropped = hosp_match[h].pop()    # reject worst
        free_residents.append(dropped)
```

Both **resident-optimal** (resident-proposing) and **hospital-optimal**
(hospital-proposing) variants are implemented in `src/gale_shapley.py`.

---

## References
- Gale, D. & Shapley, L. S. (1962). College admissions and the stability of marriage.
- Roth, A. E. (1984). The evolution of the labor market for medical interns and residents.
- Roth, A. E. & Peranson, E. (1999). The redesign of the matching market for American physicians.
