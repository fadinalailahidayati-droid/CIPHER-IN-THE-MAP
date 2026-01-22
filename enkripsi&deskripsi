import streamlit as st
import pandas as pd

# ========== KONFIGURASI SIMBOL GEOGRAFI YANG DIPERBAIKI ==========

# Tabel simbol geografi dengan mapping yang KONSISTEN
GEO_SYMBOLS = {
    # Simbol untuk Caesar Cipher (key/geseran) - 26 simbol untuk 26 shift
    'CAESAR_KEYS': {
        '●': 1,   '△': 2,   '□': 3,   '▽': 4,   '~': 5,
        '~~~': 6,  '◆': 7,   '♡': 8,   '○': 9,   '--': 10,
        '▲': 11,  '====': 12, '▶': 13,  '◇': 14,  '◎': 15,
        '+': 16,  '☉': 17,  '×': 18,  '☉☉☉☉': 19, '~ ~': 20,
        '...': 21, '●●': 22,  '□□': 23,  '△△': 24,  '▽▽': 25,
        '◆◆': 26
    },
    
    # Simbol untuk Rail Fence Cipher (jumlah rail)
    'RAIL_KEYS': {
        '|': 2,    'Z': 3,    '卍': 4,   '✠': 5,    '✪': 6,
        '❂': 7,    '✿': 8,    '❀': 9,    '✾': 10
    },
    
    # Simbol untuk representasi huruf - SETIAP HURUF HARUS UNIK!
    'LETTER_SYMBOLS': {
        'A': '●',    'B': '△',    'C': '□',    'D': '▽',    'E': '~',
        'F': '~~~',  'G': '◆',    'H': '♡',    'I': '○',    'J': '--',
        'K': '▲',    'L': '====', 'M': '▶',    'N': '◇',    'O': '◎',
        'P': '+',    'Q': '☉',    'R': '×',    'S': '☉☉☉☉', 'T': '~ ~',
        'U': '...',  'V': '●●',   'W': '□□',   'X': '△△',   'Y': '▽▽',
        'Z': '◆◆'
    },
    
    # Reverse mapping untuk dekripsi - HARUS KONSISTEN!
    'SYMBOL_TO_LETTER': {
        '●': 'A', '△': 'B', '□': 'C', '▽': 'D', '~': 'E',
        '~~~': 'F', '◆': 'G', '♡': 'H', '○': 'I', '--': 'J',
        '▲': 'K', '====': 'L', '▶': 'M', '◇': 'N', '◎': 'O',
        '+': 'P', '☉': 'Q', '×': 'R', '☉☉☉☉': 'S', '~ ~': 'T',
        '...': 'U', '●●': 'V', '□□': 'W', '△△': 'X', '▽▽': 'Y',
        '◆◆': 'Z'
    }
}

# ========== FUNGSI UTILITAS YANG DIPERBAIKI ==========

def get_symbol_value(symbol_dict, symbol):
    """Mendapatkan nilai numerik dari simbol"""
    for key, value in symbol_dict.items():
        if key == symbol:
            return value
    return 0

def get_key_from_value(symbol_dict, value):
    """Mendapatkan simbol dari nilai numerik"""
    for key, val in symbol_dict.items():
        if val == value:
            return key
    return '?'

def text_to_geo_symbols(text):
    """Mengonversi teks menjadi simbol geografi dengan aman"""
    result = []
    for char in text.upper():
        if char in GEO_SYMBOLS['LETTER_SYMBOLS']:
            result.append(GEO_SYMBOLS['LETTER_SYMBOLS'][char])
        elif char == " ":
            result.append("/")
        else:
            result.append(char)
    return " ".join(result)

