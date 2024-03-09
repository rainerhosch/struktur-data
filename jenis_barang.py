import json

def load_jenis_barang():
    # Membaca data jenis barang dari file JSON
    with open("JENIS-BARANG.json", "r") as file:
        data = json.load(file)
    return [(item["Id"], item["Nama"]) for item in data]