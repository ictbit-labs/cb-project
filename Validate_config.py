import argparse
import sys
import re

def get_indentation(line):
    """Returns the number of leading spaces."""
    return len(line) - len(line.lstrip(' '))

def find_potential_placeholders(content):
    """Finds words that look like placeholders (Uppercase, A-Z, 0-9, _)."""
    # Matches words with at least 3 uppercase letters/numbers/underscores
    # Examples: ACCOUNT_ID, REGION_1, DB_HOST
    return set(re.findall(r'\b[A-Z][A-Z0-9_]{2,}\b', content))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--template", required=True, help="Path to the original Template file")
    parser.add_argument("--target", required=True, help="Path to the generated Output file")
    args = parser.parse_args()

    # 1. Load Files
    try:
        with open(args.template, 'r') as f:
            template_lines = f.readlines()
        with open(args.target, 'r') as f:
            target_lines = f.readlines()
    except FileNotFoundError as e:
        print(f"❌ Error: File not found - {e}")
        sys.exit(1)

    print(f"🔍 Validating Target: {args.target}")
    errors = []

    # ---------------------------------------------------------
    # CHECK 1: Line Count (Structure)
    # ---------------------------------------------------------
    if len(template_lines) != len(target_lines):
        errors.append(f"Structure Mismatch: Template has {len(template_lines)} lines, but Target has {len(target_lines)}.")
    else:
        # ---------------------------------------------------------
        # CHECK 2: Indentation (YAML Structure)
        # ---------------------------------------------------------
        for i, (temp_line, targ_line) in enumerate(zip(template_lines, target_lines), 1):
            if get_indentation(temp_line) != get_indentation(targ_line):
                errors.append(f"Line {i}: Indentation mismatch. Structure may be broken.")

    # ---------------------------------------------------------
    # CHECK 3: Placeholder Leak (Did we forget to replace something?)
    # ---------------------------------------------------------
    template_content = "".join(template_lines)
    target_content = "".join(target_lines)

    # Find what looks like a placeholder in the Template
    placeholders_in_template = find_potential_placeholders(template_content)
    
    # Check if any of those specific placeholders still exist in the Target
    leaked_placeholders = []
    for ph in placeholders_in_template:
        if ph in target_content:
            leaked_placeholders.append(ph)

    if leaked_placeholders:
        errors.append(f"❌ FAILED: The following placeholders were found in the Target (Not Replaced): {', '.join(leaked_placeholders)}")

    # ---------------------------------------------------------
    # FINAL VERDICT
    # ---------------------------------------------------------
    if errors:
        print("\n".join(errors))
        sys.exit(1) # Fail the Ansible Task
    else:
        print("✅ Validation Passed: Structure matches and no placeholders found.")
        sys.exit(0)

if __name__ == "__main__":
    main()
