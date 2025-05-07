import streamlit as st
import pandas as pd
import tempfile
import os
import numpy as np
from preprocessing import preprocess_excel_file, generate_label
from modeling import (
    train_models,
    evaluate_model,
    plot_confusion_matrix,
    plot_feature_importance,
    plot_decision_tree,
)

def clean_data(df):
    # Periksa tipe data pada semua kolom
    print(df.dtypes)

    # Identifikasi kolom-kolom dengan tipe data campuran
    mixed_type_columns = []
    for col in df.columns:
        unique_types = df[col].map(type).nunique()
        if unique_types > 1:
            mixed_type_columns.append(col)

    # Bersihkan kolom-kolom dengan tipe data campuran
    for col in mixed_type_columns:
        # Identifikasi nilai unik pada kolom bermasalah
        print(f"Nilai unik pada kolom '{col}': {df[col].unique()}")

        # Ganti nilai non-numerik dengan NaN
        df[col] = df[col].replace(['Ya', 'Tidak', 'Ada', 'TIDAK', 'ada', 'ADA', 'iya', 'IYA', 'tidak', 'Iya', 'Tidak '], [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan])

        # Konversi kolom ke tipe numerik
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Hapus baris dengan nilai NaN (opsional, tergantung kebutuhan analisis Anda)
    df = df.dropna()

    # Reset index jika perlu
    df = df.reset_index(drop=True)

    return df

st.set_page_config(page_title="Stunting Classifier", layout="wide")

st.title("📊 Aplikasi Klasifikasi Efektivitas Intervensi Stunting Desa")

uploaded_file = st.file_uploader("Unggah file Excel", type=["xlsx", "xls"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_path = tmp_file.name

    try:
        df = preprocess_excel_file(temp_path)
        
        try:
            df = generate_label(
                df.copy(),
                total_diberikan_col="KONVERGENSI_LAYANAN_STUNTING_DESA_a._Total_Layanan_Konvergensi_Stunting_di_Desa",
                total_diterima_col="KONVERGENSI_LAYANAN_STUNTING_DESA_b._Total_Layanan_Konvergensi_Stunting_yang_diterima_di_Desa"
            )
            st.success("✅ Label intervensi berhasil dihitung dan ditambahkan ke DataFrame!")
        except Exception as e:
            st.error(f"❌ Gagal menghitung label intervensi: {e}")
        
        # Bersihkan data
        st.write("Cleaning data...")
        df = clean_data(df)

        # Simpan ke session_state hanya setelah label berhasil (atau setidaknya sudah diproses)
        st.session_state.df = df
        st.success("✅ File berhasil diproses dan disiapkan!")
        
        st.subheader("🧾 Dataframe Awal (Setelah Preprocessing)")
        st.dataframe(st.session_state.df, use_container_width=True)
        
        # #Untuk lihat header tabel dalam dataframe setelah di process (proses debug untuk ambil kolom header)
        # st.subheader("🧾 Daftar Kolom dalam DataFrame")
        # st.write(df.columns.tolist())
        
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

         # ------------------ Modeling ------------------ #
        st.subheader("🧠 Modeling Klasifikasi")

        label_col = "label_efektivitas"
        df_model = st.session_state.df.copy()
        
        df_model = df_model.dropna() # Pastikan tidak ada nilai NaN sebelum melatih model
        
        numeric_columns = df_model.select_dtypes(include=['number']).columns
        df_model[numeric_columns] = df_model[numeric_columns].apply(pd.to_numeric, errors='coerce')
        
        if "label_efektivitas" not in df.columns:
            st.error("Label tidak berhasil dibuat. Periksa fungsi generate_label().")
        else:
            st.success("Label berhasil dibuat!")

        if label_col not in df_model.columns:
            st.error("Label belum tersedia. Pastikan data sudah diproses dan diberi label.")
        else:
            # Konversi label ke string (antisipasi error)
            df_model[label_col] = df_model[label_col].astype(str)

            feature_selection_mode = st.radio("Pilih cara pemilihan fitur:", ["Otomatis", "Manual"])

            if feature_selection_mode == "Otomatis":
                features = df_model.select_dtypes(include="number").columns.tolist()
                if label_col in features:
                    features.remove(label_col)
            else:
                all_columns = df_model.columns.tolist()
                features = st.multiselect("Pilih fitur secara manual:", options=[col for col in all_columns if col != label_col])

            if features:
                with st.spinner("Melatih model..."):
                    try:
                        dt_model, rf_model, X_test, y_test = train_models(df_model, features, label_col)
                        st.success("✅ Model berhasil dilatih!")

                        # Evaluasi Decision Tree
                        st.subheader("📋 Evaluasi Model: Decision Tree")
                        dt_report, dt_cm = evaluate_model(dt_model, X_test, y_test)
                        st.text("Classification Report")
                        st.json(dt_report)

                        st.pyplot(plot_confusion_matrix(dt_cm, "Decision Tree"))

                        # Evaluasi Random Forest
                        st.subheader("🌲 Evaluasi Model: Random Forest")
                        rf_report, rf_cm = evaluate_model(rf_model, X_test, y_test)
                        st.text("Classification Report")
                        st.json(rf_report)

                        st.pyplot(plot_confusion_matrix(rf_cm, "Random Forest"))

                        # Visualisasi feature importance
                        st.subheader("📊 Feature Importance (Random Forest)")
                        st.pyplot(plot_feature_importance(rf_model, features))

                        # Visualisasi decision tree
                        st.subheader("🌳 Visualisasi Decision Tree")
                        st.pyplot(plot_decision_tree(dt_model, features, class_names=["Efektif", "Kurang Efektif", "Tidak Efektif"]))
                    except Exception as e:
                        st.error(f"❌ Gagal melakukan pelatihan atau evaluasi model: {e}")
            else:
                st.warning("⚠️ Belum ada fitur yang dipilih.")
        
    except Exception as e:
        st.error(f"Terjadi kesalahan saat memproses file: {e}")
    finally:
        # Hapus file sementara
        os.remove(temp_path)

