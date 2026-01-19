import streamlit as st
import pandas as pd

# ========== FUNGSI-FUNGSI CIPHER ==========

def caesar_cipher(text, shift, mode='encrypt'):
    """
    Fungsi untuk mengenkripsi atau mendekripsi teks menggunakan Caesar Cipher
    """
    result = ""
    
    # Tentukan arah pergeseran berdasarkan mode
    if mode == 'decrypt':
        shift = -shift
    
    for char in text:
        if char.isalpha():
            # Tentukan basis untuk huruf besar/kecil
            ascii_offset = 65 if char.isupper() else 97
            # Lakukan pergeseran
            shifted = (ord(char) - ascii_offset + shift) % 26
            result += chr(shifted + ascii_offset)
        else:
            # Untuk karakter non-alphabet, biarkan tetap
            result += char
    
    return result

def rail_fence_encrypt(text, rails):
    """
    Fungsi untuk mengenkripsi teks menggunakan Rail Fence Cipher
    """
    if rails <= 1:
        return text
    
    # Buat rail (list of lists)
    fence = [[] for _ in range(rails)]
    rail = 0
    direction = 1  # 1 untuk turun, -1 untuk naik
    
    for char in text:
        fence[rail].append(char)
        rail += direction
        
        # Balik arah jika mencapai rail atas atau bawah
        if rail == rails - 1 or rail == 0:
            direction = -direction
    
    # Gabungkan semua rail
    encrypted = ''.join([''.join(rail) for rail in fence])
    return encrypted

def rail_fence_decrypt(text, rails):
    """
    Fungsi untuk mendekripsi teks menggunakan Rail Fence Cipher
    """
    if rails <= 1:
        return text
    
    # Buat pola rail
    fence = [[''] * len(text) for _ in range(rails)]
    rail = 0
    direction = 1
    
    # Tentukan posisi di setiap rail
    for i in range(len(text)):
        fence[rail][i] = '*'
        rail += direction
        
        if rail == rails - 1 or rail == 0:
            direction = -direction
    
    # Isi pola dengan teks terenkripsi
    index = 0
    for r in range(rails):
        for c in range(len(text)):
            if fence[r][c] == '*' and index < len(text):
                fence[r][c] = text[index]
                index += 1
    
    # Baca teks asli
    rail = 0
    direction = 1
    result = []
    
    for i in range(len(text)):
        result.append(fence[rail][i])
        rail += direction
        
        if rail == rails - 1 or rail == 0:
            direction = -direction
    
    return ''.join(result)

# ========== FUNGSI KONVERSI SIMBOL ==========

def text_to_symbols(text):
    """
    Mengonversi teks menjadi simbol berdasarkan tabel
    """
    # Tabel konversi huruf ke simbol
    symbol_map = {
        'A': '●', 'B': '△', 'C': '□', 'D': '▽', 'E': '~ ~',
        'F': '~~~', 'G': '◆', 'H': '♡', 'I': '○', 'J': '- - - -',
        'K': '◆', 'L': '~ ~ ~ ~', 'M': '□', 'N': '▲', 'O': '====',
        'P': '▶', 'Q': '◇', 'R': '◎', 'S': '+', 'T': '+',
        'U': '+', 'V': '☉', 'W': '○', 'X': '×', 'Y': '○', 'Z': '☉☉☉☉'
    }
    
    result = ""
    for char in text.upper():
        if char in symbol_map:
            result += symbol_map[char] + " "
        elif char == " ":
            result += "  "
        else:
            result += char + " "
    
    return result.strip()

