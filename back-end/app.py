import falcon
import connectdb
import datetime
import pytz


class getBarang:
    def on_get(self, req, resp):
        query = 'SELECT * FROM public."_672020163_gudang_barang"'
        data = connectdb.selectBarang(query)

        resp.text = str(data)
        resp.status = falcon.HTTP_200

class addBarang:
    def on_post(self, req, resp):
        # Ambil data dari body request
        data = req.media

        # set timezone ke Indonesia
        wib = pytz.timezone('Asia/Jakarta')

        # ambil waktu saat ini
        dateNow = datetime.datetime.now(wib)        
        dataRiwayat = { 
            'tanggal': dateNow.strftime("%Y-%m-%d %H:%M:%S"),
            'user': data['user'],
            'tambah': f'Menambah barang dengan ID {str(data["id"])}'
        }

        # Buat query untuk insert data barang ke database
        query = 'INSERT INTO public."_672020163_gudang_barang" ("id_barang", "nama_barang", "jenis", "harga_beli", "harga_jual", "stok") VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', {});'.format(
            data["id"], data["barang"], data["jenis"], data["beli"], data["jual"], data["stok"]
        )

        # Jalankan query untuk insert data ke database
        add_berhasil = connectdb.insert(query)

        if add_berhasil == True:

            # jika berhasil insert data barang, lakukan insert ke dalam tabel gudang_aktivitas
            riwayat = 'INSERT INTO public."_672020163_gudang_aktivitas" (tanggal, admin, aktivitas) VALUES(\'{}\', \'{}\', \'{}\');'.format(dataRiwayat['tanggal'], dataRiwayat['user'], dataRiwayat['tambah'])

            add_riwayat_berhasil = connectdb.insert(riwayat)

            if add_riwayat_berhasil == True:
                resp.text = 'Data riwayat berhasil ditambahkan'
                resp.status = falcon.HTTP_200
            else:
                resp.text = 'Gagal melakukan tambah riwayat'
                resp.status = falcon.HTTP_500

            # respon data barang berhasil ditambahkan
            resp.text = 'Data barang berhasil ditambahkan'
            resp.status = falcon.HTTP_200

        else:
            resp.text = 'Gagal melakukan tambah data barang'
            resp.status = falcon.HTTP_500

class editBarang:
    def on_post(self, req, resp):
       
        data = req.media

        # set timezone ke Indonesia
        wib = pytz.timezone('Asia/Jakarta')

        # ambil waktu saat ini
        dateNow = datetime.datetime.now(wib)        
        dataRiwayat = { 
            'tanggal': dateNow.strftime("%Y-%m-%d %H:%M:%S"),
            'user': data['user'],
            'edit': f'Mengubah detail barang dengan ID {str(data["id"])}' 
        }

        query = 'UPDATE public."_672020163_gudang_barang" SET nama_barang=\'{}\', "jenis"=\'{}\', harga_beli=\'{}\', harga_jual=\'{}\', stok={} WHERE id_barang=\'{}\''.format(
            data["barang"], data["jenis"], data["beli"], data["jual"], data["stok"], data["id"]
        )
        
        # jalankan query update data ke dalam database
        edit_berhasil = connectdb.update(query)

        if edit_berhasil == True:
            
            # jika berhasil, lakukan insert ke dalam tabel gudang_aktivitas
            riwayat = 'INSERT INTO public."_672020163_gudang_aktivitas" (tanggal, admin, aktivitas) VALUES(\'{}\', \'{}\', \'{}\');'.format(dataRiwayat['tanggal'], dataRiwayat['user'], dataRiwayat['edit'])

            add_riwayat_berhasil = connectdb.insert(riwayat)

            if add_riwayat_berhasil == True:
                resp.text = 'Data riwayat berhasil ditambahkan'
                resp.status = falcon.HTTP_200
            else:
                resp.text = 'Gagal melakukan tambah riwayat'
                resp.status = falcon.HTTP_500

            # respon data barang berhasil ditambahkan
            resp.text = 'Data barang berhasil diubah'
            resp.status = falcon.HTTP_200

        else:
            resp.text = 'Gagal melakukan edit data barang'
            resp.status = falcon.HTTP_500

