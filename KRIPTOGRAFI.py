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

# ========== TABEL SIMBOL ==========

def create_symbol_table():
    """
    Membuat tabel simbol berdasarkan data dari PDF
    """
    symbols_data = {
        'Alphabet': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
                    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'],
        'Simbol': ['●', '△', '□', '▽', '~ ~', '~~~', '◆', '♡', '○', '- - - -', '◆', 
                  '~ ~ ~ ~', '□', '▲', '====', '▶', '◇', '◎', '+', '+', '+', '☉', '○', '×', '○', '☉☉☉☉'],
        'Deskripsi': ['Kota Besar', 'Gunung Non Aktif', 'Dataran Rendah', 'Lembah', 'Sungai', 
                     'Jalan Raya', 'Hutan', 'Pelabuhan', 'Danau', 'Rel Kereta Api', 'Pertambangan',
                     'Pantai', 'Pemukiman', 'Gunung Aktif', 'Batas Negara', 'Bendungan', 
                     'Air Terjun', 'Rawa', 'Rumah Sakit', 'Bandara', 'Tempat Ibadah', 
                     'Kantor Pos', 'Sumur', 'Daerah Berbahaya', 'Ibu Kota Negara', 'Laut']
    }
    
    return pd.DataFrame(symbols_data)

# ========== ANTARMUKA STREAMLIT ==========

