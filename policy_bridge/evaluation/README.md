# Rule-Based Baseline Used in the Paper

This folder contains the deterministic keyword-and-slot parser used as the
rule-based comparator in the paper's natural-language-to-policy experiments:

- 150 English commands across phrasing levels L0-L4.
- 100 contradictory commands across five conflict types.

The paper entry point is **`gate3_v4_rule_parser.parse_rule_policy(command)`**.
The parser uses predefined vocabulary and regular expressions. Its parsing
logic is unchanged from the evaluated baseline.

## Files

| File | Role |
| --- | --- |
| `gate3_v4_rule_parser.py` | Actual baseline entry point used for the paper comparisons. |
| `gate3_v3_rule_parser.py` | Required helper functions imported by v4, including destination, zone, cost, person-clearance, and direct-conflict extraction. |

Keep both Python files in the same directory: v4 imports helper functions
from v3.

## Run a Command

Python 3 and its standard library are sufficient.

From the repository root:

```bash
cd policy_bridge/evaluation
python3 - <<'PY'
import json
from gate3_v4_rule_parser import parse_rule_policy

command = "Forbid zone A and go to WP2."
print(json.dumps(parse_rule_policy(command), indent=2))
PY
```

Expected output:

```json
{
  "decision": "accept",
  "reason_code": "none",
  "plan": [{"dest": "WP2"}],
  "via_zones": [],
  "exclusions": [{"zone": "A"}],
  "weights": [],
  "dynamic_object_rules": [],
  "conditional_rules": []
}
```

For a direct contradiction:

```python
parse_rule_policy("Forbid zone A and go to WP2 through zone A.")
```

This returns `decision: "reject"` and `reason_code: "contradiction"`, with
all six executable policy arrays empty.

## Output

Each command produces a **raw candidate policy**. Post-validation and
end-to-end evaluation use the Policy Validator and the evaluation harness.

## Related Materials

- [Benchmark commands, reference policies, and prompt demonstrations](../../benchmarks/benchmark-data.json)
- [Runtime installation and navigation setup](../../README.md)
