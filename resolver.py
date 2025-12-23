import sys
import yaml
import re
import argparse

# Regex to find {{ variable }} pattern
VAR_PATTERN = re.compile(r"\{\{\s*([a-zA-Z0-9_]+)\s*\}\}")

def resolve_value(value, all_data, path=[]):
    """
    Recursively resolves a single string value.
    Handles nested references like A -> B -> C.
    """
    if not isinstance(value, str):
        return value

    matches = VAR_PATTERN.findall(value)
    if not matches:
        return value

    for var_name in matches:
        if var_name in path:
            print(f"❌ Circular dependency detected: {var_name}")
            sys.exit(1)
        
        if var_name not in all_data:
            print(f"❌ Error: Undefined variable '{var_name}' required by '{path[-1] if path else 'root'}'")
            sys.exit(1)

        # Recurse: Get the resolved value of the target variable first
        resolved_target = resolve_value(all_data[var_name], all_data, path + [var_name])
        
        # Replace {{ var_name }} with the actual value
        value = value.replace(f"{{{{ {var_name} }}}}", str(resolved_target))
        value = value.replace(f"{{{{{var_name}}}}}", str(resolved_target)) # Handle no spaces

    return value

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, help="Path to common.yml")
    parser.add_argument("--output", required=True, help="Path to save the resolved JSON/YAML")
    args = parser.parse_args()

    # 1. Load the Raw YAML
    try:
        with open(args.source, 'r') as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        print("Error: Source file not found.")
        sys.exit(1)

    # 2. Resolve every key in the dictionary
    resolved_data = {}
    for k, v in data.items():
        resolved_data[k] = resolve_value(v, data, [k])

    # 3. Save the Clean Data
    with open(args.output, 'w') as f:
        yaml.dump(resolved_data, f, default_flow_style=False)
    
    print(f"✅ Resolved config saved to {args.output}")

if __name__ == "__main__":
    main()
