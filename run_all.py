"""
Master script — runs all five experiments in sequence.
Outputs are saved to the plots/ directory.
"""
import subprocess, sys, os

EXPERIMENTS = [
    ("Experiment 1: Runtime Scaling",           "experiments/exp1_runtime.py"),
    ("Experiment 2: Bipartite Graph",            "experiments/exp2_bipartite_graph.py"),
    ("Experiment 3: Proposer-Optimality",        "experiments/exp3_asymmetry.py"),
    ("Experiment 4: Proposals Distribution",     "experiments/exp4_proposals.py"),
    ("Experiment 5: Stability Verification",     "experiments/exp5_stability_check.py"),
]

root = os.path.dirname(os.path.abspath(__file__))

print("="*60)
print("  Stable Matching — Running All Experiments")
print("="*60)

for name, script in EXPERIMENTS:
    print(f"\n▶  {name}")
    print("-"*60)
    result = subprocess.run(
        [sys.executable, os.path.join(root, script)],
        cwd=root
    )
    if result.returncode != 0:
        print(f"\n✗ {name} FAILED (exit code {result.returncode})")
        sys.exit(1)

print("\n" + "="*60)
print("  All experiments complete. Plots saved to plots/")
print("="*60)
