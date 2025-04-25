# import streamlit as st
# from preprocessing import load_and_clean_data, INDICATORS
# from modeling import train_models, evaluate_model, plot_confusion_matrix, plot_feature_importance, plot_decision_tree
# from utils import predict_manual, filter_by_label

# st.set_page_config(page_title="Klasifikasi Efektivitas Intervensi Stunting", layout="wide")

# st.title("📊 Aplikasi Klasifikasi Efektivitas Intervensi Stunting di Desa")
# st.markdown("Gunakan file Excel dari Kementerian Desa PDTT (2023)")

# # Upload file
# uploaded_file = st.file_uploader("Unggah file Excel", type=["xlsx"])

# if uploaded_file:
#     try:
#         df = load_and_clean_data(uploaded_file)
#         st.success("✅ Data berhasil dibaca dan diproses!")
#         st.write("📄 Preview Data:", df.head())

#         # Train models
#         dt_model, rf_model, X_test, y_test = train_models(df, INDICATORS)
#         st.subheader("🎓 Evaluasi Model")

#         # Evaluasi Decision Tree
#         report_dt, cm_dt = evaluate_model(dt_model, X_test, y_test)
#         st.markdown("**Decision Tree**")
#         st.text(f"Akurasi: {report_dt['accuracy']:.2%}")
#         st.pyplot(plot_confusion_matrix(cm_dt, "Decision Tree"))

#         # Evaluasi Random Forest
#         report_rf, cm_rf = evaluate_model(rf_model, X_test, y_test)
#         st.markdown("**Random Forest**")
#         st.text(f"Akurasi: {report_rf['accuracy']:.2%}")
#         st.pyplot(plot_confusion_matrix(cm_rf, "Random Forest"))

#         # Feature Importance
#         st.subheader("📌 Feature Importance (Random Forest)")
#         st.pyplot(plot_feature_importance(rf_model, INDICATORS))

#         # Visualisasi Decision Tree
#         st.subheader("🌳 Visualisasi Decision Tree")
#         st.pyplot(plot_decision_tree(dt_model, INDICATORS, dt_model.classes_))

#         # Klasifikasi Manual
#         predict_manual(rf_model, INDICATORS, [
#             "Pembentukan RDS/TPPS",
#             "Pelaku Desa mendapatkan peningkatan kapasitas",
#             "Posyandu rutin",
#             "Kelas BKB rutin",
#             "PAUD aktif",
#             "Ketahanan pangan dikembangkan",
#             "Rapat koordinasi RDS/TPPS",
#             "Monitoring/Evaluasi minimal 2 kali/tahun"
#         ])

#         # Filter Berdasarkan Efektivitas
#         filter_by_label(df)

#         # Unduh hasil
#         st.subheader("⬇️ Unduh Hasil Klasifikasi")
#         st.download_button(
#             label="Download sebagai Excel",
#             data=df.to_excel(index=False, engine="openpyxl"),
#             file_name="hasil_klasifikasi_stunting.xlsx",
#             mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#         )

#     except Exception as e:
#         st.error(f"Terjadi kesalahan saat memproses file: {e}")


# import streamlit as st
# import pandas as pd
# from preprocessing import preprocess_excel_file

# st.set_page_config(page_title="Aplikasi Klasifikasi Intervensi Stunting", layout="wide")

# st.title("📊 Aplikasi Klasifikasi Efektivitas Intervensi Stunting")
# st.markdown("Silakan unggah file Excel data stunting desa untuk diproses.")

# uploaded_file = st.file_uploader("Unggah file Excel (.xlsx)", type=["xlsx"])

# if uploaded_file is not None:
#     try:
#         with st.spinner("Sedang memproses file..."):
#             # Simpan file sementara lalu proses
#             df_cleaned = preprocess_excel_file(uploaded_file)

#         st.success("File berhasil diproses!")
#         st.subheader("🔍 Data setelah Preprocessing")
#         st.dataframe(df_cleaned.astype(str))

#         st.markdown(f"Jumlah baris: `{df_cleaned.shape[0]}` | Jumlah kolom: `{df_cleaned.shape[1]}`")

#     except Exception as e:
#         st.error(f"Terjadi kesalahan saat memproses file: {e}")

import streamlit as st
import pandas as pd
from preprocessing import preprocess_file

st.set_page_config(page_title="Stunting Classifier", layout="wide")

st.title("📊 Aplikasi Klasifikasi Efektivitas Intervensi Stunting")
st.write("Unggah file Excel data stunting dari Kemendesa PDTT untuk diproses dan dianalisis.")

uploaded_file = st.file_uploader("Unggah file Excel", type=["xlsx"])

if uploaded_file is not None:
    try:
        df_cleaned, original_headers = preprocess_file(uploaded_file)
        st.success("✅ File berhasil diproses!")

        # Tampilkan informasi dasar
        st.write(f"Jumlah baris: {df_cleaned.shape[0]}, Jumlah kolom: {df_cleaned.shape[1]}")

        # Tampilkan dataframe yang aman untuk UI
        st.subheader("📋 Preview Data (Tampilan Aman)")
        st.dataframe(df_cleaned.astype(str))  # Convert to string only for display

        # Simpan data asli untuk proses lanjut (misal modeling)
        st.session_state.df_cleaned = df_cleaned  # simpan di session_state

        # Tombol untuk ke langkah selanjutnya (misalnya modeling)
        if st.button("🔍 Lanjut ke Analisis / Modeling"):
            st.write("✅ Data siap digunakan untuk modeling (tipe data asli tetap terjaga).")
            # kamu bisa lanjutkan dengan modul analisis atau training di sini

    except Exception as e:
        st.error(f"❌ Terjadi kesalahan saat memproses file: {str(e)}")
else:
    st.info("Silakan unggah file Excel untuk mulai analisis.")
