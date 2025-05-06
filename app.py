import streamlit as st
import pandas as pd
import tempfile

from preprocessing import preprocess_excel_file, generate_label
from modeling import (
    train_models,
    evaluate_model,
    plot_confusion_matrix,
    plot_feature_importance,
    plot_decision_tree,
)

# Constants
total_given_col = (
    'KONVERGENSI_LAYANAN_STUNTING_DESA_a._Total_Layanan_Konvergensi_Stunting_di_Desa'
)
total_received_col = (
    'KONVERGENSI_LAYANAN_STUNTING_DESA_b._Total_Layanan_Konvergensi_Stunting_yang_diterima_di_Desa'
)
label_col = 'label_efektivitas'

# Cleaning function
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    # Standardize categorical mappings
    cat_map = {
        'ya': 1, 'iya': 1, 'ada': 1,
        'tidak': 0, 'tidak ada': 0,
        'rutin tiap bulan': 1, 'tiap bulan': 1, 'aktif setiap bulan': 1
    }
    # Map categorical columns
    for col in df.columns:
        if 'KONVERGENSI_LAYANAN_STUNTING_DESA' in col and col not in [total_given_col, total_received_col]:
            df[col] = (
                df[col]
                .astype(str)
                .str.lower()
                .str.strip()
                .map(cat_map)
                .astype(float)
            )
    # Numeric conversion for given/received
    for col in [total_given_col, total_received_col]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    # Derived ratio
    if total_given_col in df.columns and total_received_col in df.columns:
        df['RASIO_LAYANAN'] = df[total_received_col] / df[total_given_col]
    # Fill NaN in numeric
    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    if num_cols:
        df[num_cols] = df[num_cols].fillna(0)
    # Drop rows missing label
    if label_col in df.columns:
        df = df.dropna(subset=[label_col])
    # Drop free-text
    df = df.loc[:, ~df.columns.str.contains('kendala', case=False)]
    # Force numeric types
    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    if num_cols:
        df[num_cols] = df[num_cols].astype('float64')
    # Rebuild DataFrame to pure NumPy-backed
    df = pd.DataFrame(df.values, columns=df.columns)
    # Drop unnamed or pure-numeric column names
    df = df.loc[:, ~df.columns.str.match(r'^(Unnamed|\d+)$')]
    return df

# Streamlit UI
st.set_page_config(page_title="Stunting Classifier", layout="wide")
st.title("📊 Aplikasi Klasifikasi Efektivitas Intervensi Stunting Desa")

uploaded = st.file_uploader("Unggah file Excel", type=["xlsx", "xls"])
if uploaded:
    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
        tmp.write(uploaded.read())
        path = tmp.name
    # Load & clean
    try:
        df = preprocess_excel_file(path)
        df = generate_label(df, total_given_col, total_received_col)
        df = clean_data(df)
        if df.empty:
            st.error('Data kosong setelah preprocessing.')
            st.stop()
        st.success('✅ Data siap diproses!')
    except Exception as e:
        st.error(f'❌ Gagal preprocessing: {e}')
        st.stop()

        # Preview & Debug
    st.subheader('Preview Data')
    st.table(df.head())  # static table, no Arrow
    st.text(df.dtypes.to_string())
    st.metric('Jumlah Baris', len(df))

    # Descriptive Stats
    num_df = df.select_dtypes(include=['number'])
    if not num_df.empty:
        st.subheader('Statistik Deskriptif')
        st.write(num_df.describe())  # safe rendering
    else:
        st.warning('⚠️ Tidak ada kolom numerik untuk statistik.')

    # Modeling
    st.subheader('Modeling Klasifikasi')
    if label_col not in df.columns:
        st.error('Label tidak ditemukan.')
        st.stop()

    mode = st.radio('Mode Pemilihan Fitur', ['Otomatis', 'Manual'])
    feat_cols = df.select_dtypes(include=['number']).columns.tolist()
    for c in [total_given_col, total_received_col, 'RASIO_LAYANAN', label_col]:
        if c in feat_cols:
            feat_cols.remove(c)
    if mode == 'Otomatis':
        features = feat_cols
    else:
        features = st.multiselect('Pilih fitur:', options=feat_cols, default=feat_cols[:5])
    if not features:
        st.error('Pilih minimal satu fitur.')
        st.stop()

    X = df[features]
    y = df[label_col]
    if X.shape[1] == 0 or X.dropna(how='all').shape[0] == 0:
        st.error('Data fitur kosong.')
        st.stop()

    try:
        dt_model, rf_model, X_test, y_test = train_models(df, features, label_col)
        st.success('✅ Model berhasil dilatih!')

                # Decision Tree
        st.subheader('Decision Tree')
        rpt_dt, cm_dt, cls_dt = evaluate_model(dt_model, X_test, y_test)
        # Display classification report as text to avoid Arrow serialization
        dt_report_df = pd.DataFrame(rpt_dt).transpose()
        st.text(dt_report_df.to_string())
        st.pyplot(plot_confusion_matrix(cm_dt, 'Decision Tree', cls_dt))

        st.subheader('Decision Tree')
        rpt_dt, cm_dt, cls_dt = evaluate_model(dt_model, X_test, y_test)
        st.write(pd.DataFrame(rpt_dt).transpose())
        st.pyplot(plot_confusion_matrix(cm_dt, 'Decision Tree', cls_dt))

                # Random Forest
        st.subheader('Random Forest')
        rpt_rf, cm_rf, cls_rf = evaluate_model(rf_model, X_test, y_test)
        rf_report_df = pd.DataFrame(rpt_rf).transpose()
        st.text(rf_report_df.to_string())
        st.pyplot(plot_confusion_matrix(cm_rf, 'Random Forest', cls_rf))

        st.subheader('Random Forest')
        rpt_rf, cm_rf, cls_rf = evaluate_model(rf_model, X_test, y_test)
        st.write(pd.DataFrame(rpt_rf).transpose())
        st.pyplot(plot_confusion_matrix(cm_rf, 'Random Forest', cls_rf))

        # Feature Importance
        st.subheader('Feature Importance (RF)')
        st.pyplot(plot_feature_importance(rf_model, features))

        # Decision Tree Visualization
        st.subheader('Visualisasi Decision Tree')
        st.pyplot(plot_decision_tree(dt_model, features, class_names=cls_dt))
    except Exception as e:
        st.error(f'Gagal pelatihan: {e}')
