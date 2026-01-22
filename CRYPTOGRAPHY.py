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
    
    # Debug info
    debug_info = f"Setelah konversi simbol: '{rail_text}'"
    
    # Langkah 2: Rail Fence Decrypt
    caesar_text = rail_fence_cipher_geo(rail_text, rail_key_symbol, 'decrypt')
    
    # Debug info
    debug_info += f"\nSetelah Rail decrypt: '{caesar_text}'"
    
    # Langkah 3: Caesar Decrypt
    plaintext = caesar_cipher_geo(caesar_text, caesar_key_symbol, 'decrypt')
    
    return rail_text, caesar_text, plaintext, debug_info

# ========== ANTARMUKA STREAMLIT ==========

def main():
    # Konfigurasi halaman
    st.set_page_config(
        page_title="Cipher In The Map",
        page_icon="🗺️",
        layout="wide"
    )
    
    # Custom CSS sederhana
    st.markdown("""
    <style>
    .main-title {
        color: #1E3A8A;
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3em;
        font-weight: bold;
    }
    .symbol-display {
        font-family: 'Courier New', monospace;
        font-size: 1.2em;
        background-color: #f0f8ff;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #3B82F6;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-title">🗺️ Cipher In The Map</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666; font-size: 1.2em;">Transformasikan teks menjadi peta rahasia geografis</p>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("🧭 Navigasi")
    app_mode = st.sidebar.radio(
        "Pilih Mode:",
        ["Enkripsi", "Dekripsi", "Tabel Simbol"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info("""
    **Cara kerja:**
    1. Caesar Cipher dengan simbol geografi
    2. Rail Fence Cipher dengan simbol jalan
    3. Hasil: Peta simbol geografi
    """)
    
    # ========== HALAMAN ENKRIPSI ==========
    if app_mode == "Enkripsi":
        st.header("🔒 Enkripsi Pesan")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            plaintext = st.text_area(
                "Masukkan teks:",
                height=100,
                placeholder="Contoh: KRIPTOGRAFI",
                key="encrypt_input"
            )
            
            if plaintext:
                st.info(f"Panjang teks: {len(plaintext)} karakter")
        
        with col2:
            st.subheader("🗝️ Pilih Kunci")
            
            # Kunci Caesar
            caesar_keys = list(GEO_SYMBOLS['CAESAR_KEYS'].keys())[:10]
            caesar_key = st.selectbox(
                "Kunci Caesar:",
                options=caesar_keys,
                index=0,
                format_func=lambda x: f"{x} (shift {GEO_SYMBOLS['CAESAR_KEYS'][x]})"
            )
            
            # Kunci Rail
            rail_keys = list(GEO_SYMBOLS['RAIL_KEYS'].keys())
            rail_key = st.selectbox(
                "Kunci Rail Fence:",
                options=rail_keys,
                index=0,
                format_func=lambda x: f"{x} ({GEO_SYMBOLS['RAIL_KEYS'][x]} rail)"
            )
        
        # Tombol enkripsi
        if st.button("🚀 Enkripsi Sekarang", type="primary", use_container_width=True):
            if plaintext:
                with st.spinner("Memproses enkripsi..."):
                    try:
                        caesar_result, rail_result, final_symbols = encrypt_combination_geo(
                            plaintext, caesar_key, rail_key
                        )
                        
                        st.success("✅ Enkripsi berhasil!")
                        
                        # Tampilkan hasil
                        st.markdown("---")
                        st.subheader("📋 Hasil Enkripsi")
                        
                        col_result, col_process = st.columns(2)
                        
                        with col_result:
                            st.markdown("**Peta Simbol:**")
                            st.markdown(f'<div class="symbol-display">{final_symbols}</div>', unsafe_allow_html=True)
                            
                            # Info kunci
                            st.markdown("**Kunci yang digunakan:**")
                            st.write(f"Caesar: {caesar_key} (shift {GEO_SYMBOLS['CAESAR_KEYS'][caesar_key]})")
                            st.write(f"Rail: {rail_key} ({GEO_SYMBOLS['RAIL_KEYS'][rail_key]} rail)")
                        
                        with col_process:
                            st.markdown("**Proses Enkripsi:**")
                            st.write(f"1. Teks asli: `{plaintext.upper()}`")
                            st.write(f"2. Setelah Caesar: `{caesar_result}`")
                            st.write(f"3. Setelah Rail Fence: `{rail_result}`")
                            st.write(f"4. Simbol akhir: `{final_symbols}`")
                        
                        # Simpan ke session state untuk testing
                        st.session_state.last_encryption = {
                            'plaintext': plaintext,
                            'caesar_key': caesar_key,
                            'rail_key': rail_key,
                            'symbols': final_symbols
                        }
                        
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
            else:
                st.warning("⚠️ Masukkan teks terlebih dahulu!")
        
        # Contoh
        with st.expander("📝 Contoh Enkripsi"):
            example_text = "HELLO"
            example_caesar = '●'
            example_rail = '|'
            
            caesar_ex, rail_ex, symbols_ex = encrypt_combination_geo(
                example_text, example_caesar, example_rail
            )
            
            st.write(f"**Teks:** {example_text}")
            st.write(f"**Kunci Caesar:** {example_caesar} (shift 1)")
            st.write(f"**Kunci Rail:** {example_rail} (2 rail)")
            st.write(f"**Hasil:** {symbols_ex}")
    
    # ========== HALAMAN DEKRIPSI ==========
    elif app_mode == "Dekripsi":
        st.header("🔓 Dekripsi Pesan")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            cipher_symbols = st.text_area(
                "Masukkan simbol geografi:",
                height=100,
                placeholder="Contoh: ▲ × ○ ◇ ▶ ● △ □ ▽",
                help="Pisahkan simbol dengan spasi"
            )
            
            # Tombol load contoh dari enkripsi terakhir
            if 'last_encryption' in st.session_state:
                if st.button("📥 Gunakan hasil enkripsi terakhir"):
                    cipher_symbols = st.session_state.last_encryption['symbols']
                    st.rerun()
        
        with col2:
            st.subheader("🗝️ Masukkan Kunci")
            
            # Kunci Caesar
            caesar_keys = list(GEO_SYMBOLS['CAESAR_KEYS'].keys())[:10]
            caesar_key_decrypt = st.selectbox(
                "Kunci Caesar:",
                options=caesar_keys,
                key="decrypt_caesar",
                index=0
            )
            
            # Kunci Rail
            rail_keys = list(GEO_SYMBOLS['RAIL_KEYS'].keys())
            rail_key_decrypt = st.selectbox(
                "Kunci Rail Fence:",
                options=rail_keys,
                key="decrypt_rail",
                index=0
            )
            
            # Mode debug
            show_debug = st.checkbox("Tampilkan proses debug")
        
        # Tombol dekripsi
        if st.button("🔍 Dekripsi Sekarang", type="primary", use_container_width=True):
            if cipher_symbols:
                with st.spinner("Memproses dekripsi..."):
                    try:
                        rail_text, caesar_text, plaintext, debug_info = decrypt_combination_geo(
                            cipher_symbols, caesar_key_decrypt, rail_key_decrypt
                        )
                        
                        st.success("✅ Dekripsi berhasil!")
                        
                        # Tampilkan hasil
                        st.markdown("---")
                        st.subheader("📜 Hasil Dekripsi")
                        
                        col_result, col_debug = st.columns(2)
                        
                        with col_result:
                            st.markdown("**Teks Terdekripsi:**")
                            st.markdown(f'<div class="symbol-display" style="background-color: #e6f7e6; border-left-color: #28a745;"><h3>{plaintext}</h3></div>', unsafe_allow_html=True)
                            
                            # Verifikasi
                            if 'last_encryption' in st.session_state:
                                expected = st.session_state.last_encryption['plaintext'].upper()
                                if plaintext == expected:
                                    st.success("✅ Cocok dengan teks asli!")
                                else:
                                    st.warning(f"⚠️ Tidak cocok. Seharusnya: {expected}")
                        
                        with col_debug:
                            if show_debug:
                                st.markdown("**Proses Dekripsi:**")
                                st.text(debug_info)
                                st.write(f"1. Dari simbol: `{cipher_symbols}`")
                                st.write(f"2. Setelah konversi: `{rail_text}`")
                                st.write(f"3. Setelah Rail decrypt: `{caesar_text}`")
                                st.write(f"4. Setelah Caesar decrypt: `{plaintext}`")
                        
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                        st.info("Pastikan format simbol dan kunci benar.")
            else:
                st.warning("⚠️ Masukkan simbol geografi terlebih dahulu!")
    
    # ========== HALAMAN TABEL SIMBOL ==========
    else:
        st.header("📚 Tabel Simbol Lengkap")
        
        tab1, tab2, tab3 = st.tabs(["🗺️ Simbol Geografi", "🛣️ Simbol Jalan", "🔤 Konversi Huruf"])
        
        with tab1:
            st.markdown("### Kunci Caesar Cipher")
            caesar_data = []
            for symbol, value in GEO_SYMBOLS['CAESAR_KEYS'].items():
                caesar_data.append({
                    'Simbol': symbol,
                    'Shift': value,
                    'Contoh': f"A → {chr((0 + value) % 26 + 65)}"
                })
            
            st.dataframe(pd.DataFrame(caesar_data), use_container_width=True, hide_index=True)
        
        with tab2:
            st.markdown("### Kunci Rail Fence Cipher")
            rail_data = []
            for symbol, value in GEO_SYMBOLS['RAIL_KEYS'].items():
                rail_data.append({
                    'Simbol': symbol,
                    'Jumlah Rail': value,
                    'Pola': 'Zig-zag'
                })
            
            st.dataframe(pd.DataFrame(rail_data), use_container_width=True, hide_index=True)
        
        with tab3:
            st.markdown("### Konversi Huruf ke Simbol")
            letter_data = []
            for letter, symbol in GEO_SYMBOLS['LETTER_SYMBOLS'].items():
                letter_data.append({
                    'Huruf': letter,
                    'Simbol': symbol,
                    'Deskripsi': f"Posisi {ord(letter) - 64}"
                })
            
            st.dataframe(pd.DataFrame(letter_data), use_container_width=True, hide_index=True)
            
            # Testing tool
            st.markdown("---")
            st.subheader("🔧 Testing Konversi")
            test_text = st.text_input("Masukkan teks untuk testing:", "KRIPTOGRAFI")
            
            if test_text:
                symbols = text_to_geo_symbols(test_text)
                back_text = geo_symbols_to_text(symbols)
                
                col_test1, col_test2 = st.columns(2)
                with col_test1:
                    st.write("**Teks → Simbol:**")
                    st.code(symbols)
                with col_test2:
                    st.write("**Simbol → Teks:**")
                    st.code(back_text)
                
                if test_text.upper() == back_text:
                    st.success("✅ Konversi dua arah berhasil!")
                else:
                    st.error(f"❌ Gagal! Seharusnya: {test_text.upper()}, Hasil: {back_text}")

if __name__ == "__main__":
    main()
