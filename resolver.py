import sys
import yaml
import re
import argparse

# Regex to find {{ variable }} or {{ variable.subvar }}
# Now supports dots (.) for nested keys like aws.region
VAR_PATTERN = re.compile(r"\{\{\s*([a-zA-Z0-9_.]+)\s*\}\}")

def get_nested_value(data, key_path):
    """
    Finds a value in a nested dictionary using 'one.two.three' notation.
    """
    keys = key_path.split('.')
    current = data
    try:
        for k in keys:
            current = current[k]
        return current
    except (KeyError, TypeError):
        return None

def resolve_item(item, root_data, path_tracker=None):
    """
    Recursively walks through Dicts, Lists, and Strings to resolve {{ vars }}.
    """
    if path_tracker is None:
        path_tracker = []

    # 1. Handle Dictionary
    if isinstance(item, dict):
        return {k: resolve_item(v, root_data, path_tracker) for k, v in item.items()}
    
    # 2. Handle List
    if isinstance(item, list):
        return [resolve_item(i, root_data, path_tracker) for i in item]

    # 3. Handle String (The Logic)
    if isinstance(item, str):
        if "{{" not in item:
            return item
        
        # Find all matches in this specific string
        matches = VAR_PATTERN.findall(item)
        for var_name in matches:
            # Prevent infinite loops (Circular Dependency)
            if var_name in path_tracker:
                print(f"❌ Circular dependency detected: {var_name}")
                sys.exit(1)

            # Find the value of the variable we are looking for
            raw_val = get_nested_value(root_data, var_name)
            
            if raw_val is None:
                # If we can't find it, leave it alone (or error out)
                # print(f"⚠️ Warning: Could not resolve variable '{var_name}'")
                continue
            
            # RECURSION: Resolve the *found* value before using it
            # (In case 'region2' points to 'region1', which points to 'us-east-1')
            resolved_val = resolve_item(raw_val, root_data, path_tracker + [var_name])

            # PERFORM REPLACE
            # If the string is EXACTLY "{{ var }}", replace it with the type-safe value (int, list, etc.)
            if item.strip() == f"{{{{ {var_name} }}}}" or item.strip() == f"{{{{{var_name}}}}}":
                return resolved_val
            
            # Otherwise, do a string replacement (Result is always a string)
            item = item.replace(f"{{{{ {var_name} }}}}", str(resolved_val))
            item = item.replace(f"{{{{{var_name}}}}}", str(resolved_val))
            
        return item

    # 4. Handle Int, Float, Boolean, etc.
    return item

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, help="Path to common.yml")
    parser.add_argument("--output", required=True, help="Path to save the resolved file")
    args = parser.parse_args()

    # Load YAML
    try:
        with open(args.source, 'r') as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        print("Error: Source file not found.")
        sys.exit(1)

    # Start the Recursive Resolution
    resolved_data = resolve_item(data, data)

    # Save Output
    with open(args.output, 'w') as f:
        yaml.dump(resolved_data, f, default_flow_style=False, sort_keys=False)
    
    print(f"✅ Resolved config saved to {args.output}")

if __name__ == "__main__":
    main()

