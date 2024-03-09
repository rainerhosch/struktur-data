import tkinter as tk
from tkinter import ttk
import json
from jenis_barang import load_jenis_barang as load_jb

def simpan_barang():
    # Membaca data yang sudah ada dalam file JSON
    try:
        with open("BARANG.json", "r") as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = []

    # Menghitung jumlah data yang sudah ada
    existing_count = len(existing_data)

    # Membuat kode barang baru dengan format 'B' + nomor urut
    kode = f"BRG{existing_count + 1:03d}"

    jb = jenis_combobox.get()
    nama = entry_nama.get()
    harga = entry_harga.get()

    # Memeriksa apakah nama dan harga tidak kosong
    if nama.strip() == "" or harga.strip() == "" or jb.strip() == "":
        status_label.config(text="Nama dan harga barang harus diisi")
    else:
        # Melakukan penyimpanan data barang jika nama dan harga tidak kosong
        new_data = {"Kode": kode, "Nama": nama, "Harga": harga, "JenisId":jb}
        existing_data.append(new_data)
        
        with open("BARANG.json", "w") as file:
            json.dump(existing_data, file, indent=4)

        status_label.config(text="Data barang berhasil disimpan")
        tampilkan_data()

def tampilkan_data():
    tree.delete(*tree.get_children())  # Menghapus semua baris yang ada di tabel sebelum menambahkan data baru
    try:
        with open("BARANG.json", "r") as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = []

    try:
        with open("JENIS-BARANG.json", "r") as jb:
            data_jb = json.load(jb)
    except FileNotFoundError:
        data_jb = []
    for idx, data in enumerate(existing_data, start=1):
        kode = data["Kode"]
        nama = data["Nama"]
        harga = data["Harga"]
        for idxx, dataJb in enumerate(data_jb, start=1):
            if(dataJb["Id"] == data["JenisId"]):
                kategori = dataJb["Nama"]
        tree.insert("", tk.END, values=(idx, kode, nama, harga, kategori))

def sort_by_column(tree, col, descending=False):
    if col == "Harga":
        data = [(int(tree.set(child, col)), child) for child in tree.get_children('')]
    else:
        data = [((tree.set(child, col)), child) for child in tree.get_children('')]
    data.sort(reverse=descending)
    status_label.config(text=data)
    for index, (val, child) in enumerate(data):
        tree.move(child, '', index)

    tree.heading(col, command=lambda: sort_by_column(tree, col, not descending))
    
# Membuat jendela utama
root = tk.Tk()
root.title("PROGRAM MANUAL QUERY - TUGAS STRUKTUR DATA")
#Initial Frame
frame = tk.Frame(root)
frame.pack()
# Saving User Info
form_input_frame = tk.LabelFrame(frame, text="Input Barang")
form_input_frame.grid(row=0, column=0, padx=5, pady=5)
# Membuat selectbox untuk jenis barang
label_jenis = tk.Label(form_input_frame, text="Jenis Barang:")
label_jenis.grid(row=0, column=0)
jenis_var = tk.StringVar()
jenis_combobox = ttk.Combobox(form_input_frame, textvariable=jenis_var,  values=[nama for _, nama in load_jb()])
jenis_combobox.grid(row=0, column=1)

# Mendapatkan ID berdasarkan indeks saat combobox dipilih
def get_selected_id(event):
    selected_index = jenis_combobox.current()
    if selected_index != -1:  # Pastikan indeks yang dipilih valid
        selected_id, _ = load_jb()[selected_index]
        jenis_var.set(selected_id)

# Mengaitkan fungsi get_selected_id dengan peristiwa pemilihan combobox
jenis_combobox.bind("<<ComboboxSelected>>", get_selected_id)

# Membuat label dan entry untuk nama barang
label_nama = tk.Label(form_input_frame, text="Nama Barang:")
label_nama.grid(row=1, column=0)
entry_nama = tk.Entry(form_input_frame)
entry_nama.grid(row=1, column=1)

# Membuat label dan entry untuk harga barang
label_harga = tk.Label(form_input_frame, text="Harga Barang:")
label_harga.grid(row=2, column=0)
entry_harga = tk.Entry(form_input_frame)
entry_harga.grid(row=2, column=1)

# Tombol untuk menyimpan data barang
simpan_button = tk.Button(form_input_frame, text="Simpan", command=simpan_barang)
simpan_button.grid(row=0, column=2)

# Label untuk menampilkan status penyimpanan
status_label = tk.Label(form_input_frame, text="")
status_label.grid(row=3, columnspan=3)


frame_table = tk.LabelFrame(frame, text="LIST BARANG")
frame_table.grid(row=1, column=0, padx=5, pady=5)


# Tombol untuk menampilkan data barang
tampilkan_button = tk.Button(frame_table, text="Tampilkan Data", command=tampilkan_data)
tampilkan_button.grid(row=0, column=2)
# Membuat tabel untuk menampilkan data
tree = ttk.Treeview(frame_table, columns=("No","Kode", "Nama", "Harga", "JenisId"), show="headings")
tree.heading("No", text="No")
tree.heading("Kode", text="Kode", command=lambda: sort_by_column(tree, "Kode"))
tree.heading("Nama", text="Nama", command=lambda: sort_by_column(tree, "Nama"))
tree.heading("Harga", text="Harga", command=lambda: sort_by_column(tree, "Harga"))
tree.heading("JenisId", text="Kategori", command=lambda: sort_by_column(tree, "JenisId"))
tree.grid(row=4, columnspan=3,padx=10, pady=10)

# Menengahkan data dalam kolom
for col in tree['columns']:
    tree.heading(col, anchor=tk.CENTER)
    tree.column(col, anchor=tk.CENTER)

# Menampilkan data barang saat pertama kali program dijalankan
tampilkan_data()

# Menjalankan event loop Tkinter
root.mainloop()
