# Canonical relay input validation review

Common key P011-official-claude-relay. Reviewed plan 691d236befd010cb65332147349ca36be728bf63. Source d97c948186e7fd74d4d69d783d95f1d55f655448. See docs/verification/P011/canonical-validation/report.md and manifest SHA256 5f891c55893114a65ecd20db4d66d7a53fcc8d54045ce85b2f29b0b7880cd936.

Full regression 111 PASS, install/upgrade 34 checks PASS. Raw stream/callback identity binding and canonical input replacement succeeded. The mixed synthetic body reached one neutral receiver with matching byte hashes. Explicit sender deny exposed no callable send. Inbound refusal remains unverified because the online observer missed the peer user-event shape before receiver cleanup. A is partial and B is unattempted. Plan may review a corrected isolated refusal verification and the documented native notice classifier ambiguity. No real handoff retry or user terminal input is requested.
