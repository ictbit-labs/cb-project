import argparse
import sys
import yaml # Requires PyYAML

def flatten_dictionary(d):
    """
    Recursively flattens a nested dictionary.
    Keys are just the last part (e.g., 'account_id' not 'aws.accounts.account_id').
    """
    items = []
    for k, v in d.items():
        if isinstance(v, dict):
            items.extend(flatten_dictionary(v).items())
        else:
            items.append((k, v))
    return dict(items)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, help="Path to the Source YAML (vars)")
    parser.add_argument("--template", required=True, help="Path to the Template file")
    parser.add_argument("--target", required=True, help="Path to the Output file")
    args = parser.parse_args()

    # 1. Load Source Data
    try:
        with open(args.source, 'r') as f:
            source_data = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Source file {args.source} not found.")
        sys.exit(1)

    flat_values = flatten_dictionary(source_data)

    # 2. Read Template File (Raw Text)
    try:
        with open(args.template, 'r') as f:
            file_content = f.read()
    except FileNotFoundError:
        print(f"Error: Template file {args.template} not found.")
        sys.exit(1)

    # 3. Perform Replacement (The 'Curly Brace' Update)
    replacement_count = 0
    
    for key, value in flat_values.items():
        # OLD LOGIC: placeholder = key.upper()
        # NEW LOGIC: Wrap uppercase key in {{ }}
        placeholder = "{{" + key.upper() + "}}"
        
        if placeholder in file_content:
            file_content = file_content.replace(placeholder, str(value))
            replacement_count += 1
            # Optional: Print what we swapped (Good for debugging)
            # print(f"Swapped {placeholder} -> {value}")

    # 4. Write Output File
    with open(args.target, 'w') as f:
        f.write(file_content)

    print(f"✅ Generated {args.target} with {replacement_count} replacements.")

if __name__ == "__main__":
    main()
