import pandas as pd

# Daftar indikator yang digunakan dalam klasifikasi
# INDICATORS = [
#     "RDS/TPPS_mengadakan_rapat_koordinasi",
#     "Desa_melakukan_monitoring/evaluasi_atas_pelaksanaan_konvergensi_stunting_min._2_kali_dlm_1tahun",
#     "Aktivitas_rutin_Penyelenggaraan_posyandu_",
#     "Aktivitas_rutin_Penyelenggaraan_kelas_Bina_Keluarga_Balita_",
#     "Aktivitas_rutin_Penyelenggaraan_PAUD",
#     "Terdapat_Pelaku_Desa_(Kader,_KPM,_TPK)_mendapatkan_peningkatan_kapasitas",
#     "Terdapat_Pengembangan_Program_Ketahanan_Pangan",
#     "Terdapat_Pembentukan_RDS/TPPS"
# ]
# Error terjadi karena masih tidak terdapat header yang ada di file excel
# def load_and_clean_data(file):
#     try:
#         # Baca file Excel dengan header di baris ke-3
#         df = pd.read_excel(file, header=2, engine="openpyxl")
        
#         # Buang baris kosong
#         df.dropna(subset=["KODE_DESA", "NAMA_DESA"])# df.dropna(subset=["KODE_DESA", "NAMA_DESA"], inplace=True) ", inplace=True dibuang nih dalam kurung karena tidak cocok"

#         # Bersihkan nilai indikator
#         for col in INDICATORS:
#             df[col] = df[col].astype(str).str.lower().str.strip()
#             df[col] = df[col].apply(lambda x: 1 if "ada" in x or "rutin" in x else 0)

#         # Hitung jumlah indikator terpenuhi
#         df["jumlah_indikator_terpenuhi"] = df[INDICATORS].sum(axis=1)

#         # Tambahkan label efektivitas
#         df["label_efektivitas"] = df["jumlah_indikator_terpenuhi"].apply(label_efektivitas)

#         return df
    
#     except Exception as e:
#         raise RuntimeError(f"Terjadi kesalahan saat memproses file: {e}")

# Error masih terjadi karena INDICATORS ga cocok
# def load_and_clean_data(file):
#     try:
#         preview = pd.read_excel(file, header=None, engine="openpyxl")
#         header_row = None
#         for i in range(5):
#             row_values = preview.iloc[i].astype(str).str.upper()
#             if "KODE_DESA" in row_values.values and "NAMA_DESA" in row_values.values:
#                 header_row = i
#                 break
        
#         if header_row is None:
#             raise ValueError("Kolom 'KODE_DESA' dan 'NAMA_DESA' tidak ditemukan.")

#         # Load ulang dengan header yang ditemukan
#         df = pd.read_excel(file, header=header_row, engine="openpyxl")

#         # Cek ulang kolom yang wajib ada
#         if not all(kol in df.columns for kol in ["KODE_DESA", "NAMA_DESA"]):
#             raise ValueError("Kolom wajib tidak ditemukan setelah header diatur.")

#         df.dropna(subset=["KODE_DESA", "NAMA_DESA"], inplace=True)

#         # Proses indikator
#         for col in INDICATORS:
#             df[col] = df[col].astype(str).str.lower().str.strip()
#             df[col] = df[col].apply(lambda x: 1 if "ada" in x or "rutin" in x else 0)

#         df["jumlah_indikator_terpenuhi"] = df[INDICATORS].sum(axis=1)
#         df["label_efektivitas"] = df["jumlah_indikator_terpenuhi"].apply(label_efektivitas)

#         return df

#     except Exception as e:
#         raise RuntimeError(f"Terjadi kesalahan saat memproses file: {e}")

# Coba solusi bikin file headerCheck.py untuk lihat header yang sesuai sehingga INDICATORS bisa sesuai
# def load_and_clean_data(file):
#     try:
#         df = pd.read_excel(file, header=2, engine="openpyxl")

#         if not all(kol in df.columns for kol in ["KODE_DESA", "NAMA_DESA"]):
#             raise ValueError("Kolom 'KODE_DESA' dan 'NAMA_DESA' tidak ditemukan.")

#         df.dropna(subset=["KODE_DESA", "NAMA_DESA"], inplace=True)

#         for col in INDICATORS:
#             df[col] = df[col].astype(str).str.lower().str.strip()
#             df[col] = df[col].apply(lambda x: 1 if "ada" in x or "rutin" in x or "aktif" in x else 0)

#         df["jumlah_indikator_terpenuhi"] = df[INDICATORS].sum(axis=1)
#         df["label_efektivitas"] = df["jumlah_indikator_terpenuhi"].apply(label_efektivitas)

#         return df

#     except Exception as e:
#         raise RuntimeError(f"Terjadi kesalahan saat memproses file: {e}")

# Karena masih terjadi error karena data tabular maka, coba alternatif lain

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

        return df_raw

    except Exception as e:
        raise RuntimeError(f"Terjadi kesalahan saat memproses file: {e}")