class deleteBarang:
    def on_post(self, req, resp):

        data = req.media
        
        # set timezone ke Indonesia
        wib = pytz.timezone('Asia/Jakarta')

        # ambil waktu saat ini
        dateNow = datetime.datetime.now(wib)        
        dataRiwayat = { 
            'tanggal': dateNow.strftime("%Y-%m-%d %H:%M:%S"),
            'user': data['user'],
            'hapus': f'Menghapus barang dengan ID {str(data["id"])}'
        }

        query = 'DELETE FROM public."_672020163_gudang_barang" WHERE id_barang=\'{}\''.format(data["id"])

        # jalankan query delete barang
        delete_berhasil = connectdb.delete(query)

        if delete_berhasil == True:

            # jika berhasil, lakukan insert ke dalam tabel gudang_aktivitas
            riwayat = 'INSERT INTO public."_672020163_gudang_aktivitas" (tanggal, admin, aktivitas) VALUES(\'{}\', \'{}\', \'{}\');'.format(dataRiwayat['tanggal'], dataRiwayat['user'], dataRiwayat['hapus'])

            # jalankan query insert riwayat ke database
            add_riwayat_berhasil = connectdb.insert(riwayat)

            if add_riwayat_berhasil == True:
                resp.text = 'Data riwayat berhasil ditambahkan'
                resp.status = falcon.HTTP_200
            else:
                resp.text = 'Gagal melakukan tambah riwayat'
                resp.status = falcon.HTTP_500

            resp.text = 'Data barang berhasil dihapus'
            resp.status = falcon.HTTP_200

        else:
            resp.text = 'Gagal melakukan hapus data barang'
            resp.status = falcon.HTTP_500


# ========================================== Barang masuk ==============================================
class getRiwayat:
    def on_get(self, req, resp):
        query = 'SELECT * FROM public."_672020163_gudang_aktivitas"'
        data = connectdb.selectRiwayat(query)

        resp.text = str(data)
        resp.status = falcon.HTTP_200

class deleteRiwayat:
    def on_post(self, req, resp):
        
        data = req.media

        query = 'DELETE FROM public."_672020163_gudang_aktivitas" WHERE id={};'.format(data['id'])

        # Jalankan query untuk insert data riwayat ke database
        delete_riwayat_berhasil = connectdb.delete(query)

        if delete_riwayat_berhasil == True:
            resp.text = "Data riwayat berhasil dihapus"
            resp.status = falcon.HTTP_200
        else:
            resp.text = "Gagal melakukan hapus data riwayat"
            resp.status = falcon.HTTP_500


# ========================================== Barang Masuk ==============================================
class getBarangMasuk:
    def on_get(self, req, resp):
        
        # query join table barang dan tabel barang masuk untuk ambil nama barang yang akan ditampilkan
        query = 'SELECT a.id_masuk, a.id_barang, b.nama_barang, a.tanggal_masuk, a.jumlah \
                 FROM public.\"_672020163_gudang_barang_masuk\" AS a \
                 JOIN public.\"_672020163_gudang_barang\" AS b \
                 ON a.id_barang = b.id_barang'
        
        data = connectdb.selectBarangMasukKeluar(query)

        resp.text = str(data)
        resp.status = falcon.HTTP_200

class addBarangMasuk:
    def on_post(self, req, resp):
        
        data = req.media

        # set timezone ke Indonesia
        wib = pytz.timezone('Asia/Jakarta')

        # ambil waktu saat ini
        dateNow = datetime.datetime.now(wib)                
        dataRiwayat = { 
            'tanggal': dateNow.strftime("%Y-%m-%d %H:%M:%S"),
            'user': data['user'],
            'tambah': f'Menambah barang masuk dengan ID {str(data["id"])}'
        }

        # Buat query untuk insert data barang ke database
        query = 'INSERT INTO public."_672020163_gudang_barang_masuk" ("id_barang", "tanggal_masuk", "jumlah") VALUES (\'{}\', \'{}\', {});'.format(
            data["id"], data["tanggal"], data["jumlah"]
        )

        # Jalankan query untuk insert data ke database
        add_berhasil = connectdb.insert(query)

        if add_berhasil == True:
            # jika berhasil, lakukan insert ke dalam tabel gudang_aktivitas
            riwayat = 'INSERT INTO public."_672020163_gudang_aktivitas" (tanggal, admin, aktivitas) VALUES(\'{}\', \'{}\', \'{}\');'.format(dataRiwayat['tanggal'], dataRiwayat['user'], dataRiwayat['tambah'])

            add_riwayat_berhasil = connectdb.insert(riwayat)

            if add_riwayat_berhasil == True:
                resp.text = 'Data riwayat berhasil ditambahkan'
                resp.status = falcon.HTTP_200
            else:
                resp.text = 'Gagal melakukan tambah riwayat'
                resp.status = falcon.HTTP_500
            
            resp.text = 'Data barang masuk berhasil ditambahkan'
            resp.status = falcon.HTTP_200

        else:
            resp.text = 'Gagal melakukan tambah data barang masuk'
            resp.status = falcon.HTTP_500

