import datetime
from abc import ABC, abstractmethod

class Kamar:
    def __init__(self, nomor_kamar, tipe_kamar, harga):
        self.nomor_kamar = nomor_kamar
        self.tipe_kamar = tipe_kamar
        self.harga = harga
        self.terisi = False
        self.tamu_saat_ini = None

    def check_in(self, tamu):
        if not self.terisi:
            self.terisi = True
            self.tamu_saat_ini = tamu
            return True
        return False

    def check_out(self):
        if self.terisi:
            self.terisi = False
            self.tamu_saat_ini = None
            return True
        return False

class Tamu:
    def __init__(self, nama, nomor_identitas):
        self.nama = nama
        self.nomor_identitas = nomor_identitas
        self.kamar_saat_ini = None

    def tetapkan_kamar(self, kamar):
        self.kamar_saat_ini = kamar

    def bersihkan_kamar(self):
        self.kamar_saat_ini = None

class Karyawan(ABC):
    def __init__(self, nama, id_karyawan, posisi):
        self.nama = nama
        self.id_karyawan = id_karyawan
        self.posisi = posisi

    @abstractmethod
    def lakukan_tugas(self):
        pass

class Resepsionis(Karyawan):
    def __init__(self, nama, id_karyawan):
        super().__init__(nama, id_karyawan, "Resepsionis")

    def lakukan_tugas(self):
        return "Menangani check-in dan check-out"

class PembersihKamar(Karyawan):
    def __init__(self, nama, id_karyawan):
        super().__init__(nama, id_karyawan, "Pembersih Kamar")

    def lakukan_tugas(self):
        return "Membersihkan kamar dan merawat area hotel"

class LayananKamar(Karyawan):
    def __init__(self, nama, id_karyawan):
        super().__init__(nama, id_karyawan, "Layanan Kamar")

    def lakukan_tugas(self):
        return "Mengantarkan makanan dan keperluan ke tamu"

class Reservasi:
    def __init__(self, tamu, kamar, tanggal_check_in, tanggal_check_out):
        self.tamu = tamu
        self.kamar = kamar
        self.tanggal_check_in = tanggal_check_in
        self.tanggal_check_out = tanggal_check_out
        self.total_biaya = self.hitung_biaya()

    def hitung_biaya(self):
        hari = (self.tanggal_check_out - self.tanggal_check_in).days
        return hari * self.kamar.harga

class Hotel:
    def __init__(self, nama):
        self.nama = nama
        self.kamar = {}
        self.tamu = {}
        self.karyawan = {}
        self.reservasi = []

    def tambah_kamar(self, kamar):
        self.kamar[kamar.nomor_kamar] = kamar

    def tambah_tamu(self, tamu):
        self.tamu[tamu.nomor_identitas] = tamu

    def tambah_karyawan(self, karyawan):
        self.karyawan[karyawan.id_karyawan] = karyawan

    def buat_reservasi(self, id_tamu, nomor_kamar, tanggal_check_in, tanggal_check_out):
        if id_tamu in self.tamu and nomor_kamar in self.kamar:
            tamu = self.tamu[id_tamu]
            kamar = self.kamar[nomor_kamar]
            reservasi = Reservasi(tamu, kamar, tanggal_check_in, tanggal_check_out)
            self.reservasi.append(reservasi)
            return reservasi
        return None

    def check_in(self, reservasi):
        if reservasi.kamar.check_in(reservasi.tamu):
            reservasi.tamu.tetapkan_kamar(reservasi.kamar)
            return True
        return False

    def check_out(self, reservasi):
        if reservasi.kamar.check_out():
            reservasi.tamu.bersihkan_kamar()
            return True
        return False

    def get_kamar_tersedia(self):
        return [kamar for kamar in self.kamar.values() if not kamar.terisi]

    def get_kamar_terisi(self):
        return [kamar for kamar in self.kamar.values() if kamar.terisi]

