import sys
import yaml
from pathlib import Path

from schemas.validators import validate_yaml
from core.cache import Cache
from core.llm_client import LLMClient
from core.safety import SafetyChecker
from config.settings import GENERATED_DIR


def process_yaml(file_path: str) -> str:
    """Main pipeline: YAML → Python code"""
    
    print(f"\n{'='*50}")
    print(f"Processing: {file_path}")
    print('='*50)
    
    # Step 1: Load YAML
    print("\n[1/6] Loading YAML...")
    with open(file_path, 'r') as f:
        yaml_content = f.read()
        yaml_data = yaml.safe_load(yaml_content)
    print("✓ YAML loaded")
    
    # Step 2: Validate schema
    print("\n[2/6] Validating schema...")
    try:
        spec = validate_yaml(file_path)
        print(f"✓ Valid | Module: {spec.metadata.module} | ID: {spec.metadata.logic_id}")
    except Exception as e:
        print(f"✗ Validation failed: {e}")
        return None
    
    # Step 3: Check cache
    print("\n[3/6] Checking cache...")
    cache = Cache()
    cached_code = cache.get(yaml_data)
    
    if cached_code:
        print("✓ Cache HIT — returning cached code")
        return cached_code
    
    # Step 4: Generate code with LLM
    print("\n[4/6] Generating code with LLM...")
    llm = LLMClient()
    code = llm.generate(yaml_content)
    print("✓ Code generated")
    
    # Step 5: Safety check
    print("\n[5/6] Running safety check...")
    checker = SafetyChecker()
    result = checker.check(code)
    
    if not result['safe']:
        print(f"✗ Safety check FAILED: {result['issues']}")
        return None
    print("✓ Safety check passed")
    
    # Step 6: Cache and save
    print("\n[6/6] Saving output...")
    
    # Cache the result
    cache.set(yaml_data, code)
    
    # Save to file
    output_dir = Path(GENERATED_DIR)
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / f"{spec.metadata.logic_id}.py"
    with open(output_file, 'w') as f:
        f.write(code)
    
    print(f"✓ Saved to: {output_file}")
    
    # Done
    print(f"\n{'='*50}")
    print("✓ Pipeline complete!")
    print('='*50)
    
    return code


# Entry point
if __name__ == "__main__":
    # Check if file path provided
    if len(sys.argv) < 2:
        print("Usage: python main.py <yaml_file>")
        print("Example: python main.py tests/sample.yaml")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    # Check if file exists
    if not Path(file_path).exists():
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
    
    # Run pipeline
    code = process_yaml(file_path)
    
    if code:
        print("\n--- Generated Code ---\n")
        print(code)