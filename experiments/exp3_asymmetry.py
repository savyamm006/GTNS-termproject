import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import numpy as np
import matplotlib.pyplot as plt
from gale_shapley import resident_optimal, hospital_optimal
from data_generator import generate_uniform, average_match_rank, build_pref_rank

N_VALUES = [10, 20, 30, 50, 75, 100, 150, 200]
N_TRIALS = 20
SAVE_PATH = os.path.join(os.path.dirname(__file__), '..', 'plots', 'fig3_asymmetry.png')

ro_res_all, ro_hosp_all, ho_res_all, ho_hosp_all = [], [], [], []

for n in N_VALUES:
    ro_res, ro_hosp, ho_res, ho_hosp = [], [], [], []
    for trial in range(N_TRIALS):
        rp, hp, caps = generate_uniform(n, n, seed=trial * 1000 + n)
        rr = build_pref_rank(rp)
        hr = build_pref_rank(hp)

        rm, hm, _ = resident_optimal(n, n, rp, hp, caps)
        ro_res.append(average_match_rank(n, rm, rp, rr))
        ro_hosp.append(average_match_rank(n, {h: (hm[h][0] if hm[h] else None)
                                              for h in range(n)}, hp, hr))

        rm2, hm2 = hospital_optimal(n, n, rp, hp, caps)
        ho_res.append(average_match_rank(n, rm2, rp, rr))
        ho_hosp.append(average_match_rank(n, {h: (hm2[h][0] if hm2[h] else None)
                                               for h in range(n)}, hp, hr))

    ro_res_all.append((np.mean(ro_res),   np.std(ro_res)))
    ro_hosp_all.append((np.mean(ro_hosp), np.std(ro_hosp)))
    ho_res_all.append((np.mean(ho_res),   np.std(ho_res)))
    ho_hosp_all.append((np.mean(ho_hosp), np.std(ho_hosp)))
    print(f"n={n:3d}  RO res={np.mean(ro_res):.2f} hosp={np.mean(ro_hosp):.2f}  "
          f"HO res={np.mean(ho_res):.2f} hosp={np.mean(ho_hosp):.2f}")

def unpack(lst):
    return np.array([x[0] for x in lst]), np.array([x[1] for x in lst])

ns = np.array(N_VALUES)
ro_rm, ro_rs = unpack(ro_res_all);   ro_hm, ro_hs = unpack(ro_hosp_all)
ho_rm, ho_rs = unpack(ho_res_all);   ho_hm, ho_hs = unpack(ho_hosp_all)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7, 2.8), sharey=False)

for ax, rm, rs, hm, hs, title in [
    (ax1, ro_rm, ro_rs, ro_hm, ro_hs, 'Resident-optimal DA'),
    (ax2, ho_rm, ho_rs, ho_hm, ho_hs, 'Hospital-optimal DA'),
]:
    ax.fill_between(ns, rm - rs, rm + rs, alpha=0.15, color='#1a6faf')
    ax.fill_between(ns, hm - hs, hm + hs, alpha=0.15, color='#c0392b')
    ax.plot(ns, rm, 'o-',  color='#1a6faf', lw=1.2, markersize=3,
            label='Residents')
    ax.plot(ns, hm, 's--', color='#c0392b', lw=1.2, markersize=3,
            label='Hospitals')
    ax.set_xlabel('Number of agents ($n$)', fontsize=7)
    ax.set_ylabel('Avg. match rank (lower = better)', fontsize=7)
    ax.set_title(title, fontsize=7, pad=4)
    ax.tick_params(labelsize=6)
    ax.legend(fontsize=6, framealpha=0.9)
    ax.grid(True, linestyle='--', linewidth=0.4, alpha=0.5)
    ax.spines[['top', 'right']].set_visible(False)


plt.tight_layout()
os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
plt.savefig(SAVE_PATH, dpi=300, bbox_inches='tight')
print(f"Saved → {SAVE_PATH}")
