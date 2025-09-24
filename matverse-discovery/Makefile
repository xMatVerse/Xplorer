.PHONY: all scidis symbios rhi daq cassandra

all:
python scripts/scoreboard.py

scidis:
python scidis/src/run_eval.py

symbios:
python symbios/cli_verifier.py symbios/proofs/sample_proof.json

rhi:
python rhi-sim/src/pqc_bench.py

daq:
python daq-routing/sim/simulate.py

cassandra:
python cassandra-edge/src/quantize.py
