import os

def main():
    # Folder path 
    # Sesuaikan path ini dengan output hasil komparasi terakhir (berdasarkan script sebelumnya output_test_2)
    base_dir = "data_test/detection_display"
    
    asli_dir = os.path.join(base_dir, "asli")
    visual_dir = os.path.join(base_dir, "visual_detection")

    if not os.path.exists(asli_dir):
        print(f"Error: Folder ASLI tidak ditemukan! ({asli_dir})")
        return
    if not os.path.exists(visual_dir):
        print(f"Error: Folder VISUAL tidak ditemukan! ({visual_dir})")
        return

    print("=========================================================")
    print("SINKRONISASI IMAGE FOLDER")
    print("=========================================================")
    
    # Membaca daftar file di kedua folder
    asli_files = set(f for f in os.listdir(asli_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png')))
    visual_files = set(f for f in os.listdir(visual_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png')))
    
    print(f"Total gambar di folder ASLI saat ini   : {len(asli_files)}")
    print(f"Total gambar di folder VISUAL saat ini : {len(visual_files)}\n")
    
    # 1. Menentukan foto di 'asli' yang sudah dihapus manual oleh user di 'visual'
    files_to_delete_in_asli = asli_files - visual_files
    
    # 2. Menentukan foto di 'visual' yang mungkin tidak sengaja sisa sendirian tanpa 'asli'
    files_to_delete_in_visual = visual_files - asli_files
    
    deleted_asli_count = 0
    deleted_visual_count = 0
    
    # Proses Penghapusan di folder ASLI
    if files_to_delete_in_asli:
        print(f"🔍 Ditemukan {len(files_to_delete_in_asli)} gambar di folder ASLI yang sudah Anda hapus di VISUAL. Sedang disinkronisasi (dihapus)...")
        for f in files_to_delete_in_asli:
            file_path = os.path.join(asli_dir, f)
            if os.path.isfile(file_path):
                os.remove(file_path)
                deleted_asli_count += 1
                
    # Proses Penghapusan di folder VISUAL (berjaga-jaga jika terbalik hapus)
    if files_to_delete_in_visual:
        print(f"🔍 Ditemukan {len(files_to_delete_in_visual)} gambar di folder VISUAL yang tidak ada pasangannya di ASLI. Sedang disinkronisasi (dihapus)...")
        for f in files_to_delete_in_visual:
            file_path = os.path.join(visual_dir, f)
            if os.path.isfile(file_path):
                os.remove(file_path)
                deleted_visual_count += 1

    # Finalisasi dan Cetak Rekap
    if deleted_asli_count == 0 and deleted_visual_count == 0:
        print("✅ Status: KEDUA FOLDER SUDAH SINKRON (SAMA PERSIS). Tidak ada file yang perlu dihapus.")
    else:
        print(f"\n✅ Proses Sinkronisasi Selesai!")
        print(f"   [-] Berhasil menghapus {deleted_asli_count} file di folder ASLI.")
        if deleted_visual_count > 0:
            print(f"   [-] Berhasil menghapus {deleted_visual_count} file di folder VISUAL.")
            
        print(f"   [=] Sisa sekarang: {len(os.listdir(visual_dir))} pasang gambar yang identik ditiap folder.")

if __name__ == "__main__":
    main()
