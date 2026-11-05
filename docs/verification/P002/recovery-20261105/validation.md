# Recovery proposal validation

Initial guard/pre-commit correctly rejected the new STATE log because its evidence
column used a path instead of required `-` (exit 1). Corrected only that new log
format, retaining the evidence path in its narrative. No historical log changed.
The proposal and inventory do not execute fixture controls or count as C3 PASS.
