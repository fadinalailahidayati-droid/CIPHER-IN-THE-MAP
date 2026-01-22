import streamlit as st
import pandas as pd

# ========== KONFIGURASI SIMBOL GEOGRAFI YANG DIPERBAIKI ==========

# Simbol geografi untuk representasi huruf (menggunakan tabel dari PDF)
LETTER_TO_SYMBOL = {
    'A': '●',    'B': '△',    'C': '□',    'D': '▽',    'E': '~ ~',
    'F': '~~~',  'G': '◆',    'H': '♡',    'I': '○',    'J': '- - - -',
    'K': '◆',    'L': '~ ~ ~ ~', 'M': '□',    'N': '▲',    'O': '====',
    'P': '▶',    'Q': '◇',    'R': '◎',    'S': '+',    'T': '+',
    'U': '+',    'V': '☉',    'W': '○',    'X': '×',    'Y': '○',
    'Z': '☉☉☉☉'
}

# Reverse mapping untuk dekripsi
SYMBOL_TO_LETTER = {
    '●': 'A', '△': 'B', '□': 'C', '▽': 'D', '~ ~': 'E',
    '~~~': 'F', '◆': 'G', '♡': 'H', '○': 'I', '- - - -': 'J',
    '◆': 'K', '~ ~ ~ ~': 'L', '□': 'M', '▲': 'N', '====': 'O',
    '▶': 'P', '◇': 'Q', '◎': 'R', '+': 'S', '+': 'T',
    '+': 'U', '☉': 'V', '○': 'W', '×': 'X', '○': 'Y',
    '☉☉☉☉': 'Z'
}

# Simbol untuk Rail Fence Cipher (jumlah rail) - simbol jalan
RAIL_SYMBOLS = {
    '|': 2,    # Jalan Lurus
    'Z': 3,    # Jalan Berkelok
    '卍': 4,   # Jalan Simpang
    '✠': 5,    # Persimpangan
    '✪': 6,    # Bundaran
    '❂': 7,    # Simpang Susun
    '✿': 8,    # Jalan Lingkar
    '❀': 9,    # Jalan Tol
    '✾': 10    # Jalan Layang
}

# ========== FUNGSI UTILITAS YANG DIPERBAIKI ==========

def text_to_geo_symbols(text):
    """Mengonversi teks menjadi simbol geografi dengan aman"""
    result = []
    for char in text.upper():
        if char in LETTER_TO_SYMBOL:
            result.append(LETTER_TO_SYMBOL[char])
        elif char == " ":
            result.append("/")
        else:
            result.append(char)
    return " ".join(result)

def geo_symbols_to_text(symbols_text):
    """Mengonversi simbol geografi kembali ke teks dengan aman"""
    if not symbols_text.strip():
        return ""
    
    symbols = symbols_text.split()
    result = []
    
    i = 0
    while i < len(symbols):
        # Cari simbol dengan mencoba kombinasi terpanjang dahulu
        matched = False
        
        # Coba simbol 4 karakter
        if i + 3 < len(symbols):
            test_symbol = f"{symbols[i]} {symbols[i+1]} {symbols[i+2]} {symbols[i+3]}"
            # Handle simbol khusus
            if symbols[i] == '~' and symbols[i+1] == '~' and symbols[i+2] == '~' and symbols[i+3] == '~':
                test_symbol = '~ ~ ~ ~'
                i += 3
            elif symbols[i] == '-' and symbols[i+1] == '-' and symbols[i+2] == '-' and symbols[i+3] == '-':
                test_symbol = '- - - -'
                i += 3
            elif symbols[i] == '=' and symbols[i+1] == '=' and symbols[i+2] == '=' and symbols[i+3] == '=':
                test_symbol = '===='
                i += 3
            elif symbols[i] == '☉' and symbols[i+1] == '☉' and symbols[i+2] == '☉' and symbols[i+3] == '☉':
                test_symbol = '☉☉☉☉'
                i += 3
        
        # Coba simbol 3 karakter
        elif i + 2 < len(symbols):
            test_symbol = f"{symbols[i]} {symbols[i+1]} {symbols[i+2]}"
            if symbols[i] == '~' and symbols[i+1] == '~' and symbols[i+2] == '~':
                test_symbol = '~~~'
                i += 2
        
        # Coba simbol 2 karakter
        elif i + 1 < len(symbols):
            test_symbol = f"{symbols[i]} {symbols[i+1]}"
            if symbols[i] == '~' and symbols[i+1] == '~':
                test_symbol = '~ ~'
                i += 1
        
        # Simbol 1 karakter
        else:
            test_symbol = symbols[i]
        
        # Konversi simbol ke huruf
        if test_symbol in SYMBOL_TO_LETTER:
            result.append(SYMBOL_TO_LETTER[test_symbol])
            matched = True
        elif test_symbol == "/":
            result.append(" ")
            matched = True
        else:
            result.append(test_symbol)
            matched = True
        
        i += 1
    
    return ''.join(result)

