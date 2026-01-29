from pydantic import BaseModel
from typing import Literal, Any
import yaml  


# Metadata Schema
class Metadata(BaseModel):
    schema_version: str
    module: Literal['scoring', 'portfolio', 'ingestion', 'execution']
    logic_id: str
    author: str | None = None
    created_at: str | None = None
    description: str | None = None

# Logic Block Schema
class LogicBlock(BaseModel):
    id: str
    type: Literal['calculation', 'conditional', 'aggregation', 'llm_call']
    operation: str | None = None
    formula: str | None = None
    inputs: dict[str, Any] | list[str] | None = None
    outputs: dict[str, Any] | None = None
    cases: dict[str, Any] | None = None
    default: dict[str, Any] | None = None

# Guardrail Schema
class Guardrail(BaseModel):
    id: str
    type: Literal['validation', 'static']
    target: str | None = None
    rule: str | None = None
    min: float | None = None
    max: float | None = None
    on_violation: Literal['error', 'flag'] | None = None

# Output Schema
class Output(BaseModel):
    type: str
    source: str | None = None


# Main YAML Schema
class YAMLSpec(BaseModel):
    metadata: Metadata
    inputs: dict[str, Any]
    parameters: dict[str, Any] | None = None
    logic_blocks: list[LogicBlock]
    guardrails: list[Guardrail] | None = None
    outputs: dict[str, Output]


# Validation Function
def validate_yaml(file_path: str) -> YAMLSpec:
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)
    
    return YAMLSpec(**data)


# Test 
if __name__ == "__main__":
    # Quick test
    test_yaml = """
metadata:
  schema_version: "1.0"
  module: "scoring"
  logic_id: "test_logic"

inputs:
  candidate_data:
    type: dict
    schema:
      score: float

logic_blocks:
  - id: z_score_calc
    type: calculation
    operation: z_score
    inputs:
      x: candidate_data.score
    outputs:
      z_score: float

outputs:
  z_score:
    type: float
    source: z_score_calc.z_score
"""
    data = yaml.safe_load(test_yaml)
    spec = YAMLSpec(**data)
    print("✓ Validation passed!")
    print(f"Logic ID: {spec.metadata.logic_id}")
    print(f"Logic Blocks: {len(spec.logic_blocks)}")