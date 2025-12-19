import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO
import json

def init_session_state():
    """Inisialisasi session state untuk menyimpan data"""
    if 'data_produksi' not in st.session_state:
        # Data awal yang sudah ada (bisa diubah sesuai kebutuhan)
        initial_data = [
            {
                'No.': 1,
                'Tanggal': '15-01-2024',
                'Jenis': 'Prod',
                'Kode Produksi': '076',
                'Jumlah (kg)': 100.5,
                'Kode Palet': 'P001',
                'Status': 'Ada',
                'Kondisi': 'Baik',
                'Catatan': ''
            },
            {
                'No.': 2,
                'Tanggal': '15-01-2024',
                'Jenis': 'Prod',
                'Kode Produksi': '054',
                'Jumlah (kg)': 85.2,
                'Kode Palet': 'P002',
                'Status': 'Ada',
                'Kondisi': 'Baik',
                'Catatan': ''
            },
            {
                'No.': 3,
                'Tanggal': '16-01-2024',
                'Jenis': 'Blen',
                'Kode Produksi': '082',
                'Jumlah (kg)': 120.0,
                'Kode Palet': 'P003',
                'Status': 'Ada',
                'Kondisi': 'Baik',
                'Catatan': ''
            },
            {
                'No.': 4,
                'Tanggal': '16-01-2024',
                'Jenis': 'Prod',
                'Kode Produksi': '091',
                'Jumlah (kg)': 95.7,
                'Kode Palet': 'P004',
                'Status': 'Ada',
                'Kondisi': 'Baik',
                'Catatan': ''
            },
            {
                'No.': 5,
                'Tanggal': '17-01-2024',
                'Jenis': 'Blen',
                'Kode Produksi': '067',
                'Jumlah (kg)': 110.3,
                'Kode Palet': 'P005',
                'Status': 'Ada',
                'Kondisi': 'Baik',
                'Catatan': ''
            }
        ]
        st.session_state.data_produksi = pd.DataFrame(initial_data)
    
    if 'data_edited' not in st.session_state:
        st.session_state.data_edited = False

