# Fungsi untuk menyembunyikan pesan dalam teks menggunakan spasi
def hide_message_in_text(cover_text, message):
    # Ubah pesan menjadi biner
    binary_message = ''.join(format(ord(c), '08b') for c in message)
    
    # Pisahkan teks penutup menjadi kata-kata
    words = cover_text.split()
    
    # Pastikan ada cukup celah antar kata untuk menyimpan pesan
    if len(binary_message) > len(words) - 1:
        raise ValueError(f"Teks penutup terlalu pendek! Butuh minimal {len(binary_message) + 1} kata, tersedia {len(words)} kata.")
    
    # Bangun teks dengan spasi sesuai bit pesan
    result = words[0]
    for i in range(len(binary_message)):
        # Tambahkan satu spasi untuk bit 0, dua spasi untuk bit 1
        result += '  ' if binary_message[i] == '1' else ' '
        result += words[i + 1]
    
    # Tambahkan sisa kata jika ada
    for i in range(len(binary_message) + 1, len(words)):
        result += ' ' + words[i]
    
    return result

# Fungsi untuk mengekstrak pesan dari teks
def extract_message_from_text(stego_text):
    # Ambil semua spasi antar kata
    spaces = []
    current_space = ''
    for char in stego_text:
        if char == ' ':
            current_space += char
        else:
            if current_space:
                spaces.append(current_space)
                current_space = ''
    if current_space:
        spaces.append(current_space)
    
    # Ubah spasi menjadi bit (1 spasi = 0, 2 spasi = 1)
    binary_message = ''
    for space in spaces:
        binary_message += '0' if len(space) == 1 else '1'
    
    # Konversi biner ke teks
    message = ''
    for i in range(0, len(binary_message) - 7, 8):
        byte = binary_message[i:i+8]
        message += chr(int(byte, 2))
    
    return message

# Teks penutup
cover_text = (
    "Catur adalah permainan strategi kuno yang dimainkan oleh dua orang pada papan berukuran delapan kali delapan kotak "
    "permainan ini membutuhkan pemikiran mendalam dan perencanaan matang untuk mengalahkan lawan setiap pemain memiliki enam "
    "jenis bidak yaitu raja ratu gajah kuda benteng dan pion yang masing masing memiliki gerakan unik tujuan utama catur adalah "
    "melakukan skakmat yaitu menyerang raja lawan sehingga tidak bisa melarikan diri atau dilindungi catur telah dimainkan selama "
    "berabad abad dan menjadi olahraga intelektual yang populer di seluruh dunia turnamen catur seperti kejuaraan dunia menarik "
    "perhatian jutaan penggemar strategi pembukaan seperti pembukaan Italia atau pertahanan Sisilia sering digunakan untuk mengontrol "
    "pusat papan sejak awal permainan catur juga mengajarkan kesabaran ketelitian kemampuan berpikir kritis serta manajemen waktu "
    "yang sangat bermanfaat dalam kehidupan sehari hari baik untuk anak anak maupun orang dewasa. Selain itu, catur sering dijadikan "
    "media pembelajaran di sekolah untuk meningkatkan logika berpikir. Banyak grandmaster lahir dari latihan yang konsisten dan semangat "
    "pantang menyerah dalam menghadapi tantangan. Permainan ini tidak hanya mengasah otak, tetapi juga membentuk karakter yang kuat dan disiplin."
)

# Pesan yang akan disembunyikan
message = "kelas kriptografi"

# Sembunyikan pesan
stego_text = hide_message_in_text(cover_text, message)
print("Teks dengan pesan tersembunyi:\n", stego_text)

# Ekstrak pesan
extracted_message = extract_message_from_text(stego_text)
print("\nPesan yang diekstrak:", extracted_message)
