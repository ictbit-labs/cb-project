import yaml
import sys

# --- CONFIGURATION ---
SOURCE_FILE = 'source.yml'
TARGET_FILE = 'target.yml'
OUTPUT_FILE = 'final_config.yml'
# ---------------------

def flatten_dictionary(d, parent_key='', sep='_'):
    """
    Turns a nested dictionary into a flat one.
    Example: 
       {'aws': {'account': {'id': 123}}} 
    Becomes:
       {'id': 123}  (We keep the 'leaf' key name)
    """
    items = []
    for k, v in d.items():
        # If the value is another dictionary, dig deeper (recursion)
        if isinstance(v, dict):
            items.extend(flatten_dictionary(v, k, sep=sep).items())
        else:
            # We found a value! Add it to our list.
            # We only use the key 'k' (e.g., 'mgmt_account_id')
            # ignoring the parent folders to match your placeholder style.
            items.append((k, v))
    return dict(items)

def main():
    # 1. Load the Source YAML
    with open(SOURCE_FILE, 'r') as f:
        source_data = yaml.safe_load(f)

    # 2. Flatten the source data
    # This grabs EVERY key/value pair from the file, no matter the depth.
    flat_values = flatten_dictionary(source_data)
    
    print(f"--- Found {len(flat_values)} variables in source file ---")

    # 3. Read Target as Raw Text
    with open(TARGET_FILE, 'r') as f:
        file_content = f.read()

    # 4. Replace Everything
    for key, value in flat_values.items():
        # Convert key to placeholder (mgmt_account_id -> MGMT_ACCOUNT_ID)
        placeholder = key.upper()
        
        if placeholder in file_content:
            print(f"✅ Replacing {placeholder} -> {value}")
            file_content = file_content.replace(placeholder, str(value))
        
    # 5. Save
    with open(OUTPUT_FILE, 'w') as f:
        f.write(file_content)
    print(f"--- Saved to {OUTPUT_FILE} ---")

if __name__ == "__main__":
    main()
