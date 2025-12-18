import streamlit as st
import pandas as pd
from datetime import datetime
import io
from io import BytesIO

# Konfigurasi halaman
st.set_page_config(
    page_title="Form Input Data Produksi",
    page_icon="🏭",
    layout="wide"
)

# CSS untuk styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.8rem;
        color: #1E40AF;
        border-bottom: 3px solid #3B82F6;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }
    .sub-section {
        background-color: #F3F4F6;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        border-left: 5px solid #3B82F6;
    }
    .stButton > button {
        background-color: #10B981;
        color: white;
        font-weight: bold;
        padding: 0.5rem 2rem;
        border-radius: 5px;
        border: none;
    }
    .stButton > button:hover {
        background-color: #059669;
    }
    .success-message {
        background-color: #D1FAE5;
        color: #065F46;
        padding: 1rem;
        border-radius: 5px;
        border-left: 5px solid #10B981;
        margin: 1rem 0;
    }
    .data-preview {
        background-color: #FEF3C7;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #F59E0B;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #DBEAFE;
        padding: 1rem;
        border-radius: 5px;
        border-left: 5px solid #3B82F6;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header aplikasi
st.markdown('<h1 class="main-header">🏭 FORM INPUT DATA PRODUKSI</h1>', unsafe_allow_html=True)

# Inisialisasi session state untuk menyimpan data
if 'prod_data' not in st.session_state:
    st.session_state.prod_data = []
if 'blen_data' not in st.session_state:
    st.session_state.blen_data = []

def tambah_data_prod():
    """Menambahkan data Prod ke session state"""
    if st.session_state.tgl_prod and st.session_state.berat_prod:
        data = {
            'Tanggal': st.session_state.tgl_prod.strftime('%d-%m-%Y'),
            'Kode Produksi': st.session_state.kode_prod,
            'Jumlah (kg)': st.session_state.berat_prod,
            'Kode Palet': st.session_state.pallet_prod
        }
        st.session_state.prod_data.append(data)
        
        # Reset form fields
        st.session_state.tgl_prod = datetime.now()
        st.session_state.kode_prod = ""
        st.session_state.berat_prod = 0.0
        st.session_state.pallet_prod = ""
        
        st.success("✅ Data Prod berhasil ditambahkan!")

def tambah_data_blen():
    """Menambahkan data Blen ke session state"""
    if st.session_state.tgl_blen and st.session_state.kode_produksi_blen:
        data = {
            'Tanggal': st.session_state.tgl_blen.strftime('%d-%m-%Y'),
            'Kode Produksi': st.session_state.kode_produksi_blen,
            'Kode Palet': st.session_state.pallet_blen
        }
        st.session_state.blen_data.append(data)
        
        # Reset form fields
        st.session_state.tgl_blen = datetime.now()
        st.session_state.kode_produksi_blen = ""
        st.session_state.pallet_blen = ""
        
        st.success("✅ Data Blen berhasil ditambahkan!")

def hapus_data_prod(index):
    """Menghapus data Prod berdasarkan index"""
    del st.session_state.prod_data[index]
    st.success("🗑️ Data Prod berhasil dihapus!")

def hapus_data_blen(index):
    """Menghapus data Blen berdasarkan index"""
    del st.session_state.blen_data[index]
    st.success("🗑️ Data Blen berhasil dihapus!")

def buat_file_excel():
    """Membuat file Excel dari data yang ada"""
    # Buat DataFrame untuk Prod
    if st.session_state.prod_data:
        df_prod = pd.DataFrame(st.session_state.prod_data)
    else:
        df_prod = pd.DataFrame(columns=['Tanggal', 'Kode Produksi', 'Jumlah (kg)', 'Kode Palet'])
    
    # Buat DataFrame untuk Blen
    if st.session_state.blen_data:
        df_blen = pd.DataFrame(st.session_state.blen_data)
        # Tambahkan kolom Jumlah (kg) kosong untuk Blen
        df_blen['Jumlah (kg)'] = ''
    else:
        df_blen = pd.DataFrame(columns=['Tanggal', 'Kode Produksi', 'Kode Palet', 'Jumlah (kg)'])
    
    # Buat file Excel di memory
    output = BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        if not df_prod.empty:
            df_prod.to_excel(writer, sheet_name='DATA PROD', index=False)
            worksheet_prod = writer.sheets['DATA PROD']
            # Atur lebar kolom
            for column in worksheet_prod.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 30)
                worksheet_prod.column_dimensions[column_letter].width = adjusted_width
        
        if not df_blen.empty:
            df_blen.to_excel(writer, sheet_name='DATA BLEN', index=False)
            worksheet_blen = writer.sheets['DATA BLEN']
            # Atur lebar kolom
            for column in worksheet_blen.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 30)
                worksheet_blen.column_dimensions[column_letter].width = adjusted_width
    
    output.seek(0)
    
    return output

# Bagian Input Data
col1, col2 = st.columns([2, 1])

