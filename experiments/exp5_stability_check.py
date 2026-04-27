import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from gale_shapley import resident_optimal, hospital_optimal
from data_generator import generate_uniform
from verifier import is_stable, find_blocking_pairs, build_rank

N_VALUES = [10, 20, 50, 100, 200, 500]
N_TRIALS = 20

print(f"{'n':>6} | {'RO stable':>12} | {'HO stable':>12} | {'Status':>8}")
print("-" * 50)

all_passed = True
for n in N_VALUES:
    ro_ok = ho_ok = 0
    for trial in range(N_TRIALS):
        rp, hp, caps = generate_uniform(n, n, seed=trial * 777 + n)
        rr = build_rank(rp)
        hr = build_rank(hp)

        rm,  hm,  _ = resident_optimal(n, n, rp, hp, caps)
        rm2, hm2    = hospital_optimal(n, n, rp, hp, caps)

        if is_stable(n, n, rp, hp, rm,  hm,  caps, rr, hr): ro_ok += 1
        else:
            bp = find_blocking_pairs(n, n, rp, hp, rm, hm, caps, rr, hr)
            print(f"  RO fail n={n} trial={trial}: {len(bp)} blocking pairs")
            all_passed = False

        if is_stable(n, n, rp, hp, rm2, hm2, caps, rr, hr): ho_ok += 1
        else:
            bp = find_blocking_pairs(n, n, rp, hp, rm2, hm2, caps, rr, hr)
            print(f"  HO fail n={n} trial={trial}: {len(bp)} blocking pairs")
            all_passed = False

    status = "PASS" if ro_ok == ho_ok == N_TRIALS else "FAIL"
    print(f"{n:>6} | {ro_ok:>4}/{N_TRIALS:<7} | {ho_ok:>4}/{N_TRIALS:<7} | {status:>8}")

print()
if all_passed:
    print("All trials stable. Zero blocking pairs across all instances.")
