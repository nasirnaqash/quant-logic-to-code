# LLM Code Generator

An automated pipeline that converts YAML logic definitions into production-ready Python code using Large Language Models.

## What It Does

```
YAML Logic File → LLM Pipeline → Executable Python Code
```

**Input:** Structured YAML defining business logic (calculations, conditionals, aggregations)

**Output:** Clean, type-safe, validated Python code ready for production

## Example

### Input (YAML)
```yaml
logic_blocks:
  - id: momentum_calc
    type: calculation
    formula: "(price_today - price_20d_ago) / price_20d_ago * 100"
    
  - id: sector_adjustment
    type: conditional
    cases:
      technology: 1.15
      finance: 1.10
    default: 1.0
```

### Output (Python)
```python
def momentum_calc(price_today: float, price_20d_ago: float) -> float:
    return (price_today - price_20d_ago) / price_20d_ago * 100

def sector_adjustment(sector: str) -> float:
    if sector == "technology":
        return 1.15
    elif sector == "finance":
        return 1.10
    return 1.0
```

## Pipeline Steps

| Step | Description |
|------|-------------|
| 1. Validate | Schema validation using Pydantic |
| 2. Cache Check | Redis lookup for deterministic outputs |
| 3. Generate | LLM converts YAML to Python |
| 4. Safety Check | AST analysis blocks dangerous code |
| 5. Save | Cache result and save to file |

## Key Features

- **Deterministic** — Same input always produces same output (temperature=0 + caching)
- **Safe** — Blocks dangerous imports (`os`, `subprocess`, `eval`, etc.)
- **Validated** — Pydantic schema ensures YAML correctness
- **Cached** — Redis caching for instant repeat requests
- **Production-Ready** — Generated code includes type hints and error handling

## Tech Stack

- Python 3.11+
- LangChain + Gemini (LLM)
- Pydantic (Validation)
- Redis (Caching)
- AST (Safety Analysis)

## Usage

```bash
python main.py input.yaml
```

## Project Structure

```
├── config/
│   └── settings.py       # Configuration
├── schemas/
│   └── validators.py     # Pydantic schemas
├── core/
│   ├── cache.py          # Redis caching
│   ├── llm_client.py     # LLM integration
│   └── safety.py         # AST safety checker
├── prompts/
│   └── v1.0.txt          # LLM prompt template
├── generated/            # Output Python files
└── main.py               # Entry point
```

## Safety Guardrails

Generated code is blocked if it contains:

| Blocked | Reason |
|---------|--------|
| `os`, `subprocess` | System access |
| `socket`, `requests` | Network access |
| `eval`, `exec` | Arbitrary code execution |
| `open` | File system access |
| `random` | Non-deterministic output |