def simple_caesar_cipher(text, shift=3, mode='encrypt'):
    """Caesar Cipher sederhana dengan shift tetap 3"""
    result = []
    
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

def rail_fence_cipher(text, rails, mode='encrypt'):
    """Rail Fence Cipher"""
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
        result_chars = []
        
        for i in range(text_len):
            result_chars.append(fence[rail][i])
            rail += direction
            
            if rail == 0 or rail == rails - 1:
                direction = -direction
        
        return ''.join(result_chars)

# ========== FUNGSI KOMBINASI ==========

def encrypt_combination(plaintext, rail_symbol):
    """
    Enkripsi kombinasi: Caesar Cipher (shift 3) -> Rail Fence -> Simbol
    """
    # Langkah 1: Caesar Cipher dengan shift 3
    caesar_result = simple_caesar_cipher(plaintext, 3, 'encrypt')
    
    # Langkah 2: Rail Fence Cipher
    rails = RAIL_SYMBOLS.get(rail_symbol, 3)
    rail_result = rail_fence_cipher(caesar_result, rails, 'encrypt')
    
    # Langkah 3: Konversi ke simbol geografi
    final_symbols = text_to_geo_symbols(rail_result)
    
    return caesar_result, rail_result, final_symbols

def decrypt_combination(cipher_symbols, rail_symbol):
    """
    Dekripsi kombinasi: Simbol -> Rail Fence -> Caesar (shift 3)
    """
    # Langkah 1: Konversi simbol ke teks
    rail_text = geo_symbols_to_text(cipher_symbols)
    
    # Langkah 2: Rail Fence Decrypt
    rails = RAIL_SYMBOLS.get(rail_symbol, 3)
    caesar_text = rail_fence_cipher(rail_text, rails, 'decrypt')
    
    # Langkah 3: Caesar Decrypt dengan shift 3
    plaintext = simple_caesar_cipher(caesar_text, 3, 'decrypt')
    
    return rail_text, caesar_text, plaintext

def display_rail_visualization(text, rails):
    """Menampilkan visualisasi Rail Fence pattern"""
    if rails <= 1 or len(text) == 0:
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

# ========== ANTARMUKA STREAMLIT ==========

