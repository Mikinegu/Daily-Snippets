import qrcode

# Example student list (later we can load from CSV)
students = {
    "FSP2025001": "John Doe",
    "FSP2025002": "Jane Smith",
    "FSP2025003": "Michael Lee"
}

for sid, name in students.items():
    data = f"{sid}|{name}"
    img = qrcode.make(data)
    pil_img = img.get_image()  # Convert to PIL Image
    pil_img.save(f"qrcodes/{sid}.png")  # Save to qrcodes folder
    print(f"Generated QR for {name}")
