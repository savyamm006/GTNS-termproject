import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from gale_shapley import resident_optimal
from data_generator import generate_uniform

N_VALUES = [10, 20, 30, 50, 75, 100, 150, 200, 300, 400, 500]
N_TRIALS = 20
SAVE_PATH = os.path.join(os.path.dirname(__file__), '..', 'plots', 'fig1_runtime.png')

means, stds = [], []
for n in N_VALUES:
    times = []
    for trial in range(N_TRIALS):
        rp, hp, caps = generate_uniform(n, n, seed=trial * 1000 + n)
        t0 = time.perf_counter()
        resident_optimal(n, n, rp, hp, caps)
        times.append((time.perf_counter() - t0) * 1000)
    means.append(np.mean(times))
    stds.append(np.std(times))
    print(f"n={n:4d}  mean={means[-1]:.3f} ms  std={stds[-1]:.3f} ms")

means, stds, ns = np.array(means), np.array(stds), np.array(N_VALUES)
c = np.mean(means / ns**2)

fig, ax = plt.subplots(figsize=(3.5, 2.8))

ax.fill_between(ns, means - stds, means + stds, alpha=0.18, color='#1a6faf')
ax.plot(ns, means, 'o-', color='#1a6faf', lw=1.2, markersize=3,
        label='Empirical runtime')
ax.plot(ns, c * ns**2, '--', color='#c0392b', lw=1.2,
        label=r'$O(n^2)$ reference')

ax.set_xlabel('Number of agents per side ($n$)', fontsize=7)
ax.set_ylabel('Runtime (ms)', fontsize=7)
ax.tick_params(labelsize=6)
ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
ax.grid(True, which='major', linestyle='--', linewidth=0.4, alpha=0.5)
ax.grid(True, which='minor', linestyle=':', linewidth=0.3, alpha=0.3)
ax.legend(fontsize=6, framealpha=0.9)
ax.spines[['top', 'right']].set_visible(False)


plt.tight_layout()
os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
plt.savefig(SAVE_PATH, dpi=300, bbox_inches='tight')
print(f"Saved → {SAVE_PATH}")