class deleteBarangMasuk:
    def on_post(self, req, resp):

        data = req.media
        
        # set timezone ke Indonesia
        wib = pytz.timezone('Asia/Jakarta')

        # ambil waktu saat ini
        dateNow = datetime.datetime.now(wib)        
        dataRiwayat = { 
            'tanggal': dateNow.strftime("%Y-%m-%d %H:%M:%S"),
            'user': data['user'],
            'hapus': f'Menghapus barang masuk dengan ID {str(data["id"])}'
        }

        query = 'DELETE FROM public."_672020163_gudang_barang_masuk"WHERE id_masuk={}'.format(data["id"])

        # jalankan query delete barang
        delete_berhasil = connectdb.delete(query)

        if delete_berhasil == True:

            # jika berhasil, lakukan insert ke dalam tabel gudang_aktivitas
            riwayat = 'INSERT INTO public."_672020163_gudang_aktivitas" (tanggal, admin, aktivitas) VALUES(\'{}\', \'{}\', \'{}\');'.format(dataRiwayat['tanggal'], dataRiwayat['user'], dataRiwayat['hapus'])

            # jalankan query insert riwayat ke database
            add_riwayat_berhasil = connectdb.insert(riwayat)

            if add_riwayat_berhasil == True:
                resp.text = 'Data riwayat berhasil ditambahkan'
                resp.status = falcon.HTTP_200
            else:
                resp.text = 'Gagal melakukan tambah riwayat'
                resp.status = falcon.HTTP_500

            resp.text = 'Data barang masuk berhasil dihapus'
            resp.status = falcon.HTTP_200

        else:
            resp.text = 'Gagal melakukan hapus data barang'
            resp.status = falcon.HTTP_500


# ========================================== Barang Keluar ==============================================
class getBarangKeluar:
    def on_get(self, req, resp):
        
        # query join table barang dan tabel barang keluar untuk ambil nama barang yang akan ditampilkan
        query = 'SELECT a.id_keluar, a.id_barang, b.nama_barang, a.tanggal_keluar, a.jumlah \
                 FROM public.\"_672020163_gudang_barang_keluar\" AS a \
                 JOIN public.\"_672020163_gudang_barang\" AS b \
                 ON a.id_barang = b.id_barang'
        
        data = connectdb.selectBarangMasukKeluar(query)

        resp.text = str(data)
        resp.status = falcon.HTTP_200

class addBarangKeluar:
    def on_post(self, req, resp):
        
        data = req.media

        # set timezone ke Indonesia
        wib = pytz.timezone('Asia/Jakarta')

        # ambil waktu saat ini
        dateNow = datetime.datetime.now(wib)           
        dataRiwayat = { 
            'tanggal': dateNow.strftime("%Y-%m-%d %H:%M:%S"),
            'user': data['user'],
            'tambah': f'Menambah barang keluar dengan ID {str(data["id"])}'
        }

        # Buat query untuk insert data barang ke database
        query = 'INSERT INTO public."_672020163_gudang_barang_keluar" ("id_barang", "tanggal_keluar", "jumlah") VALUES (\'{}\', \'{}\', {});'.format(
            data["id"], data["tanggal"], data["jumlah"]
        )

        # Jalankan query untuk insert data ke database
        add_berhasil = connectdb.insert(query)

        if add_berhasil == True:
            # jika berhasil, lakukan insert ke dalam tabel gudang_aktivitas
            riwayat = 'INSERT INTO public."_672020163_gudang_aktivitas" (tanggal, admin, aktivitas) VALUES(\'{}\', \'{}\', \'{}\');'.format(dataRiwayat['tanggal'], dataRiwayat['user'], dataRiwayat['tambah'])

            add_riwayat_berhasil = connectdb.insert(riwayat)

            if add_riwayat_berhasil == True:
                resp.text = 'Data riwayat berhasil ditambahkan'
                resp.status = falcon.HTTP_200
            else:
                resp.text = 'Gagal melakukan tambah riwayat'
                resp.status = falcon.HTTP_500
            
            resp.text = 'Data barang keluar berhasil ditambahkan'
            resp.status = falcon.HTTP_200

        else:
            resp.text = 'Gagal melakukan tambah data barang keluar'
            resp.status = falcon.HTTP_500

