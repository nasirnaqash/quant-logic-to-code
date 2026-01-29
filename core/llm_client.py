import sys
sys.path.append(".")

from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import GEMINI_API_KEY, MODEL_NAME, TEMPERATURE, MAX_TOKENS, PROMPTS_DIR, PROMPT_VERSION


class LLMClient:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=MODEL_NAME,
            google_api_key=GEMINI_API_KEY,
            temperature=TEMPERATURE,
            max_output_tokens=MAX_TOKENS,
        )
        self.prompt_template = self.load_prompt()
    
    def load_prompt(self) -> str:
        """Load prompt template from file"""
        prompt_path = f"{PROMPTS_DIR}/{PROMPT_VERSION}.txt"
        with open(prompt_path, "r") as f:
            return f.read()
    
    def generate(self, yaml_content: str) -> str:
        """Generate Python code from YAML"""
        # Replace placeholder with actual YAML
        prompt = self.prompt_template.replace("{yaml_content}", yaml_content)
        
        # Call Gemini via LangChain
        response = self.llm.invoke(prompt)
        
        # Extract code from response
        code = response.content
        return code


# Test it
if __name__ == "__main__":
    client = LLMClient()
    
    test_yaml = """
metadata:
  schema_version: "1.0"
  module: "scoring"
  logic_id: "test_score"

inputs:
  candidate:
    type: dict
    schema:
      score: float
      sector: string

logic_blocks:
  - id: sector_adjustment
    type: conditional
    input: candidate.sector
    cases:
      technology:
        multiplier: 1.15
      finance:
        multiplier: 1.10
    default:
      multiplier: 1.0
    outputs:
      multiplier: float

outputs:
  multiplier:
    type: float
    source: sector_adjustment.multiplier
"""
    
    print("Generating code...")
    code = client.generate(test_yaml)
    print("\n--- Generated Code ---\n")
    print(code)