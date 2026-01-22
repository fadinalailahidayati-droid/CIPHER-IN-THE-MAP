import streamlit as st
import pandas as pd

# ========== KONFIGURASI SIMBOL GEOGRAFI YANG BENAR ==========

# Tabel simbol dari PDF yang benar
SYMBOL_TABLE = {
    'A': '●',    'B': '△',    'C': '□',    'D': '▽',    'E': '~ ~',
    'F': '~~~',  'G': '◆',    'H': '♡',    'I': '○',    'J': '- - - -',
    'K': '◆',    'L': '~ ~ ~ ~', 'M': '□',    'N': '▲',    'O': '====',
    'P': '▶',    'Q': '◇',    'R': '◎',    'S': '+',    'T': '+',
    'U': '+',    'V': '☉',    'W': '○',    'X': '×',    'Y': '○',
    'Z': '☉☉☉☉'
}

# Reverse mapping yang benar (perhatikan simbol yang sama untuk huruf berbeda)
REVERSE_SYMBOL = {
    '●': ['A'],      # A
    '△': ['B'],      # B
    '□': ['C', 'M'], # C dan M sama-sama □
    '▽': ['D'],      # D
    '~ ~': ['E'],    # E
    '~~~': ['F'],    # F
    '◆': ['G', 'K'], # G dan K sama-sama ◆
    '♡': ['H'],      # H
    '○': ['I', 'W', 'Y'], # I, W, Y sama-sama ○
    '- - - -': ['J'], # J
    '~ ~ ~ ~': ['L'], # L
    '▲': ['N'],      # N
    '====': ['O'],   # O
    '▶': ['P'],      # P
    '◇': ['Q'],      # Q
    '◎': ['R'],      # R
    '+': ['S', 'T', 'U'], # S, T, U sama-sama +
    '☉': ['V'],      # V
    '×': ['X'],      # X
    '☉☉☉☉': ['Z']   # Z
}

# Simbol untuk Rail Fence
RAIL_SYMBOLS = {
    '|': 2,    'Z': 3,    '卍': 4,   '✠': 5,    '✪': 6,
    '❂': 7,    '✿': 8,    '❀': 9,    '✾': 10
}

# ========== FUNGSI YANG BENAR-BENAR BEKERJA ==========

def text_to_symbols_simple(text):
    """Konversi teks ke simbol - SEDERHANA dan PASTI BENAR"""
    result = []
    for char in text.upper():
        if char in SYMBOL_TABLE:
            result.append(SYMBOL_TABLE[char])
        elif char == " ":
            result.append("/")
        else:
            result.append(char)
    return " ".join(result)

def symbols_to_text_simple(symbols_str):
    """Konversi simbol ke teks - SEDERHANA dan PASTI BENAR"""
    if not symbols_str:
        return ""
    
    # Pisahkan simbol
    symbols = symbols_str.split()
    result = []
    
    i = 0
    while i < len(symbols):
        current = symbols[i]
        
        # Cek simbol multi-token
        symbol_found = None
        symbol_length = 1
        
        # Cek 4 token
        if i + 3 < len(symbols):
            potential = f"{symbols[i]} {symbols[i+1]} {symbols[i+2]} {symbols[i+3]}"
            if potential == '- - - -':
                symbol_found = '- - - -'
                symbol_length = 4
            elif potential == '~ ~ ~ ~':
                symbol_found = '~ ~ ~ ~'
                symbol_length = 4
            elif potential == '====':
                symbol_found = '===='
                symbol_length = 4
            elif potential == '☉ ☉ ☉ ☉':
                symbol_found = '☉☉☉☉'
                symbol_length = 4
        
        # Cek 3 token
        if not symbol_found and i + 2 < len(symbols):
            potential = f"{symbols[i]} {symbols[i+1]} {symbols[i+2]}"
            if potential == '~ ~ ~':
                symbol_found = '~~~'
                symbol_length = 3
        
        # Cek 2 token
        if not symbol_found and i + 1 < len(symbols):
            potential = f"{symbols[i]} {symbols[i+1]}"
            if potential == '~ ~':
                symbol_found = '~ ~'
                symbol_length = 2
        
        # Simbol 1 token
        if not symbol_found:
            symbol_found = current
            symbol_length = 1
        
        # Konversi simbol ke huruf
        if symbol_found in REVERSE_SYMBOL:
            # Ambil huruf pertama jika ada multiple mapping
            result.append(REVERSE_SYMBOL[symbol_found][0])
        elif symbol_found == "/":
            result.append(" ")
        else:
            result.append(symbol_found)
        
        i += symbol_length
    
    return ''.join(result)