def geo_symbols_to_text(symbols_text):
    """Mengonversi simbol geografi kembali ke teks dengan aman"""
    # Pisahkan simbol dengan aman
    symbols = symbols_text.split()
    result = []
    
    i = 0
    while i < len(symbols):
        current_symbol = symbols[i]
        
        # Cek simbol multi-karakter secara spesifik
        combined_symbol = current_symbol
        
        # Cek untuk simbol panjang 4
        if i + 3 < len(symbols):
            test_4 = f"{symbols[i]}{symbols[i+1]}{symbols[i+2]}{symbols[i+3]}"
            if test_4 == '☉☉☉☉':
                combined_symbol = '☉☉☉☉'
                i += 3
            elif test_4 == '====':
                combined_symbol = '===='
                i += 3
        
        # Cek untuk simbol panjang 2
        elif i + 1 < len(symbols):
            test_2 = f"{symbols[i]}{symbols[i+1]}"
            if test_2 == '~ ~':
                combined_symbol = '~ ~'
                i += 1
            elif test_2 == '●●':
                combined_symbol = '●●'
                i += 1
            elif test_2 == '□□':
                combined_symbol = '□□'
                i += 1
            elif test_2 == '△△':
                combined_symbol = '△△'
                i += 1
            elif test_2 == '▽▽':
                combined_symbol = '▽▽'
                i += 1
            elif test_2 == '◆◆':
                combined_symbol = '◆◆'
                i += 1
            elif test_2 == '--':
                combined_symbol = '--'
                i += 1
        
        # Cek untuk simbol panjang 3
        elif i + 2 < len(symbols):
            test_3 = f"{symbols[i]}{symbols[i+1]}{symbols[i+2]}"
            if test_3 == '~~~':
                combined_symbol = '~~~'
                i += 2
            elif test_3 == '...':
                combined_symbol = '...'
                i += 2
        
        # Konversi simbol ke huruf
        if combined_symbol in GEO_SYMBOLS['SYMBOL_TO_LETTER']:
            result.append(GEO_SYMBOLS['SYMBOL_TO_LETTER'][combined_symbol])
        elif combined_symbol == "/":
            result.append(" ")
        else:
            result.append(combined_symbol)
        
        i += 1
    
    return ''.join(result)

def caesar_cipher_geo(text, shift_symbol, mode='encrypt'):
    """Caesar Cipher dengan simbol geografi sebagai kunci"""
    # Konversi simbol ke nilai shift
    shift = GEO_SYMBOLS['CAESAR_KEYS'].get(shift_symbol, 3)
    
    result = []
    
    # Tentukan arah pergeseran berdasarkan mode
    if mode == 'decrypt':
        shift = -shift
    
    for char in text.upper():
        if 'A' <= char <= 'Z':
            # Lakukan pergeseran
            shifted = (ord(char) - 65 + shift) % 26
            result.append(chr(shifted + 65))
        elif char == " ":
            result.append(" ")
        else:
            result.append(char)
    
    return ''.join(result)

def rail_fence_cipher_geo(text, rail_symbol, mode='encrypt'):
    """Rail Fence Cipher dengan simbol geografi sebagai kunci"""
    # Konversi simbol ke jumlah rail
    rails = GEO_SYMBOLS['RAIL_KEYS'].get(rail_symbol, 3)
    
    if rails <= 1 or rails > 10:
        return text
    
    text_len = len(text)
    
    if mode == 'encrypt':
        # Buat rail (list of strings)
        fence = [''] * rails
        rail = 0
        direction = 1
        
        for char in text:
            fence[rail] += char
            rail += direction
            
            # Balik arah jika mencapai rail atas atau bawah
            if rail == 0 or rail == rails - 1:
                direction = -direction
        
        # Gabungkan semua rail
        return ''.join(fence)
    
    else:  # mode == 'decrypt'
        if text_len == 0:
            return ""
        
        # Buat pola rail untuk dekripsi
        fence = [[''] * text_len for _ in range(rails)]
        rail = 0
        direction = 1
        
        # Tentukan posisi di setiap rail
        for i in range(text_len):
            fence[rail][i] = '*'
            rail += direction
            
            if rail == 0 or rail == rails - 1:
                direction = -direction
        
        # Isi pola dengan teks terenkripsi
        index = 0
        for r in range(rails):
            for c in range(text_len):
                if fence[r][c] == '*' and index < text_len:
                    fence[r][c] = text[index]
                    index += 1
        
        # Baca teks asli
        rail = 0
        direction = 1
        result = []
        
        for i in range(text_len):
            result.append(fence[rail][i])
            rail += direction
            
            if rail == 0 or rail == rails - 1:
                direction = -direction
        
        return ''.join(result)

def display_rail_visualization(text, rails):
    """Menampilkan visualisasi Rail Fence pattern"""
    if rails <= 1:
        return
    
    # Buat grid untuk visualisasi
    grid = []
    for _ in range(rails):
        grid.append(['.'] * len(text))
    
    # Isi grid
    rail = 0
    direction = 1
    
    for i, char in enumerate(text):
        grid[rail][i] = char
        rail += direction
        
        if rail == 0 or rail == rails - 1:
            direction = -direction
    
    # Tampilkan
    st.markdown("**Visualisasi Rail Pattern:**")
    for i in range(rails):
        rail_display = " ".join(grid[i])
        st.text(f"Rail {i+1}: {rail_display}")