class SistemManajemenHotel:
    def __init__(self):
        self.hotel = Hotel("Hotel Python Megah")

    def jalankan(self):
        self.inisialisasi_hotel()
        while True:
            print("\n--- Sistem Manajemen Hotel ---")
            print("1. Buat Reservasi")
            print("2. Check-in")
            print("3. Check-out")
            print("4. Lihat Kamar Tersedia")
            print("5. Lihat Kamar Terisi")
            print("6. Tambah Tamu")
            print("7. Tambah Karyawan")
            print("8. Lihat Karyawan")
            print("9. Keluar")

            pilihan = input("Masukkan pilihan Anda: ")

            if pilihan == '1':
                self.buat_reservasi()
            elif pilihan == '2':
                self.check_in()
            elif pilihan == '3':
                self.check_out()
            elif pilihan == '4':
                self.lihat_kamar_tersedia()
            elif pilihan == '5':
                self.lihat_kamar_terisi()
            elif pilihan == '6':
                self.tambah_tamu()
            elif pilihan == '7':
                self.tambah_karyawan()
            elif pilihan == '8':
                self.lihat_karyawan()
            elif pilihan == '9':
                print("Terima kasih telah menggunakan Sistem Manajemen Hotel.")
                break
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")

    def inisialisasi_hotel(self):
        # Tambahkan beberapa kamar
        for i in range(1, 11):
            kamar = Kamar(f"10{i}", "Standar", 100000)
            self.hotel.tambah_kamar(kamar)
        for i in range(1, 6):
            kamar = Kamar(f"20{i}", "Deluxe", 200000)
            self.hotel.tambah_kamar(kamar)
        for i in range(1, 3):
            kamar = Kamar(f"30{i}", "Suite", 300000)
            self.hotel.tambah_kamar(kamar)

        # Tambahkan beberapa karyawan
        self.hotel.tambah_karyawan(Resepsionis("Budi Santoso", "K001"))
        self.hotel.tambah_karyawan(PembersihKamar("Siti Aminah", "K002"))
        self.hotel.tambah_karyawan(LayananKamar("Agus Setiawan", "K003"))

    def buat_reservasi(self):
        id_tamu = input("Masukkan ID tamu: ")
        nomor_kamar = input("Masukkan nomor kamar: ")
        check_in = input("Masukkan tanggal check-in (YYYY-MM-DD): ")
        check_out = input("Masukkan tanggal check-out (YYYY-MM-DD): ")

        try:
            tanggal_check_in = datetime.datetime.strptime(check_in, "%Y-%m-%d").date()
            tanggal_check_out = datetime.datetime.strptime(check_out, "%Y-%m-%d").date()
            reservasi = self.hotel.buat_reservasi(id_tamu, nomor_kamar, tanggal_check_in, tanggal_check_out)
            if reservasi:
                print(f"Reservasi berhasil dibuat. Total biaya: Rp{reservasi.total_biaya:,}")
            else:
                print("Tidak dapat membuat reservasi. Silakan periksa ID tamu dan nomor kamar.")
        except ValueError:
            print("Format tanggal tidak valid. Gunakan format YYYY-MM-DD.")

    def check_in(self):
        id_tamu = input("Masukkan ID tamu: ")
        nomor_kamar = input("Masukkan nomor kamar: ")
        for reservasi in self.hotel.reservasi:
            if reservasi.tamu.nomor_identitas == id_tamu and reservasi.kamar.nomor_kamar == nomor_kamar:
                if self.hotel.check_in(reservasi):
                    print("Check-in berhasil.")
                else:
                    print("Check-in gagal. Kamar mungkin sudah terisi.")
                return
        print("Reservasi tidak ditemukan.")

    def check_out(self):
        nomor_kamar = input("Masukkan nomor kamar: ")
        for reservasi in self.hotel.reservasi:
            if reservasi.kamar.nomor_kamar == nomor_kamar and reservasi.kamar.terisi:
                if self.hotel.check_out(reservasi):
                    print("Check-out berhasil.")
                else:
                    print("Check-out gagal.")
                return
        print("Tidak ada reservasi aktif untuk kamar ini.")

    def lihat_kamar_tersedia(self):
        kamar_tersedia = self.hotel.get_kamar_tersedia()
        if kamar_tersedia:
            print("Kamar Tersedia:")
            for kamar in kamar_tersedia:
                print(f"Kamar {kamar.nomor_kamar} - {kamar.tipe_kamar} - Rp{kamar.harga:,}/malam")
        else:
            print("Tidak ada kamar tersedia.")

    def lihat_kamar_terisi(self):
        kamar_terisi = self.hotel.get_kamar_terisi()
        if kamar_terisi:
            print("Kamar Terisi:")
            for kamar in kamar_terisi:
                print(f"Kamar {kamar.nomor_kamar} - {kamar.tipe_kamar} - Ditempati oleh {kamar.tamu_saat_ini.nama}")
        else:
            print("Tidak ada kamar yang terisi saat ini.")

    def tambah_tamu(self):
        nama = input("Masukkan nama tamu: ")
        nomor_identitas = input("Masukkan nomor identitas tamu: ")
        tamu = Tamu(nama, nomor_identitas)
        self.hotel.tambah_tamu(tamu)
        print("Tamu berhasil ditambahkan.")

    def tambah_karyawan(self):
        nama = input("Masukkan nama karyawan: ")
        id_karyawan = input("Masukkan ID karyawan: ")
        posisi = input("Masukkan posisi (Resepsionis/PembersihKamar/LayananKamar): ")
        
        if posisi.lower() == "resepsionis":
            karyawan = Resepsionis(nama, id_karyawan)
        elif posisi.lower() == "pembersihkamar":
            karyawan = PembersihKamar(nama, id_karyawan)
        elif posisi.lower() == "layanankamar":
            karyawan = LayananKamar(nama, id_karyawan)
        else:
            print("Posisi tidak valid.")
            return

        self.hotel.tambah_karyawan(karyawan)
        print("Karyawan berhasil ditambahkan.")

    def lihat_karyawan(self):
        if self.hotel.karyawan:
            print("Karyawan Hotel:")
            for karyawan in self.hotel.karyawan.values():
                print(f"{karyawan.nama} - {karyawan.posisi} (ID: {karyawan.id_karyawan})")
        else:
            print("Tidak ada karyawan terdaftar.")

if __name__ == "__main__":
    sistem = SistemManajemenHotel()
    sistem.jalankan()