def symbols_to_text(symbols):
    """
    Mengonversi simbol kembali menjadi teks
    """
    # Tabel konversi simbol ke huruf
    text_map = {
        '●': 'A', '△': 'B', '□': 'C', '▽': 'D', '~ ~': 'E',
        '~~~': 'F', '◆': 'G', '♡': 'H', '○': 'I', '- - - -': 'J',
        '◆': 'K', '~ ~ ~ ~': 'L', '□': 'M', '▲': 'N', '====': 'O',
        '▶': 'P', '◇': 'Q', '◎': 'R', '+': 'S', '+': 'T',
        '+': 'U', '☉': 'V', '○': 'W', '×': 'X', '○': 'Y', '☉☉☉☉': 'Z'
    }
    
    # Pisahkan simbol (perhatikan bahwa beberapa simbol memiliki spasi)
    symbols_list = symbols.split()
    result = ""
    
    i = 0
    while i < len(symbols_list):
        symbol = symbols_list[i]
        
        # Cek simbol multi-token
        if symbol == '~' and i + 1 < len(symbols_list):
            if symbols_list[i + 1] == '~':
                symbol = '~ ~'
                i += 1
        elif symbol == '~~~':
            # Sudah benar
            pass
        elif symbol == '~' and i + 3 < len(symbols_list):
            if symbols_list[i + 1] == '~' and symbols_list[i + 2] == '~' and symbols_list[i + 3] == '~':
                symbol = '~ ~ ~ ~'
                i += 3
        elif symbol == '-' and i + 3 < len(symbols_list):
            if symbols_list[i + 1] == '-' and symbols_list[i + 2] == '-' and symbols_list[i + 3] == '-':
                symbol = '- - - -'
                i += 3
        elif symbol == '=' and i + 3 < len(symbols_list):
            if symbols_list[i + 1] == '=' and symbols_list[i + 2] == '=' and symbols_list[i + 3] == '=':
                symbol = '===='
                i += 3
        elif symbol == '☉' and i + 3 < len(symbols_list):
            if symbols_list[i + 1] == '☉' and symbols_list[i + 2] == '☉' and symbols_list[i + 3] == '☉':
                symbol = '☉☉☉☉'
                i += 3
        
        if symbol in text_map:
            result += text_map[symbol]
        elif symbol == "":
            result += " "
        else:
            result += symbol
        
        i += 1
    
    return result

# ========== ANTARMUKA STREAMLIT ==========

