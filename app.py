import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO

def main():
    st.set_page_config(
        page_title="Form Input Data Produksi",
        page_icon="🏭",
        layout="wide"
    )
    
    st.title("🏭 FORM INPUT DATA PRODUKSI")
    st.markdown("---")
    
    # SIMPLE VERSION - hanya form basic
    with st.form("input_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            tgl = st.date_input("📅 Tanggal", datetime.now())
            jenis = st.selectbox("📦 Jenis Data", ["Prod", "Blen"])
        
        with col2:
            kode = st.text_input("🏷️ Kode Produksi", placeholder="076, 054, etc")
            berat = st.number_input("⚖️ Jumlah (kg)", min_value=0.0, step=0.01)
        
        kode_palet = st.text_input("📦 Kode Palet", placeholder="Opsional")
        
        submitted = st.form_submit_button("💾 SIMPAN DATA")
    
    if submitted:
        st.success(f"✅ Data berhasil disimpan!")
        
        # Buat DataFrame
        data = pd.DataFrame([{
            'Tanggal': tgl.strftime('%d-%m-%Y'),
            'Jenis': jenis,
            'Kode Produksi': kode,
            'Jumlah (kg)': berat,
            'Kode Palet': kode_palet
        }])
        
        # Tampilkan preview
        st.dataframe(data)
        
        # Download Excel
        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            data.to_excel(writer, index=False, sheet_name='Data Produksi')
        
        excel_buffer.seek(0)
        
        st.download_button(
            label="📥 DOWNLOAD EXCEL",
            data=excel_buffer,
            file_name=f"data_produksi_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    st.markdown("---")
    st.info("ℹ️ Aplikasi berjalan dengan baik!")

if __name__ == "__main__":
    main()
