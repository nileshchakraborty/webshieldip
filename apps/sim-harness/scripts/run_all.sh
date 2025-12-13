#!/bin/bash
set -e

# Ensure we are in the root
cd "$(dirname "$0")/../../.."

echo "Running Advanced Simulation Harness..."
export PYTHONPATH=$PYTHONPATH:$(pwd)

python3 apps/sim-harness/run.py \
    --config apps/sim-harness/config/baseline.yaml \
    --data apps/sim-harness/data \
    --out apps/sim-harness/outputs

echo "Simulation Complete. Results in apps/sim-harness/outputs/session_outcomes.csv"
cat apps/sim-harness/outputs/session_outcomes.csv
