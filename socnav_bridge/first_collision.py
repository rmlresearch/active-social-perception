"""Outcome partition of the SocNavBench vision runs (seeds 7-16) by the FIRST non-spawn collision, from existing logs:
  success | collision with an undetected pedestrian | collision with a detected pedestrian | timeout.
A collision (centre distance < 0.44 m, from the saved simulator states) counts if the pedestrian had existed >= 2 s.
The pedestrian is "detected" if, at the planner step nearest the collision time, the planner's log holds an estimate
within MATCH m of a pedestrian within 0.44 m of the robot (the log stores estimate positions, not identities).
    python -m socnav_bridge.first_collision
"""
import glob, json, os
import numpy as np
from socnav_bridge.episodes import EPISODES

DT, MATCH, SPAWN_S = 0.4, 0.5, 2.0
METHODS = {"Risk-aware (ours)": "active", "Decoupled": "decoupled", "Information gain": "infogain", "Fixed": "fixed"}


def classify(d, e, cam):
    lg, cj = f"{d}/{e}.episode_log.txt", f"{d}/{e}.collisions.json"
    js = [f"{d}/{e}_{cam}_vision.json"]
    if not (os.path.exists(lg) and os.path.exists(cj) and os.path.exists(js[0])):
        return None
    reached = "termination cause: Success" in open(lg).read()
    coll = sorted([c for c in json.load(open(cj))["coll"] if c[2] >= SPAWN_S], key=lambda c: c[1])
    if not coll:
        return "success" if reached else "timeout"
    L = json.load(open(js[0]))["log"]
    t = coll[0][1]
    k = int(np.clip(round(t / DT), 0, len(L["robot"]) - 1))
    rob = np.array(L["robot"][k][:2])
    peds = [np.array(q) for q in L["peds"][k].values()]
    near = [q for q in peds if np.linalg.norm(q - rob) < 0.44 + 0.3]  # a little slack: the step is up to 0.2 s off
    if not near:
        return "undetected"
    q = min(near, key=lambda q: np.linalg.norm(q - rob))
    tracks = [np.array(tr[:2]) for tr in L["tracks"][k]]
    return "detected" if any(np.linalg.norm(tr - q) < MATCH for tr in tracks) else "undetected"


def main():
    print(f"{'gaze':18s} {'n':>4s} {'success':>8s} {'coll. undetected':>16s} {'coll. detected':>14s} {'timeout':>8s}")
    for name, cam in METHODS.items():
        out = {"success": 0, "undetected": 0, "detected": 0, "timeout": 0}
        for s in range(7, 17):
            for e in EPISODES:
                c = classify(f"results/socnav/f61_vis_{cam}_s{s}", e, cam)
                if c:
                    out[c] += 1
        n = sum(out.values())
        print(f"{name:18s} {n:4d} {out['success']/n:8.3f} {out['undetected']:9d} {out['undetected']/n:.3f} "
              f"{out['detected']:7d} {out['detected']/n:.3f} {out['timeout']:4d} {out['timeout']/n:.3f}")


if __name__ == "__main__":
    main()
