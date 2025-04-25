import pandas as pd

# Ganti path dengan file Excel kamu
file_path = "raw_data/jumlah-penerima-layanan-pencegahan-stunting-tahun-2023.xlsx"

# Baca tanpa header, agar kita bisa eksplorasi semua baris
df = pd.read_excel(file_path, header=None, engine="openpyxl")

# Tampilkan 5 baris awal untuk lihat posisi header sebenarnya
print("5 baris pertama:")
print(df.head())

# Tampilkan jumlah kolom
print(f"\nJumlah kolom: {df.shape[1]}")

# Tampilkan semua kolom dari baris ke-0 dan ke-2
print("\nHeader baris ke-0 (administratif):")
print(df.iloc[0].tolist())

print("\nHeader baris ke-2 (indikator):")
print(df.iloc[2].tolist())
