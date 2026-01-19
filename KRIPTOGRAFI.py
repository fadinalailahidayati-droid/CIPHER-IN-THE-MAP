import streamlit as st

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

# ========== FUNGSI KOMBINASI CIPHER ==========

def encrypt_combination(text, caesar_shift, rail_rails):
    """
    Melakukan enkripsi kombinasi: Caesar Cipher kemudian Rail Fence Cipher
    """
    # Langkah 1: Caesar Cipher
    caesar_result = caesar_cipher(text.upper(), caesar_shift, 'encrypt')
    
    # Langkah 2: Rail Fence Cipher
    rail_result = rail_fence_encrypt(caesar_result, rail_rails)
    
    # Langkah 3: Konversi ke simbol
    symbol_result = text_to_symbols(rail_result)
    
    return caesar_result, rail_result, symbol_result

def decrypt_combination(text, caesar_shift, rail_rails, is_symbols=False):
    """
    Melakukan dekripsi kombinasi: Rail Fence Cipher kemudian Caesar Cipher
    """
    if is_symbols:
        # Konversi simbol ke teks terlebih dahulu
        symbol_map_reverse = {
            '●': 'A', '△': 'B', '□': 'C', '▽': 'D', '~ ~': 'E',
            '~~~': 'F', '◆': 'G', '♡': 'H', '○': 'I', '- - - -': 'J',
            '◆': 'K', '~ ~ ~ ~': 'L', '□': 'M', '▲': 'N', '====': 'O',
            '▶': 'P', '◇': 'Q', '◎': 'R', '+': 'S', '+': 'T',
            '+': 'U', '☉': 'V', '○': 'W', '×': 'X', '○': 'Y', '☉☉☉☉': 'Z'
        }
        
        # Pisahkan simbol
        symbols = text.split()
        rail_input = ""
        
        i = 0
        while i < len(symbols):
            symbol = symbols[i]
            
            # Handle simbol multi-token
            if symbol == '~' and i + 1 < len(symbols) and symbols[i + 1] == '~':
                symbol = '~ ~'
                i += 1
            elif symbol == '~' and i + 3 < len(symbols):
                if all(symbols[i + j] == '~' for j in range(4)):
                    symbol = '~ ~ ~ ~'
                    i += 3
            elif symbol == '-' and i + 3 < len(symbols):
                if all(symbols[i + j] == '-' for j in range(4)):
                    symbol = '- - - -'
                    i += 3
            elif symbol == '=' and i + 3 < len(symbols):
                if all(symbols[i + j] == '=' for j in range(4)):
                    symbol = '===='
                    i += 3
            elif symbol == '☉' and i + 3 < len(symbols):
                if all(symbols[i + j] == '☉' for j in range(4)):
                    symbol = '☉☉☉☉'
                    i += 3
            
            if symbol in symbol_map_reverse:
                rail_input += symbol_map_reverse[symbol]
            elif symbol == "":
                rail_input += " "
            
            i += 1
    else:
        rail_input = text.upper()
    
    # Langkah 1: Rail Fence Decrypt
    rail_decrypted = rail_fence_decrypt(rail_input, rail_rails)
    
    # Langkah 2: Caesar Decrypt
    caesar_decrypted = caesar_cipher(rail_decrypted, caesar_shift, 'decrypt')
    
    return caesar_decrypted

# ========== ANTARMUKA STREAMLIT ==========

