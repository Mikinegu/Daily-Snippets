import json
import base64
import os

VAULT_FILE = "vault.json"

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

def add_entry(vault):
    site = input("🔹 Enter Site Name: ").strip()
    user = input("🔹 Enter Username: ").strip()
    pwd = input("🔹 Enter Password: ").strip()

    if not site or not user or not pwd:
        print("❌ Fields cannot be empty!")
        return

    vault[site] = {
        "username": user,
        "password": encode_password(pwd)
    }
    save_vault(vault)
    print(f"✅ Credentials for '{site}' saved.")

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
        print("3. Exit")
        choice = input("Select option (1/2/3): ").strip()

        if choice == '1':
            add_entry(vault)
        elif choice == '2':
            retrieve_entry(vault)
        elif choice == '3':
            print("🔒 Vault closed. Stay safe!")
            break
        else:
            print("❌ Invalid option. Try again.")

if __name__ == "__main__":
    main()
