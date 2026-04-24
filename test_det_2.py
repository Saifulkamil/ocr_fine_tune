from paddleocr import TextDetection

model = TextDetection(model_name="PP-OCRv5_mobile_det")

# Memprediksi semua gambar di dalam folder data_test
output = model.predict("data_test/", batch_size=1)

for res in output:
    res.print()
    # Menyimpan hasil visualisasi (gambar) ke output_test/
    res.save_to_img(save_path="./output_test_2/")
    # Menyimpan hasil prediksi dalam bentuk JSON
    # Kita berikan directory path agar disimpan terpisah untuk tiap file
    res.save_to_json(save_path="./output_test_2/")