def main():
    # Konfigurasi halaman
    st.set_page_config(
        page_title="Aplikasi Kriptografi Kombinasi",
        page_icon="🔐",
        layout="wide"
    )
    
    # Judul aplikasi
    st.title("🔐 Aplikasi Kriptografi Kombinasi: Caesar + Rail Fence")
    st.markdown("---")
    
    # Sidebar untuk navigasi
    st.sidebar.title("Navigasi")
    app_mode = st.sidebar.radio(
        "Pilih Mode:",
        ["Enkripsi", "Dekripsi"]
    )
    
    # ========== TABEL SIMBOL REFERENSI ==========
    with st.sidebar.expander("📋 Tabel Simbol", expanded=False):
        st.markdown("""
        | Huruf | Simbol | Deskripsi |
        |-------|--------|-----------|
        | A | ● | Kota Besar |
        | B | △ | Gunung Non Aktif |
        | C | □ | Dataran Rendah |
        | D | ▽ | Lembah |
        | E | ~ ~ | Sungai |
        | F | ~~~ | Jalan Raya |
        | G | ◆ | Hutan |
        | H | ♡ | Pelabuhan |
        | I | ○ | Danau |
        | J | - - - - | Rel Kereta Api |
        | K | ◆ | Pertambangan |
        | L | ~ ~ ~ ~ | Pantai |
        | M | □ | Pemukiman |
        | N | ▲ | Gunung Aktif |
        | O | ==== | Batas Negara |
        | P | ▶ | Bendungan |
        | Q | ◇ | Air Terjun |
        | R | ◎ | Rawa |
        | S | + | Rumah Sakit |
        | T | + | Bandara |
        | U | + | Tempat Ibadah |
        | V | ☉ | Kantor Pos |
        | W | ○ | Sumur |
        | X | × | Daerah Berbahaya |
        | Y | ○ | Ibu Kota Negara |
        | Z | ☉☉☉☉ | Laut |
        """)
    
    st.sidebar.markdown("---")
    st.sidebar.info("""
    **Alur Enkripsi:**
    1. Caesar Cipher
    2. Rail Fence Cipher  
    3. Konversi ke Simbol
    
    **Alur Dekripsi:**
    1. Konversi dari Simbol (jika perlu)
    2. Rail Fence Decrypt
    3. Caesar Decrypt
    """)
    
    # ========== HALAMAN ENKRIPSI ==========
    if app_mode == "Enkripsi":
        st.header("🔒 Enkripsi Kombinasi")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Input teks
            text_input = st.text_area(
                "Masukkan teks yang akan dienkripsi:",
                height=150,
                placeholder="Masukkan teks di sini...",
                key="encrypt_input"
            )
            
            # Parameter Caesar Cipher
            st.subheader("⚙️ Parameter Caesar Cipher")
            caesar_shift = st.slider(
                "Shift (kunci pergeseran):",
                min_value=1,
                max_value=25,
                value=3,
                help="Jumlah pergeseran huruf untuk Caesar Cipher"
            )
        
        with col2:
            # Parameter Rail Fence Cipher
            st.subheader("⚙️ Parameter Rail Fence Cipher")
            rail_rails = st.slider(
                "Jumlah Rail:",
                min_value=2,
                max_value=10,
                value=3,
                help="Jumlah baris untuk pola zig-zag"
            )
            
            # Tampilkan sebagai simbol
            show_as_symbols = st.checkbox(
                "Tampilkan hasil sebagai simbol",
                value=True,
                help="Konversi hasil akhir ke simbol grafis"
            )
            
            # Tombol proses
            if st.button("🚀 Mulai Enkripsi", type="primary", use_container_width=True):
                if text_input:
                    with st.spinner("Melakukan enkripsi..."):
                        try:
                            # Lakukan enkripsi kombinasi
                            caesar_result, rail_result, symbol_result = encrypt_combination(
                                text_input, caesar_shift, rail_rails
                            )
                            
                            st.success("✅ Enkripsi berhasil!")
                            st.balloons()
                            
                            # Tampilkan hasil bertahap
                            st.markdown("---")
                            st.subheader("📊 Proses Enkripsi")
                            
                            # Tampilkan dalam tab
                            tab1, tab2, tab3 = st.tabs([
                                "🔑 Langkah 1: Caesar Cipher", 
                                "🚂 Langkah 2: Rail Fence", 
                                "🎨 Hasil Akhir"
                            ])
                            
                            with tab1:
                                st.markdown("**Teks setelah Caesar Cipher:**")
                                st.code(caesar_result, language="text")
                                st.caption(f"Shift: {caesar_shift}")
                            
                            with tab2:
                                st.markdown("**Teks setelah Rail Fence Cipher:**")
                                st.code(rail_result, language="text")
                                st.caption(f"Jumlah Rail: {rail_rails}")
                                
                                # Tampilkan pola rail
                                st.markdown("**Visualisasi Pola Rail:**")
                                display_rail_pattern(caesar_result, rail_rails)
                            
                            with tab3:
                                if show_as_symbols:
                                    st.markdown("**Hasil Akhir (dalam simbol):**")
                                    st.code(symbol_result, language="text")
                                    st.markdown("**Format:** Simbol dipisahkan spasi")
                                else:
                                    st.markdown("**Hasil Akhir (dalam huruf):**")
                                    st.code(rail_result, language="text")
                                
                                # Tombol copy
                                result_to_copy = symbol_result if show_as_symbols else rail_result
                                st.code(result_to_copy, language="text")
                                if st.button("📋 Copy Hasil", key="copy_encrypt"):
                                    st.write("Hasil telah disalin ke clipboard!")
                            
                            # Informasi dekripsi
                            st.markdown("---")
                            with st.expander("🔍 Informasi untuk Dekripsi", expanded=False):
                                st.info(f"""
                                **Parameter yang digunakan:**
                                - Caesar Shift: {caesar_shift}
                                - Rail Rails: {rail_rails}
                                - Format: {'Simbol' if show_as_symbols else 'Huruf'}
                                
                                **Untuk dekripsi:**
                                1. Gunakan mode Dekripsi
                                2. Masukkan hasil di atas
                                3. Gunakan parameter yang sama
                                4. {'Centang "Input dalam bentuk simbol"' if show_as_symbols else 'Biarkan tidak dicentang'}
                                """)
                            
                        except Exception as e:
                            st.error(f"❌ Terjadi kesalahan: {str(e)}")
                else:
                    st.warning("⚠️ Silakan masukkan teks terlebih dahulu!")
        
        # Contoh
        with st.expander("📋 Contoh Enkripsi", expanded=False):
            example_text = "KRIPTOGRAFI"
            example_shift = 3
            example_rails = 3
            
            caesar_example = caesar_cipher(example_text, example_shift, 'encrypt')
            rail_example = rail_fence_encrypt(caesar_example, example_rails)
            symbols_example = text_to_symbols(rail_example)
            
            st.write(f"**Teks Asli:** {example_text}")
            st.write(f"**Caesar Shift:** {example_shift}")
            st.write(f"**Jumlah Rail:** {example_rails}")
            st.write(f"**Setelah Caesar:** {caesar_example}")
            st.write(f"**Setelah Rail Fence:** {rail_example}")
            st.write(f"**Hasil Simbol:** {symbols_example}")
    
    # ========== HALAMAN DEKRIPSI ==========
    else:
        st.header("🔓 Dekripsi Kombinasi")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Input teks terenkripsi
            encrypted_input = st.text_area(
                "Masukkan teks terenkripsi:",
                height=150,
                placeholder="Masukkan teks atau simbol di sini...",
                key="decrypt_input"
            )
            
            # Parameter Caesar Cipher
            st.subheader("⚙️ Parameter Caesar Cipher")
            caesar_shift_decrypt = st.slider(
                "Shift (kunci pergeseran):",
                min_value=1,
                max_value=25,
                value=3,
                key="decrypt_shift",
                help="Jumlah pergeseran huruf yang digunakan saat enkripsi"
            )
        
        with col2:
            # Parameter Rail Fence Cipher
            st.subheader("⚙️ Parameter Rail Fence Cipher")
            rail_rails_decrypt = st.slider(
                "Jumlah Rail:",
                min_value=2,
                max_value=10,
                value=3,
                key="decrypt_rails",
                help="Jumlah baris yang digunakan saat enkripsi"
            )
            
            # Opsi input simbol
            input_is_symbols = st.checkbox(
                "Input dalam bentuk simbol",
                value=False,
                help="Centang jika input adalah simbol grafis"
            )
            
            # Tombol proses
            if st.button("🚀 Mulai Dekripsi", type="primary", use_container_width=True):
                if encrypted_input:
                    with st.spinner("Melakukan dekripsi..."):
                        try:
                            # Lakukan dekripsi kombinasi
                            decrypted_result = decrypt_combination(
                                encrypted_input, 
                                caesar_shift_decrypt, 
                                rail_rails_decrypt,
                                is_symbols=input_is_symbols
                            )
                            
                            st.success("✅ Dekripsi berhasil!")
                            
                            # Tampilkan hasil
                            st.markdown("---")
                            st.subheader("📊 Hasil Dekripsi")
                            
                            col_result1, col_result2 = st.columns(2)
                            
                            with col_result1:
                                st.markdown("**Teks Asli:**")
                                st.info(decrypted_result)
                            
                            with col_result2:
                                st.markdown("**Detail:**")
                                st.write(f"Input: {'Simbol' if input_is_symbols else 'Huruf'}")
                                st.write(f"Caesar Shift: {caesar_shift_decrypt}")
                                st.write(f"Jumlah Rail: {rail_rails_decrypt}")
                            
                            # Tampilkan proses
                            with st.expander("🔍 Proses Dekripsi", expanded=False):
                                if input_is_symbols:
                                    st.write("1. Input dalam bentuk simbol")
                                    st.write("2. Rail Fence Decrypt")
                                    st.write("3. Caesar Decrypt")
                                else:
                                    st.write("1. Rail Fence Decrypt")
                                    st.write("2. Caesar Decrypt")
                            
                            # Tombol copy
                            st.code(decrypted_result, language="text")
                            if st.button("📋 Copy Hasil", key="copy_decrypt"):
                                st.write("Hasil telah disalin ke clipboard!")
                            
                        except Exception as e:
                            st.error(f"❌ Terjadi kesalahan: {str(e)}")
                            st.info("Pastikan parameter dan format input sudah benar.")
                else:
                    st.warning("⚠️ Silakan masukkan teks terenkripsi terlebih dahulu!")
        
        # Contoh
        with st.expander("📋 Contoh Dekripsi", expanded=False):
            st.write("**Dari Contoh Enkripsi:**")
            example_encrypted = "◆ ◎ ○ + ==== ◆ ▽ ● △ + ○"
            st.write(f"**Input Simbol:** {example_encrypted}")
            st.write(f"**Caesar Shift:** 3")
            st.write(f"**Jumlah Rail:** 3")
            st.write(f"**Hasil:** KRIPTOGRAFI")

def display_rail_pattern(text, rails):
    """
    Menampilkan visualisasi pola Rail Fence
    """
    if rails <= 1:
        return
    
    # Siapkan grid
    pattern = []
    for _ in range(rails):
        pattern.append(["."] * len(text))
    
    # Isi pola
    rail = 0
    direction = 1
    
    for i, char in enumerate(text):
        pattern[rail][i] = char
        rail += direction
        
        if rail == 0 or rail == rails - 1:
            direction = -direction
    
    # Tampilkan
    for i in range(rails):
        row_display = " ".join(pattern[i])
        st.text(f"Rail {i+1}: {row_display}")

# ========== MENJALANKAN APLIKASI ==========
if __name__ == "__main__":
    main()