def main():
    st.set_page_config(
        page_title="Form Pengecekan Data Produksi",
        page_icon="✅",
        layout="wide"
    )
    
    # Inisialisasi session state
    init_session_state()
    
    st.title("✅ FORM PENGEČEKAN DATA PRODUKSI")
    st.markdown("---")
    
    # Informasi aplikasi
    st.info("""
    **📋 PETUNJUK PENGGUNAAN:**
    1. Data produksi sudah terisi sebelumnya
    2. Lakukan pengecekan di lapangan untuk setiap item
    3. Update **Status**, **Kondisi**, dan **Jumlah (kg)** sesuai kondisi aktual
    4. Tambahkan **Catatan** jika diperlukan
    5. Klik **SIMPAN PERUBAHAN** setelah selesai
    """)
    
    # Tampilkan semua data dalam bentuk form yang bisa diedit
    st.subheader("📋 DATA PRODUKSI YANG AKAN DICEK")
    
    # Buat form untuk editing data
    with st.form("edit_form"):
        edited_data = []
        
        # Loop melalui setiap baris data
        for idx, row in st.session_state.data_produksi.iterrows():
            st.markdown(f"### Data #{int(row['No.'])}")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**Tanggal:** {row['Tanggal']}")
                st.write(f"**Jenis:** {row['Jenis']}")
                st.write(f"**Kode:** {row['Kode Produksi']}")
            
            with col2:
                st.write(f"**Kode Palet:** {row['Kode Palet']}")
                
                # Status dropdown
                status = st.selectbox(
                    f"Status #{int(row['No.'])}",
                    ["Ada", "Tidak Ada", "Berkurang", "Rusak"],
                    index=["Ada", "Tidak Ada", "Berkurang", "Rusak"].index(row['Status']),
                    key=f"status_{idx}"
                )
                
                # Kondisi dropdown
                kondisi = st.selectbox(
                    f"Kondisi #{int(row['No.'])}",
                    ["Baik", "Rusak Ringan", "Rusak Berat", "Kadaluarsa"],
                    index=["Baik", "Rusak Ringan", "Rusak Berat", "Kadaluarsa"].index(row['Kondisi']),
                    key=f"kondisi_{idx}"
                )
            
            with col3:
                # Jumlah (kg) - bisa diedit
                jumlah = st.number_input(
                    f"Jumlah Aktual (kg) #{int(row['No.'])}",
                    min_value=0.0,
                    step=0.01,
                    value=float(row['Jumlah (kg)']),
                    key=f"jumlah_{idx}"
                )
                
                # Catatan
                catatan = st.text_area(
                    f"Catatan #{int(row['No.'])}",
                    value=row['Catatan'],
                    placeholder="Tambahkan catatan jika diperlukan...",
                    key=f"catatan_{idx}"
                )
            
            # Tambahkan data yang diedit
            edited_data.append({
                'No.': row['No.'],
                'Tanggal': row['Tanggal'],
                'Jenis': row['Jenis'],
                'Kode Produksi': row['Kode Produksi'],
                'Jumlah (kg)': jumlah,
                'Kode Palet': row['Kode Palet'],
                'Status': status,
                'Kondisi': kondisi,
                'Catatan': catatan
            })
            
            st.markdown("---")
        
        # Tombol submit
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button(
                "💾 SIMPAN SEMUA PERUBAHAN",
                use_container_width=True,
                type="primary"
            )
    
    # Proses ketika form disubmit
    if submitted:
        # Update session state dengan data yang diedit
        st.session_state.data_produksi = pd.DataFrame(edited_data)
        st.session_state.data_edited = True
        
        st.success("✅ Semua perubahan berhasil disimpan!")
        st.balloons()
    
    # Tampilkan summary setelah edit
    st.markdown("---")
    st.subheader("📊 SUMMARY PENGEČEKAN")
    
    if not st.session_state.data_produksi.empty:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_data = len(st.session_state.data_produksi)
            st.metric("Total Data", total_data)
        
        with col2:
            status_ada = len(st.session_state.data_produksi[st.session_state.data_produksi['Status'] == 'Ada'])
            st.metric("Status: Ada", f"{status_ada}/{total_data}")
        
        with col3:
            status_tidak_ada = len(st.session_state.data_produksi[st.session_state.data_produksi['Status'] == 'Tidak Ada'])
            st.metric("Status: Tidak Ada", f"{status_tidak_ada}/{total_data}")
        
        with col4:
            kondisi_baik = len(st.session_state.data_produksi[st.session_state.data_produksi['Kondisi'] == 'Baik'])
            st.metric("Kondisi: Baik", f"{kondisi_baik}/{total_data}")
        
        # Tampilkan data dalam tabel
        st.markdown("### 📋 DATA TERUPDATE")
        
        # Format dataframe untuk display
        display_df = st.session_state.data_produksi.copy()
        
        # Tambahkan warna untuk status
        def color_status(val):
            if val == 'Ada':
                return 'background-color: #d4edda; color: #155724;'
            elif val == 'Tidak Ada':
                return 'background-color: #f8d7da; color: #721c24;'
            elif val == 'Berkurang':
                return 'background-color: #fff3cd; color: #856404;'
            elif val == 'Rusak':
                return 'background-color: #f5c6cb; color: #721c24;'
            return ''
        
        # Tambahkan warna untuk kondisi
        def color_kondisi(val):
            if val == 'Baik':
                return 'background-color: #d1ecf1; color: #0c5460;'
            elif val == 'Rusak Ringan':
                return 'background-color: #ffeaa7; color: #856404;'
            elif val == 'Rusak Berat':
                return 'background-color: #fab1a0; color: #b33939;'
            elif val == 'Kadaluarsa':
                return 'background-color: #a29bfe; color: #2d3436;'
            return ''
        
        # Apply styling
        styled_df = display_df.style.map(color_status, subset=['Status'])\
                                   .map(color_kondisi, subset=['Kondisi'])
        
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
        
        # Tombol download
        st.markdown("---")
        st.subheader("💾 EXPORT DATA")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Download Excel
            excel_buffer = BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                st.session_state.data_produksi.to_excel(
                    writer,
                    index=False,
                    sheet_name='Hasil Pengecekan'
                )
            
            excel_buffer.seek(0)
            
            st.download_button(
                label="📥 DOWNLOAD EXCEL",
                data=excel_buffer,
                file_name=f"hasil_pengecekan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        
        with col2:
            # Download CSV
            csv_buffer = BytesIO()
            st.session_state.data_produksi.to_csv(csv_buffer, index=False)
            csv_buffer.seek(0)
            
            st.download_button(
                label="📄 DOWNLOAD CSV",
                data=csv_buffer,
                file_name=f"hasil_pengecekan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col3:
            # Tombol reset ke data awal
            if st.button("🔄 RESET KE DATA AWAL", use_container_width=True):
                init_session_state()
                st.success("✅ Data telah direset ke kondisi awal!")
                st.rerun()
        
        # Tampilkan data yang bermasalah
        st.markdown("---")
        st.subheader("⚠️ DATA YANG PERLU PERHATIAN")
        
        # Filter data yang bermasalah
        masalah_df = st.session_state.data_produksi[
            (st.session_state.data_produksi['Status'] != 'Ada') |
            (st.session_state.data_produksi['Kondisi'] != 'Baik') |
            (st.session_state.data_produksi['Catatan'] != '')
        ]
        
        if not masalah_df.empty:
            st.dataframe(masalah_df, use_container_width=True, hide_index=True)
            
            # Summary masalah
            st.markdown("**Ringkasan Masalah:**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                for status in ['Tidak Ada', 'Berkurang', 'Rusak']:
                    count = len(st.session_state.data_produksi[st.session_state.data_produksi['Status'] == status])
                    if count > 0:
                        st.write(f"- **Status {status}:** {count} data")
            
            with col2:
                for kondisi in ['Rusak Ringan', 'Rusak Berat', 'Kadaluarsa']:
                    count = len(st.session_state.data_produksi[st.session_state.data_produksi['Kondisi'] == kondisi])
                    if count > 0:
                        st.write(f"- **Kondisi {kondisi}:** {count} data")
        else:
            st.success("🎉 Semua data dalam kondisi baik!")
    
    st.markdown("---")
    st.caption("""
    **Aplikasi Pengecekan Data Produksi** - 
    Data awal sudah terisi. Lakukan pengecekan di lapangan dan update sesuai kondisi aktual.
    """)

if __name__ == "__main__":
    main()