class deleteBarangKeluar:
    def on_post(self, req, resp):

        data = req.media
        
        # set timezone ke Indonesia
        wib = pytz.timezone('Asia/Jakarta')

        # ambil waktu saat ini
        dateNow = datetime.datetime.now(wib)        
        dataRiwayat = { 
            'tanggal': dateNow.strftime("%Y-%m-%d %H:%M:%S"),
            'user': data['user'],
            'hapus': f'Menghapus barang keluar dengan ID {str(data["id"])}'
        }

        query = 'DELETE FROM public."_672020163_gudang_barang_keluar"WHERE id_keluar={}'.format(data["id"])

        # jalankan query delete barang
        delete_berhasil = connectdb.delete(query)

        if delete_berhasil == True:

            # jika berhasil, lakukan insert ke dalam tabel gudang_aktivitas
            riwayat = 'INSERT INTO public."_672020163_gudang_aktivitas" (tanggal, admin, aktivitas) VALUES(\'{}\', \'{}\', \'{}\');'.format(dataRiwayat['tanggal'], dataRiwayat['user'], dataRiwayat['hapus'])

            # jalankan query insert riwayat ke database
            add_riwayat_berhasil = connectdb.insert(riwayat)

            if add_riwayat_berhasil == True:
                resp.text = 'Data riwayat berhasil ditambahkan'
                resp.status = falcon.HTTP_200
            else:
                resp.text = 'Gagal melakukan tambah riwayat'
                resp.status = falcon.HTTP_500

            resp.text = 'Data barang keluar berhasil dihapus'
            resp.status = falcon.HTTP_200

        else:
            resp.text = 'Gagal melakukan hapus data keluar'
            resp.status = falcon.HTTP_500

class updateStok:
    def on_post(self, req, resp):
        data = req.media

        query = 'UPDATE public."_672020163_gudang_barang" SET stok={} WHERE id_barang=\'{}\';'.format(data['stok'], data['id'])

        # jalankan query ubah stok
        edit_berhasil = connectdb.update(query)

        if edit_berhasil == True:
            resp.text = 'Data stok barang berhasil diubah'
            resp.status = falcon.HTTP_200                
        else:
            resp.text = 'Gagal melakukan ubah stok barang'
            resp.status = falcon.HTTP_500
        


class getAdmin:
    def on_get(self, req, resp):
        query = 'SELECT * FROM public."_672020163_gudang_admin"'
        data = connectdb.selectAdmin(query)

        resp.text = str(data)
        resp.status = falcon.HTTP_200



app = falcon.App(cors_enable=True)

# route
app.add_route("/data-barang", getBarang())
app.add_route("/tambah-barang", addBarang())
app.add_route("/edit-barang", editBarang())
app.add_route("/hapus-barang", deleteBarang())

app.add_route("/data-riwayat", getRiwayat())
app.add_route("/hapus-riwayat", deleteRiwayat())

app.add_route("/data-barang-masuk", getBarangMasuk())
app.add_route("/tambah-barang-masuk", addBarangMasuk())
# app.add_route("/edit-barang-masuk", editBarangMasuk())
app.add_route("/hapus-barang-masuk", deleteBarangMasuk())

app.add_route("/data-barang-keluar", getBarangKeluar())
app.add_route("/tambah-barang-keluar", addBarangKeluar())
# app.add_route("/edit-barang-masuk", editBarangMasuk())
app.add_route("/hapus-barang-keluar", deleteBarangKeluar())

app.add_route("/edit-stok", updateStok())

app.add_route("/data-admin", getAdmin())