def display_symbol_conversion(text):
    """Menampilkan konversi huruf ke simbol"""
    st.markdown("**Konversi per huruf:**")
    
    conversion_text = ""
    for char in text.upper():
        if char in GEO_SYMBOLS['LETTER_SYMBOLS']:
            symbol = GEO_SYMBOLS['LETTER_SYMBOLS'][char]
            conversion_text += f"{char} → {symbol}  |  "
        elif char == " ":
            conversion_text += "spasi → /  |  "
    
    st.write(conversion_text)

# ========== FUNGSI KOMBINASI YANG DIPERBAIKI ==========

def encrypt_combination_geo(plaintext, caesar_key_symbol, rail_key_symbol):
    """
    Enkripsi kombinasi: Caesar Cipher -> Rail Fence -> Simbol
    """
    # Validasi input
    plaintext = plaintext.upper()
    
    # Langkah 1: Caesar Cipher
    caesar_result = caesar_cipher_geo(plaintext, caesar_key_symbol, 'encrypt')
    
    # Langkah 2: Rail Fence Cipher
    rail_result = rail_fence_cipher_geo(caesar_result, rail_key_symbol, 'encrypt')
    
    # Langkah 3: Konversi ke simbol geografi
    final_symbols = text_to_geo_symbols(rail_result)
    
    return caesar_result, rail_result, final_symbols

def decrypt_combination_geo(cipher_symbols, caesar_key_symbol, rail_key_symbol):
    """
    Dekripsi kombinasi: Simbol -> Rail Fence -> Caesar
    """
    # Langkah 1: Konversi simbol ke teks
    rail_text = geo_symbols_to_text(cipher_symbols)
    
    # Langkah 2: Rail Fence Decrypt
    caesar_text = rail_fence_cipher_geo(rail_text, rail_key_symbol, 'decrypt')
    
    # Langkah 3: Caesar Decrypt
    plaintext = caesar_cipher_geo(caesar_text, caesar_key_symbol, 'decrypt')
    
    return rail_text, caesar_text, plaintext

# ========== ANTARMUKA STREAMLIT ==========

