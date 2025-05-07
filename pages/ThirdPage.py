import streamlit as st
import pandas as pd
from modeling import train_models, evaluate_model, plot_confusion_matrix, plot_feature_importance, plot_decision_tree

st.header("🧠 Modeling Klasifikasi Efektivitas Intervensi")

if "df" not in st.session_state or "label_efektivitas" not in st.session_state.df.columns:
    st.warning("⚠️ Label belum tersedia. Silakan proses data terlebih dahulu di halaman 'Unggah dan Preprocessing'.")
    st.stop()

df = st.session_state.df
label_col = "label_efektivitas"
df[label_col] = df[label_col].astype(str)

mode = st.radio("Pilih mode pemilihan fitur:", ["Otomatis", "Manual"])
if mode == "Otomatis":
    features = df.select_dtypes(include="number").columns.tolist()
    if label_col in features:
        features.remove(label_col)
else:
    features = st.multiselect("Pilih fitur manual:", options=[col for col in df.columns if col != label_col])

if features:
    # Bersihkan data numerik
    df_clean = df.copy()
    df_clean[features] = df_clean[features].apply(pd.to_numeric, errors="coerce")  # ubah ke numerik
    df_clean[features] = df_clean[features].replace([float("inf"), float("-inf")], pd.NA)  # ubah inf jadi NaN
    df_clean = df_clean.dropna(subset=features)  # buang baris dengan NaN di fitur

    # Gunakan df_clean untuk modeling
    df = df_clean
    with st.spinner("Melatih model..."):
        try:
            dt_model, rf_model, X_test, y_test = train_models(df, features, label_col)
            st.success("✅ Model berhasil dilatih!")

            # Decision Tree
            st.subheader("📋 Decision Tree")
            dt_report, dt_cm = evaluate_model(dt_model, X_test, y_test)
            st.json(dt_report)
            st.pyplot(plot_confusion_matrix(dt_cm, "Decision Tree"))

            # Random Forest
            st.subheader("🌲 Random Forest")
            rf_report, rf_cm = evaluate_model(rf_model, X_test, y_test)
            st.json(rf_report)
            st.pyplot(plot_confusion_matrix(rf_cm, "Random Forest"))

            # Feature Importance
            st.subheader("📊 Feature Importance (Random Forest)")
            st.pyplot(plot_feature_importance(rf_model, features))

            # Visualisasi Decision Tree
            st.subheader("🌳 Visualisasi Decision Tree")
            st.pyplot(plot_decision_tree(dt_model, features, class_names=["Efektif", "Kurang Efektif", "Tidak Efektif"]))
        except Exception as e:
            st.error(f"❌ Gagal melatih model: {e}")
else:
    st.warning("⚠️ Belum ada fitur yang dipilih.")
