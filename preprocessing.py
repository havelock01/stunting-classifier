import pandas as pd
import numpy as np

# Definisi nama kolom penting (hasil dari debug_headers.py)
KODE_DESA_COL = "KODE_DESA_Unnamed: 6_level_1"
NAMA_DESA_COL = "NAMA_DESA_Unnamed: 7_level_1"

def preprocess_excel_file(file_path: str) -> pd.DataFrame:
    global KODE_DESA_COL, NAMA_DESA_COL
    try:
        # Membaca 2 baris pertama sebagai multi-header
        df_raw = pd.read_excel(file_path, header=[0, 2])

        # Gabungkan nama kolom multi-index menjadi satu string
        df_raw.columns = [
            f"{col[0]}_{col[1]}" if "Unnamed" not in col[1] else f"{col[0]}_{col[1]}"
            for col in df_raw.columns
        ]

        # Buang kolom yang semua nilainya kosong
        df_raw.dropna(axis=1, how="all", inplace=True)

        # Validasi: pastikan kolom KODE_DESA dan NAMA_DESA ada
        if KODE_DESA_COL not in df_raw.columns or NAMA_DESA_COL not in df_raw.columns:
            # Try to find columns with similar names if exact match not found
            kode_desa_cols = [col for col in df_raw.columns if "KODE_DESA" in col]
            nama_desa_cols = [col for col in df_raw.columns if "NAMA_DESA" in col]
            
            if kode_desa_cols and nama_desa_cols:
                # Use the first matching column
                KODE_DESA_COL = kode_desa_cols[0]
                NAMA_DESA_COL = nama_desa_cols[0]
                print(f"Using alternative columns: {KODE_DESA_COL} and {NAMA_DESA_COL}")
            else:
                raise ValueError(f"Kolom KODE_DESA dan NAMA_DESA tidak ditemukan.")

        # Hapus baris-baris yang tidak memiliki KODE_DESA atau NAMA_DESA
        df_raw = df_raw.dropna(subset=[KODE_DESA_COL, NAMA_DESA_COL])

        # Reset index untuk memastikan indexing rapi
        df_raw.reset_index(drop=True, inplace=True)
        
        return df_raw

    except Exception as e:
        raise RuntimeError(f"Terjadi kesalahan saat memproses file: {e}")

# Fungsi generate label
def generate_label(df, total_diberikan_col: str, total_diterima_col: str, label_col: str = "label_efektivitas") -> pd.DataFrame:
    # Check if required columns exist
    if total_diberikan_col not in df.columns:
        raise ValueError(f"Kolom '{total_diberikan_col}' tidak ditemukan dalam DataFrame.")
    if total_diterima_col not in df.columns:
        raise ValueError(f"Kolom '{total_diterima_col}' tidak ditemukan dalam DataFrame.")

    try:
        # Convert to numeric, with additional handling for non-numeric values
        df[total_diberikan_col] = pd.to_numeric(df[total_diberikan_col], errors='coerce')
        df[total_diterima_col] = pd.to_numeric(df[total_diterima_col], errors='coerce')
        
        # Handle division by zero - replace zeros with NaN
        df_copy = df.copy()
        mask = (df_copy[total_diberikan_col] > 0) 
        
        # Initialize RASIO_LAYANAN with NaN
        df_copy["RASIO_LAYANAN"] = np.nan
        
        # Calculate ratio only where denominator > 0
        df_copy.loc[mask, "RASIO_LAYANAN"] = df_copy.loc[mask, total_diterima_col] / df_copy.loc[mask, total_diberikan_col]
        
        # Apply label categorization
        df_copy[label_col] = df_copy["RASIO_LAYANAN"].apply(
            lambda x: "Efektif" if x > 0.8 else 
                     ("Tidak Efektif" if x < 0.5 else 
                      "Kurang Efektif") if pd.notnull(x) else np.nan
        )
        
        return df_copy
        
    except Exception as e:
        raise RuntimeError(f"Gagal menghitung label intervensi: {e}")