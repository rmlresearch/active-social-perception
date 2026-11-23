#!/bin/bash
# Ablation rerun with episodes ending at their first non-spawn collision (results/final61/abl_*_stop.csv).
# Same settings as run.sh; success (excl. spawn) is now reached-without-non-spawn-collision (see analyze.py).
cd "c:/Users/James/Desktop/active-social-perception-main"
export LOO_PREFIX=loorot
D=results/final61
C="--protocol clean --episodes 450 --workers 13 --fov 60 --range 4 --delta-unseen 0.02 --scenes zara01 zara02 eth hotel --seed 61 --stop-on-collision"
ev () { out=$1; shift; python evaluate_nav.py $C "$@" --out $D/${out}_stop.csv > $D/${out}_stop.log 2>&1; echo "done $out failures: $(grep -c FAILED $D/${out}_stop.log)"; }
ev abl_no_unseen_constraint --pmb-set prune_pos_std=1.0 --set unseen_joint=False unseen_constraint=False --planners supermpc-active
ev abl_no_unseen_term       --pmb-set prune_pos_std=1.0 --set unseen_joint=False --planners active-tracked-only
ev abl_no_tracked_term      --pmb-set prune_pos_std=1.0 --set unseen_joint=False --planners active-unseen-only
ev abl_kf_tracker           --pmb-set prune_pos_std=1.0 --set unseen_joint=False --planners active-kf
ev abl_prune25              --pmb-set prune_pos_std=2.5 --set unseen_joint=False --planners supermpc-active
ev abl_no_existence         --pmb-set prune_pos_std=1.0 --set unseen_joint=False existence_weighting=False --planners supermpc-active
ev abl_no_robot_sens        --pmb-set prune_pos_std=1.0 --set unseen_joint=False --planners active-no-sens
ev abl_no_state_cov         --pmb-set prune_pos_std=1.0 --set unseen_joint=False --planners active-no-statecov