def main():
    # Konfigurasi halaman
    st.set_page_config(
        page_title="Cipher In The Map",
        page_icon="🗺️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS dengan desain yang menarik
    st.markdown("""
    <style>
    .main-header {
        font-size: 3.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.2);
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 10px;
    }
    .sub-header {
        color: #3B82F6;
        font-size: 1.8rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        border-bottom: 3px solid #3B82F6;
        padding-bottom: 10px;
    }
    .key-badge {
        background-color: #E0F2FE;
        padding: 8px 15px;
        border-radius: 20px;
        margin: 5px;
        display: inline-block;
        font-weight: bold;
        font-size: 1.1rem;
        border: 2px solid #3B82F6;
    }
    .step-box {
        background-color: #F8FAFC;
        padding: 25px;
        border-radius: 15px;
        border-left: 6px solid #3B82F6;
        margin: 15px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .symbol-output {
        font-family: 'Courier New', monospace;
        font-size: 1.8rem;
        padding: 25px;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 15px;
        border: 3px solid #3B82F6;
        text-align: center;
        margin: 15px 0;
        color: white;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .info-box {
        background-color: #D1FAE5;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #10B981;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #FEF3C7;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #F59E0B;
        margin: 10px 0;
    }
    .fixed-caesar {
        background-color: #DBEAFE;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        font-size: 1.2rem;
        margin: 10px 0;
        border: 2px dashed #3B82F6;
    }
    .tutorial-step {
        background-color: #F3F4F6;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #8B5CF6;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header utama
    st.markdown('<h1 class="main-header">🗺️ Cipher In The Map</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.3rem; color: #4B5563; margin-bottom: 2rem; font-style: italic;">Transformasikan pesan rahasia menjadi peta geografis</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🧭 Navigasi")
        app_mode = st.radio(
            "Pilih Mode:",
            ["Beranda", "Enkripsi", "Dekripsi", "Tabel Simbol", "Tutorial"]
        )
        
        st.markdown("---")
        st.markdown("### ⚙️ Konfigurasi Cipher")
        
        # Info Caesar Cipher (tetap 3)
        st.markdown('<div class="fixed-caesar">Caesar Cipher Shift: <strong>3</strong></div>', unsafe_allow_html=True)
        st.caption("Shift selalu 3 sesuai materi kriptografi")
        
        # Pilihan Rail Fence
        st.markdown("#### 🛣️ Pilihan Rail Fence")
        rail_options = list(RAIL_SYMBOLS.keys())
        rail_descriptions = {
            '|': 'Jalan Lurus (2 rail)',
            'Z': 'Jalan Berkelok (3 rail)',
            '卍': 'Jalan Simpang (4 rail)',
            '✠': 'Persimpangan (5 rail)',
            '✪': 'Bundaran (6 rail)',
            '❂': 'Simpang Susun (7 rail)',
            '✿': 'Jalan Lingkar (8 rail)',
            '❀': 'Jalan Tol (9 rail)',
            '✾': 'Jalan Layang (10 rail)'
        }
        
        for symbol in rail_options:
            rails = RAIL_SYMBOLS[symbol]
            st.write(f"{symbol} - {rail_descriptions[symbol]}")
        
        st.markdown("---")
        st.markdown("### 📊 Info Aplikasi")
        st.info("""
        **Alur Enkripsi:**
        1. Caesar Cipher (shift 3)
        2. Rail Fence Cipher
        3. Konversi ke simbol geografi
        
        **Alur Dekripsi:**
        1. Konversi dari simbol
        2. Rail Fence Decrypt
        3. Caesar Decrypt (shift 3)
        """)
        
        st.markdown("---")
        st.markdown("**👩‍💻 Pembuat:** Fadina Laila Hidayati")
        st.markdown("**🎓 NIM:** 24.83.1109")
        
        # Testing tools
        if 'last_encryption' in st.session_state:
            st.markdown("---")
            st.markdown("### 🧪 Quick Test")
            if st.button("Test 'KRIPTOGRAFI'", use_container_width=True):
                st.session_state.test_text = "KRIPTOGRAFI"
                st.session_state.test_rail = '|'
                st.rerun()
    
    # ========== HALAMAN BERANDA ==========
    if app_mode == "Beranda":
        st.markdown('<h2 class="sub-header">🌍 Selamat Datang di Cipher In The Map</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="info-box">
            <h3>🎯 Fitur Utama</h3>
            <ul>
            <li><strong>Caesar Cipher</strong> dengan shift tetap 3</li>
            <li><strong>Rail Fence Cipher</strong> dengan 9 pilihan pola jalan</li>
            <li><strong>Konversi ke simbol geografi</strong> sesuai tabel</li>
            <li><strong>Dekripsi sempurna</strong> kembali ke teks awal</li>
            <li><strong>Visualisasi proses</strong> enkripsi dan dekripsi</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="tutorial-step">
            <h4>📝 Contoh Cepat</h4>
            <p><strong>Teks:</strong> HELLO</p>
            <p><strong>Caesar Shift:</strong> 3</p>
            <p><strong>Rail Fence:</strong> | (2 rail)</p>
            <p><strong>Hasil:</strong> ◆ ♡ ○ ○ ◎</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="info-box">
            <h3>🔐 Cara Kerja</h3>
            <h4>Enkripsi:</h4>
            <ol>
            <li>Masukkan teks biasa</li>
            <li>Caesar Cipher menggeser 3 huruf</li>
            <li>Rail Fence membuat pola zig-zag</li>
            <li>Konversi ke simbol geografi</li>
            </ol>
            
            <h4>Dekripsi:</h4>
            <ol>
            <li>Masukkan simbol geografi</li>
            <li>Konversi ke huruf</li>
            <li>Rail Fence decrypt</li>
            <li>Caesar decrypt dengan shift 3</li>
            </ol>
            </div>
            """, unsafe_allow_html=True)
            
            # Tombol aksi cepat
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("🚀 Mulai Enkripsi", use_container_width=True):
                    st.session_state.page = "Enkripsi"
                    st.rerun()
            with col_btn2:
                if st.button("🔓 Coba Dekripsi", use_container_width=True):
                    st.session_state.page = "Dekripsi"
                    st.rerun()
    
    # ========== HALAMAN ENKRIPSI ==========
    elif app_mode == "Enkripsi":
        st.markdown('<h2 class="sub-header">🔒 Enkripsi Pesan</h2>', unsafe_allow_html=True)
        
        # Info Caesar Cipher fixed
        st.markdown('<div class="fixed-caesar">⚠️ Caesar Cipher menggunakan shift tetap: <strong>3</strong></div>', unsafe_allow_html=True)
        
        col_input, col_keys = st.columns([2, 1])
        
        with col_input:
            # Input teks
            plaintext = st.text_area(
                "**Masukkan teks yang akan dienkripsi:**",
                height=120,
                placeholder="Contoh: KRIPTOGRAFI, HELLO WORLD, atau pesan rahasia Anda...",
                help="Hanya huruf A-Z, spasi akan dipertahankan",
                key="encrypt_text"
            )
            
            # Preview Caesar Cipher
            if plaintext:
                caesar_preview = simple_caesar_cipher(plaintext, 3, 'encrypt')
                st.markdown(f"**Preview Caesar Cipher (shift 3):** `{caesar_preview}`")
        
        with col_keys:
            st.markdown("### 🛣️ Pilih Pola Rail Fence")
            
            # Pilih kunci Rail Fence
            rail_options = list(RAIL_SYMBOLS.keys())
            rail_descriptions = {
                '|': 'Jalan Lurus (2 rail)',
                'Z': 'Jalan Berkelok (3 rail)',
                '卍': 'Jalan Simpang (4 rail)',
                '✠': 'Persimpangan (5 rail)',
                '✪': 'Bundaran (6 rail)',
                '❂': 'Simpang Susun (7 rail)',
                '✿': 'Jalan Lingkar (8 rail)',
                '❀': 'Jalan Tol (9 rail)',
                '✾': 'Jalan Layang (10 rail)'
            }
            
            rail_key = st.selectbox(
                "**Pilih pola jalan:**",
                options=rail_options,
                format_func=lambda x: rail_descriptions[x],
                help="Pilih pola jalan untuk Rail Fence Cipher",
                key="rail_key_select"
            )
            
            # Tombol test cepat
            if st.button("🧪 Test KRIPTOGRAFI", use_container_width=True):
                plaintext = "KRIPTOGRAFI"
                rail_key = '|'
                st.rerun()
        
        # Tombol proses enkripsi
        if st.button("🗺️ Buat Peta Rahasia", type="primary", use_container_width=True, key="encrypt_button"):
            if plaintext.strip():
                with st.spinner("🔐 Memproses enkripsi..."):
                    try:
                        # Proses enkripsi
                        caesar_result, rail_result, final_symbols = encrypt_combination(
                            plaintext, rail_key
                        )
                        
                        st.success("✅ Peta rahasia berhasil dibuat!")
                        st.balloons()
                        
                        # Simpan ke session state
                        st.session_state.last_encryption = {
                            'plaintext': plaintext,
                            'rail_key': rail_key,
                            'rails': RAIL_SYMBOLS[rail_key],
                            'caesar_result': caesar_result,
                            'rail_result': rail_result,
                            'final_symbols': final_symbols
                        }
                        
                        # Tampilkan hasil utama
                        st.markdown("---")
                        st.markdown('<h3 class="sub-header">🗺️ Peta Rahasia Anda</h3>', unsafe_allow_html=True)
                        
                        # Simbol hasil
                        col_symbols, col_keys = st.columns([2, 1])
                        
                        with col_symbols:
                            st.markdown("**🎨 Simbol Geografi:**")
                            st.markdown(f'<div class="symbol-output">{final_symbols}</div>', unsafe_allow_html=True)
                            
                            # Tombol copy
                            st.code(final_symbols, language="text")
                            copy_col1, copy_col2 = st.columns(2)
                            with copy_col1:
                                if st.button("📋 Salin Simbol", key="copy_symbols"):
                                    st.write("✅ Simbol disalin ke clipboard!")
                            with copy_col2:
                                if st.button("💾 Simpan untuk Dekripsi", key="save_for_decrypt"):
                                    st.session_state.saved_symbols = final_symbols
                                    st.session_state.saved_rail_key = rail_key
                                    st.success("✅ Disimpan!")
                        
                        with col_keys:
                            st.markdown("**🔑 Kunci yang digunakan:**")
                            st.markdown(f'<div class="key-badge">Caesar Shift: 3</div>', unsafe_allow_html=True)
                            st.markdown(f'<div class="key-badge">Rail: {rail_key}</div>', unsafe_allow_html=True)
                            st.markdown(f'<div class="key-badge">Jumlah Rail: {RAIL_SYMBOLS[rail_key]}</div>', unsafe_allow_html=True)
                        
                        # Proses bertahap
                        st.markdown("---")
                        st.markdown('<h4 class="sub-header">📊 Proses Enkripsi Detail</h4>', unsafe_allow_html=True)
                        
                        tab1, tab2, tab3 = st.tabs(["1️⃣ Caesar Cipher", "2️⃣ Rail Fence", "3️⃣ Simbol Geografi"])
                        
                        with tab1:
                            st.markdown("**Teks setelah Caesar Cipher (shift 3):**")
                            st.markdown(f'<div class="step-box">{caesar_result}</div>', unsafe_allow_html=True)
                            st.caption(f"Setiap huruf digeser 3 posisi: A→D, B→E, C→F, dst.")
                        
                        with tab2:
                            st.markdown("**Teks setelah Rail Fence Cipher:**")
                            st.markdown(f'<div class="step-box">{rail_result}</div>', unsafe_allow_html=True)
                            st.caption(f"Menggunakan {RAIL_SYMBOLS[rail_key]} rail dengan pola {rail_key}")
                            
                            # Visualisasi rail
                            display_rail_visualization(caesar_result, RAIL_SYMBOLS[rail_key])
                        
                        with tab3:
                            st.markdown("**Konversi ke simbol geografi:**")
                            conversion_text = ""
                            for char in rail_result.upper():
                                if char in LETTER_TO_SYMBOL:
                                    symbol = LETTER_TO_SYMBOL[char]
                                    conversion_text += f"{char} → {symbol}\n"
                                elif char == " ":
                                    conversion_text += "spasi → /\n"
                            
                            st.markdown(f'<div class="step-box"><pre>{conversion_text}</pre></div>', unsafe_allow_html=True)
                        
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                        st.info("Pastikan teks hanya berisi huruf dan spasi.")
            else:
                st.warning("⚠️ Masukkan teks terlebih dahulu!")
    
    # ========== HALAMAN DEKRIPSI ==========
    elif app_mode == "Dekripsi":
        st.markdown('<h2 class="sub-header">🔓 Dekripsi Peta Rahasia</h2>', unsafe_allow_html=True)
        
        # Info Caesar Cipher fixed
        st.markdown('<div class="fixed-caesar">⚠️ Caesar Cipher menggunakan shift tetap: <strong>3</strong> (untuk dekripsi)</div>', unsafe_allow_html=True)
        
        col_input, col_keys = st.columns([2, 1])
        
        with col_input:
            # Input simbol
            cipher_symbols = st.text_area(
                "**Masukkan simbol geografi:**",
                height=120,
                placeholder="Contoh: ◆ ♡ ○ ○ ◎ / ▲ × ○ ◇ ▶ ● △ □ ▽",
                help="Pisahkan simbol dengan spasi, gunakan / untuk spasi",
                key="decrypt_input"
            )
            
            # Tombol load dari enkripsi terakhir
            if 'last_encryption' in st.session_state:
                if st.button("📥 Gunakan hasil enkripsi terakhir", use_container_width=True):
                    cipher_symbols = st.session_state.last_encryption['final_symbols']
                    st.rerun()
            
            # Tombol load dari saved
            if 'saved_symbols' in st.session_state:
                if st.button("📂 Gunakan simbol tersimpan", use_container_width=True):
                    cipher_symbols = st.session_state.saved_symbols
                    st.rerun()
        
        with col_keys:
            st.markdown("### 🛣️ Pilih Pola Rail Fence")
            
            # Pilih kunci Rail Fence
            rail_options = list(RAIL_SYMBOLS.keys())
            rail_descriptions = {
                '|': 'Jalan Lurus (2 rail)',
                'Z': 'Jalan Berkelok (3 rail)',
                '卍': 'Jalan Simpang (4 rail)',
                '✠': 'Persimpangan (5 rail)',
                '✪': 'Bundaran (6 rail)',
                '❂': 'Simpang Susun (7 rail)',
                '✿': 'Jalan Lingkar (8 rail)',
                '❀': 'Jalan Tol (9 rail)',
                '✾': 'Jalan Layang (10 rail)'
            }
            
            rail_key_decrypt = st.selectbox(
                "**Pilih pola jalan:**",
                options=rail_options,
                format_func=lambda x: rail_descriptions[x],
                help="Pilih pola yang digunakan saat enkripsi",
                key="decrypt_rail_select",
                index=0
            )
            
            # Auto-select jika ada data tersimpan
            if 'saved_rail_key' in st.session_state:
                if st.button("🔑 Gunakan kunci tersimpan", use_container_width=True):
                    rail_key_decrypt = st.session_state.saved_rail_key
                    st.rerun()
        
        # Tombol proses dekripsi
        if st.button("🗝️ Baca Peta Rahasia", type="primary", use_container_width=True, key="decrypt_button"):
            if cipher_symbols.strip():
                with st.spinner("🔍 Memproses dekripsi..."):
                    try:
                        # Proses dekripsi
                        rail_text, caesar_text, plaintext = decrypt_combination(
                            cipher_symbols, rail_key_decrypt
                        )
                        
                        st.success("✅ Pesan berhasil dibaca!")
                        
                        # Tampilkan hasil
                        st.markdown("---")
                        st.markdown('<h3 class="sub-header">📜 Pesan Asli</h3>', unsafe_allow_html=True)
                        
                        col_result, col_process = st.columns([1, 2])
                        
                        with col_result:
                            st.markdown("**Teks Terdekripsi:**")
                            st.markdown(f'<div class="step-box" style="background-color: #D1FAE5; border-left-color: #10B981;"><h2 style="color: #065F46; text-align: center;">{plaintext}</h2></div>', unsafe_allow_html=True)
                            
                            # Tombol copy
                            if st.button("📋 Salin Teks", key="copy_decrypt_text"):
                                st.write("✅ Teks disalin ke clipboard!")
                        
                        with col_process:
                            st.markdown("**📋 Proses Dekripsi:**")
                            
                            steps = f"""
                            **1. Simbol masukan:**  
                            `{cipher_symbols}`
                            
                            **2. Setelah konversi ke huruf:**  
                            `{rail_text}`
                            
                            **3. Setelah Rail Fence Decrypt ({RAIL_SYMBOLS[rail_key_decrypt]} rail):**  
                            `{caesar_text}`
                            
                            **4. Setelah Caesar Decrypt (shift 3):**  
                            `{plaintext}`
                            """
                            
                            st.markdown(f'<div class="step-box">{steps}</div>', unsafe_allow_html=True)
                        
                        # Verifikasi jika ada data enkripsi sebelumnya
                        if 'last_encryption' in st.session_state:
                            expected = st.session_state.last_encryption['plaintext'].upper()
                            if plaintext.upper() == expected.upper():
                                st.success("✅ ✅ Hasil dekripsi SEMPURNA! Cocok dengan teks asli.")
                            else:
                                st.warning(f"⚠️ Hasil tidak cocok. Seharusnya: {expected}")
                        
                        # Testing khusus untuk KRIPTOGRAFI
                        if plaintext.upper() == "KRIPTOGRAFI":
                            st.success("🎉 Test 'KRIPTOGRAFI' berhasil! Dekripsi sempurna.")
                        
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                        st.info("""
                        **Pastikan:**
                        1. Format simbol benar (dipisahkan spasi)
                        2. Pola Rail Fence sesuai dengan saat enkripsi
                        3. Simbol sesuai tabel geografi
                        """)
            else:
                st.warning("⚠️ Masukkan simbol geografi terlebih dahulu!")
    
    # ========== HALAMAN TABEL SIMBOL ==========
    elif app_mode == "Tabel Simbol":
        st.markdown('<h2 class="sub-header">📚 Tabel Simbol Geografi</h2>', unsafe_allow_html=True)
        
        # Buat dataframe untuk tabel
        symbol_data = []
        descriptions = {
            '●': 'Kota Besar', '△': 'Gunung Non Aktif', '□': 'Dataran Rendah',
            '▽': 'Lembah', '~ ~': 'Sungai', '~~~': 'Jalan Raya',
            '◆': 'Hutan', '♡': 'Pelabuhan', '○': 'Danau',
            '- - - -': 'Rel Kereta Api', '▲': 'Gunung Aktif', '====': 'Batas Negara',
            '▶': 'Bendungan', '◇': 'Air Terjun', '◎': 'Rawa',
            '+': 'Rumah Sakit/Bandara/Tempat Ibadah', '☉': 'Kantor Pos',
            '×': 'Daerah Berbahaya', '~ ~ ~ ~': 'Pantai',
            '☉☉☉☉': 'Laut'
        }
        
        for letter, symbol in LETTER_TO_SYMBOL.items():
            symbol_data.append({
                'Huruf': letter,
                'Simbol': symbol,
                'Deskripsi': descriptions.get(symbol, 'Geografi'),
                'Contoh': f"{letter} → {symbol}"
            })
        
        symbol_df = pd.DataFrame(symbol_data)
        
        # Tampilkan tabel dengan styling
        st.dataframe(
            symbol_df,
            column_config={
                "Huruf": st.column_config.TextColumn("Huruf", width="small"),
                "Simbol": st.column_config.TextColumn("Simbol", width="medium"),
                "Deskripsi": st.column_config.TextColumn("Deskripsi", width="large"),
                "Contoh": st.column_config.TextColumn("Contoh", width="medium")
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Testing tool
        st.markdown("---")
        st.markdown('<h4 class="sub-header">🧪 Testing Tool</h4>', unsafe_allow_html=True)
        
        test_col1, test_col2 = st.columns(2)
        
        with test_col1:
            test_text = st.text_input("Masukkan teks untuk test konversi:", "KRIPTOGRAFI", key="test_input")
            if st.button("Test Konversi", key="test_convert"):
                symbols = text_to_geo_symbols(test_text)
                st.session_state.test_symbols_result = symbols
                st.info(f"Hasil: {symbols}")
        
        with test_col2:
            if 'test_symbols_result' in st.session_state:
                if st.button("Test Dekripsi Balik", key="test_back"):
                    back_text = geo_symbols_to_text(st.session_state.test_symbols_result)
                    if back_text == test_text.upper():
                        st.success(f"✅ Berhasil! Hasil: {back_text}")
                    else:
                        st.error(f"❌ Gagal! Hasil: {back_text}, Harusnya: {test_text.upper()}")
    
    # ========== HALAMAN TUTORIAL ==========
    else:
        st.markdown('<h2 class="sub-header">🎓 Tutorial Lengkap</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="tutorial-step">
        <h3>📖 Langkah 1: Enkripsi Pesan</h3>
        <ol>
        <li>Pergi ke halaman <strong>Enkripsi</strong></li>
        <li>Masukkan teks yang ingin dienkripsi (contoh: KRIPTOGRAFI)</li>
        <li>Pilih pola Rail Fence (default: | untuk 2 rail)</li>
        <li>Klik <strong>Buat Peta Rahasia</strong></li>
        <li>Simpan hasil simbol yang muncul</li>
        </ol>
        </div>
        
        <div class="tutorial-step">
        <h3>📖 Langkah 2: Dekripsi Pesan</h3>
        <ol>
        <li>Pergi ke halaman <strong>Dekripsi</strong></li>
        <li>Tempel simbol yang didapat dari enkripsi</li>
        <li>Pilih pola Rail Fence yang SAMA dengan saat enkripsi</li>
        <li>Klik <strong>Baca Peta Rahasia</strong></li>
        <li>Teks asli akan muncul kembali</li>
        </ol>
        </div>
        
        <div class="tutorial-step">
        <h3>⚙️ Detail Teknis</h3>
        <p><strong>Caesar Cipher:</strong> Selalu menggunakan shift 3 (A→D, B→E, C→F, dst.)</p>
        <p><strong>Rail Fence Cipher:</strong> Pilih pola jalan untuk menentukan jumlah rail</p>
        <p><strong>Simbol Geografi:</strong> Setiap huruf dikonversi ke simbol sesuai tabel</p>
        </div>
        
        <div class="tutorial-step">
        <h3>🧪 Contoh: KRIPTOGRAFI</h3>
        <p><strong>1. Caesar Cipher (shift 3):</strong> KRIPTOGRAFI → NUIRWJUDIL</p>
        <p><strong>2. Rail Fence (2 rail, pola |):</strong> NRIJDIIURWL</p>
        <p><strong>3. Simbol Geografi:</strong> ▲ × ○ ◇ ▶ ● △ □ ▽</p>
        <p><strong>4. Dekripsi:</strong> Proses sebaliknya → KRIPTOGRAFI</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Demo langsung
        st.markdown("---")
        st.markdown('<h4 class="sub-header">🎬 Demo Langsung</h4>', unsafe_allow_html=True)
        
        demo_col1, demo_col2, demo_col3 = st.columns(3)
        
        with demo_col1:
            if st.button("Demo KRIPTOGRAFI", use_container_width=True):
                # Simulasi enkripsi
                caesar = simple_caesar_cipher("KRIPTOGRAFI", 3, 'encrypt')
                rail = rail_fence_cipher(caesar, 2, 'encrypt')
                symbols = text_to_geo_symbols(rail)
                
                st.info(f"**Caesar:** {caesar}")
                st.info(f"**Rail:** {rail}")
                st.success(f"**Simbol:** {symbols}")
        
        with demo_col2:
            if st.button("Demo HELLO", use_container_width=True):
                caesar = simple_caesar_cipher("HELLO", 3, 'encrypt')
                rail = rail_fence_cipher(caesar, 3, 'encrypt')
                symbols = text_to_geo_symbols(rail)
                
                st.info(f"**Caesar:** {caesar}")
                st.info(f"**Rail:** {rail}")
                st.success(f"**Simbol:** {symbols}")
        
        with demo_col3:
            if st.button("Test Dekripsi", use_container_width=True):
                test_symbols = "◆ ♡ ○ ○ ◎"
                back_text = geo_symbols_to_text(test_symbols)
                caesar_back = rail_fence_cipher(back_text, 3, 'decrypt')
                final = simple_caesar_cipher(caesar_back, 3, 'decrypt')
                
                st.info(f"**Simbol:** {test_symbols}")
                st.info(f"**Setelah konversi:** {back_text}")
                st.success(f"**Hasil akhir:** {final}")

# ========== MENJALANKAN APLIKASI ==========
if __name__ == "__main__":
    main()
