import psycopg2
import json

instance_name = "sat-kapita-selekta-b:asia-southeast2:training-kapita-selekta"
port = 5432
db = "postgres"
user = "postgres"
password = "FwF6qfEA5AzlztzG"

# param = f"host='localhost' port={port} dbname='{db}' user='{user}' password='{password}'"
param = f"host='/cloudsql/{instance_name}' port={port} dbname='{db}' user='{user}' password='{password}'"


# ================================================ Barang ===============================================
def selectBarang(query=""):
    try:
        conn = psycopg2.connect(param)
        
        curs = conn.cursor()
        curs.execute(query)
        data = curs.fetchall()


        dataBarang = []
        for row in data:
            dataBarang.append({
                "id": row[0],
                "barang": row[1],
                "jenis": row[2],
                "beli": row[3],
                "jual": row[4],
                "stok": row[5]
            })

        # ubah menjadi format string JSON
        barang = json.dumps(dataBarang)

        curs.close()
        del(conn)
        return barang
    
    except Exception as e:
        print(e)
        return False, str(e)
    

def insert(query=""):
    try:
        conn = psycopg2.connect(param)

        curs = conn.cursor()
        curs.execute(query)
        conn.commit()

        curs.close()
        del(conn)
        return True
    
    except Exception as e:
        print(e)
        return False, str(e)
    
def update(query=""):
    try:
        conn = psycopg2.connect(param)

        curs = conn.cursor()
        curs.execute(query)
        conn.commit()

        curs.close()
        del(conn)
        return True
    
    except Exception as e:
        print(e)
        return False, str(e)
    
def delete(query=""):
    try:
        conn = psycopg2.connect(param)

        curs = conn.cursor()
        curs.execute(query)
        conn.commit()

        curs.close()
        del(conn)
        return True
    
    except Exception as e:
        print(e)
        return False, str(e)


# ================================================ Riwayat Aktivitas ===============================================
def selectRiwayat(query=""):
    try:
        conn = psycopg2.connect(param)
        
        curs = conn.cursor()
        curs.execute(query)
        data = curs.fetchall()

        dataRiwayat = []
        for row in data:
            dataRiwayat.append({
                "id": row[0],
                "tanggal": row[1].strftime("%Y-%m-%d %H:%M:%S"),
                "admin": row[2],
                "aktivitas": row[3],
            })

        riwayat = json.dumps(dataRiwayat)

        curs.close()
        del(conn)
        return riwayat
    
    except Exception as e:
        print(e)
        return False, str(e)


# ================================================ Barang Masuk dan Keluar ===============================================
def selectBarangMasukKeluar(query=""):
    try:
        conn = psycopg2.connect(param)
        
        curs = conn.cursor()
        curs.execute(query)
        data = curs.fetchall()

        barangMasukKeluar = []
        for row in data:
            barangMasukKeluar.append({
                "id": row[0],
                "id_barang": row[1],
                "barang": row[2],
                "tanggal": row[3].strftime('%Y-%m-%d'),
                "stok": row[4],
            })

        dataMasukKeluar = json.dumps(barangMasukKeluar)

        curs.close()
        del(conn)
        return dataMasukKeluar
    
    except Exception as e:
        print(e)
        return False, str(e)



# ================================================ Admin ===============================================
def selectAdmin(query=""):
    try:
        conn = psycopg2.connect(param)
        
        curs = conn.cursor()
        curs.execute(query)
        data = curs.fetchall()

        dataAdmin = []
        for row in data:
            dataAdmin.append({
                "nama": row[1],
                "username": row[2],
                "password": row[3]
            })

        # ubah menjadi format string JSON
        admin = json.dumps(dataAdmin)

        curs.close()
        del(conn)
        return admin
    
    except Exception as e:
        print(e)
        return False, str(e)