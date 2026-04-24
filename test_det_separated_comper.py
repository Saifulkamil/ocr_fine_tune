import os
import shutil
from paddleocr import TextDetection

def main():
    modelfineTune = TextDetection(model_dir="./result_model", model_name="PP-OCRv5_mobile_det")
    modelasli = TextDetection(model_name="PP-OCRv5_mobile_det")
    
    # Konfigurasi Path Input
    input_dir = "data_test/detection_display/asli"
    
    # Setup Path Output untuk Komparasi
    out_dir = "./output_test_2/"
    dir_both = os.path.join(out_dir, "detection_display")
    
    # Membuat folder utama dan subfolder untuk visualisasinya
    for d in [dir_both]:
        os.makedirs(d, exist_ok=True)
        os.makedirs(os.path.join(d, "asli"), exist_ok=True)  # Folder spesifik untuk gambar polos
        os.makedirs(os.path.join(d, "visual_detection"), exist_ok=True) # Folder untuk gambar bergaris + JSON (asli)
        
    print(f"Memulai prediksi pada folder: {input_dir}")
    print("Mencari daftar gambar...")
    
    # Ambil semua gambar di dalam input_dir beserta subfoldernya
    image_paths = []
    for root, dirs, files in os.walk(input_dir):
        for f in files:
            if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_paths.append(os.path.join(root, f))
                
    print(f"Ditemukan {len(image_paths)} gambar. Proses ini akan menjalankan prediksi dari kedua model secara bersamaan...")
    
    counts = {"ft_only": 0, "ori_only": 0, "both": 0, "miss": 0, "error": 0}
    
    for img_path in image_paths:
        img_name = os.path.basename(img_path)
        
        try:
            # Prediksi per gambar untuk menghindari file corrupt menghentikan seluruh proses
            out_ft = list(modelfineTune.predict(img_path, batch_size=1))
            out_ori = list(modelasli.predict(img_path, batch_size=1))
            
            res_ft = out_ft[0]
            res_ori = out_ori[0]
            
            # Menghitung panjang kotak deteksi yang didapat
            dt_ft = res_ft.get("dt_scores", [])
            dt_ori = res_ori.get("dt_scores", [])
            
            is_ft_detect = len(dt_ft) > 0
            is_ori_detect = len(dt_ori) > 0
            
            target_dir = ""
            
            # Mengevaluasi 4 kondisi komparasi
            if is_ft_detect and is_ori_detect:
                counts["both"] += 1
                target_dir = dir_both
                print(f"[{img_name}] 🔵 KEDUANYA (FT: {len(dt_ft)} vs Asli: {len(dt_ori)})")
            else:
                counts["miss"] += 1
                 
            # HANYA proses penyimpanan/kopi file jika kondisinya KEDUANYA DAPAT
            if target_dir == dir_both:
                # 1. Copy gambar aslinya (polos) ke subfolder 'asli' untuk ditraining
                shutil.copy(img_path, os.path.join(target_dir, "asli"))
                
                # 2. Simpan gambar visualisasi (kotak) dari model FINETUNE
                visual_dir = os.path.join(target_dir, "visual_detection")
                res_ft.save_to_img(save_path=visual_dir)
                
                # Menghilangkan akhiran "_res" (atau sejenisnya) yang otomatis ditambahkan oleh PaddleX
                name_without_ext, ext = os.path.splitext(img_name)
                
                # Cek file yang barusan dibuat oleh Paddle (mengandung 'res' di belakang nama)
                # Umumnya PaddleX menambahkan awalan atau akhiran "_res" ke nama aslinya
                saved_res_path = os.path.join(visual_dir, f"{name_without_ext}_res{ext}")
                final_path = os.path.join(visual_dir, img_name)
                
                if os.path.exists(saved_res_path):
                    if os.path.exists(final_path):
                        os.remove(final_path)
                    os.rename(saved_res_path, final_path)
                
        except Exception as e:
            counts["error"] += 1
            print(f"❌ ERROR membaca gambar {img_name}: {e}")
            continue

    print("\n=======================================================")
    print("REKAP HASIL KOMPARASI DETEKSI:")
    print("=======================================================")
    print(f"KEDUA Model Keduanya DAPAT       : {counts['both']} gambar")
    print(f"File Gagal Dibaca (Corrupt)      : {counts['error']} gambar")
    print("=======================================================")
    print(f"Semua hasil perbandingan ini dapat dilihat di folder:")
    print(os.path.abspath(out_dir))

if __name__ == "__main__":
    main()
