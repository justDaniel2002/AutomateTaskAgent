import json
from pathlib import Path

RULES_PATH = Path(__file__).resolve().parents[2] / "data" / "rules.json"

with RULES_PATH.open(encoding="utf-8") as file:
    rules = json.load(file)

# print(f"Loaded rules from {RULES_PATH}: {rules['commons']}")