import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO
import json

def init_session_state():
    """Inisialisasi session state untuk menyimpan data"""
    if 'data_produksi' not in st.session_state:
        # Coba load dari query params atau session storage
        try:
            # Cek jika ada data di query params (untuk persistensi)
            if st.query_params.get("data"):
                data_json = st.query_params.get("data")
                data_dict = json.loads(data_json)
                st.session_state.data_produksi = pd.DataFrame(data_dict)
            else:
                st.session_state.data_produksi = pd.DataFrame(columns=[
                    'No.', 'Tanggal', 'Jenis', 'Kode Produksi', 'Jumlah (kg)', 'Kode Palet'
                ])
        except:
            st.session_state.data_produksi = pd.DataFrame(columns=[
                'No.', 'Tanggal', 'Jenis', 'Kode Produksi', 'Jumlah (kg)', 'Kode Palet'
            ])

def save_to_query_params(df):
    """Simpan data ke query params untuk persistensi"""
    if not df.empty:
        data_dict = df.to_dict('records')
        data_json = json.dumps(data_dict)
        st.query_params["data"] = data_json

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
            
            # Simpan ke query params untuk persistensi
            save_to_query_params(st.session_state.data_produksi)
            
            st.success(f"✅ Data berhasil ditambahkan! Total data: {len(st.session_state.data_produksi)}")
            st.rerun()
    
    st.markdown("---")
    
    # Bagian 2: Tampilkan Data yang Telah Disimpan
    st.subheader("📊 Data Produksi yang Tersimpan")
    
    if not st.session_state.data_produksi.empty:
        # Buat dataframe untuk display dengan tombol hapus
        display_df = st.session_state.data_produksi.copy()
        
        # Tampilkan dataframe
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )
        
        # Bagian untuk hapus data spesifik
        st.markdown("### 🗑️ Hapus Data Spesifik")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Pilihan hapus berdasarkan nomor
            hapus_no = st.number_input(
                "Nomor data yang akan dihapus:",
                min_value=1,
                max_value=len(st.session_state.data_produksi) if not st.session_state.data_produksi.empty else 1,
                step=1,
                key="hapus_no"
            )
        
        with col2:
            # Pilihan hapus berdasarkan kode produksi
            kode_options = st.session_state.data_produksi['Kode Produksi'].unique().tolist()
            hapus_kode = st.selectbox(
                "Atau pilih berdasarkan Kode Produksi:",
                ["Pilih kode"] + kode_options,
                key="hapus_kode"
            )
        
        with col3:
            st.write("")
            st.write("")
            if st.button("🗑️ HAPUS DATA TERPILIH", use_container_width=True):
                if hapus_kode != "Pilih kode":
                    # Hapus berdasarkan kode produksi
                    sebelum = len(st.session_state.data_produksi)
                    st.session_state.data_produksi = st.session_state.data_produksi[
                        st.session_state.data_produksi['Kode Produksi'] != hapus_kode
                    ]
                    sesudah = len(st.session_state.data_produksi)
                    if sebelum > sesudah:
                        st.success(f"✅ Data dengan kode {hapus_kode} berhasil dihapus!")
                        # Update nomor urut
                        st.session_state.data_produksi['No.'] = range(1, len(st.session_state.data_produksi) + 1)
                        save_to_query_params(st.session_state.data_produksi)
                        st.rerun()
                elif hapus_no and 1 <= hapus_no <= len(st.session_state.data_produksi):
                    # Hapus berdasarkan nomor
                    st.session_state.data_produksi = st.session_state.data_produksi.drop(
                        st.session_state.data_produksi.index[hapus_no - 1]
                    )
                    # Update nomor urut
                    st.session_state.data_produksi['No.'] = range(1, len(st.session_state.data_produksi) + 1)
                    save_to_query_params(st.session_state.data_produksi)
                    st.success(f"✅ Data nomor {hapus_no} berhasil dihapus!")
                    st.rerun()
        
        # Tampilkan statistik
        st.markdown("### 📈 Statistik Data")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Data", len(st.session_state.data_produksi))
        
        with col2:
            total_berat = st.session_state.data_produksi['Jumlah (kg)'].sum()
            st.metric("Total Berat (kg)", f"{total_berat:.2f}")
        
        with col3:
            avg_berat = st.session_state.data_produksi['Jumlah (kg)'].mean()
            st.metric("Rata-rata (kg)", f"{avg_berat:.2f}")
        
        with col4:
            st.metric("Tanggal Terakhir", 
                     st.session_state.data_produksi.iloc[-1]['Tanggal'])
        
        # Tampilkan data per jenis
        st.markdown("### 📊 Distribusi per Jenis")
        jenis_counts = st.session_state.data_produksi['Jenis'].value_counts()
        col1, col2 = st.columns(2)
        
        with col1:
            for jenis, count in jenis_counts.items():
                st.write(f"**{jenis}**: {count} data")
        
        with col2:
            jenis_berat = st.session_state.data_produksi.groupby('Jenis')['Jumlah (kg)'].sum()
            for jenis, berat in jenis_berat.items():
                st.write(f"**{jenis}**: {berat:.2f} kg")
        
        # Bagian 3: Download dan Reset
        st.markdown("---")
        st.subheader("💾 Export & Management Data")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            # Download Excel
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
            # Tombol reset semua data
            if st.button("🗑️ RESET SEMUA DATA", use_container_width=True, type="secondary"):
                st.session_state.data_produksi = pd.DataFrame(columns=[
                    'No.', 'Tanggal', 'Jenis', 'Kode Produksi', 'Jumlah (kg)', 'Kode Palet'
                ])
                # Hapus juga dari query params
                if "data" in st.query_params:
                    del st.query_params["data"]
                st.success("✅ Semua data telah direset!")
                st.rerun()
        
        with col3:
            # Tombol backup ke session storage
            if st.button("💾 BACKUP DATA", use_container_width=True):
                save_to_query_params(st.session_state.data_produksi)
                st.success("✅ Data telah di-backup! Data akan tersimpan meskipun browser di-refresh.")
    
    else:
        st.info("📭 Belum ada data. Silakan input data terlebih dahulu.")
    
    st.markdown("---")
    st.info("""
    ℹ️ **Cara penggunaan:**
    1. Input data melalui form di atas
    2. Klik **TAMBAH DATA** untuk menyimpan
    3. Ulangi untuk menambah data lain
    4. Gunakan fitur **HAPUS DATA TERPILIH** untuk menghapus data tertentu
    5. Klik **BACKUP DATA** agar data tidak hilang saat refresh
    6. **DOWNLOAD EXCEL** untuk menyimpan data permanen
    """)

if __name__ == "__main__":
    main()
