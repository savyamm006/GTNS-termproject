import sys, os, matplotlib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from gale_shapley import resident_optimal
from data_generator import generate_uniform, match_rank, build_pref_rank

# 20 residents, 5 hospitals each with capacity 4
N_RES   = 20
N_HOSP  = 5
CAPS    = [4] * N_HOSP
SEED    = 42
SAVE_PATH = os.path.join(os.path.dirname(__file__), '..', 'plots', 'fig2_bipartite.png')

rp, hp, caps = generate_uniform(N_RES, N_HOSP, capacities=CAPS, seed=SEED)
res_match, hosp_match, _ = resident_optimal(N_RES, N_HOSP, rp, hp, caps)
rr = build_pref_rank(rp)
hr = build_pref_rank(hp)

RANK_COLORS = ['#2166ac', '#4393c3', '#92c5de', '#f4a582', '#d6604d', '#b2182b']
def rank_color(rank):
    return RANK_COLORS[min(rank, len(RANK_COLORS) - 1)]

# resident y positions — evenly spaced
res_y = {r: N_RES - 1 - r for r in range(N_RES)}

# hospital y positions — centred on the midpoint of their matched residents
hosp_y = {}
for h in range(N_HOSP):
    matched = hosp_match[h]
    if matched:
        hosp_y[h] = np.mean([res_y[r] for r in matched])
    else:
        hosp_y[h] = (N_RES - 1) / 2  # fallback centre

X_RES, X_HOSP = 0.0, 3.5
NODE_R = 0.28

fig, ax = plt.subplots(figsize=(5, 6))
ax.set_xlim(-0.7, 4.3)
ax.set_ylim(-1.2, N_RES + 0.6)
ax.axis('off')

# draw edges first
for r in range(N_RES):
    h = res_match[r]
    if h is not None:
        ax.plot([X_RES + NODE_R, X_HOSP - NODE_R],
                [res_y[r], hosp_y[h]],
                color='#aaaaaa', lw=0.8, zorder=1, solid_capstyle='round')

# resident circles
for r in range(N_RES):
    y = res_y[r]
    rank = match_rank(r, res_match[r], rp, rr)
    circle = mpatches.Circle((X_RES, y), NODE_R, color=rank_color(rank),
                              ec='white', lw=0.7, zorder=3)
    ax.add_patch(circle)
    ax.text(X_RES, y, f'R{r}', ha='center', va='center',
            fontsize=5, color='white', fontweight='bold', zorder=4)

# hospital squares — wider to show capacity label
for h in range(N_HOSP):
    y = hosp_y[h]
    matched = hosp_match[h]
    # colour by best-ranked matched resident
    if matched:
        best_rank = min(match_rank(h, r, hp, hr) for r in matched)
        color = rank_color(best_rank)
    else:
        color = '#cccccc'

    W, H = 0.7, 0.48
    square = mpatches.FancyBboxPatch(
        (X_HOSP - W/2, y - H/2), W, H,
        boxstyle="round,pad=0.03", color=color, ec='white', lw=0.7, zorder=3
    )
    ax.add_patch(square)
    ax.text(X_HOSP, y + 0.06, f'H{h}', ha='center', va='center',
            fontsize=5.5, color='white', fontweight='bold', zorder=4)
    ax.text(X_HOSP, y - 0.13, f'cap={caps[h]}  matched={len(matched)}',
            ha='center', va='center', fontsize=4, color='white', zorder=4)

# column headers
ax.text(X_RES,  N_RES - 0.1, 'Residents', ha='center', va='bottom',
        fontsize=7, fontweight='bold', color='#333333')
ax.text(X_HOSP, N_RES - 0.1, 'Hospitals', ha='center', va='bottom',
        fontsize=7, fontweight='bold', color='#333333')

legend_items = [
    mpatches.Patch(color=RANK_COLORS[0], label='1st choice'),
    mpatches.Patch(color=RANK_COLORS[1], label='2nd choice'),
    mpatches.Patch(color=RANK_COLORS[2], label='3rd choice'),
    mpatches.Patch(color=RANK_COLORS[3], label='4th choice'),
    mpatches.Patch(color=RANK_COLORS[4], label='5th choice'),
    mpatches.Patch(color=RANK_COLORS[5], label='6th+'),
    mlines.Line2D([], [], color='#aaaaaa', lw=0.9, label='Stable match'),
]
ax.legend(handles=legend_items, loc='lower center',
          bbox_to_anchor=(0.5, -0.09), ncol=4, fontsize=5.5,
          framealpha=0.9, edgecolor='#cccccc')


plt.tight_layout()
os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
plt.savefig(SAVE_PATH, dpi=300, bbox_inches='tight')
print(f"Saved → {SAVE_PATH}")
