import requests
import time

# Fungsi untuk mengambil data dari server
def get_data_from_server():
    try:
        # Kirim GET request ke API di sisi server
        response = requests.get('http://127.0.0.1:5000/api/data')

        # Cek jika respons berhasil (kode status 200)
        if response.status_code == 200:
            data = response.json()  # Ambil data JSON dari respons
            print("Data yang diterima:", data)
        else:
            print("Gagal mendapatkan data:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Koneksi terputus:", e)

# Looping untuk mengambil data sebanyak 20 kali
for i in range(50):
    print(f"Permintaan ke-{i+1}:")
    get_data_from_server()  # Panggil fungsi untuk mengambil data dari server
    print("Menunggu 2 detik sebelum permintaan berikutnya...")
    time.sleep(2)  # Istirahat selama 2 detik sebelum permintaan berikutnya