with col1:
    # SECTION 1: INPUT DATA PROD
    st.markdown('<h2 class="section-header">📦 INPUT DATA PROD</h2>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="sub-section">', unsafe_allow_html=True)
        
        # Form input Prod
        col_prod1, col_prod2 = st.columns(2)
        
        with col_prod1:
            st.date_input(
                "Tanggal*",
                key="tgl_prod",
                value=datetime.now(),
                format="DD-MM-YYYY"
            )
            
            st.text_input(
                "Kode Produksi",
                key="kode_prod",
                placeholder="Contoh: 076, 054, 081"
            )
        
        with col_prod2:
            st.number_input(
                "Jumlah (kg)*",
                key="berat_prod",
                min_value=0.0,
                step=0.01,
                format="%.2f"
            )
            
            st.text_input(
                "Kode Palet",
                key="pallet_prod",
                placeholder="Opsional"
            )
        
        st.button("➕ Tambah Data Prod", on_click=tambah_data_prod, type="primary")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # SECTION 2: INPUT DATA BLEN
    st.markdown('<h2 class="section-header">📊 INPUT DATA BLEN</h2>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="sub-section">', unsafe_allow_html=True)
        
        # Form input Blen
        col_blen1, col_blen2 = st.columns(2)
        
        with col_blen1:
            st.date_input(
                "Tanggal*",
                key="tgl_blen",
                value=datetime.now(),
                format="DD-MM-YYYY"
            )
        
        with col_blen2:
            st.text_input(
                "Kode Produksi*",
                key="kode_produksi_blen",
                placeholder="Contoh: 11, 12, 13"
            )
        
        st.text_input(
            "Kode Palet",
            key="pallet_blen",
            placeholder="Contoh: 083, 100, 060"
        )
        
        st.button("➕ Tambah Data Blen", on_click=tambah_data_blen, type="primary")
        
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # SECTION 3: INFORMASI FORMAT
    st.markdown('<h2 class="section-header">ℹ️ INFORMASI</h2>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        
        st.markdown("**FORMAT DATA:**")
        st.markdown("""
        **Prod:**
        - Format: `DD-MM berat_kg kode_palet`
        - Contoh: `01-06 0.65 kg 076`
        
        **Blen:**
        - Format: `DD-KK kode_palet`
        - DD = Tanggal
        - KK = Kode Produksi
        - Contoh: `15-11 083`
        """)
        
        st.markdown("**KETERANGAN:**")
        st.markdown("""
        - * = Wajib diisi
        - Tanggal otomatis hari ini
        - Kode Palet opsional
        - Data bisa diedit/hapus
        """)
        
        st.markdown("**FITUR:**")
        st.markdown("""
        ✓ Input form yang mudah
        ✓ Preview data langsung
        ✓ Edit/Hapus data
        ✓ Export ke Excel
        ✓ Format otomatis
        """)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Tombol Export
    if st.session_state.prod_data or st.session_state.blen_data:
        st.markdown("---")
        excel_file = buat_file_excel()
        
        st.download_button(
            label="📥 DOWNLOAD EXCEL",
            data=excel_file,
            file_name=f"data_produksi_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary",
            use_container_width=True
        )

# SECTION 4: PREVIEW DATA
st.markdown('<h2 class="section-header">👁️ PREVIEW DATA</h2>', unsafe_allow_html=True)

# Tampilkan data Prod
if st.session_state.prod_data:
    st.markdown("#### 📦 DATA PROD")
    
    # Buat DataFrame untuk preview
    df_prod_preview = pd.DataFrame(st.session_state.prod_data)
    
    # Tampilkan tabel dengan tombol hapus
    for i, row in df_prod_preview.iterrows():
        col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
        
        with col1:
            st.text(f"📅 {row['Tanggal']}")
        with col2:
            st.text(f"🏷️ {row['Kode Produksi']}")
        with col3:
            st.text(f"⚖️ {row['Jumlah (kg')} kg")
        with col4:
            st.text(f"📦 {row['Kode Palet']}")
        with col5:
            if st.button("🗑️", key=f"hapus_prod_{i}"):
                hapus_data_prod(i)
                st.rerun()
    
    st.markdown(f"**Total Data Prod: {len(st.session_state.prod_data)}**")
else:
    st.info("📝 Belum ada data Prod. Silakan tambahkan data di form di atas.")

st.markdown("---")

# Tampilkan data Blen
if st.session_state.blen_data:
    st.markdown("#### 📊 DATA BLEN")
    
    # Buat DataFrame untuk preview
    df_blen_preview = pd.DataFrame(st.session_state.blen_data)
    
    # Tampilkan tabel dengan tombol hapus
    for i, row in df_blen_preview.iterrows():
        col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
        
        with col1:
            st.text(f"📅 {row['Tanggal']}")
        with col2:
            st.text(f"🏷️ {row['Kode Produksi']}")
        with col3:
            st.text(f"📦 {row['Kode Palet']}")
        with col4:
            if st.button("🗑️", key=f"hapus_blen_{i}"):
                hapus_data_blen(i)
                st.rerun()
    
    st.markdown(f"**Total Data Blen: {len(st.session_state.blen_data)}**")
else:
    st.info("📝 Belum ada data Blen. Silakan tambahkan data di form di atas.")

# SECTION 5: STATISTIK
if st.session_state.prod_data or st.session_state.blen_data:
    st.markdown('<h2 class="section-header">📈 STATISTIK DATA</h2>', unsafe_allow_html=True)
    
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    
    with col_stat1:
        st.metric("Total Data Prod", len(st.session_state.prod_data))
    
    with col_stat2:
        st.metric("Total Data Blen", len(st.session_state.blen_data))
    
    with col_stat3:
        total_all = len(st.session_state.prod_data) + len(st.session_state.blen_data)
        st.metric("Total Semua Data", total_all)

# Tombol reset semua data
if st.session_state.prod_data or st.session_state.blen_data:
    st.markdown("---")
    if st.button("🔄 RESET SEMUA DATA", type="secondary", use_container_width=True):
        st.session_state.prod_data = []
        st.session_state.blen_data = []
        st.success("Semua data telah direset!")
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6B7280; padding: 1rem;">
    <p>Form Input Data Produksi • Data otomatis tersimpan di session</p>
    <p>Gunakan tombol Download untuk export ke Excel</p>
</div>
""", unsafe_allow_html=True)
