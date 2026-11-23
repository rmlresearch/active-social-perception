"""Outcome partition of the seed-61 replay episodes with early termination (results/final61/main_stop.csv):
each episode is exactly one of  success | collision with an undetected pedestrian | collision with a detected
pedestrian | timeout (spawn collisions excluded, as in the primary metric). Success is reached without a collision
with any non-spawn pedestrian (first_coll == ""). The original main.csv tested collision steps minus spawn
pedestrian-steps == 0, which misclassifies episodes in which two pedestrians are hit in one step; the script
reports how many episodes that affected (11 false successes and 50 false failures of 16,200).
    python results/final61/partition.py
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(os.path.join(HERE, "..", "..")); sys.path.insert(0, ".")
from evaluate_nav import load
flag = lambda x: x if isinstance(x, bool) else str(x) in ("True", "1", "1.0")
P = {"Risk-aware (ours)": "supermpc-active", "Decoupled": "supermpc-decoupled", "Information gain": "supermpc-infogain",
     "Fixed": "supermpc", "Look at nearest": "supermpc-nearest", "TTC heuristic": "supermpc-ttc", "Scan": "supermpc-scan",
     "Gaze oracle": "supermpc-gazeoracle", "360 camera": "supermpc-360"}
new = load(f"{HERE}/main_stop.csv"); old = {(r["scene"], int(r["episode"]), r["planner"]): r for r in load(f"{HERE}/main.csv")}
succ = lambda r: flag(r["reached"]) and r["first_coll"] == ""
fs = sum(succ(r) < flag(old[(r["scene"], int(r["episode"]), r["planner"])]["success_nospawn"]) for r in new)
ff = sum(succ(r) > flag(old[(r["scene"], int(r["episode"]), r["planner"])]["success_nospawn"]) for r in new)
print(f"{len(new)} episodes; the original step-count test had {fs} false successes and {ff} false failures")
print(f"{'gaze':18s} {'n':>5s} {'success':>8s} {'coll. undetected':>16s} {'coll. detected':>14s} {'timeout':>8s}   (episodes, fractions)")
for name, p in P.items():
    r = [x for x in new if x["planner"] == p]; n = len(r)
    s = sum(succ(x) for x in r)
    cu = sum(x["first_coll"] == "untracked" for x in r); cd = sum(x["first_coll"] == "tracked" for x in r)
    to = n - s - cu - cd
    print(f"{name:18s} {n:5d} {s:4d} {s/n:.3f} {cu:7d} {cu/n:.3f}    {cd:6d} {cd/n:.3f}  {to:4d} {to/n:.3f}")
