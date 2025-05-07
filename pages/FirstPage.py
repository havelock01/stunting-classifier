import streamlit as st
import pandas as pd
import tempfile
import os
from preprocessing import preprocess_excel_file, generate_label

st.header("📥 Unggah dan Preprocessing Data")

uploaded_file = st.file_uploader("Unggah file Excel", type=["xlsx", "xls"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_path = tmp_file.name

    try:
        df = preprocess_excel_file(temp_path)
        st.session_state.df = df
        st.success("✅ File berhasil diproses!")

        try:
            df_labeled = generate_label(
                df.copy(),
                total_diberikan_col="KONVERGENSI_LAYANAN_STUNTING_DESA_a._Total_Layanan_Konvergensi_Stunting_di_Desa",
                total_diterima_col="KONVERGENSI_LAYANAN_STUNTING_DESA_b._Total_Layanan_Konvergensi_Stunting_yang_diterima_di_Desa"
            )
            st.session_state.df = df_labeled
            st.success("✅ Label intervensi berhasil dihitung!")
        except Exception as e:
            st.error(f"❌ Gagal menghitung label: {e}")

        st.subheader("📋 Dataframe Awal")
        st.dataframe(st.session_state.df, use_container_width=True)

    except Exception as e:
        st.error(f"Terjadi kesalahan saat memproses file: {e}")
    finally:
        os.remove(temp_path)
