import yaml
import sys
import argparse

def flatten_dictionary(d):
    """Turns nested dictionary into flat key-value pairs."""
    items = []
    for k, v in d.items():
        if isinstance(v, dict):
            items.extend(flatten_dictionary(v).items())
        else:
            items.append((k, v))
    return dict(items)

def main():
    # 1. Setup Argument Parser
    parser = argparse.ArgumentParser(description="Replace placeholders in target file with values from source YAML.")
    
    # Define the arguments we expect
    parser.add_argument("--source", required=True, help="Path to the Source YAML file")
    parser.add_argument("--target", required=True, help="Path to the Target template file")
    parser.add_argument("--output", required=True, help="Path to save the Result file")
    
    args = parser.parse_args()

    # 2. Load Source Data
    print(f"Reading source: {args.source}")
    try:
        with open(args.source, 'r') as f:
            source_data = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Source file '{args.source}' not found.")
        sys.exit(1)

    flat_values = flatten_dictionary(source_data)

    # 3. Read Target File
    print(f"Reading target: {args.target}")
    try:
        with open(args.target, 'r') as f:
            file_content = f.read()
    except FileNotFoundError:
        print(f"Error: Target file '{args.target}' not found.")
        sys.exit(1)

    # 4. Perform Replacement
    print("Processing replacements...")
    for key, value in flat_values.items():
        placeholder = key.upper()
        if placeholder in file_content:
            file_content = file_content.replace(placeholder, str(value))
    
    # 5. Save Output
    with open(args.output, 'w') as f:
        f.write(file_content)
    
    print(f"Success! Saved to {args.output}")

if __name__ == "__main__":
    main()

