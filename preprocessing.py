import pandas as pd

# Definisi nama kolom penting (hasil dari debug_headers.py)
KODE_DESA_COL = "KODE_DESA_Unnamed: 6_level_1"
NAMA_DESA_COL = "NAMA_DESA_Unnamed: 7_level_1"

def preprocess_excel_file(file_path: str) -> pd.DataFrame:
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
            raise ValueError(f"Kolom '{KODE_DESA_COL}' dan '{NAMA_DESA_COL}' tidak ditemukan.")

        # Hapus baris-baris yang tidak memiliki KODE_DESA atau NAMA_DESA
        df_raw = df_raw.dropna(subset=[KODE_DESA_COL, NAMA_DESA_COL])

        # Reset index untuk memastikan indexing rapi
        df_raw.reset_index(drop=True, inplace=True)
        
        # Ubah semua kolom ke string agar kompatibel dengan Streamlit dan Arrow
        df_raw = df_raw.astype(str)

        return df_raw

    except Exception as e:
        raise RuntimeError(f"Terjadi kesalahan saat memproses file: {e}")

#Fungsi generate label
def generate_label(df, total_diberikan_col: str, total_diterima_col: str, label_col: str = "LABEL_INTERVENSI") -> pd.DataFrame:
    if total_diberikan_col not in df.columns or total_diterima_col not in df.columns:
        raise ValueError(f"Kolom '{total_diberikan_col}' atau '{total_diterima_col}' tidak ditemukan dalam DataFrame.")

    try:
        df[total_diberikan_col] = pd.to_numeric(df[total_diberikan_col], errors='coerce')
        df[total_diterima_col] = pd.to_numeric(df[total_diterima_col], errors='coerce')

        df["RASIO_LAYANAN"] = df[total_diterima_col] / df[total_diberikan_col]
        df[label_col] = df["RASIO_LAYANAN"].apply(
            lambda x: 1 if x > 0.8 else (0 if x < 0.5 else None)
        )
    except Exception as e:
        raise RuntimeError(f"Gagal menghitung label intervensi: {e}")

    return df
