import psycopg2
import csv
import os

database = "kron"
user = "kron_support"
password = "Bau1234."
host = "192.168.1.102"
port = "5432"
directory = "."  # CSV dosyalarının bulunduğu dizin

def import_data(database, user, password, host, port, directory):
    # Veritabanına bağlan
    conn = psycopg2.connect(
        dbname=database,
        user=user,
        password=password,
        host=host,
        port=port
    )
    cursor = conn.cursor()

    # CSV dosyalarını bul ve işle
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)

            # CSV dosyasını aç ve verileri oku
            with open(file_path, 'r') as file:
                csv_data = csv.reader(file)
                next(csv_data)  # Başlık satırını atla

                # INSERT işlemini gerçekleştir
                table_name = filename.split(".")[0]
                table_parts = table_name.split("_")
                schema_name = "_".join(table_parts[:-1])
                table_name = table_parts[-1]
                insert_query = f"""INSERT INTO "{schema_name}"."{table_name}" (id, name) VALUES (%s, %s);"""

                for row in csv_data:
                    values = (row[0], row[1])
                    cursor.execute(insert_query, values)

    # Değişiklikleri kaydet
    conn.commit()

    # Bağlantıyı kapat
    cursor.close()
    conn.close()

# Veriyi içe aktar
import_data(database, user, password, host, port, directory)
