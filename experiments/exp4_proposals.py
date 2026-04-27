import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import numpy as np
import matplotlib.pyplot as plt
from gale_shapley import resident_optimal
from data_generator import generate_uniform

N        = 100
N_TRIALS = 20
SAVE_PATH = os.path.join(os.path.dirname(__file__), '..', 'plots', 'fig4_proposals.png')

all_props = []
for trial in range(N_TRIALS):
    rp, hp, caps = generate_uniform(N, N, seed=trial * 999)
    _, _, proposals = resident_optimal(N, N, rp, hp, caps)
    all_props.extend(proposals)

all_props = np.array(all_props)
print(f"n={N}, {N_TRIALS} trials")
print(f"  mean={all_props.mean():.2f}  median={np.median(all_props):.0f}  "
      f"max={all_props.max()}  >5: {(all_props>5).mean()*100:.1f}%")

fig, ax1 = plt.subplots(figsize=(3.5, 2.8))

bins = range(1, int(all_props.max()) + 2)
ax1.hist(all_props, bins=bins, color='#1a6faf', edgecolor='white',
         linewidth=0.4, alpha=0.85)
ax1.axvline(all_props.mean(),     color='#c0392b', lw=1.2, linestyle='--',
            label=f'Mean = {all_props.mean():.1f}')
ax1.axvline(np.median(all_props), color='#e67e22', lw=1.2, linestyle=':',
            label=f'Median = {np.median(all_props):.0f}')
ax1.set_xlabel('Proposals made before acceptance', fontsize=7)
ax1.set_ylabel('Count (all trials)', fontsize=7)
ax1.set_title(f'Proposal count distribution ($n={N}$, {N_TRIALS} trials)', fontsize=7, pad=4)
ax1.tick_params(labelsize=6)
ax1.legend(fontsize=6, framealpha=0.9)
ax1.grid(True, axis='y', linestyle='--', linewidth=0.4, alpha=0.5)
ax1.spines[['top', 'right']].set_visible(False)

plt.tight_layout()
os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
plt.savefig(SAVE_PATH, dpi=300, bbox_inches='tight')
print(f"Saved → {SAVE_PATH}")
