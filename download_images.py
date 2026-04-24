import os
import urllib.request
import re
from concurrent.futures import ThreadPoolExecutor

def get_links(url):
    """Fungsi untuk mengambil semua link dari halaman directory listing"""
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            html = response.read().decode('utf-8', errors='ignore')
            # Ambil semua text di dalam href="..." atau href='...'
            links = re.findall(r'href=["\']?([^"\'>]+)["\']?', html, re.IGNORECASE)
            return links
    except Exception as e:
        print(f"Error membaca {url}: {e}")
        return []

def download_file(url, filepath):
    """Fungsi untuk mendownload satu file"""
    try:
        # Hanya download jika file belum ada
        if not os.path.exists(filepath):
            urllib.request.urlretrieve(url, filepath)
            print(f"✅ Downloaded: {os.path.basename(filepath)}")
    except Exception as e:
        print(f"❌ Gagal download {url}: {e}")

def main():
    base_url = "http://192.168.0.194/uploads/image-penerimaan-produk-pekerja"
    output_dir = "downloaded_images_all"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Membuka direktori utama: {base_url}/ ...\n")
    directories = get_links(f"{base_url}/")
    
    # Filter folder yang menggunakan format tanggal, misalnya 2026-04-21
    date_dirs = []
    
    target_date = "2026-03-18"
    
    for link in directories:
        # Cari pola YYYY-MM-DD di dalam link (misal: /uploads/.../2026-03-15/ atau 2026-03-15)
        match = re.search(r'(\d{4}-\d{2}-\d{2})', link)
        if match:
            date_str = match.group(1)
            # Filter hanya tanggal target yang dipilih
            if target_date is not None and date_str != target_date:
                continue
            if date_str not in date_dirs:
                date_dirs.append(date_str)
    
    print(f"Ditemukan {len(date_dirs)} folder (berdasarkan tanggal).")

    # Loop setiap folder tanggal
    for d in sorted(date_dirs):
        dir_url = f"{base_url}/{d}/"
        print(f"\n=====================================")
        print(f"Mengecek folder: {d}")
        print(f"=====================================")
        
        # Buat folder lokal sesuai nama tanggalnya
        local_dir = os.path.join(output_dir, d)
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)
            
        # Ambil semua file di dalam folder tersebut
        files = get_links(dir_url)
        # Filter yang murni file gambar (ekstensi .jpg, .jpeg, .png)
        # Menghapus parent directory seperti '/' atau '..'
        image_files = []
        for f in files:
            img = f.split('/')[-1] # ambil nama file nya saja
            if img.lower().endswith(('.jpg', '.jpeg', '.png')):
                if img not in image_files:
                    image_files.append(img)
        
        print(f"Ditemukan {len(image_files)} gambar di folder {d}. Mulai mengunduh...")
        
        # Menggunakan ThreadPoolExecutor untuk download banyak file secara paralel (lebih cepat)
        concurrency = 20
        with ThreadPoolExecutor(max_workers=concurrency) as executor:
            for img in image_files:
                file_url = f"{dir_url}{img}"
                filepath = os.path.join(local_dir, img)
                executor.submit(download_file, file_url, filepath)

    print(f"\n🎉 Selesai! Semua gambar telah berhasil didownload ke folder: {os.path.abspath(output_dir)}")

if __name__ == "__main__":
    main()