def main():
    # Konfigurasi halaman
    st.set_page_config(
        page_title="Cipher In The Map",
        page_icon="🗺️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        color: #3B82F6;
        font-size: 1.5rem;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .geo-symbol {
        font-size: 1.8rem;
        display: inline-block;
        margin: 0 5px;
    }
    .key-badge {
        background-color: #E0F2FE;
        padding: 5px 10px;
        border-radius: 15px;
        margin: 2px;
        display: inline-block;
        font-weight: bold;
    }
    .step-box {
        background-color: #F8FAFC;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #3B82F6;
        margin: 10px 0;
    }
    .symbol-output {
        font-family: 'Courier New', monospace;
        font-size: 1.5rem;
        padding: 20px;
        background-color: #f0f8ff;
        border-radius: 10px;
        border: 2px solid #3B82F6;
        text-align: center;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header utama
    st.markdown('<h1 class="main-header">🗺️ Cipher In The Map</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666; margin-bottom: 2rem;">Kriptografi dengan Simbol Geografi</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🧭 Navigasi")
        app_mode = st.radio(
            "Pilih Mode:",
            ["Beranda", "Enkripsi", "Dekripsi", "Panduan Simbol"]
        )
        
        st.markdown("---")
        st.markdown("### 📊 Info Aplikasi")
        st.info("""
        **Cipher In The Map** mengubah teks menjadi peta geografis rahasia menggunakan:
        
        1. **Caesar Cipher** dengan simbol geografi
        2. **Rail Fence Cipher** dengan simbol jalan
        3. **Hasil akhir** dalam bentuk peta simbol
        """)
        
        st.markdown("---")
        st.markdown("**👩‍💻 Pembuat:** Fadina Laila Hidayati")
        st.markdown("**🎓 NIM:** 24.83.1109")
        
        # Testing tools di sidebar
        if 'last_encryption' in st.session_state:
            st.markdown("---")
            st.markdown("### 🧪 Testing Tools")
            if st.button("🧪 Test Konversi KRIPTOGRAFI"):
                test_result = text_to_geo_symbols("KRIPTOGRAFI")
                test_back = geo_symbols_to_text(test_result)
                if "KRIPTOGRAFI" == test_back:
                    st.success("✅ Konversi berhasil!")
                else:
                    st.error(f"❌ Gagal: {test_back}")
    
    # ========== HALAMAN BERANDA ==========
    if app_mode == "Beranda":
        st.markdown('<h2 class="sub-header">Selamat Datang di Dunia Kriptografi Geografis!</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🗝️ Cara Kerja
            
            **Alur Enkripsi:**
            1. Masukkan teks biasa
            2. Pilih kunci Caesar dari simbol geografi
            3. Pilih kunci Rail Fence dari simbol jalan
            4. Dapatkan pesan rahasia dalam bentuk peta simbol
            
            **Alur Dekripsi:**
            1. Masukkan simbol geografi
            2. Gunakan kunci yang sama
            3. Dapatkan kembali teks asli
            """)
            
        with col2:
            st.markdown("""
            ### 🎯 Fitur Utama
            
            ✅ **Caesar Cipher** dengan 26 simbol geografi
            ✅ **Rail Fence Cipher** dengan 9 pola jalan
            ✅ **Konversi otomatis** teks ↔ simbol
            ✅ **Tampilan visual** proses enkripsi
            ✅ **Dekripsi sempurna** ke teks asli
            
            ### 📝 Contoh Cepat
            
            **Teks:** `HELLO`
            **Kunci Caesar:** `●` (Kota Besar = shift 1)
            **Kunci Rail:** `|` (Jalan Lurus = 2 rail)
            **Hasil:** `● △ ○ ○ ◎`
            """)
            
            # Tombol cepat
            if st.button("🚀 Mulai Enkripsi", use_container_width=True):
                st.session_state.page = "Enkripsi"
                st.rerun()
    
    # ========== HALAMAN ENKRIPSI ==========
    elif app_mode == "Enkripsi":
        st.markdown('<h2 class="sub-header">🔒 Enkripsi Pesan</h2>', unsafe_allow_html=True)
        
        # Input utama
        col_input, col_keys = st.columns([2, 1])
        
        with col_input:
            plaintext = st.text_area(
                "**Teks yang akan dienkripsi:**",
                height=150,
                placeholder="Masukkan pesan rahasia Anda di sini...",
                help="Hanya huruf A-Z akan diproses, spasi dipertahankan",
                key="encrypt_text"
            )
            
            # Preview konversi langsung
            if plaintext:
                preview_symbols = text_to_geo_symbols(plaintext.upper())
                st.caption(f"Preview konversi langsung: {preview_symbols}")
        
        with col_keys:
            st.markdown("### 🗝️ Pilih Kunci")
            
            # Pilih kunci Caesar
            caesar_options = list(GEO_SYMBOLS['CAESAR_KEYS'].keys())[:15]  # Ambil 15 pertama
            caesar_key = st.selectbox(
                "**Kunci Caesar (simbol geografi):**",
                options=caesar_options,
                format_func=lambda x: f"{x} (shift {GEO_SYMBOLS['CAESAR_KEYS'][x]})",
                help="Pilih simbol geografi sebagai kunci pergeseran",
                key="caesar_key_select"
            )
            
            # Pilih kunci Rail Fence
            rail_options = list(GEO_SYMBOLS['RAIL_KEYS'].keys())
            rail_key = st.selectbox(
                "**Kunci Rail Fence (pola jalan):**",
                options=rail_options,
                format_func=lambda x: f"{x} ({GEO_SYMBOLS['RAIL_KEYS'][x]} rail)",
                help="Pilih pola jalan sebagai jumlah rail",
                key="rail_key_select"
            )
            
            # Testing button untuk KRIPTOGRAFI
            if st.button("🧪 Test dengan 'KRIPTOGRAFI'"):
                plaintext = "KRIPTOGRAFI"
                caesar_key = '●'
                rail_key = '|'
                st.rerun()
        
        # Tombol proses
        if st.button("🗺️ Buat Peta Rahasia", type="primary", use_container_width=True):
            if plaintext.strip():
                with st.spinner("Membuat peta kriptografi..."):
                    try:
                        # Proses enkripsi
                        caesar_result, rail_result, final_symbols = encrypt_combination_geo(
                            plaintext, caesar_key, rail_key
                        )
                        
                        st.success("✅ Peta rahasia berhasil dibuat!")
                        st.balloons()
                        
                        # Simpan ke session state
                        st.session_state.last_encryption = {
                            'plaintext': plaintext,
                            'caesar_key': caesar_key,
                            'rail_key': rail_key,
                            'caesar_result': caesar_result,
                            'rail_result': rail_result,
                            'final_symbols': final_symbols
                        }
                        
                        # Tampilkan hasil
                        st.markdown("---")
                        st.markdown('<h3 class="sub-header">🗺️ Peta Rahasia Anda</h3>', unsafe_allow_html=True)
                        
                        # Hasil akhir dalam simbol
                        col_final, col_info = st.columns([2, 1])
                        
                        with col_final:
                            st.markdown("**Simbol Geografi:**")
                            st.markdown(f'<div class="symbol-output">{final_symbols}</div>', unsafe_allow_html=True)
                            
                            # Tombol copy
                            st.code(final_symbols, language="text")
                            if st.button("📋 Salin Simbol", key="copy_encrypt"):
                                st.write("✅ Simbol telah disalin!")
                        
                        with col_info:
                            st.markdown("**Kunci yang digunakan:**")
                            st.markdown(f'<div class="key-badge">Caesar: {caesar_key}</div>', unsafe_allow_html=True)
                            st.markdown(f'<div class="key-badge">Rail: {rail_key}</div>', unsafe_allow_html=True)
                            st.markdown(f'<div class="key-badge">Shift: {GEO_SYMBOLS["CAESAR_KEYS"][caesar_key]}</div>', unsafe_allow_html=True)
                            st.markdown(f'<div class="key-badge">Rails: {GEO_SYMBOLS["RAIL_KEYS"][rail_key]}</div>', unsafe_allow_html=True)
                        
                        # Proses bertahap
                        st.markdown("---")
                        st.markdown('<h4 class="sub-header">📊 Proses Enkripsi</h4>', unsafe_allow_html=True)
                        
                        tab1, tab2, tab3 = st.tabs(["1️⃣ Caesar Cipher", "2️⃣ Rail Fence", "3️⃣ Simbol Geografi"])
                        
                        with tab1:
                            st.markdown("**Teks setelah Caesar Cipher:**")
                            st.info(caesar_result)
                            st.caption(f"Shift: {GEO_SYMBOLS['CAESAR_KEYS'][caesar_key]} ({caesar_key})")
                        
                        with tab2:
                            st.markdown("**Teks setelah Rail Fence Cipher:**")
                            st.info(rail_result)
                            st.caption(f"Rail: {GEO_SYMBOLS['RAIL_KEYS'][rail_key]} ({rail_key})")
                            
                            # Visualisasi rail
                            display_rail_visualization(caesar_result, GEO_SYMBOLS['RAIL_KEYS'][rail_key])
                        
                        with tab3:
                            st.markdown("**Konversi ke simbol geografi:**")
                            display_symbol_conversion(rail_result)
                        
                        # Testing verifikasi
                        st.markdown("---")
                        with st.expander("🔍 Verifikasi Konversi", expanded=False):
                            # Test konversi dua arah
                            test_back = geo_symbols_to_text(final_symbols)
                            if test_back == rail_result:
                                st.success("✅ Konversi dua arah berhasil!")
                                st.write(f"Simbol → Teks: `{test_back}`")
                                st.write(f"Teks asli Rail: `{rail_result}`")
                            else:
                                st.error(f"❌ Konversi gagal! Hasil: {test_back}, Harusnya: {rail_result}")
                        
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
            else:
                st.warning("⚠️ Masukkan teks terlebih dahulu!")
    
    # ========== HALAMAN DEKRIPSI ==========
    elif app_mode == "Dekripsi":
        st.markdown('<h2 class="sub-header">🔓 Dekripsi Peta Rahasia</h2>', unsafe_allow_html=True)
        
        # Input untuk dekripsi
        col_input, col_keys = st.columns([2, 1])
        
        with col_input:
            cipher_symbols = st.text_area(
                "**Simbol geografi yang akan didekripsi:**",
                height=150,
                placeholder="Tempel simbol geografi di sini...",
                help="Contoh: ● △ ○ ○ ◎ / ◆ ♡",
                key="decrypt_input"
            )
            
            # Tombol load contoh dari enkripsi terakhir
            if 'last_encryption' in st.session_state:
                if st.button("📥 Gunakan hasil enkripsi terakhir", use_container_width=True):
                    cipher_symbols = st.session_state.last_encryption['final_symbols']
                    st.rerun()
        
        with col_keys:
            st.markdown("### 🔑 Masukkan Kunci")
            
            # Pilih kunci Caesar
            caesar_options_decrypt = list(GEO_SYMBOLS['CAESAR_KEYS'].keys())[:15]
            caesar_key_decrypt = st.selectbox(
                "**Kunci Caesar:**",
                options=caesar_options_decrypt,
                key="decrypt_caesar",
                help="Kunci yang digunakan saat enkripsi",
                index=0  # Default ke pertama
            )
            
            # Pilih kunci Rail Fence
            rail_options_decrypt = list(GEO_SYMBOLS['RAIL_KEYS'].keys())
            rail_key_decrypt = st.selectbox(
                "**Kunci Rail Fence:**",
                options=rail_options_decrypt,
                key="decrypt_rail",
                help="Kunci yang digunakan saat enkripsi",
                index=0  # Default ke pertama
            )
        
        # Tombol proses
        if st.button("🗝️ Baca Peta Rahasia", type="primary", use_container_width=True):
            if cipher_symbols.strip():
                with st.spinner("Membaca peta kriptografi..."):
                    try:
                        # Proses dekripsi
                        rail_text, caesar_text, plaintext = decrypt_combination_geo(
                            cipher_symbols, caesar_key_decrypt, rail_key_decrypt
                        )
                        
                        st.success("✅ Pesan berhasil dibaca!")
                        
                        # Tampilkan hasil
                        st.markdown("---")
                        st.markdown('<h3 class="sub-header">📜 Pesan Asli</h3>', unsafe_allow_html=True)
                        
                        col_result, col_process = st.columns([1, 2])
                        
                        with col_result:
                            st.markdown("**Teks Terdekripsi:**")
                            st.markdown(f'<div class="step-box" style="background-color: #D1FAE5;"><h3 style="color: #065F46; text-align: center;">{plaintext}</h3></div>', unsafe_allow_html=True)
                            
                            if st.button("📋 Salin Teks", key="copy_decrypt"):
                                st.write("✅ Teks telah disalin!")
                        
                        with col_process:
                            st.markdown("**Proses Dekripsi:**")
                            
                            # Tampilkan langkah-langkah
                            st.write(f"**1. Dari simbol:** `{cipher_symbols}`")
                            st.write(f"**2. Ke teks Rail:** `{rail_text}`")
                            st.write(f"**3. Setelah Rail Decrypt:** `{caesar_text}`")
                            st.write(f"**4. Setelah Caesar Decrypt:** `{plaintext}`")
                        
                        # Verifikasi jika ada data enkripsi sebelumnya
                        if 'last_encryption' in st.session_state:
                            expected = st.session_state.last_encryption['plaintext'].upper()
                            if plaintext == expected:
                                st.success("✅ Cocok dengan teks asli!")
                            else:
                                st.warning(f"⚠️ Tidak cocok. Seharusnya: {expected}")
                        
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                        st.info("Pastikan simbol dan kunci sesuai dengan saat enkripsi.")
            else:
                st.warning("⚠️ Masukkan simbol geografi terlebih dahulu!")
    
    # ========== HALAMAN PANDUAN SIMBOL ==========
    else:
        st.markdown('<h2 class="sub-header">📚 Panduan Simbol Geografi</h2>', unsafe_allow_html=True)
        
        tab_guide1, tab_guide2, tab_guide3 = st.tabs(["🗺️ Simbol Geografi", "🛣️ Simbol Jalan", "🔤 Huruf ke Simbol"])
        
        with tab_guide1:
            st.markdown("### Kunci Caesar Cipher (26 Simbol)")
            
            # Tampilkan tabel simbol geografi dengan deskripsi
            geo_data = []
            descriptions = {
                '●': 'Kota Besar', '△': 'Gunung Non Aktif', '□': 'Dataran Rendah',
                '▽': 'Lembah', '~': 'Sungai', '~~~': 'Jalan Raya',
                '◆': 'Hutan', '♡': 'Pelabuhan', '○': 'Danau',
                '--': 'Rel Kereta Api', '▲': 'Gunung Aktif', '====': 'Batas Negara',
                '▶': 'Bendungan', '◇': 'Air Terjun', '◎': 'Rawa',
                '+': 'Bangunan Publik', '☉': 'Kantor Pos', '×': 'Daerah Berbahaya',
                '☉☉☉☉': 'Laut', '~ ~': 'Pantai', '...': 'Pemukiman',
                '●●': 'Ibu Kota', '□□': 'Kota Kecil', '△△': 'Bukit',
                '▽▽': 'Jurang', '◆◆': 'Hutan Lebat'
            }
            
            for symbol, value in GEO_SYMBOLS['CAESAR_KEYS'].items():
                geo_data.append({
                    'Simbol': symbol,
                    'Nilai Shift': value,
                    'Deskripsi': descriptions.get(symbol, 'Geografi'),
                    'Contoh Enkripsi': f"A → {chr((0 + value) % 26 + 65)}"
                })
            
            geo_df = pd.DataFrame(geo_data)
            st.dataframe(geo_df, use_container_width=True, hide_index=True)
        
        with tab_guide2:
            st.markdown("### Kunci Rail Fence Cipher (9 Pola)")
            
            rail_data = []
            descriptions = {
                '|': 'Jalan Lurus',
                'Z': 'Jalan Berkelok',
                '卍': 'Jalan Simpang',
                '✠': 'Persimpangan',
                '✪': 'Bundaran',
                '❂': 'Simpang Susun',
                '✿': 'Jalan Lingkar',
                '❀': 'Jalan Tol',
                '✾': 'Jalan Layang'
            }
            
            for symbol, value in GEO_SYMBOLS['RAIL_KEYS'].items():
                rail_data.append({
                    'Simbol Jalan': symbol,
                    'Jumlah Rail': value,
                    'Deskripsi': descriptions.get(symbol, 'Pola Jalan')
                })
            
            rail_df = pd.DataFrame(rail_data)
            st.dataframe(rail_df, use_container_width=True, hide_index=True)
        
        with tab_guide3:
            st.markdown("### Konversi Huruf ke Simbol")
            
            letter_data = []
            descriptions = {
                'A': 'Kota Besar', 'B': 'Gunung Non Aktif', 'C': 'Dataran Rendah',
                'D': 'Lembah', 'E': 'Sungai', 'F': 'Jalan Raya',
                'G': 'Hutan', 'H': 'Pelabuhan', 'I': 'Danau',
                'J': 'Rel Kereta Api', 'K': 'Gunung Aktif', 'L': 'Batas Negara',
                'M': 'Bendungan', 'N': 'Air Terjun', 'O': 'Rawa',
                'P': 'Rumah Sakit', 'Q': 'Bandara', 'R': 'Tempat Ibadah',
                'S': 'Kantor Pos', 'T': 'Daerah Berbahaya', 'U': 'Laut',
                'V': 'Pantai', 'W': 'Pemukiman', 'X': 'Ibu Kota',
                'Y': 'Kota Kecil', 'Z': 'Bukit'
            }
            
            for letter, symbol in GEO_SYMBOLS['LETTER_SYMBOLS'].items():
                letter_data.append({
                    'Huruf': letter,
                    'Simbol': symbol,
                    'Deskripsi': descriptions.get(letter, 'Geografi'),
                    'Posisi': ord(letter) - 64
                })
            
            letter_df = pd.DataFrame(letter_data)
            st.dataframe(letter_df, use_container_width=True, hide_index=True)
            
            # Testing tool khusus untuk KRIPTOGRAFI
            st.markdown("---")
            st.subheader("🧪 Testing Tool: KRIPTOGRAFI")
            
            test_col1, test_col2 = st.columns(2)
            
            with test_col1:
                if st.button("Test Konversi KRIPTOGRAFI", use_container_width=True):
                    test_symbols = text_to_geo_symbols("KRIPTOGRAFI")
                    st.session_state.test_symbols = test_symbols
                    st.info(f"Simbol: {test_symbols}")
            
            with test_col2:
                if st.button("Test Dekripsi KRIPTOGRAFI", use_container_width=True):
                    if 'test_symbols' in st.session_state:
                        test_back = geo_symbols_to_text(st.session_state.test_symbols)
                        if test_back == "KRIPTOGRAFI":
                            st.success(f"✅ Berhasil! Hasil: {test_back}")
                        else:
                            st.error(f"❌ Gagal! Hasil: {test_back}")
                    else:
                        st.warning("Lakukan konversi terlebih dahulu")

# ========== MENJALANKAN APLIKASI ==========
if __name__ == "__main__":
    main()