def main():
    # Konfigurasi halaman
    st.set_page_config(
        page_title="Aplikasi Kriptografi Simbol",
        page_icon="🔐",
        layout="wide"
    )
    
    # Judul aplikasi
    st.title("🔐 Aplikasi Kriptografi dengan Simbol")
    st.markdown("---")
    
    # Sidebar untuk navigasi (hanya 2 menu)
    st.sidebar.title("Navigasi")
    app_mode = st.sidebar.radio(
        "Pilih Menu:",
        ["Caesar Cipher", "Rail Fence Cipher"]
    )
    
    # ========== HALAMAN CAESAR CIPHER ==========
    if app_mode == "Caesar Cipher":
        st.header("Caesar Cipher dengan Simbol")
        
        # Penjelasan singkat
        with st.expander("📖 Tentang Caesar Cipher"):
            st.markdown("""
            **Caesar Cipher** adalah teknik kriptografi kuno yang menggeser setiap huruf.
            
            **Hasil akan dikonversi menjadi simbol:**
            - A → ● (Kota Besar)
            - B → △ (Gunung Non Aktif)
            - C → □ (Dataran Rendah)
            - ... dan seterusnya
            """)
        
        # Input pengguna
        col1, col2 = st.columns(2)
        
        with col1:
            text_input = st.text_area("Masukkan teks:", height=100, 
                                      placeholder="Masukkan teks di sini...", key="caesar_input")
            show_original = st.checkbox("Tampilkan teks asli", value=True)
        
        with col2:
            mode = st.radio("Pilih mode:", ["Enkripsi", "Dekripsi"])
            shift_key = st.slider("Pilih key (nilai pergeseran):", 
                                 min_value=1, max_value=25, value=3)
            
            convert_symbols = st.checkbox("Konversi hasil ke simbol", value=True)
            
            if st.button("🚀 Proses Caesar Cipher", use_container_width=True):
                if text_input:
                    if mode == "Enkripsi":
                        # Proses Caesar Cipher
                        caesar_result = caesar_cipher(text_input, shift_key, 'encrypt')
                        
                        # Konversi ke simbol jika dipilih
                        if convert_symbols:
                            final_result = text_to_symbols(caesar_result)
                        else:
                            final_result = caesar_result
                        
                        st.success("✅ Enkripsi Berhasil!")
                    else:
                        # Untuk dekripsi, pertama konversi dari simbol jika perlu
                        if convert_symbols:
                            # Coba konversi dari simbol ke teks
                            try:
                                text_from_symbols = symbols_to_text(text_input)
                                final_result = caesar_cipher(text_from_symbols, shift_key, 'decrypt')
                            except:
                                st.error("Gagal mengonversi simbol. Pastikan format simbol benar.")
                                return
                        else:
                            final_result = caesar_cipher(text_input, shift_key, 'decrypt')
                        
                        st.success("✅ Dekripsi Berhasil!")
                    
                    # Tampilkan hasil
                    col_result1, col_result2 = st.columns(2)
                    
                    with col_result1:
                        st.subheader("Hasil:")
                        st.code(final_result, language="text")
                    
                    with col_result2:
                        if show_original and mode == "Enkripsi":
                            st.subheader("Teks Asli:")
                            st.info(text_input)
                        
                        if convert_symbols:
                            st.subheader("Keterangan:")
                            st.caption("Hasil telah dikonversi ke dalam bentuk simbol")
                    
                    # Tampilkan tabel simbol kecil
                    with st.expander("📋 Tabel Simbol Referensi"):
                        symbols_data = {
                            'Huruf': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'],
                            'Simbol': ['●', '△', '□', '▽', '~ ~', '~~~', '◆', '♡', '○', '- - - -', '◆'],
                            'Deskripsi': ['Kota Besar', 'Gunung Non Aktif', 'Dataran Rendah', 'Lembah', 
                                         'Sungai', 'Jalan Raya', 'Hutan', 'Pelabuhan', 'Danau', 
                                         'Rel Kereta Api', 'Pertambangan']
                        }
                        
                        symbols_data2 = {
                            'Huruf': ['L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V'],
                            'Simbol': ['~ ~ ~ ~', '□', '▲', '====', '▶', '◇', '◎', '+', '+', '+', '☉'],
                            'Deskripsi': ['Pantai', 'Pemukiman', 'Gunung Aktif', 'Batas Negara', 
                                         'Bendungan', 'Air Terjun', 'Rawa', 'Rumah Sakit', 
                                         'Bandara', 'Tempat Ibadah', 'Kantor Pos']
                        }
                        
                        symbols_data3 = {
                            'Huruf': ['W', 'X', 'Y', 'Z'],
                            'Simbol': ['○', '×', '○', '☉☉☉☉'],
                            'Deskripsi': ['Sumur', 'Daerah Berbahaya', 'Ibu Kota Negara', 'Laut']
                        }
                        
                        col_t1, col_t2, col_t3 = st.columns(3)
                        with col_t1:
                            st.dataframe(pd.DataFrame(symbols_data), hide_index=True, use_container_width=True)
                        with col_t2:
                            st.dataframe(pd.DataFrame(symbols_data2), hide_index=True, use_container_width=True)
                        with col_t3:
                            st.dataframe(pd.DataFrame(symbols_data3), hide_index=True, use_container_width=True)
                
                else:
                    st.warning("⚠️ Silakan masukkan teks terlebih dahulu!")
        
        # Contoh
        with st.expander("📋 Contoh Caesar Cipher dengan Simbol"):
            example_text = "HELLO"
            example_encrypted = caesar_cipher(example_text, 3, 'encrypt')
            example_symbols = text_to_symbols(example_encrypted)
            
            st.write(f"**Plaintext:** {example_text}")
            st.write(f"**Key:** 3")
            st.write(f"**Ciphertext (huruf):** {example_encrypted}")
            st.write(f"**Ciphertext (simbol):** {example_symbols}")
            st.write(f"**Dekripsi kembali:** {caesar_cipher(example_encrypted, 3, 'decrypt')}")
    
    # ========== HALAMAN RAIL FENCE CIPHER ==========
    elif app_mode == "Rail Fence Cipher":
        st.header("Rail Fence Cipher dengan Simbol")
        
        # Penjelasan singkat
        with st.expander("📖 Tentang Rail Fence Cipher"):
            st.markdown("""
            **Rail Fence Cipher** menulis teks dalam pola zig-zag di beberapa "rail".
            
            **Hasil akan dikonversi menjadi simbol:**
            - Setiap huruf hasil enkripsi diubah ke simbol sesuai tabel
            - Contoh: A → ●, B → △, dst.
            """)
        
        # Input pengguna
        col1, col2 = st.columns(2)
        
        with col1:
            rf_text_input = st.text_area("Masukkan teks:", height=100, 
                                         placeholder="Masukkan teks di sini...", key="rf_input")
            show_original_rf = st.checkbox("Tampilkan teks asli", value=True, key="rf_original")
        
        with col2:
            rf_mode = st.radio("Pilih mode:", ["Enkripsi", "Dekripsi"], key="rf_mode")
            num_rails = st.slider("Pilih jumlah rail:", 
                                 min_value=2, max_value=10, value=3, key="rf_rails")
            
            convert_symbols_rf = st.checkbox("Konversi hasil ke simbol", value=True, key="rf_symbols")
            
            if st.button("🚀 Proses Rail Fence Cipher", use_container_width=True, key="rf_button"):
                if rf_text_input:
                    if rf_mode == "Enkripsi":
                        # Proses Rail Fence Cipher
                        rf_result = rail_fence_encrypt(rf_text_input.upper(), num_rails)
                        
                        # Konversi ke simbol jika dipilih
                        if convert_symbols_rf:
                            final_result = text_to_symbols(rf_result)
                        else:
                            final_result = rf_result
                        
                        st.success("✅ Enkripsi Berhasil!")
                    else:
                        # Untuk dekripsi
                        if convert_symbols_rf:
                            # Coba konversi dari simbol ke teks
                            try:
                                text_from_symbols = symbols_to_text(rf_text_input)
                                final_result = rail_fence_decrypt(text_from_symbols, num_rails)
                            except:
                                st.error("Gagal mengonversi simbol. Pastikan format simbol benar.")
                                return
                        else:
                            final_result = rail_fence_decrypt(rf_text_input, num_rails)
                        
                        st.success("✅ Dekripsi Berhasil!")
                    
                    # Tampilkan hasil
                    col_result1, col_result2 = st.columns(2)
                    
                    with col_result1:
                        st.subheader("Hasil:")
                        st.code(final_result, language="text")
                    
                    with col_result2:
                        if show_original_rf and rf_mode == "Enkripsi":
                            st.subheader("Teks Asli:")
                            st.info(rf_text_input)
                        
                        if convert_symbols_rf:
                            st.subheader("Keterangan:")
                            st.caption("Hasil telah dikonversi ke dalam bentuk simbol")
                            
                            # Tampilkan pola rail
                            if rf_mode == "Enkripsi" and len(rf_text_input) <= 30:
                                st.subheader("Pola Rail:")
                                rails_display = []
                                for i in range(num_rails):
                                    rails_display.append([])
                                
                                rail_idx = 0
                                direction = 1
                                for char in rf_text_input.upper():
                                    for j in range(num_rails):
                                        if j == rail_idx:
                                            rails_display[j].append(char)
                                        else:
                                            rails_display[j].append(".")
                                    rail_idx += direction
                                    if rail_idx == 0 or rail_idx == num_rails - 1:
                                        direction = -direction
                                
                                for i in range(num_rails):
                                    st.text(f"Rail {i+1}: {' '.join(rails_display[i])}")
                
                else:
                    st.warning("⚠️ Silakan masukkan teks terlebih dahulu!")
        
        # Contoh
        with st.expander("📋 Contoh Rail Fence Cipher dengan Simbol"):
            example_text = "RAILFENCE"
            example_encrypted = rail_fence_encrypt(example_text, 3)
            example_symbols = text_to_symbols(example_encrypted)
            
            st.write(f"**Plaintext:** {example_text}")
            st.write(f"**Jumlah rail:** 3")
            st.write(f"**Ciphertext (huruf):** {example_encrypted}")
            st.write(f"**Ciphertext (simbol):** {example_symbols}")
            st.write(f"**Dekripsi kembali:** {rail_fence_decrypt(example_encrypted, 3)}")

# ========== MENJALANKAN APLIKASI ==========
if __name__ == "__main__":
    main()
