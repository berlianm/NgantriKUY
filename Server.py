# Server
# import library
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from datetime import datetime,timedelta
import time
import os

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)
with SimpleXMLRPCServer(("127.0.0.1",8008), requestHandler=RequestHandler, allow_none=True) as server: #local IP
    server.register_introspection_functions()
    
    # untuk menyimpan data registrasi (array data medis)
    jamKlinik = {}    # dictionary untuk jam klinik
    daftarKlinik = {} # dictionary untuk daftar klinik
    tempKlinik = {}   # dictionary untuk data klinik sementara
    dataMedis = []   # list data medis

    # untuk menyimpan jumlah iterasi program (berapa banyak) dijalankan oleh client 
    # iterasi ini digunakan untuk mengakses index sekarang dari array DataMedis
    iterasi = 0
    number = len(daftarKlinik)
    
    # fungsi registrasi
    def registrasi(noRekam,nama,tanggalLahir,klinik): # parameter (data medis) pasien
        # inisialiasi variabel global untuk iterasi
        global iterasi

        # pengkodisian untuk menghandle jika data medisnya kosong
        if len(dataMedis) == 0:
            iterasi = 0

        # untuk menyimpan data yang diinputkan user kedalam array dataMedis
        dataMedis.append([])                    # data ditambahkan ke array datamedis
        dataMedis[iterasi].append(noRekam)      # data no rekam medis ditambahkan
        dataMedis[iterasi].append(nama)         # data nama pasien ditambahkan
        dataMedis[iterasi].append(tanggalLahir) # data tanggal lahir ditambahkan
        dataMedis[iterasi].append(klinik)       # data klinik ditambahkan

        # menghitung jam masuk ke klinik (antrian pasien)
        noAntrian = hitungAntrian(dataMedis,klinik)

        # kondisi jika antrian adalah antrian pertama
        if(noAntrian-1 == 0):   
            # perkiraan waktu selesai dari pasien
            dataMedis[iterasi].append((datetime.now() + timedelta(minutes = 10)).strftime("%H:%M:%S"))
        # kondisi jika bukan antrian pertama
        else:
            # untuk mengambil waktu selesai dari antrian sebelumnya
            waktuSelesai = datetime.strptime(datetime.now().date().strftime("%d%m%y")+" "+dataMedis[len(dataMedis)-2][4], "%d%m%y %H:%M:%S")
            
            # kondisi untuk meng-handle waktu selesai antrian terakhir yang kurang dari waktu sekarang
            if(waktuSelesai < datetime.now()):
                # jika waktu selesai antrian terakhir kurang dari waktu sekarang, maka akan diisi dengan waktu sekarang ditambahkan 10 menit
                dataMedis[iterasi].append((datetime.now() + timedelta(minutes = 10)).strftime("%H:%M:%S"))
            else:
                # jika tidak, maka waktu selesai adalah waktu selesai dari antrian sebelumnya ditambah dengan 10 menit
                dataMedis[iterasi].append((waktuSelesai + timedelta(minutes = 10)).strftime("%H:%M:%S"))

        # untuk menghitung nomor antrian sesuai dengan klinik yang dipilih
        dataMedis[iterasi].append(noAntrian)

        # jumlah iterasi ditambah
        iterasi += 1

        # kondisi untuk menghandle jika antrian adalah antrian yang pertama
        if noAntrian == 0:
            noAntrian += 1

        arr = noAntrian
        # mengembalikkan nilai arr
        return arr

    # fungsi untuk menampilkan data medis
    def seeList():
        return dataMedis

    # fungsi untuk menghitung antrian sesuai dengan klinik
    def hitungAntrian(arr,key):
        jumlah = 0
        for j in range(len(arr)):
            for k in range(len(arr[j])):
                if arr[j][k] == key:
                    jumlah += 1
        return jumlah

    # fungsi untuk melihat antrian berdasarkan klinik dan norekam medis
    def lihatAntrian(noRekam,klinik):
        global dataMedis
        k = 0
        for j in range(len(dataMedis)):
            # untuk mengecek klinik dan no rekam medis dari array
            if dataMedis[j][3] == klinik and dataMedis[j][0] == noRekam:
                return k,dataMedis[j][5]
            else:
                if dataMedis[j][3] == klinik:
                    k += 1
        return False,False

    # fungsi untuk menghapus antrian sesuai waktu
    def refreshUrutan():
        global dataMedis, iterasi
        if len(dataMedis) > 0:
            if dataMedis[0][4] < datetime.now().strftime("%H:%M:%S"):
                dataMedis.pop(0)
                iterasi -= 1
        return True

    # fungsi untuk menambahkan klinik
    def addKlinik(nama, waktu):
        global number
        daftarKlinik[str(number+1)] = nama
        jamKlinik[nama] = waktu
        number+=1
        return daftarKlinik, jamKlinik

    # fungsi untuk menghapus klinik
    def deleteKlinik(nama):
        for key, value in list(daftarKlinik.items()):
            if value == nama:
                del daftarKlinik[key]
                jamKlinik.pop(nama)
                updateKey()
            else:
                pass
        
    # fungsi untuk mengembalikkan nilai daftarklinik
    def getKlinik():
        return daftarKlinik
    
    # fungsi untuk mengembalikkan nilai jamklinik
    def getJamKlinik():
        return jamKlinik

    # fungsi untuk mengembalikkan nilai datamedis
    def getDataMedis():
        return dataMedis

    # fungsi untuk update key
    def updateKey():
        index = 1
        for i in daftarKlinik:
            tempKlinik[str(index)] = daftarKlinik[i]
            index+=1
        for key, value in list(daftarKlinik.items()):
            del daftarKlinik[key]
        for key in tempKlinik:
            daftarKlinik[key] = tempKlinik[key]
        clearTemp()

    # fungsi untuk clear data sementara       
    def clearTemp():
        for key, value in list(tempKlinik.items()):
            del tempKlinik[key]

    # menginisialisasi semua fungsi agar dapat digunakan oleh client
    server.register_function(registrasi, 'registrasi')
    server.register_function(seeList, 'seeList')
    server.register_function(lihatAntrian, 'lihatAntrian')
    server.register_function(refreshUrutan, 'refreshUrutan')
    server.register_function(addKlinik, 'addKlinik')
    server.register_function(deleteKlinik, 'deleteKlinik')
    server.register_function(getKlinik, 'getKlinik')
    server.register_function(getJamKlinik, 'getJamKlinik')
    server.register_function(getDataMedis, 'getDataMedis')
    server.register_function(updateKey, 'updateKey')
    server.register_function(clearTemp, 'clearTemp')
    
    os.system("CLS")
    print("Serving.....")

    # menjalankan server selamanya
    server.serve_forever()
