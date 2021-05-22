import pygame
import os
import random

pygame.init()

#Konstanta global
papan_tinggi = 600
papan_lebar = 1100
papan = pygame.display.set_mode((papan_lebar,papan_tinggi))

WARNA_HITAM = (0, 0, 0)
WARNA_PUTIH = (255, 255, 255)
WARNA_ABUABU = (211, 211, 211)

LARI = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
        pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]

LOMPAT = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))

NUNDUK = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
          pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

KAKTUS_KECIL = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]

KAKTUS_BESAR = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BURUNG = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
          pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

AWAN = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

LATAR = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

MATI = pygame.image.load(os.path.join("Assets/Dino", "DinoDead.png"))

PERMAINAN_SELESAI = pygame.image.load(os.path.join("Assets/Other", "GameOver.png"))

SUARA_LOMPAT = pygame.mixer.Sound('Assets/Sound/jump.wav')
SUARA_MATI = pygame.mixer.Sound('Assets/Sound/die.wav')
SUARA_BONUS = pygame.mixer.Sound('Assets/Sound/checkPoint.wav')


class Dinosaurus:
    POSISI_X = 80
    POSISI_Y = 310
    POSISI_Y_NUNDUK = 340
    KECEPATAN_LOMPAT = 8.5

    def __init__(self):
        self.nunduk_gmbr = NUNDUK
        self.lari_gmbr = LARI
        self.lompat_gmbr = LOMPAT
        self.suara_lompat = SUARA_LOMPAT

        self.dino_nunduk = False
        self.dino_lari = True
        self.dino_lompat = False      

        self.index_langkah = 0
        self.gerak_lompat = self.KECEPATAN_LOMPAT
        self.gambar = self.lari_gmbr[0]
        self.kotak_dino = self.gambar.get_rect()
        self.kotak_dino.x = self.POSISI_X
        self.kotak_dino.y = self.POSISI_Y

    def gerakan(self, userInput):
        if self.dino_nunduk:
            self.nunduk()
        if self.dino_lari:
            self.lari()
        if self.dino_lompat:
            self.lompat()
       
        if self.index_langkah >= 10:
            self.index_langkah = 0
        
        if userInput[pygame.K_UP] and not self.dino_lompat:
            self.dino_nunduk = False
            self.dino_lari = False
            self.dino_lompat = True
            if pygame.mixer.get_init() != None:
                self.suara_lompat.play()
        elif userInput[pygame.K_DOWN] and not self.dino_lompat:
            self.dino_nunduk = True
            self.dino_lari = False
            self.dino_lompat = False
        elif not (self.dino_lompat or userInput[pygame.K_DOWN]):
            self.dino_nunduk = False
            self.dino_lari = True
            self.dino_lompat = False
        
    def nunduk(self):
        self.gambar = self.nunduk_gmbr[self.index_langkah // 5]
        self.kotak_dino = self.gambar.get_rect()
        self.kotak_dino.x = self.POSISI_X
        self.kotak_dino.y = self.POSISI_Y_NUNDUK
        self.index_langkah += 1

    def lari(self):
        self.gambar = self.lari_gmbr[self.index_langkah // 5]
        self.kotak_dino = self.gambar.get_rect()
        self.kotak_dino.x = self.POSISI_X
        self.kotak_dino.y = self.POSISI_Y
        self.index_langkah += 1

    def lompat(self):
        self.gambar = self.lompat_gmbr
        if self.dino_lompat:
            self.kotak_dino.y -= self.gerak_lompat * 4
            self.gerak_lompat -= 0.8
        if self.gerak_lompat < - self.KECEPATAN_LOMPAT:
            self.dino_lompat = False
            self.gerak_lompat = self.KECEPATAN_LOMPAT
    
    def tampil(self, papan):
        papan.blit(self.gambar, (self.kotak_dino.x, self.kotak_dino.y))


class Awan:
    def __init__(self):
        self.koordinat_x = papan_lebar 
        self.koordinat_y = random.randint(50, 150)
        self.gambar = AWAN
        self.lebar = self.gambar.get_width()

    def gerakan(self):
        self.koordinat_x -= kecepatan_permainan -5
        if self.koordinat_x < - self.lebar:
            self.koordinat_x = papan_lebar 
            self.koordinat_y = random.randint(50, 150)

    def tampil(self, papan):
        papan.blit(self.gambar, (self.koordinat_x, self.koordinat_y))


class Rintangan:
    def __init__(self, gambar, tipe):
        self.gambar = gambar
        self.tipe = tipe
        self.kotak = self.gambar[self.tipe].get_rect()
        self.kotak.x = papan_lebar
        self.lebar_picu = self.gambar[self.tipe].get_width()
        self.tinggi_picu = papan_tinggi // 2

    def gerakan(self):
        self.kotak.x -= kecepatan_permainan
        if self.kotak.x < -self.kotak.width:
            rintangan.pop()

    def tampil(self, papan):
        self.picu = pygame.draw.rect(papan, WARNA_PUTIH, (self.kotak.x, papan_tinggi // 5, self.lebar_picu, self.tinggi_picu), 0)
        papan.blit(self.gambar[self.tipe], self.kotak)


class KaktusKecil(Rintangan):
    def __init__(self, gambar):
        self.tipe = random.randint(0, 2)
        super().__init__(gambar, self.tipe)
        self.kotak.y = 325


class KaktusBesar(Rintangan):
    def __init__(self, gambar):
        self.tipe = random.randint(0, 2)
        super().__init__(gambar, self.tipe)
        self.kotak.y = 315


class Burung(Rintangan):
    def __init__(self, gambar):
        self.tipe = 0
        super().__init__(gambar, self.tipe)
        self.kotak.y = 250
        self.indeks = 0
    
    def tampil(self, papan):
        self.picu = pygame.draw.rect(papan, WARNA_PUTIH, (self.kotak.x, papan_tinggi // 5, self.lebar_picu, self.tinggi_picu), 0)
        if self.indeks >= 9:
            self.indeks = 0
        papan.blit(self.gambar[self.indeks // 5], self.kotak)
        self.indeks += 1


class Tombol:
    def __init__(self, warna, x, y, teks=""):
        self.warna = warna
        self.tombol_posisi_x = x
        self.tombol_posisi_y = y
        self.lebar_tombol = 250
        self.tinggi_tombol = 50
        self.teks = teks
    
    def tampil(self):
        pygame.draw.rect(papan, WARNA_HITAM, (self.tombol_posisi_x - 2, self.tombol_posisi_y - 2, self.lebar_tombol + 4, self.tinggi_tombol + 4), 0)
        pygame.draw.rect(papan, self.warna, (self.tombol_posisi_x, self.tombol_posisi_y, self.lebar_tombol, self.tinggi_tombol), 0)

        if self.teks != "":
            font = pygame.font.Font("freesansbold.ttf", 20)
            teks = font.render(self.teks, True, WARNA_HITAM)
            papan.blit(teks, (self.tombol_posisi_x + (self.lebar_tombol / 2 - teks.get_width() / 2), self.tombol_posisi_y + (self.tinggi_tombol / 2 - teks.get_height() / 2)))

    def klik_tombol(self, posisi):
        if posisi[0] > self.tombol_posisi_x and posisi[0] < self.tombol_posisi_x + self.lebar_tombol:
            if posisi[1] > self.tombol_posisi_y and posisi[1] < self.tombol_posisi_y + self.tinggi_tombol:
                return True
        
        return False


def main():
    global kecepatan_permainan, posisi_x_latar, posisi_y_latar, poin, rintangan, lari, kondisi_skor, bonus_poin, indeks_rintangan
    lari = True
    waktu = pygame.time.Clock()
    pemain = Dinosaurus()
    awan = Awan()
    kecepatan_permainan = 15
    posisi_x_latar = 0
    posisi_y_latar = 380
    poin = 0
    font = pygame.font.Font("freesansbold.ttf", 20)
    rintangan = []
    jumlah_mati = 0
    indeks_rintangan = 0
    kondisi_skor = True
    bonus_poin = False

    def skor():
        global poin, kecepatan_permainan, kondisi_skor, bonus_poin, indeks_rintangan
        for satu_rintangan in rintangan:
            if pemain.kotak_dino.colliderect(satu_rintangan.picu) and kondisi_skor == True:
               poin += 1
               indeks_rintangan += 1
               kondisi_skor = False
            elif not pemain.kotak_dino.colliderect(satu_rintangan.picu):
               kondisi_skor = True
        
        if indeks_rintangan == 10:
            kecepatan_permainan += 3
            indeks_rintangan = 0

        if poin % 5 == 0 and poin != 0:
            teks = font.render("+10", True, WARNA_HITAM)
            kotak_teks = teks.get_rect()
            kotak_teks.center = (1035, 65)
            papan.blit(teks, kotak_teks)
            

        if poin % 5 == 0 and bonus_poin == True:
            poin += 10
            bonus_poin = False
            if pygame.mixer.get_init() != None:
                SUARA_BONUS.play()
        elif not poin % 5 == 0:
            bonus_poin = True

        teks = font.render("Skor: " + str(poin), True, WARNA_HITAM)
        kotak_teks = teks.get_rect()
        kotak_teks.center = (1000, 40)
        papan.blit(teks, kotak_teks)

    def latar():
        global posisi_x_latar, posisi_y_latar
        lebar_gambar = LATAR.get_width()
        papan.blit(LATAR, (posisi_x_latar, posisi_y_latar))
        papan.blit(LATAR, (lebar_gambar + posisi_x_latar, posisi_y_latar))
        if posisi_x_latar <= -lebar_gambar:
            papan.blit(LATAR, (lebar_gambar + posisi_x_latar, posisi_y_latar))
            posisi_x_latar = 0
        posisi_x_latar -= kecepatan_permainan

    while lari:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                lari = False
        
        papan.fill(WARNA_PUTIH)
        userInput = pygame.key.get_pressed()

        if len(rintangan) == 0:
            if random.randint(0, 2) == 0:
                rintangan.append(KaktusKecil(KAKTUS_KECIL))
            elif random.randint(0, 2) == 1:
                rintangan.append(KaktusBesar(KAKTUS_BESAR))
            elif random.randint(0, 2) == 2:
                rintangan.append(Burung(BURUNG))
        
        for satu_rintangan in rintangan:
            satu_rintangan.tampil(papan)
            satu_rintangan.gerakan()
            if pemain.kotak_dino.colliderect(satu_rintangan.kotak):
                if pygame.mixer.get_init() != None:
                    SUARA_MATI.play()
                pygame.time.delay(500)
                jumlah_mati += 1
                menu(jumlah_mati)

        latar()

        awan.tampil(papan)
        awan.gerakan()

        pemain.tampil(papan)
        pemain.gerakan(userInput)

        skor()

        waktu.tick(30)
        pygame.display.update()


def menu(jumlah_mati):
    global poin, lari
    tombol_mulai = Tombol(WARNA_PUTIH, 290, 295, "Mulai Permainan")
    tombol_keluar = Tombol(WARNA_PUTIH, 550, 295, "Keluar")
    lari = True
    while lari:
        papan.fill(WARNA_PUTIH)
        font = pygame.font.Font("freesansbold.ttf", 30)
        
        if jumlah_mati == 0:
            pengembang = font.render("Tim Pengembang: Dinocode ITERA", True, WARNA_HITAM)
            judul = font.render("++DISCONECTOSAURUS++", True, WARNA_HITAM)
            kotak_judul = judul.get_rect()
            kotak_judul.center = (papan_lebar // 2, papan_tinggi //2 + - 155)
            papan.blit(judul, (kotak_judul))
            kotak_pengembang = pengembang.get_rect()
            kotak_pengembang.center = (papan_lebar // 2, papan_tinggi //2 + 85)
            papan.blit(pengembang, kotak_pengembang)
            papan.blit(LARI[0], (papan_lebar // 2 - 40, papan_tinggi // 2 - 125))
            tombol_mulai.tampil()
            tombol_keluar.tampil()
        elif jumlah_mati > 0:
            tombol_keluar.tombol_posisi_y = 295
            tombol_mulai.tombol_posisi_y = 295
            tombol_keluar.tampil()
            tombol_mulai.teks = "Mulai Kembali"
            tombol_mulai.tampil()
            skor = font.render("Total Skor: " + str(poin), True, WARNA_HITAM)
            kotak_skor = skor.get_rect()
            kotak_skor.center = (papan_lebar // 2, papan_tinggi // 2 + 80)
            berakhir = font.render("PERMAINAN BERAKHIR", True, WARNA_HITAM)
            kotak_berakhir = berakhir.get_rect()
            kotak_berakhir.center = (papan_lebar // 2, papan_tinggi // 2 - 170)
            papan.blit(skor, kotak_skor)
            papan.blit(MATI, (papan_lebar // 2 - 40, papan_tinggi // 2 - 130))
            papan.blit(berakhir, kotak_berakhir)

        pygame.display.update()

        for event in pygame.event.get():
            kursor = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                lari = False
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tombol_mulai.klik_tombol(kursor):
                    main()
                elif tombol_keluar.klik_tombol(kursor):
                    lari = False
                    pygame.quit()
                    quit()
            if event.type == pygame.MOUSEMOTION:
                if tombol_mulai.klik_tombol(kursor):
                    tombol_mulai.warna = WARNA_ABUABU
                elif tombol_keluar.klik_tombol(kursor):
                    tombol_keluar.warna = WARNA_ABUABU
                else:
                    tombol_mulai.warna = WARNA_PUTIH
                    tombol_keluar.warna = WARNA_PUTIH
                

menu(jumlah_mati = 0)
