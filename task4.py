from google.cloud import vision, translate_v2 as translate, bigquery
import os

# Set Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/service-account.json"

# Inisialisasi klien untuk Vision API, Translation API, dan BigQuery
vision_client = vision.ImageAnnotatorClient()
translate_client = translate.Client()
bigquery_client = bigquery.Client()

# Fungsi untuk mendeteksi teks dengan Vision API
def detect_text(image_path):
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = vision_client.text_detection(image=image)
    
    texts = response.text_annotations
    if texts:
        return texts[0].description.strip()  # Ambil teks pertama (hasil utama)
    return None

# Fungsi untuk menerjemahkan teks ke bahasa Prancis
def translate_text(text, target_language="fr"):
    response = translate_client.translate(text, target_language=target_language)
    return response["translatedText"]

# Fungsi untuk menyimpan hasil ke BigQuery
def save_to_bigquery(original_text, translated_text):
    dataset_id = "your_dataset_id"
    table_id = "your_table_id"
    table_ref = bigquery_client.dataset(dataset_id).table(table_id)

    rows_to_insert = [{
        "original_text": original_text,
        "translated_text": translated_text
    }]

    errors = bigquery_client.insert_rows_json(table_ref, rows_to_insert)
    if errors:
        print("Error inserting data into BigQuery:", errors)
    else:
        print("Data successfully inserted into BigQuery.")

# Path ke gambar input
image_path = "path/to/your/image.jpg"

# Jalankan proses ekstraksi dan terjemahan
extracted_text = detect_text(image_path)
if extracted_text:
    print("Extracted Text:", extracted_text)
    
    translated_text = translate_text(extracted_text)
    print("Translated Text:", translated_text)

    # Simpan hasil ke BigQuery
    save_to_bigquery(extracted_text, translated_text)
else:
    print("No text detected in the image.")
