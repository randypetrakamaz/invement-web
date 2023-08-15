from flask import Flask, render_template, url_for, redirect, request, session
import requests

app = Flask(__name__)

app.secret_key = 'abcd1234'

@app.route("/", methods=['GET'])
def index():
    if "user" in session:
        try:
            barang = requests.get('https://backend-randy-5zn7xh2gqq-et.a.run.app/data-barang')
        except Exception as e:
            print("ERROR | Get data barang |", e)
        
        # Hitung total barang
        data = barang.json()
        jumlah_barang = len(data)

        # Hitung total stok limit
        total_limit_stok = 0
        for i in range(jumlah_barang):
            if data[i]['stok'] < 6:
                total_limit_stok += 1

        # Hitung total data barang masuk
        try:
            barang_masuk = requests.get('https://backend-randy-5zn7xh2gqq-et.a.run.app/data-barang-masuk')
        except Exception as e:
            print("ERROR | Get data barang masuk |", e)    
        
        data_barang_masuk = barang_masuk.json()
        total_barang_masuk = len(data_barang_masuk)

        # Hitung total data barang keluar
        try:
            barang_keluar = requests.get('https://backend-randy-5zn7xh2gqq-et.a.run.app/data-barang-keluar')
        except Exception as e:
            print("ERROR | Get data barang keluar|", e)
        
        data_barang_keluar = barang_keluar.json()
        total_barang_keluar = len(data_barang_keluar)

        return render_template("index.html", user=session["user"], totalBarang = jumlah_barang, totalLimitStok = total_limit_stok, totalBarangMasuk = total_barang_masuk, totalBarangKeluar = total_barang_keluar)
    
    else:
        return redirect(url_for('login'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    error = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['pass']

        # Ambil data dari API
        try:
            users = requests.get('https://backend-randy-5zn7xh2gqq-et.a.run.app/data-admin')
        except Exception as e:
            print("ERROR | Get admin data |", e)

        for user in users.json():
            if user["username"] == username:
                if password == user['password']:
                    session["user"] = user["nama"]
                    return redirect(url_for('index'))
                else:
                    error = "Login gagal, silahkan coba lagi!"
            else:
                 error = "Login gagal, silahkan coba lagi!"
    return render_template('login.html', error=error)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for('login'))

@app.route("/barang", methods=['GET', 'POST'])
def barang():
    if "user" in session:
        response_data = ""
        if request.method == 'POST':
            aksi = request.form['action']
            user = session['user']
            id = request.form['id']

            if aksi != "hapus" :
                barang = request.form['barang']
                jenis = request.form['jenis']
                beli = request.form['beli']
                jual = request.form['jual']
                stok = int(request.form['stok'])

                # dictionary untuk dikirim ke server
                data = { 
                    'id': id, 
                    'barang': barang, 
                    'jenis': jenis,
                    'beli': beli,
                    'jual': jual,
                    'stok': stok,
                    'user': user
                }
                
                if aksi == "tambah" :
                    # melakukan POST request ke URL dengan  data
                    response = requests.post('https://backend-randy-5zn7xh2gqq-et.a.run.app/tambah-barang', data)
                    response_data = response.text

                elif aksi == "edit" :
                    response = requests.post('https://backend-randy-5zn7xh2gqq-et.a.run.app/edit-barang', data)
                    response_data = response.text

            else:
                # id = request.form['id']
                data = {
                    'id': id,
                    'user': user
                }
                response = requests.post('https://backend-randy-5zn7xh2gqq-et.a.run.app/hapus-barang', data)
                response_data = response.text

            return render_template("barang.html", user=session["user"], status = response_data)
            
        return render_template("barang.html", user=session["user"])
    else:
        return redirect(url_for('login'))



#===================================== Riwayat Aktivitas ===================================
@app.route("/riwayat", methods=['GET', 'POST'])
def riwayat():
    if "user" in session:
        if request.method == 'POST':
            if "user" in session:
                id = request.form['id']
                data = {
                    'id': id
                }
                response = requests.post('https://backend-randy-5zn7xh2gqq-et.a.run.app/hapus-riwayat', data)
                response_data = response.text

            return render_template("riwayat.html", user=session["user"], status = response_data)
        
        return render_template("riwayat.html", user=session["user"])
    else:
        return redirect(url_for('login'))
    
    
#===================================== Barang Masuk ===================================    
@app.route("/barang-masuk", methods=['GET', 'POST'])
def barang_masuk():
    if "user" in session:
        if request.method == 'POST':
            aksi = request.form['action']
            user = session['user']

            if aksi != "hapus" :
                id = request.form['id_barang']
                tanggal = request.form['tanggal']
                jumlah = request.form['jumlah']

                if int(jumlah) < 1 :
                    return render_template("barang_keluar.html", user=session["user"], status = "Jumlah barang tidak boleh nol")

                # dictionary untuk dikirim ke server
                data = { 
                    'id': id, 
                    'tanggal': tanggal,
                    'jumlah': int(jumlah),
                    'user': user
                }
                
                if aksi == "tambah" :
                    # melakukan POST request ke URL tertentu dengan  data
                    response = requests.post('https://backend-randy-5zn7xh2gqq-et.a.run.app/tambah-barang-masuk', data)

                    # Status Memperbarui stok di data barang
                    response_data = response.text
                    
                    if response_data == 'Data barang masuk berhasil ditambahkan':
                        # Ambil data barang dari server
                        barang = requests.get('https://backend-randy-5zn7xh2gqq-et.a.run.app/data-barang')
                        dataBarang = barang.json()
                        
                        dataStok = {
                            'id': id,
                        }

                        for b in dataBarang:
                            if b['id'] == id:
                                dataStok['stok'] = b['stok'] + int(jumlah)
                                break
                        
                        # Kirim data barang yang sudah diperbarui ke server
                        response = requests.post('https://backend-randy-5zn7xh2gqq-et.a.run.app/edit-stok', dataStok)

                elif aksi == "edit" :
                    response = requests.post('https://backend-randy-5zn7xh2gqq-et.a.run.app/edit-barang-masuk', data)
                    response_data = response.text

            else:
                id = request.form['id']
                data = {
                    'id': id,
                    'user': user
                }
                response = requests.post('https://backend-randy-5zn7xh2gqq-et.a.run.app/hapus-barang-masuk', data)
                response_data = response.text

            return render_template("barang_masuk.html", user=session["user"], status = response_data)
        
        return render_template("barang_masuk.html", user=session["user"])
    else:
        return redirect(url_for('login'))


#===================================== Barang Keluar ===================================    
@app.route("/barang-keluar", methods=['GET', 'POST'])
def barang_keluar():
    if "user" in session:
        if request.method == 'POST':
            aksi = request.form['action']
            user = session['user']

            if aksi != "hapus" :
                id = request.form['id_barang']
                tanggal = request.form['tanggal']
                jumlah = request.form['jumlah']

                if int(jumlah) < 1 :
                    return render_template("barang_keluar.html", user=session["user"], status = "Jumlah barang tidak boleh nol")

                # dictionary untuk dikirim ke server
                data = { 
                    'id': id, 
                    'tanggal': tanggal,
                    'jumlah': int(jumlah),
                    'user': user
                }
                
                if aksi == "tambah" :
                    
                    # Ambil data barang dari server
                    barang = requests.get('https://backend-randy-5zn7xh2gqq-et.a.run.app/data-barang')
                    dataBarang = barang.json()
                    
                    dataStok = {
                        'id': id,
                    }

                    for b in dataBarang:
                        if b['id'] == id:
                            dataStok['stok'] = b['stok'] - int(jumlah)
                            if dataStok['stok'] < 0:
                                return render_template("barang_keluar.html", user=session["user"], status = "Jumlah barang melebihi stok")
                            
                            else: 
                                response = requests.post('https://backend-randy-5zn7xh2gqq-et.a.run.app/tambah-barang-keluar', data)
                                response_data = response.text

                            break
                    
                    if response_data == 'Data barang keluar berhasil ditambahkan':
                        # Kirim data barang yang sudah diperbarui ke server
                        response = requests.post('https://backend-randy-5zn7xh2gqq-et.a.run.app/edit-stok', dataStok)

                elif aksi == "edit" :
                    response = requests.post('https://backend-randy-5zn7xh2gqq-et.a.run.app/edit-barang-keluar', data)
                    
            else:
                id = request.form['id']
                data = {
                    'id': id,
                    'user': user
                }
                response = requests.post('https://backend-randy-5zn7xh2gqq-et.a.run.app/hapus-barang-keluar', data)
                response_data = response.text

            return render_template("barang_keluar.html", user=session["user"], status = response_data)

        return render_template("barang_keluar.html", user=session["user"])
    else:
        return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)