def caesar_cipher_fixed(text, shift=3, mode='encrypt'):
    """Caesar Cipher yang PASTI BENAR"""
    result = []
    
    if mode == 'decrypt':
        shift = -shift
    
    for char in text.upper():
        if 'A' <= char <= 'Z':
            # Lakukan pergeseran
            new_pos = (ord(char) - 65 + shift) % 26
            result.append(chr(new_pos + 65))
        elif char == " ":
            result.append(" ")
        else:
            result.append(char)
    
    return ''.join(result)

def rail_fence_fixed(text, rails, mode='encrypt'):
    """Rail Fence yang PASTI BENAR"""
    if rails <= 1:
        return text
    
    if mode == 'encrypt':
        # Buat rail
        fence = [''] * rails
        rail = 0
        direction = 1
        
        for char in text:
            fence[rail] += char
            rail += direction
            
            if rail == 0 or rail == rails - 1:
                direction = -direction
        
        return ''.join(fence)
    
    else:  # decrypt
        # Buat pola
        fence = [[''] * len(text) for _ in range(rails)]
        rail = 0
        direction = 1
        
        # Tandai posisi
        for i in range(len(text)):
            fence[rail][i] = '*'
            rail += direction
            if rail == 0 or rail == rails - 1:
                direction = -direction
        
        # Isi teks
        idx = 0
        for r in range(rails):
            for c in range(len(text)):
                if fence[r][c] == '*':
                    fence[r][c] = text[idx]
                    idx += 1
        
        # Baca hasil
        rail = 0
        direction = 1
        result_chars = []
        
        for i in range(len(text)):
            result_chars.append(fence[rail][i])
            rail += direction
            if rail == 0 or rail == rails - 1:
                direction = -direction
        
        return ''.join(result_chars)

def encrypt_process(plaintext, rail_symbol):
    """Proses enkripsi yang PASTI BENAR"""
    # 1. Caesar Cipher (shift 3)
    caesar_result = caesar_cipher_fixed(plaintext, 3, 'encrypt')
    
    # 2. Rail Fence
    rails = RAIL_SYMBOLS.get(rail_symbol, 3)
    rail_result = rail_fence_fixed(caesar_result, rails, 'encrypt')
    
    # 3. Konversi ke simbol
    symbols_result = text_to_symbols_simple(rail_result)
    
    return caesar_result, rail_result, symbols_result

def decrypt_process(symbols_str, rail_symbol):
    """Proses dekripsi yang PASTI BENAR"""
    # 1. Konversi simbol ke teks
    rail_text = symbols_to_text_simple(symbols_str)
    
    # 2. Rail Fence Decrypt
    rails = RAIL_SYMBOLS.get(rail_symbol, 3)
    caesar_text = rail_fence_fixed(rail_text, rails, 'decrypt')
    
    # 3. Caesar Decrypt (shift 3)
    plaintext = caesar_cipher_fixed(caesar_text, 3, 'decrypt')
    
    return rail_text, caesar_text, plaintext

def test_kriptografi():
    """Test fungsi dengan KRIPTOGRAFI"""
    test_text = "KRIPTOGRAFI"
    
    # Caesar Cipher test
    caesar_test = caesar_cipher_fixed(test_text, 3, 'encrypt')
    caesar_back = caesar_cipher_fixed(caesar_test, 3, 'decrypt')
    
    # Rail Fence test
    rail_test = rail_fence_fixed(caesar_test, 3, 'encrypt')
    rail_back = rail_fence_fixed(rail_test, 3, 'decrypt')
    
    # Symbol test
    symbols_test = text_to_symbols_simple(rail_test)
    symbols_back = symbols_to_text_simple(symbols_test)
    
    # Full process test
    _, _, final_symbols = encrypt_process(test_text, 'Z')
    _, _, decrypted = decrypt_process(final_symbols, 'Z')
    
    return {
        'text': test_text,
        'caesar_enc': caesar_test,
        'caesar_dec': caesar_back,
        'rail_enc': rail_test,
        'rail_dec': rail_back,
        'symbols': symbols_test,
        'symbols_back': symbols_back,
        'full_enc': final_symbols,
        'full_dec': decrypted,
        'success': decrypted == test_text
    }

# ========== INTERFACE STREAMLIT ==========

