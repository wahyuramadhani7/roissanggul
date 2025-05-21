from PIL import Image

# Fungsi untuk menyembunyikan pesan dalam gambar
def hide_message(image_path, message, output_path):
    img = Image.open(image_path)
    img = img.convert('RGB')
    pixels = img.load()

    # Ubah pesan menjadi biner + penanda akhir
    binary_message = ''.join(format(ord(c), '08b') for c in message)
    binary_message += '11111111'  # Penanda akhir pesan

    width, height = img.size
    if len(binary_message) > width * height * 3:
        raise ValueError("Pesan terlalu panjang untuk gambar ini!")

    data_index = 0
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            rgb = [r, g, b]
            for i in range(3):
                if data_index < len(binary_message):
                    rgb[i] = (rgb[i] & ~1) | int(binary_message[data_index])
                    data_index += 1
            pixels[x, y] = tuple(rgb)

            if data_index >= len(binary_message):
                break
        if data_index >= len(binary_message):
            break

    img.save(output_path)
    print(f"✅ Pesan berhasil disisipkan ke dalam '{output_path}'.")

# Fungsi untuk mengekstrak pesan dari gambar
def extract_message(image_path):
    img = Image.open(image_path)
    img = img.convert('RGB')
    pixels = img.load()

    width, height = img.size
    binary_message = ""

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            for color in (r, g, b):
                binary_message += str(color & 1)
                if binary_message[-8:] == '11111111':
                    binary_message = binary_message[:-8]  # Hapus penanda akhir
                    message = ""
                    for i in range(0, len(binary_message), 8):
                        byte = binary_message[i:i+8]
                        message += chr(int(byte, 2))
                    return message
    return "❌ Tidak ditemukan pesan."

# Penggunaan
image_path = "input.png" 
message = "hello ini pesan rahasia dari kelompok verry dan fin"
output_path = "output.png"

# Sembunyikan pesan
hide_message(image_path, message, output_path)

# Ekstrak pesan
extracted_message = extract_message(output_path)
print(f"📤 Pesan yang diekstrak: {extracted_message}")
