# Read the prompt
with open("prompts/v1.0.txt", "r") as f:
    prompt = f.read()

print("Prompt loaded successfully!")
print(f"Length: {len(prompt)} characters")