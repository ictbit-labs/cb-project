import argparse
import sys
import yaml # Requires PyYAML

def flatten_keys(d):
    """
    Recursively finds all keys in the source dictionary.
    Returns a list of UPPERCASE keys (the expected placeholders).
    """
    keys = []
    for k, v in d.items():
        keys.append(k.upper()) # Add the key itself (e.g. ACCOUNT_ID)
        if isinstance(v, dict):
            keys.extend(flatten_keys(v)) # Dig deeper
    return keys

def get_indentation(line):
    """Returns the number of leading spaces."""
    return len(line) - len(line.lstrip(' '))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, help="Path to the Source YAML (vars)")
    parser.add_argument("--template", required=True, help="Path to the Template file")
    parser.add_argument("--target", required=True, help="Path to the generated Target file")
    args = parser.parse_args()

    errors = []

    # 1. Load Files
    try:
        with open(args.source, 'r') as f:
            source_data = yaml.safe_load(f)
        
        with open(args.template, 'r') as f:
            template_lines = f.readlines()
            
        with open(args.target, 'r') as f:
            target_lines = f.readlines()
    except FileNotFoundError as e:
        print(f"❌ Error: File not found - {e}")
        sys.exit(1)

    # ---------------------------------------------------------
    # CHECK 1: Structure (Line Count & Indentation)
    # ---------------------------------------------------------
    # This ensures we didn't accidentally delete lines or break YAML nesting
    if len(template_lines) != len(target_lines):
        errors.append(f"Structure Mismatch: Template has {len(template_lines)} lines, but Target has {len(target_lines)}.")
    else:
        for i, (temp_line, targ_line) in enumerate(zip(template_lines, target_lines), 1):
            if get_indentation(temp_line) != get_indentation(targ_line):
                errors.append(f"Line {i}: Indentation mismatch. YAML structure may be broken.")

    # ---------------------------------------------------------
    # CHECK 2: Placeholder Leaks (Source-Driven)
    # ---------------------------------------------------------
    # Only check for keys that actually exist in your source file
    expected_placeholders = flatten_keys(source_data)
    
    target_content = "".join(target_lines)
    
    found_leaks = []
    for placeholder in expected_placeholders:
        # Check if the specific placeholder (e.g. MGMT_ACCOUNT_ID) exists in the target
        if placeholder in target_content:
            found_leaks.append(placeholder)

    if found_leaks:
        errors.append(f"❌ FAILED: The following placeholders were NOT replaced: {', '.join(found_leaks)}")

    # ---------------------------------------------------------
    # FINAL VERDICT
    # ---------------------------------------------------------
    if errors:
        print("\n".join(errors))
        sys.exit(1) # Fail the Ansible Task
    else:
        print("✅ Validation Passed: Structure matches and no known placeholders found.")
        sys.exit(0)

if __name__ == "__main__":
    main()
