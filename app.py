import streamlit as st
import pandas as pd
import tempfile
import os
from preprocessing import preprocess_excel_file

st.set_page_config(page_title="Stunting Classifier", layout="wide")

st.title("📊 Aplikasi Klasifikasi Efektivitas Intervensi Stunting Desa")

uploaded_file = st.file_uploader("Unggah file Excel", type=["xlsx", "xls"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_path = tmp_file.name

    try:
        df = preprocess_excel_file(temp_path)
        st.success("✅ File berhasil diproses!")
        st.subheader("🧾 Dataframe Awal (Setelah Preprocessing)")
        st.dataframe(df, use_container_width=True)

        # --- ANALISIS AWAL ---
        st.subheader("🔍 Analisis Awal Data")

        # Jumlah baris dan kolom
        num_rows, num_cols = df.shape
        st.write(f"Jumlah baris: **{num_rows}**, Jumlah kolom: **{num_cols}**")

        # Deteksi kolom dengan tipe data campuran
        mixed_type_columns = []
        for col in df.columns:
            unique_types = df[col].map(type).nunique()
            if unique_types > 1:
                mixed_type_columns.append(col)

        if mixed_type_columns:
            st.warning("⚠️ Ditemukan kolom dengan tipe data campuran:")
            for col in mixed_type_columns:
                st.write(f"- {col}")
        else:
            st.success("✅ Tidak ada kolom bertipe campuran.")

        # Statistik deskriptif
        st.subheader("📈 Statistik Deskriptif (Numerik)")
        try:
            df_numeric = df.apply(pd.to_numeric, errors="coerce")
            st.dataframe(df_numeric.describe(), use_container_width=True)
        except Exception as e:
            st.error(f"Gagal menghitung statistik deskriptif: {e}")

        # Distribusi nilai unik dari beberapa kolom awal (optional)
        st.subheader("🔢 Distribusi Nilai Unik Beberapa Kolom Awal")
        cols_to_check = df.columns[:5]  # contoh 5 kolom pertama
        for col in cols_to_check:
            st.write(f"**{col}** - Jumlah nilai unik: {df[col].nunique()}")
            st.dataframe(df[col].value_counts().reset_index().rename(columns={'index': 'Nilai', col: 'Frekuensi'}))

    except Exception as e:
        st.error(f"Terjadi kesalahan saat memproses file: {e}")
    finally:
        # Hapus file sementara
        os.remove(temp_path)