def main():
    # Konfigurasi halaman
    st.set_page_config(
        page_title="Aplikasi Kriptografi",
        page_icon="🔐",
        layout="wide"
    )
    
    # Judul aplikasi
    st.title("🔐 Aplikasi Kriptografi: Rail Cipher & Caesar Cipher")
    st.markdown("---")
    
    # Sidebar untuk navigasi
    st.sidebar.title("Navigasi")
    app_mode = st.sidebar.radio(
        "Pilih Menu:",
        ["Beranda", "Caesar Cipher", "Rail Fence Cipher", "Tabel Simbol", "Tentang"]
    )
    
    # ========== HALAMAN BERANDA ==========
    if app_mode == "Beranda":
        st.header("Selamat Datang di Aplikasi Kriptografi")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Caesar Cipher")
            st.markdown("""
            **Penjelasan:**
            - Metode substitusi sederhana
            - Menggeser setiap huruf sejauh 3 posisi (default)
            - Ditemukan oleh Julius Caesar
            """)
            
            st.info("""
            **Contoh:**
            - Plaintext: HELLO
            - Key: 3
            - Ciphertext: KHOOR
            """)
        
        with col2:
            st.subheader("Rail Fence Cipher")
            st.markdown("""
            **Penjelasan:**
            - Metode transposisi
            - Menulis teks dalam pola zig-zag
            - Membaca per baris untuk menghasilkan ciphertext
            """)
            
            st.info("""
            **Contoh:**
            - Plaintext: HELLO WORLD
            - Rails: 3
            - Ciphertext: HOREL OLWLD
            """)
        
        st.markdown("---")
        st.subheader("Cara Penggunaan")
        st.write("1. Pilih menu di sidebar")
        st.write("2. Untuk Caesar Cipher: masukkan teks dan pilih enkripsi/dekripsi")
        st.write("3. Untuk Rail Fence Cipher: masukkan teks dan jumlah rail")
        st.write("4. Untuk Tabel Simbol: lihat kode simbol untuk setiap huruf")
    
    # ========== HALAMAN CAESAR CIPHER ==========
    elif app_mode == "Caesar Cipher":
        st.header("Caesar Cipher")
        
        # Penjelasan
        with st.expander("📖 Tentang Caesar Cipher"):
            st.markdown("""
            **Caesar Cipher** adalah salah satu teknik kriptografi tertua yang dikenal.
            
            **Cara kerja:**
            1. Setiap huruf pada plaintext digeser sejauh nilai key
            2. Default key adalah 3 (seperti yang digunakan Julius Caesar)
            3. Pergeseran dilakukan dalam alfabet (A-Z)
            
            **Rumus:**
            - Enkripsi: C = (P + K) mod 26
            - Dekripsi: P = (C - K) mod 26
            
            Dimana:
            - C = Ciphertext
            - P = Plaintext
            - K = Key (nilai pergeseran)
            """)
        
        # Input pengguna
        col1, col2 = st.columns(2)
        
        with col1:
            text_input = st.text_area("Masukkan teks:", height=100, 
                                      placeholder="Masukkan teks di sini...")
        
        with col2:
            mode = st.radio("Pilih mode:", ["Enkripsi", "Dekripsi"])
            shift_key = st.slider("Pilih key (nilai pergeseran):", 
                                 min_value=1, max_value=25, value=3)
            
            if st.button("🚀 Proses Caesar Cipher", use_container_width=True):
                if text_input:
                    if mode == "Enkripsi":
                        result = caesar_cipher(text_input, shift_key, 'encrypt')
                        st.success("✅ Enkripsi Berhasil!")
                    else:
                        result = caesar_cipher(text_input, shift_key, 'decrypt')
                        st.success("✅ Dekripsi Berhasil!")
                    
                    # Tampilkan hasil
                    st.subheader("Hasil:")
                    st.code(result, language="text")
                else:
                    st.warning("⚠️ Silakan masukkan teks terlebih dahulu!")
        
        # Contoh
        with st.expander("📋 Contoh Caesar Cipher"):
            example_text = "KRIPTOGRAFI"
            example_encrypted = caesar_cipher(example_text, 3, 'encrypt')
            example_decrypted = caesar_cipher(example_encrypted, 3, 'decrypt')
            
            st.write(f"**Plaintext:** {example_text}")
            st.write(f"**Key:** 3")
            st.write(f"**Ciphertext:** {example_encrypted}")
            st.write(f"**Dekripsi kembali:** {example_decrypted}")
    
    # ========== HALAMAN RAIL FENCE CIPHER ==========
    elif app_mode == "Rail Fence Cipher":
        st.header("Rail Fence Cipher")
        
        # Penjelasan
        with st.expander("📖 Tentang Rail Fence Cipher"):
            st.markdown("""
            **Rail Fence Cipher** adalah metode transposisi yang menulis teks dalam pola zig-zag.
            
            **Cara kerja:**
            1. Teks ditulis secara diagonal (zig-zag) pada sejumlah "rail"
            2. Ciphertext dibaca per baris secara horizontal
            3. Untuk dekripsi, dibangun kembali pola zig-zag
            
            **Contoh visual (3 rail):**
            ```
            H   O   R   L
              E   L   W   D
                L   O   
            ```
            Dibaca sebagai: HOREL OLWLD
            """)
        
        # Input pengguna
        col1, col2 = st.columns(2)
        
        with col1:
            rf_text_input = st.text_area("Masukkan teks:", height=100, 
                                         placeholder="Masukkan teks di sini...", key="rf_input")
        
        with col2:
            rf_mode = st.radio("Pilih mode:", ["Enkripsi", "Dekripsi"], key="rf_mode")
            num_rails = st.slider("Pilih jumlah rail:", 
                                 min_value=2, max_value=10, value=3)
            
            if st.button("🚀 Proses Rail Fence Cipher", use_container_width=True):
                if rf_text_input:
                    if rf_mode == "Enkripsi":
                        result = rail_fence_encrypt(rf_text_input, num_rails)
                        st.success("✅ Enkripsi Berhasil!")
                    else:
                        result = rail_fence_decrypt(rf_text_input, num_rails)
                        st.success("✅ Dekripsi Berhasil!")
                    
                    # Tampilkan hasil
                    st.subheader("Hasil:")
                    st.code(result, language="text")
                else:
                    st.warning("⚠️ Silakan masukkan teks terlebih dahulu!")
        
        # Contoh
        with st.expander("📋 Contoh Rail Fence Cipher"):
            example_text = "RAILFENCE"
            example_encrypted = rail_fence_encrypt(example_text, 3)
            example_decrypted = rail_fence_decrypt(example_encrypted, 3)
            
            st.write(f"**Plaintext:** {example_text}")
            st.write(f"**Jumlah rail:** 3")
            st.write(f"**Ciphertext:** {example_encrypted}")
            st.write(f"**Dekripsi kembali:** {example_decrypted}")
    
    # ========== HALAMAN TABEL SIMBOL ==========
    elif app_mode == "Tabel Simbol":
        st.header("Tabel Simbol Kriptografi")
        st.markdown("Tabel konversi huruf ke simbol berdasarkan materi kriptografi")
        
        # Buat dan tampilkan tabel
        symbol_df = create_symbol_table()
        
        # Tampilkan dengan styling
        st.dataframe(
            symbol_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Alphabet": st.column_config.TextColumn("Huruf", width="small"),
                "Simbol": st.column_config.TextColumn("Simbol", width="medium"),
                "Deskripsi": st.column_config.TextColumn("Deskripsi", width="large")
            }
        )
        
        # Opsi pencarian
        st.subheader("Cari Simbol")
        search_option = st.radio("Cari berdasarkan:", ["Huruf", "Deskripsi"])
        
        if search_option == "Huruf":
            search_letter = st.text_input("Masukkan huruf (A-Z):", max_chars=1).upper()
            if search_letter and search_letter in symbol_df['Alphabet'].values:
                result = symbol_df[symbol_df['Alphabet'] == search_letter].iloc[0]
                st.info(f"**{result['Alphabet']}** → **{result['Simbol']}** : {result['Deskripsi']}")
            elif search_letter:
                st.warning(f"Huruf '{search_letter}' tidak ditemukan dalam tabel.")
        else:
            search_desc = st.text_input("Masukkan kata kunci deskripsi:")
            if search_desc:
                filtered = symbol_df[symbol_df['Deskripsi'].str.contains(search_desc, case=False, na=False)]
                if not filtered.empty:
                    for _, row in filtered.iterrows():
                        st.write(f"**{row['Alphabet']}** → **{row['Simbol']}** : {row['Deskripsi']}")
                else:
                    st.warning(f"Tidak ditemukan deskripsi dengan kata kunci '{search_desc}'.")
    
    # ========== HALAMAN TENTANG ==========
    elif app_mode == "Tentang":
        st.header("Tentang Aplikasi")
        
        st.markdown("""
        ### 📚 Informasi Aplikasi
        
        **Nama:** Aplikasi Kriptografi - Rail Cipher & Caesar Cipher  
        **Pembuat:** Fadina Laila Hidayati  
        **NIM:** 24.83.1109  
        **Mata Kuliah:** Kriptografi
        
        ### 🔐 Fitur Aplikasi
        
        1. **Caesar Cipher**
           - Enkripsi dan dekripsi teks
           - Kustomisasi key (nilai pergeseran)
           - Contoh implementasi
        
        2. **Rail Fence Cipher**
           - Enkripsi dan dekripsi teks
           - Kustomisasi jumlah rail
           - Contoh implementasi
        
        3. **Tabel Simbol**
           - Tabel lengkap konversi huruf ke simbol
           - Fungsi pencarian
           - Berdasarkan materi kriptografi
        
        ### 🛠️ Teknologi
        
        - **Python 3.x**
        - **Streamlit** untuk antarmuka web
        - **Pandas** untuk manipulasi data
        
        ### 📖 Referensi
        
        - Materi Kriptografi
        - Rail Cipher & Caesar Cipher
        - Tabel Simbol Kriptografi
        """)
        
        st.markdown("---")
        st.caption("© 2024 Aplikasi Kriptografi - Dibuat untuk pembelajaran")

# ========== MENJALANKAN APLIKASI ==========
if __name__ == "__main__":
    main()
