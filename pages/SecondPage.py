import streamlit as st
import pandas as pd

st.header("📊 Analisis Awal Data")

if "df" not in st.session_state:
    st.warning("⚠️ Silakan unggah dan proses file terlebih dahulu di halaman 'Unggah dan Preprocessing'.")
    st.stop()

df = st.session_state.df

st.write(f"Jumlah baris: **{df.shape[0]}**, kolom: **{df.shape[1]}**")

# Deteksi tipe campuran
mixed_cols = [col for col in df.columns if df[col].map(type).nunique() > 1]
if mixed_cols:
    st.warning("Kolom bertipe data campuran:")
    st.write(mixed_cols)
else:
    st.success("✅ Tidak ada kolom bertipe campuran.")

# Statistik numerik
st.subheader("📈 Statistik Numerik")
st.dataframe(df.select_dtypes(include="number").describe(), use_container_width=True)

# Distribusi nilai unik 5 kolom pertama
st.subheader("🔢 Distribusi Nilai Unik (5 Kolom Pertama)")
for col in df.columns[:5]:
    st.write(f"**{col}** - Jumlah nilai unik: {df[col].nunique()}")
    st.dataframe(df[col].value_counts().reset_index().rename(columns={"index": "Nilai", col: "Frekuensi"}))
