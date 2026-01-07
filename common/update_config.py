import sys
import argparse
import json
import os
from ruamel.yaml import YAML

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True, help="Path to common.yml")
    parser.add_argument("--data", required=True, help="JSON string of Key-Values to update")
    args = parser.parse_args()

    # 1. Parse Data
    try:
        updates = json.loads(args.data)
    except json.JSONDecodeError as e:
        print(f"❌ JSON Error: {e}")
        sys.exit(1)

    # 2. Setup YAML Loader (Preserves comments)
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.default_flow_style = False

    # 3. Read File
    if not os.path.exists(args.target):
        print(f"❌ File not found: {args.target}")
        sys.exit(1)

    with open(args.target, 'r') as f:
        code = yaml.load(f) or {}

    # 4. Update Values
    print(f"📝 Updating {args.target}...")
    for key, value in updates.items():
        if key in code and code[key] != value:
            print(f"   🔄 Updating: {key} -> {value}")
            code[key] = value
        elif key not in code:
            print(f"   ➕ Adding: {key} -> {value}")
            code[key] = value

    # 5. Save
    with open(args.target, 'w') as f:
        yaml.dump(code, f)
    
    print("✅ Success.")

if __name__ == "__main__":
    main()
