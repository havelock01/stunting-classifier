import streamlit as st
import pandas as pd

def predict_manual(model, indicators, indicator_names):
    st.subheader("📝 Klasifikasi Manual untuk 1 Desa")

    # Input checkbox untuk 8 indikator
    values = []
    for ind in indicator_names:
        values.append(st.checkbox(ind))

    # Buat DataFrame untuk prediksi
    input_df = pd.DataFrame([values], columns=indicators)

    # Lakukan prediksi
    if st.button("Prediksi"):
        prediction = model.predict(input_df)[0]
        st.success(f"🎯 Hasil Prediksi: **{prediction}**")

def filter_by_label(df):
    st.subheader("🔍 Filter Berdasarkan Efektivitas")

    label_filter = st.multiselect(
        "Pilih kategori efektivitas yang ingin ditampilkan:",
        options=df["label_efektivitas"].unique().tolist(),
        default=df["label_efektivitas"].unique().tolist()
    )

    filtered_df = df[df["label_efektivitas"].isin(label_filter)]
    st.dataframe(filtered_df)

    return filtered_df
