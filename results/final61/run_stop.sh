#!/bin/bash
# Seed-61 main set rerun with episodes ending at their first non-spawn collision (results/final61/main_stop.csv).
# Same settings as run.sh part A; success must reproduce main.csv exactly; the collision columns become a partition.
cd "c:/Users/James/Desktop/active-social-perception-main"
export LOO_PREFIX=loorot
python evaluate_nav.py --protocol clean --episodes 450 --workers 13 --fov 60 --range 4 --delta-unseen 0.02 \
  --scenes zara01 zara02 eth hotel --seed 61 --pmb-set prune_pos_std=1.0 --set unseen_joint=False --stop-on-collision \
  --planners supermpc-active supermpc-infogain supermpc-ttc supermpc-nearest supermpc-decoupled supermpc-scan supermpc supermpc-gazeoracle supermpc-360 \
  --out results/final61/main_stop.csv > results/final61/main_stop.log 2>&1
echo "done failures: $(grep -c FAILED results/final61/main_stop.log)"