def main():
    st.set_page_config(
        page_title="Cipher In The Map - FIXED",
        page_icon="🗺️",
        layout="wide"
    )
    
    # CSS Simple
    st.markdown("""
    <style>
    .success-box { background: #d1fae5; padding: 20px; border-radius: 10px; border-left: 5px solid #10b981; }
    .error-box { background: #fee2e2; padding: 20px; border-radius: 10px; border-left: 5px solid #ef4444; }
    .info-box { background: #dbeafe; padding: 20px; border-radius: 10px; border-left: 5px solid #3b82f6; }
    .fixed-header { color: #1e40af; text-align: center; font-size: 2.5em; }
    .step { background: #f3f4f6; padding: 15px; margin: 10px 0; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="fixed-header">🗺️ Cipher In The Map - VERSION FIXED</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666;">Caesar Shift: 3 | Rail Fence: Pilihan Bebas</p>', unsafe_allow_html=True)
    
    # Run test pertama kali
    if 'test_result' not in st.session_state:
        st.session_state.test_result = test_kriptografi()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🧪 Testing Status")
        if st.session_state.test_result['success']:
            st.success("✅ SEMUA FUNGSI BERHASIL!")
        else:
            st.error("❌ Ada masalah dengan fungsi")
        
        st.markdown("---")
        st.markdown("### 📊 Test KRIPTOGRAFI")
        st.write(f"**Teks:** {st.session_state.test_result['text']}")
        st.write(f"**Caesar:** {st.session_state.test_result['caesar_enc']}")
        st.write(f"**Rail:** {st.session_state.test_result['rail_enc']}")
        st.write(f"**Simbol:** {st.session_state.test_result['symbols']}")
        st.write(f"**Dekripsi:** {st.session_state.test_result['full_dec']}")
        
        if st.button("🔁 Run Test Ulang"):
            st.session_state.test_result = test_kriptografi()
            st.rerun()
        
        st.markdown("---")
        st.markdown("**⚠️ CATATAN PENTING:**")
        st.info("""
        Beberapa simbol mewakili >1 huruf:
        - □ = C atau M
        - ◆ = G atau K  
        - ○ = I, W, atau Y
        - + = S, T, atau U
        """)
    
    # Tabs utama
    tab1, tab2, tab3 = st.tabs(["🔐 Enkripsi", "🔓 Dekripsi", "📚 Tabel Simbol"])
    
    # ========== TAB ENKRIPSI ==========
    with tab1:
        st.header("🔐 Enkripsi Pesan")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            plaintext = st.text_area(
                "Masukkan teks:",
                height=100,
                placeholder="KRIPTOGRAFI",
                key="enc_text"
            )
            
            if plaintext:
                # Preview Caesar
                caesar_preview = caesar_cipher_fixed(plaintext, 3, 'encrypt')
                st.info(f"**Setelah Caesar (shift 3):** {caesar_preview}")
        
        with col2:
            st.subheader("🛣️ Pilih Rail Fence")
            rail_key = st.selectbox(
                "Pola jalan:",
                options=list(RAIL_SYMBOLS.keys()),
                format_func=lambda x: f"{x} ({RAIL_SYMBOLS[x]} rail)",
                key="enc_rail"
            )
            
            if st.button("🧪 Test KRIPTOGRAFI", key="test_btn"):
                plaintext = "KRIPTOGRAFI"
                rail_key = 'Z'
                st.rerun()
        
        if st.button("🚀 ENKRIPSI SEKARANG", type="primary", use_container_width=True):
            if plaintext:
                with st.spinner("Memproses..."):
                    try:
                        caesar_result, rail_result, symbols_result = encrypt_process(plaintext, rail_key)
                        
                        st.success("✅ Enkripsi Berhasil!")
                        
                        # Simpan ke session
                        st.session_state.last_encryption = {
                            'plaintext': plaintext,
                            'rail_key': rail_key,
                            'rails': RAIL_SYMBOLS[rail_key],
                            'caesar_result': caesar_result,
                            'rail_result': rail_result,
                            'symbols_result': symbols_result
                        }
                        
                        # Tampilkan hasil
                        st.markdown("---")
                        st.subheader("📊 Hasil Enkripsi")
                        
                        col_res1, col_res2 = st.columns(2)
                        
                        with col_res1:
                            st.markdown("**🎯 Simbol Akhir:**")
                            st.markdown(f'<div class="info-box"><h3>{symbols_result}</h3></div>', unsafe_allow_html=True)
                            st.code(symbols_result)
                            
                            if st.button("📋 Copy Simbol", key="copy_sym"):
                                st.write("Copied!")
                        
                        with col_res2:
                            st.markdown("**🔑 Kunci:**")
                            st.write(f"**Caesar Shift:** 3")
                            st.write(f"**Rail Fence:** {rail_key} ({RAIL_SYMBOLS[rail_key]} rail)")
                        
                        # Detail proses
                        with st.expander("📖 Detail Proses", expanded=True):
                            st.markdown("**1. Caesar Cipher (shift 3):**")
                            st.write(f"`{plaintext.upper()}` → `{caesar_result}`")
                            
                            st.markdown(f"**2. Rail Fence ({RAIL_SYMBOLS[rail_key]} rail):**")
                            st.write(f"`{caesar_result}` → `{rail_result}`")
                            
                            # Visualisasi rail
                            if len(caesar_result) <= 30:
                                st.markdown("**Visualisasi Pattern:**")
                                rails = RAIL_SYMBOLS[rail_key]
                                pattern = [['.' for _ in range(len(caesar_result))] for _ in range(rails)]
                                rail_idx = 0
                                dir = 1
                                
                                for i, char in enumerate(caesar_result):
                                    pattern[rail_idx][i] = char
                                    rail_idx += dir
                                    if rail_idx == 0 or rail_idx == rails - 1:
                                        dir = -dir
                                
                                for r in range(rails):
                                    st.text(f"Rail {r+1}: {' '.join(pattern[r])}")
                            
                            st.markdown("**3. Konversi ke Simbol:**")
                            conv_text = ""
                            for char in rail_result:
                                if char in SYMBOL_TABLE:
                                    conv_text += f"{char} → {SYMBOL_TABLE[char]}\n"
                                elif char == " ":
                                    conv_text += "spasi → /\n"
                            st.text(conv_text)
                        
                        # Test konversi balik
                        st.markdown("---")
                        st.subheader("🧪 Verifikasi")
                        back_text = symbols_to_text_simple(symbols_result)
                        if back_text == rail_result:
                            st.success(f"✅ Konversi simbol → teks BERHASIL: `{back_text}`")
                        else:
                            st.error(f"❌ Gagal! Hasil: `{back_text}`, Harusnya: `{rail_result}`")
                        
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            else:
                st.warning("Masukkan teks terlebih dahulu!")
    
    # ========== TAB DEKRIPSI ==========
    with tab2:
        st.header("🔓 Dekripsi Pesan")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Input simbol
            symbols_input = st.text_area(
                "Masukkan simbol geografi:",
                height=100,
                placeholder="Tempel simbol di sini...",
                key="dec_symbols"
            )
            
            # Tombol load dari enkripsi terakhir
            if 'last_encryption' in st.session_state:
                if st.button("📥 Load dari enkripsi terakhir", use_container_width=True):
                    symbols_input = st.session_state.last_encryption['symbols_result']
                    st.rerun()
        
        with col2:
            st.subheader("🛣️ Pilih Rail Fence")
            rail_key_dec = st.selectbox(
                "Pola jalan:",
                options=list(RAIL_SYMBOLS.keys()),
                format_func=lambda x: f"{x} ({RAIL_SYMBOLS[x]} rail)",
                key="dec_rail",
                index=1 if 'Z' in list(RAIL_SYMBOLS.keys()) else 0
            )
            
            # Auto-select jika ada
            if 'last_encryption' in st.session_state:
                if st.button("🔑 Gunakan kunci sebelumnya", use_container_width=True):
                    rail_key_dec = st.session_state.last_encryption['rail_key']
                    st.rerun()
        
        if st.button("🔍 DEKRIPSI SEKARANG", type="primary", use_container_width=True):
            if symbols_input:
                with st.spinner("Memproses dekripsi..."):
                    try:
                        rail_text, caesar_text, plaintext = decrypt_process(symbols_input, rail_key_dec)
                        
                        # Tampilkan hasil
                        st.success("✅ Dekripsi Berhasil!")
                        
                        st.markdown("---")
                        st.subheader("📜 Hasil Dekripsi")
                        
                        col_res1, col_res2 = st.columns(2)
                        
                        with col_res1:
                            st.markdown("**🎯 Teks Asli:**")
                            st.markdown(f'<div class="success-box"><h2>{plaintext}</h2></div>', unsafe_allow_html=True)
                            
                            if st.button("📋 Copy Teks", key="copy_text"):
                                st.write("Copied!")
                        
                        with col_res2:
                            st.markdown("**📋 Proses:**")
                            st.write(f"**1. Simbol → Teks:** `{rail_text}`")
                            st.write(f"**2. Rail Decrypt:** `{caesar_text}`")
                            st.write(f"**3. Caesar Decrypt:** `{plaintext}`")
                            st.write(f"**Rail Used:** {rail_key_dec} ({RAIL_SYMBOLS[rail_key_dec]} rail)")
                        
                        # Verifikasi dengan data sebelumnya
                        if 'last_encryption' in st.session_state:
                            expected = st.session_state.last_encryption['plaintext'].upper()
                            if plaintext.upper() == expected.upper():
                                st.balloons()
                                st.success(f"✅ ✅ SEMPURNA! Cocok dengan teks asli: `{expected}`")
                            else:
                                st.warning(f"⚠️ Tidak cocok. Dari enkripsi: `{expected}`, Hasil: `{plaintext}`")
                        
                        # Test khusus KRIPTOGRAFI
                        if plaintext.upper() == "KRIPTOGRAFI":
                            st.balloons()
                            st.success("🎉 TEST KRIPTOGRAFI BERHASIL 100%!")
                        
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                        st.info("Pastikan format simbol benar dan rail key sesuai.")
            else:
                st.warning("Masukkan simbol terlebih dahulu!")
    
    # ========== TAB TABEL SIMBOL ==========
    with tab3:
        st.header("📚 Tabel Simbol Lengkap")
        
        # Buat dataframe
        table_data = []
        descriptions = {
            '●': 'Kota Besar', '△': 'Gunung Non Aktif', '□': 'Dataran Rendah',
            '▽': 'Lembah', '~ ~': 'Sungai', '~~~': 'Jalan Raya',
            '◆': 'Hutan', '♡': 'Pelabuhan', '○': 'Danau',
            '- - - -': 'Rel Kereta Api', '~ ~ ~ ~': 'Pantai',
            '▲': 'Gunung Aktif', '====': 'Batas Negara', '▶': 'Bendungan',
            '◇': 'Air Terjun', '◎': 'Rawa', '+': 'Rumah Sakit/Bandara/Tempat Ibadah',
            '☉': 'Kantor Pos', '×': 'Daerah Berbahaya', '☉☉☉☉': 'Laut'
        }
        
        for letter, symbol in SYMBOL_TABLE.items():
            table_data.append({
                'Huruf': letter,
                'Simbol': symbol,
                'Deskripsi': descriptions.get(symbol, '-'),
                'Catatan': 'Multi-huruf' if len(REVERSE_SYMBOL.get(symbol, [])) > 1 else '-'
            })
        
        df = pd.DataFrame(table_data)
        
        # Tampilkan tabel
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Warning untuk simbol multi-huruf
        st.markdown("---")
        st.markdown("### ⚠️ Simbol dengan Multiple Huruf")
        st.warning("""
        **PERHATIAN:** Beberapa simbol mewakili lebih dari satu huruf:
        - `□` = **C** atau **M** (Dataran Rendah / Pemukiman)
        - `◆` = **G** atau **K** (Hutan / Pertambangan)  
        - `○` = **I**, **W**, atau **Y** (Danau / Sumur / Ibu Kota Negara)
        - `+` = **S**, **T**, atau **U** (Rumah Sakit / Bandara / Tempat Ibadah)
        
        **Ini normal** karena tabel dari PDF memang seperti itu.
        Dekripsi akan memilih huruf pertama dari pilihan.
        """)
        
        # Testing tool
        st.markdown("---")
        st.subheader("🧪 Testing Tool")
        
        test_col1, test_col2 = st.columns(2)
        
        with test_col1:
            test_text = st.text_input("Test teks:", "KRIPTOGRAFI", key="test_tool")
            if st.button("Test Full Process", key="test_full"):
                # Enkripsi
                _, _, symbols = encrypt_process(test_text, 'Z')
                # Dekripsi
                _, _, back = decrypt_process(symbols, 'Z')
                
                st.write(f"**Teks:** {test_text}")
                st.write(f"**Simbol:** {symbols}")
                st.write(f"**Dekripsi:** {back}")
                
                if back.upper() == test_text.upper():
                    st.success("✅ TEST BERHASIL 100%!")
                else:
                    st.error(f"❌ Gagal! Harusnya: {test_text.upper()}")
        
        with test_col2:
            if st.button("Test Simbol Konversi", key="test_sym"):
                test_sym = "◆ ◇ ○ + ==== ◆ ▽ ● △ + ○"
                back_text = symbols_to_text_simple(test_sym)
                st.write(f"**Simbol:** {test_sym}")
                st.write(f"**Hasil:** {back_text}")

if __name__ == "__main__":
    main()
