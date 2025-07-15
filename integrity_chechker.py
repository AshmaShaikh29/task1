import os
import hashlib
import json

FOLDER_TO_CHECK = "files_to_check"
HASH_DB_FILE = "file_hashes.json"

# 🔐 Generate hash for a file
def generate_file_hash(filepath):
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

# 📦 Scan folder and generate hashes
def scan_and_hash_files(folder):
    hashes = {}
    for root, _, files in os.walk(folder):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_hash = generate_file_hash(filepath)
            relative_path = os.path.relpath(filepath, folder)
            hashes[relative_path] = file_hash
    return hashes

# 💾 Save hashes to file
def save_hashes(hashes, filename):
    with open(filename, "w") as f:
        json.dump(hashes, f, indent=4)

# 📂 Load saved hashes
def load_saved_hashes(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return {}

# ⚖️ Compare old and new hashes
def compare_hashes(old, new):
    changes = {"modified": [], "new": [], "deleted": []}
    for file in new:
        if file not in old:
            changes["new"].append(file)
        elif new[file] != old[file]:
            changes["modified"].append(file)

    for file in old:
        if file not in new:
            changes["deleted"].append(file)

    return changes

# 🚀 Main
def main():
    print("🔍 Scanning for file integrity...")

    old_hashes = load_saved_hashes(HASH_DB_FILE)
    new_hashes = scan_and_hash_files(FOLDER_TO_CHECK)

    changes = compare_hashes(old_hashes, new_hashes)

    if any(changes.values()):
        print("⚠️  Changes detected:")
        for ctype, files in changes.items():
            for f in files:
                print(f"  {ctype.upper()}: {f}")
    else:
        print("✅ All files are intact.")

    # Update saved hashes
    save_hashes(new_hashes, HASH_DB_FILE)

if __name__ == "__main__":
    main()
