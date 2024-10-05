import csv

# CSV dosyasını oku ve sorulara cevap ver
def process_csv(csv_file_path, default_response_function):
    sorular = []
    with open(csv_file_path, mode='r', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            soru = row["Soru"]
            cevap = default_response_function(soru)
            sorular.append({"Soru": soru, "Cevap": cevap})

    # Sonuçları aynı CSV dosyasına yaz
    with open(csv_file_path, mode='w', newline='', encoding='utf-8-sig') as file:
        fieldnames = ["Soru", "Cevap"]
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)

        csv_writer.writeheader()
        for soru in sorular:
            csv_writer.writerow(soru)

    print(f"Cevaplı sorular {csv_file_path} dosyasına kaydedildi.")
