import argparse
import sys
import yaml # Requires PyYAML
import os

# ANSI Colors for better readability in Ansible output
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def compare_dicts(new_data, existing_data, path="root"):
    """
    Recursively compares two dictionaries/lists to find gaps.
    Returns a list of specific gap descriptions.
    """
    gaps = []

    # 1. Check for keys present in NEW but missing in EXISTING (New Feature)
    if isinstance(new_data, dict) and isinstance(existing_data, dict):
        for key in new_data:
            current_path = f"{path}.{key}"
            
            if key not in existing_data:
                gaps.append(f"{GREEN}[+] NEW CONFIG:{RESET} '{current_path}' will be added (Value: {new_data[key]})")
                continue
            
            # Recurse if both are dicts
            if isinstance(new_data[key], dict) and isinstance(existing_data[key], dict):
                gaps.extend(compare_dicts(new_data[key], existing_data[key], current_path))
            
            # Check for Value Mismatch (The Gap)
            elif new_data[key] != existing_data[key]:
                gaps.append(f"{RED}[!] VALUE MISMATCH:{RESET} '{current_path}'\n    - Current (Target): {existing_data[key]}\n    - New (Source):     {new_data[key]}")

        # 2. Check for keys present in EXISTING but missing in NEW (Deletion)
        for key in existing_data:
            if key not in new_data:
                gaps.append(f"{YELLOW}[-] REMOVED CONFIG:{RESET} '{path}.{key}' exists in Target but missing in Source.")

    # 3. List Comparison (Simple strict check)
    elif isinstance(new_data, list) and isinstance(existing_data, list):
        if new_data != existing_data:
             gaps.append(f"{RED}[!] LIST CHANGE:{RESET} '{path}'\n    - Current: {existing_data}\n    - New:     {new_data}")
    
    return gaps

def main():
    parser = argparse.ArgumentParser()
    # "Source" = The New Candidate File you just generated
    parser.add_argument("--source", required=True, help="Path to the New Candidate file")
    # "Target" = The Existing File on disk
    parser.add_argument("--target", required=True, help="Path to the Existing Target file")
    args = parser.parse_args()

    # 1. Load Source (Candidate)
    try:
        with open(args.source, 'r') as f:
            source_data = yaml.safe_load(f) or {}
    except FileNotFoundError:
        print(f"❌ Error: Source file '{args.source}' not found.")
        sys.exit(1)

    # 2. Load Target (Existing)
    if not os.path.exists(args.target):
        print(f"{GREEN}ℹ️ Target file does not exist yet. This is a fresh deployment (No gaps).{RESET}")
        sys.exit(0)

    try:
        with open(args.target, 'r') as f:
            target_data = yaml.safe_load(f) or {}
    except Exception as e:
        print(f"⚠️ Warning: Existing target file is corrupt or empty. Treating as fresh.")
        target_data = {}

    # 3. Run Comparison
    print(f"🔍 Checking gaps between Source (New) and Target (Existing)...")
    gaps = compare_dicts(source_data, target_data)

    # 4. Final Verdict
    if gaps:
        print(f"\n{YELLOW}⚠️  GAPS DETECTED ({len(gaps)} differences):{RESET}")
        print("---------------------------------------------------")
        for gap in gaps:
            print(gap)
        print("---------------------------------------------------")
        print(f"{RED}❌ Validation Failed: There are gaps between the new configuration and the existing one.{RESET}")
        sys.exit(1) # Fail the pipeline so you can review
    else:
        print(f"{GREEN}✅ No Gaps Found: Source and Target are identical.{RESET}")
        sys.exit(0)

if __name__ == "__main__":
    main()
