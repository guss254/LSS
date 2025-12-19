import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO

def init_session_state():
    """Inisialisasi session state untuk menyimpan data"""
    if 'data_produksi' not in st.session_state:
        st.session_state.data_produksi = pd.DataFrame(columns=[
            'Tanggal', 'Jenis', 'Kode Produksi', 'Jumlah (kg)', 'Kode Palet'
        ])
    if 'data_counter' not in st.session_state:
        st.session_state.data_counter = 0

def main():
    st.set_page_config(
        page_title="Form Input Data Produksi",
        page_icon="🏭",
        layout="wide"
    )
    
    # Inisialisasi session state
    init_session_state()
    
    st.title("🏭 FORM INPUT DATA PRODUKSI")
    st.markdown("---")
    
    # Bagian 1: Form Input
    st.subheader("📝 Input Data Baru")
    
    with st.form("input_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            tgl = st.date_input("📅 Tanggal", datetime.now())
            jenis = st.selectbox("📦 Jenis Data", ["Prod", "Blen"])
        
        with col2:
            kode = st.text_input("🏷️ Kode Produksi", placeholder="076, 054, etc")
            berat = st.number_input("⚖️ Jumlah (kg)", min_value=0.0, step=0.01)
        
        kode_palet = st.text_input("📦 Kode Palet", placeholder="Opsional")
        
        submitted = st.form_submit_button("💾 TAMBAH DATA")
    
    # Proses ketika form disubmit
    if submitted:
        if not kode:
            st.error("⚠️ Harap isi Kode Produksi!")
        elif berat <= 0:
            st.error("⚠️ Jumlah (kg) harus lebih dari 0!")
        else:
            # Buat data baru
            new_data = pd.DataFrame([{
                'No.': len(st.session_state.data_produksi) + 1,
                'Tanggal': tgl.strftime('%d-%m-%Y'),
                'Jenis': jenis,
                'Kode Produksi': kode,
                'Jumlah (kg)': berat,
                'Kode Palet': kode_palet if kode_palet else '-'
            }])
            
            # Tambahkan ke session state
            st.session_state.data_produksi = pd.concat(
                [st.session_state.data_produksi, new_data], 
                ignore_index=True
            )
            
            st.success(f"✅ Data berhasil ditambahkan! Total data: {len(st.session_state.data_produksi)}")
            st.rerun()
    
    st.markdown("---")
    
    # Bagian 2: Tampilkan Data yang Telah Disimpan
    st.subheader("📊 Data Produksi yang Tersimpan")
    
    if not st.session_state.data_produksi.empty:
        # Tampilkan dataframe dengan styling
        st.dataframe(
            st.session_state.data_produksi,
            use_container_width=True,
            hide_index=True
        )
        
        # Tampilkan statistik
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Data", len(st.session_state.data_produksi))
        with col2:
            total_berat = st.session_state.data_produksi['Jumlah (kg)'].sum()
            st.metric("Total Berat (kg)", f"{total_berat:.2f}")
        with col3:
            st.metric("Tanggal Terakhir", 
                     st.session_state.data_produksi.iloc[-1]['Tanggal'])
        
        # Bagian 3: Download dan Reset
        st.markdown("---")
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            # Download Excel
            if not st.session_state.data_produksi.empty:
                excel_buffer = BytesIO()
                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                    st.session_state.data_produksi.to_excel(
                        writer, 
                        index=False, 
                        sheet_name='Data Produksi'
                    )
                
                excel_buffer.seek(0)
                
                st.download_button(
                    label="📥 DOWNLOAD EXCEL",
                    data=excel_buffer,
                    file_name=f"data_produksi_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
        
        with col2:
            # Tombol reset data
            if st.button("🗑️ RESET DATA", use_container_width=True):
                st.session_state.data_produksi = pd.DataFrame(columns=[
                    'No.', 'Tanggal', 'Jenis', 'Kode Produksi', 'Jumlah (kg)', 'Kode Palet'
                ])
                st.success("✅ Semua data telah direset!")
                st.rerun()
                
        with col3:
            # Tombol hapus data terakhir
            if st.button("↩️ HAPUS TERAKHIR", use_container_width=True):
                if not st.session_state.data_produksi.empty:
                    st.session_state.data_produksi = st.session_state.data_produksi.iloc[:-1]
                    st.success("✅ Data terakhir dihapus!")
                    st.rerun()
    
    else:
        st.info("📭 Belum ada data. Silakan input data terlebih dahulu.")
    
    st.markdown("---")
    st.info("ℹ️ Input data sebanyak yang Anda butuhkan. Data akan tersimpan selama sesi berjalan.")

if __name__ == "__main__":
    main()
