import os
import hashlib
import json

# 🔧 Yeh folder monitor hoga
FOLDER_TO_MONITOR = "files_to_monitor"
HASH_DB_FILE = "file_hashes.json"

# 🔐 File ka hash nikalta hai
def get_file_hash(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

# 📂 Folder ke sabhi files scan karta hai
def scan_files(directory):
    file_hashes = {}
    for root, _, files in os.walk(directory):
        for name in files:
            full_path = os.path.join(root, name)
            try:
                file_hashes[full_path] = get_file_hash(full_path)
            except Exception as e:
                print(f"Error hashing {full_path}: {e}")
    return file_hashes

# 💾 Hash data JSON file me save karta hai
def save_hash_db(hashes):
    with open(HASH_DB_FILE, 'w') as f:
        json.dump(hashes, f, indent=4)

# 📤 JSON file se hash data load karta hai
def load_hash_db():
    if not os.path.exists(HASH_DB_FILE):
        return {}
    with open(HASH_DB_FILE, 'r') as f:
        return json.load(f)

# 🔄 Changes compare karta hai purane aur naye hash me
def compare_hashes(old_hashes, new_hashes):
    changes = {
        "new": [],
        "modified": [],
        "deleted": []
    }

    old_files = set(old_hashes.keys())
    new_files = set(new_hashes.keys())

    for file in new_files:
        if file not in old_hashes:
            changes["new"].append(file)
        elif old_hashes[file] != new_hashes[file]:
            changes["modified"].append(file)

    for file in old_files - new_files:
        changes["deleted"].append(file)

    return changes

# 📝 Changes ko log file me save karta hai
def save_changes_to_log(changes):
    with open("change_log.txt", "a") as log_file:
        log_file.write("\n=== Change Detected ===\n")
        for change_type, files in changes.items():
            for file in files:
                log_file.write(f"{change_type.upper()}: {file}\n")

# 🧠 Main function
def main():
    print("🔍 Scanning folder for changes...")

    old_hashes = load_hash_db()
    new_hashes = scan_files(FOLDER_TO_MONITOR)
    changes = compare_hashes(old_hashes, new_hashes)

    if any(changes.values()):
        print("⚠️ Changes detected:")
        for change_type, files in changes.items():
            for file in files:
                print(f"{change_type.upper()}: {file}")
        save_changes_to_log(changes)
    else:
        print("✅ No changes found.")

    save_hash_db(new_hashes)

# 🏁 Run the program
if __name__ == "__main__":
    main()
