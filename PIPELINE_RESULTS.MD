# LLM Pipeline Results

## Input: `momentum_score.yaml`

```yaml
metadata:
  schema_version: "1.0"
  module: "scoring"
  logic_id: "momentum_score"
  author: "quant_team"
  description: "Score assets based on momentum signals"

inputs:
  asset_data:
    type: dict
    schema:
      ticker: string
      price_20d_ago: float
      price_today: float
      volume_avg_10d: float
      volume_today: float

parameters:
  momentum_weight:
    type: float
    default: 0.6
  volume_weight:
    type: float
    default: 0.4

logic_blocks:
  - id: momentum_calc
    type: calculation
    formula: "(price_today - price_20d_ago) / price_20d_ago * 100"

  - id: volume_calc
    type: calculation
    formula: "volume_today / volume_avg_10d"

  - id: final_score
    type: aggregation
    method: weighted_sum

guardrails:
  - id: score_bounds
    type: validation
    rule: range
    min: -100
    max: 100

outputs:
  score: float
  momentum_pct: float
```

---

## Pipeline Execution

```
==================================================
Processing: tests/sample.yaml
==================================================

[1/6] Loading YAML...
✓ YAML loaded

[2/6] Validating schema...
✓ Valid | Module: scoring | ID: momentum_score

[3/6] Checking cache...
Cache MISS: f6f82f29463d1765...

[4/6] Generating code with LLM...
✓ Code generated

[5/6] Running safety check...
✓ Safety check passed

[6/6] Saving output...
Cached: f6f82f29463d1765...
✓ Saved to: generated/momentum_score.py

==================================================
✓ Pipeline complete!
==================================================
```

---

## Output: `momentum_score.py`

```python
from typing import TypedDict
import math

class AssetData(TypedDict):
    ticker: str
    price_20d_ago: float
    price_today: float
    volume_avg_10d: float
    volume_today: float

def momentum_calc(asset_data: AssetData) -> dict[str, float]:
    price_today = asset_data["price_today"]
    price_20d_ago = asset_data["price_20d_ago"]
    momentum_pct = (price_today - price_20d_ago) / price_20d_ago * 100
    return {"momentum_pct": momentum_pct}

def volume_calc(asset_data: AssetData) -> dict[str, float]:
    volume_today = asset_data["volume_today"]
    volume_avg_10d = asset_data["volume_avg_10d"]
    volume_ratio = volume_today / volume_avg_10d
    return {"volume_ratio": volume_ratio}

def final_score(momentum_pct: float, volume_ratio: float, momentum_weight: float, volume_weight: float) -> dict[str, float]:
    score = (momentum_pct * momentum_weight) + (volume_ratio * volume_weight)
    return {"score": score}

def main(asset_data: AssetData, momentum_weight: float = 0.6, volume_weight: float = 0.4) -> dict:
    momentum_result = momentum_calc(asset_data)
    volume_result = volume_calc(asset_data)
    final_score_result = final_score(
        momentum_pct=momentum_result["momentum_pct"],
        volume_ratio=volume_result["volume_ratio"],
        momentum_weight=momentum_weight,
        volume_weight=volume_weight
    )

    score = final_score_result["score"]

    if not (-100 <= score <= 100):
        raise ValueError("score is out of bounds: must be between -100 and 100")

    return {
        "score": score,
        "momentum_pct": momentum_result["momentum_pct"]
    }
```

---

## Verification: Cache Hit (Determinism)

Second run returns identical code from cache:

```
[3/6] Checking cache...
Cache HIT: f6f82f29463d1765...
✓ Cache HIT — returning cached code
```

Same input → Same output ✓