from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)
file_csv = "data_paket.csv"

# Buat CSV jika belum ada
if not os.path.exists(file_csv):
    with open(file_csv, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Nama Paket", "Tracking Number", "Status"])

def baca_data():
    data = []
    with open(file_csv, mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

def simpan_data(data):
    with open(file_csv, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Nama Paket", "Tracking Number", "Status"])
        for p in data:
            writer.writerow([p["Nama Paket"], p["Tracking Number"], p["Status"]])

@app.route("/")
def index():
    data = baca_data()
    stats = {"Inbound":0, "Outbound":0, "Delivered":0}
    for p in data:
        if p["Status"] in stats:
            stats[p["Status"]] += 1
    return render_template("index.html", data=data, stats=stats)

@app.route("/filter/<status>")
def filter_status(status):
    data = baca_data()
    if status != "All":
        data = [p for p in data if p["Status"]==status]
    stats = {"Inbound":0, "Outbound":0, "Delivered":0}
    for p in baca_data():
        if p["Status"] in stats:
            stats[p["Status"]] += 1
    return render_template("index.html", data=data, stats=stats)

@app.route("/tambah", methods=["GET", "POST"])
def tambah():
    if request.method == "POST":
        data = baca_data()
        data.append({
            "Nama Paket": request.form["nama"],
            "Tracking Number": request.form["tracking"],
            "Status": request.form["status"]
        })
        simpan_data(data)
        return redirect("/")
    return render_template("tambah.html")

@app.route("/edit/<int:index>", methods=["GET", "POST"])
def edit(index):
    data = baca_data()
    paket = data[index]
    if request.method == "POST":
        paket["Nama Paket"] = request.form["nama"]
        paket["Tracking Number"] = request.form["tracking"]
        paket["Status"] = request.form["status"]
        simpan_data(data)
        return redirect("/")
    return render_template("edit.html", paket=paket, index=index)

@app.route("/hapus/<int:index>")
def hapus(index):
    data = baca_data()
    data.pop(index)
    simpan_data(data)
    return redirect("/")

if __name__ == "__main__":
    # Gunakan host 0.0.0.0 dan port dari environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
