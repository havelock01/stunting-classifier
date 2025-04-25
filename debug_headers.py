import pandas as pd

def main():
    # Path ke file Excel kamu
    file_path = "raw_data/jumlah-penerima-layanan-pencegahan-stunting-tahun-2023.xlsx"

    try:
        # Baca file Excel dengan dua baris header
        df = pd.read_excel(file_path, header=[0, 2], engine="openpyxl")

        # Gabungkan header multi-level menjadi satu baris
        df.columns = ['_'.join([str(i).strip() for i in col if str(i) != 'nan']).strip() for col in df.columns]

        # Tampilkan semua nama kolom hasil gabungan
        print("\n--- DAFTAR NAMA KOLOM SETELAH GABUNGAN HEADER ---")
        for i, col in enumerate(df.columns):
            print(f"{i+1}. {col}")

        print(f"\nTotal kolom: {len(df.columns)}")

        # Tampilkan 5 baris pertama
        print("\n--- 5 Baris Pertama ---")
        print(df.head())

    except Exception as e:
        print(f"❌ Terjadi kesalahan saat membaca atau memproses file: {e}")

if __name__ == "__main__":
    main()
