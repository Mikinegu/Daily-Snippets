import json
import base64
import os
import random
import string

VAULT_FILE = "vault.json"

def generate_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

def load_vault():
    if os.path.exists(VAULT_FILE):
        with open(VAULT_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_vault(data):
    with open(VAULT_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def encode_password(password):
    return base64.b64encode(password.encode()).decode()

def decode_password(encoded):
    try:
        return base64.b64decode(encoded.encode()).decode()
    except:
        return "[Decoding Failed]"

def password_strength(password):
    length = len(password)
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)
    score = sum([has_lower, has_upper, has_digit, has_special])
    if length >= 12 and score == 4:
        return "Strong"
    elif length >= 8 and score >= 3:
        return "Medium"
    else:
        return "Weak"

def add_entry(vault):
    site = input("🔹 Enter Site Name: ").strip()
    user = input("🔹 Enter Username: ").strip()
    print("1. Enter password manually")
    print("2. Generate strong password")
    pwd_choice = input("Select option (1/2): ").strip()
    if pwd_choice == '2':
        try:
            length = int(input("Enter password length (default 12): ").strip() or "12")
        except ValueError:
            length = 12
        pwd = generate_password(length)
        print(f"🔑 Generated Password: {pwd}")
    else:
        pwd = input(" Enter Password: ").strip()

    print(f"Password Strength: {password_strength(pwd)}")

    if not site or not user or not pwd:
        print("❌ Fields cannot be empty!")
        return

    vault[site] = {
        "username": user,
        "password": encode_password(pwd)
    }
    save_vault(vault)
    print(f"✅ Credentials for '{site}' saved.")

def update_entry(vault):
    site = input("✏️ Enter Site Name to Update: ").strip()
    if site not in vault:
        print("❌ No credentials found for that site.")
        return
    entry = vault[site]
    print(f"Current Username: {entry['username']}")
    new_user = input("Enter new username (leave blank to keep current): ").strip()
    print("1. Keep current password")
    print("2. Enter new password")
    print("3. Generate new password")
    pwd_choice = input("Select option (1/2/3): ").strip()
    if pwd_choice == '2':
        new_pwd = input("Enter new password: ").strip()
    elif pwd_choice == '3':
        try:
            length = int(input("Enter password length (default 12): ").strip() or "12")
        except ValueError:
            length = 12
        new_pwd = generate_password(length)
        print(f"🔑 Generated Password: {new_pwd}")
    else:
        new_pwd = decode_password(entry['password'])
    print(f"Password Strength: {password_strength(new_pwd)}")
    vault[site] = {
        "username": new_user if new_user else entry['username'],
        "password": encode_password(new_pwd)
    }
    save_vault(vault)
    print(f"✅ Credentials for '{site}' updated.")

def delete_entry(vault):
    site = input("🗑️ Enter Site Name to Delete: ").strip()
    if site in vault:
        confirm = input(f"Are you sure you want to delete credentials for '{site}'? (y/n): ").strip().lower()
        if confirm == 'y':
            del vault[site]
            save_vault(vault)
            print(f"✅ Credentials for '{site}' deleted.")
        else:
            print("❌ Deletion cancelled.")
    else:
        print("❌ No credentials found for that site.")

def search_entries(vault):
    query = input("🔎 Enter search term (site or username): ").strip().lower()
    if not query:
        print("❌ Search term cannot be empty!")
        return
    found = False
    for site, entry in vault.items():
        if query in site.lower() or query in entry["username"].lower():
            print(f"\nSite: {site}")
            print(f"👤 Username: {entry['username']}")
            print(f"🔑 Password: {decode_password(entry['password'])}")
            found = True
    if not found:
        print("❌ No matching entries found.")

def retrieve_entry(vault):
    site = input("🔍 Enter Site Name to Retrieve: ").strip()
    if site in vault:
        entry = vault[site]
        print(f"👤 Username: {entry['username']}")
        print(f"🔑 Password: {decode_password(entry['password'])}")
    else:
        print("❌ No credentials found for that site.")

def main():
    print("🔐 Welcome to Simple Password Vault 🔐")
    vault = load_vault()

    while True:
        print("\n--- Menu ---")
        print("1. Add New Entry")
        print("2. Retrieve Entry")
        print("3. Generate Password")
        print("4. Search Entries")
        print("5. Update Entry")
        print("6. Delete Entry")
        print("5. Exit")
        choice = input("Select option (1/2/3/4/5/6/7): ").strip()

        if choice == '1':
            add_entry(vault)
        elif choice == '2':
            retrieve_entry(vault)
        elif choice == '3':
            try:
                length = int(input("Enter password length (default 12): ").strip() or "12")
            except ValueError:
                length = 12
            pwd = generate_password(length)
            print(f"🔑 Generated Password: {pwd}")
        elif choice == '4':
            search_entries(vault)
        elif choice == '5':
            update_entry(vault)
        elif choice == '6':
            delete_entry(vault)
        elif choice == '7':
            print("🔒 Vault closed. Stay safe!")
            break
        else:
            print("❌ Invalid option. Try again.")

if __name__ == "__main__":
    main()
