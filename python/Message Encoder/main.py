def encode_message(message):
    encoded = ""
    for char in message:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shifted = (ord(char) - base + 3) % 26 + base
            encoded += chr(shifted)
        else:
            encoded += char
    return encoded

def decode_message(message):
    decoded = ""
    for char in message:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shifted = (ord(char) - base - 3) % 26 + base
            decoded += chr(shifted)
        else:
            decoded += char
    return decoded

secret = "I love Python"
encoded = encode_message(secret)
decoded = decode_message(encoded)

print("Original: ", secret)
print("Encoded:  ", encoded)
print("Decoded:  ", decoded)
