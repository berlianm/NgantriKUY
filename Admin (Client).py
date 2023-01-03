# Admin
# import library
import xmlrpc.client
import os
import datetime

s = xmlrpc.client.ServerProxy('http://127.0.0.1:8008', allow_none=True)

# fungsi menu untuk consol application
def HomePage():
    while True:
        # os.system("CLS")
        e = datetime.datetime.now()
  
        # untuk mengecek waktu urutan dan jika melebihi akan dihapus
        s.refreshUrutan()
  
        # menu
        print("==========>   NGANTRIKUY   <==========")
        print ("Tanggal Hari Ini: ",e.strftime("%a, %d-%b-%Y"))
        print()
        print("=====================================")
        print("=========> Selamat Datang <==========")
        print("===>  Orang Sabar Disayang ALLAH <===")
        print("=====================================")
        print("=====|        ADMIN MENU        |====")
        print("=====|                          |====")
        print("=====|  1) Tambah Klinik        |====")
        print("=====|  2) Hapus Klinik         |====")
        print("=====|  3) List Klinik          |====")
        print("=====|  0) Exit                 |====")
        print("=====|                          |====")
        print("=====================================")
        print("=====> Masukkan Pilihan Anda <=======")
        print("=====================================")

        # untuk menyimpan jawaban dari inputan user
        answer = input('Pilihan Anda: ')

        # kondisi pilihan menu
        if answer == '0':
            AreYouSure()
            os.system("CLS")
            break

        elif answer == '1':
            now = datetime.datetime.now()
            nama = str(input("Masukkan nama klinik: "))
            print("Masukkan waktu tutup klinik")
            jam = int(input("jam: "))
            menit = int(input("menit: "))
            detik = int(input("detik: "))
            waktu = now.replace(hour=jam, minute=menit, second=detik, microsecond = 0)
            s.addKlinik(nama, waktu)
            print("berhasil")

        elif answer == '2':
            nama = str(input("Masukkan nama klinik: "))
            s.deleteKlinik(nama)

        elif answer == '3':
            iterasi = 1
            listKlinik = s.getKlinik()
            for i in listKlinik:
               print(iterasi," : ",listKlinik[str(i)], end =", ")
               print("")
               iterasi+=1

        else:
            print()
            print("==== Masukkan Pilihan Anda dengan benar  ====")
            print("=============================================")
            print("======= TEKAN ENTER UNTUK MELANJUTKAN =======")
            print("=============================================")
            input()
            os.system("CLS")

# UI jika user ingin exit
def AreYouSure():
    print("======================================")
    print("Apakah kamu benar-benar ingin keluar ?")
    print(" 1. Ya")
    print(" 2. Tidak")
    print("======================================")

    #untuk menyimpan jawaban dari inputan user
    answer = input('Pilihan Anda: ')

    # kondisi pilihan jika user ingin keluar dari Homepage
    if answer == '1':
        print()
        print("============> Sekian Terima Kasih Dan Sampai Jumpa <============")
        print("==================> Orang Sabar Disayang ALLAH <================")
        input()
        
    elif answer == '2':
        HomePage()

os.system("CLS")

# menampilkan UI Homepage
HomePage()
