import sys
import random
import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QDesktopWidget, QLineEdit, QGraphicsView, QGraphicsScene
from PyQt5.QtCore import Qt, QUrl, QTimer, QRectF
from PyQt5.QtGui import QFont, QFontDatabase, QPalette, QColor, QLinearGradient, QBrush, QPainter, QPen
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer


class GlavnoeMenyu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.imya_igroka = None
        self.indeks_skina = 0
        self.monety = self.zagruzit_monety()
        self.skiny = ["Скин 1", "Скин 2", "Скин 3"]
        self.fon_muzika = None
        self.zvuk_knopki = None
        self.rekordy = self.zagruzit_rekordy()
        self.init_interfeis()

    def init_interfeis(self):
        ekran = QDesktopWidget().screenGeometry()
        shirina_ekrana = ekran.width()
        visota_ekrana = ekran.height()

        shirina_okna = int(shirina_ekrana * 0.6)
        visota_okna = int(visota_ekrana * 0.7)
        self.setFixedSize(shirina_okna, visota_okna)

        self.move(
            (shirina_ekrana - shirina_okna) // 2,
            (visota_ekrana - visota_okna) // 2
        )
        self.setWindowTitle("Flappy Bird")

        put_k_fontu = "mat/f/Comfortaa.ttf"
        id_fonta = QFontDatabase.addApplicationFont(put_k_fontu)
        self.svoy_font = QFontDatabase.applicationFontFamilies(id_fonta)[0]

        self.zvuk_knopki = QMediaPlayer()
        self.zvuk_knopki.setMedia(QMediaContent(QUrl.fromLocalFile("mat/s/hump.mp3")))
        self.zvuk_knopki.setVolume(50)

        self.fon_muzika = QMediaPlayer()
        self.fon_muzika.setMedia(QMediaContent(QUrl.fromLocalFile("mat/mus/muslo.mp3")))
        self.fon_muzika.setVolume(20)
        self.fon_muzika.mediaStatusChanged.connect(self.kogda_muzika_zakonchilas)

        osnovnoy_widget = QWidget()
        self.setCentralWidget(osnovnoy_widget)

        self.osnovnoy_layout = QVBoxLayout()
        self.osnovnoy_layout.setAlignment(Qt.AlignCenter)
        self.osnovnoy_layout.setSpacing(30)
        osnovnoy_widget.setLayout(self.osnovnoy_layout)

        self.sozdat_ekran_imya()
        self.sozdat_glavnoe_menyu()
        self.sozdat_magazin()
        self.sozdat_tablitsu_rekordov()
        self.sozdat_ekran_igry()

        self.osnovnoy_layout.addWidget(self.widget_imya)
        self.osnovnoy_layout.addWidget(self.widget_menyu)
        self.osnovnoy_layout.addWidget(self.widget_magazin)
        self.osnovnoy_layout.addWidget(self.widget_rekordy)
        self.osnovnoy_layout.addWidget(self.widget_igra)

        self.pokazat_ekran_imya()
        self.ustanovit_fon()

    def kogda_muzika_zakonchilas(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.fon_muzika.setPosition(0)
            self.fon_muzika.play()

    def sozdat_knopku(self, tekst, razmer_fonta=24, otstup=15, shirina=None, visota=None):
        knopka = QPushButton(tekst)
        stil = f"""
            QPushButton {{
                background-color: rgba(255, 105, 180, 0.3);
                color: white;
                border: 2px solid #ff69b4;
                border-radius: 15px;
                padding: {otstup}px;
                font-size: {razmer_fonta}px;
                font-family: "{self.svoy_font}";
                text-shadow: 0 0 8px #ff69b4;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 105, 180, 0.6);
                border: 2px solid #ff1493;
            }}
        """
        knopka.setStyleSheet(stil)
        if shirina and visota:
            knopka.setFixedSize(shirina, visota)
        return knopka

    def sozdat_ekran_imya(self):
        self.widget_imya = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(30)

        zagolovok = QLabel("ВВЕДИТЕ ИМЯ")
        zagolovok.setAlignment(Qt.AlignCenter)
        zagolovok.setFont(QFont(self.svoy_font, 48, QFont.Bold))
        zagolovok.setStyleSheet("""
            color: #ff00ff;
            text-shadow: 0 0 10px #ff00ff, 0 0 20px #ff00ff;
        """)
        layout.addWidget(zagolovok)

        self.pole_imya = QLineEdit()
        self.pole_imya.setPlaceholderText("Ваше имя")
        self.pole_imya.setAlignment(Qt.AlignCenter)
        self.pole_imya.setFont(QFont(self.svoy_font, 24))
        self.pole_imya.setStyleSheet("""
            padding: 15px;
            border: 2px solid #ff69b4;
            border-radius: 15px;
            background-color: rgba(255, 255, 255, 0.2);
            color: white;
        """)
        self.pole_imya.setMaxLength(15)
        layout.addWidget(self.pole_imya)

        knopka_dalee = self.sozdat_knopku("Продолжить")
        knopka_dalee.clicked.connect(self.nazhat_dalee)
        layout.addWidget(knopka_dalee)

        self.widget_imya.setLayout(layout)

    def sozdat_glavnoe_menyu(self):
        self.widget_menyu = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(30)

        zagolovok = QLabel("FLAPPY BIRD")
        zagolovok.setAlignment(Qt.AlignCenter)
        zagolovok.setFont(QFont(self.svoy_font, 48, QFont.Bold))
        zagolovok.setStyleSheet("""
            color: #ff00ff;
            text-shadow: 0 0 10px #ff00ff, 0 0 20px #ff00ff;
        """)
        layout.addWidget(zagolovok)

        knopki = [
            ("Играть", self.nachat_igru),
            ("Магазин", self.pokazat_magazin),
            ("Таблица рекордов", self.pokazat_rekordy),
            ("Выход", self.vyiti)
        ]

        for tekst, obrabotka in knopki:
            knopka = self.sozdat_knopku(tekst)
            knopka.clicked.connect(obrabotka)
            layout.addWidget(knopka)

        self.widget_menyu.setLayout(layout)

    def sozdat_magazin(self):
        self.widget_magazin = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        verhniy_ryad = QHBoxLayout()
        knopka_nazad = self.sozdat_knopku("Вернуться", razmer_fonta=18, otstup=10)
        knopka_nazad.clicked.connect(self.pokazat_glavnoe_menyu)

        label_monety = QLabel(f"Монеты: {self.monety}")
        label_monety.setObjectName("label_monety")
        label_monety.setFont(QFont(self.svoy_font, 18))
        label_monety.setStyleSheet("color: yellow; font-weight: bold;")

        verhniy_ryad.addWidget(knopka_nazad)
        verhniy_ryad.addStretch()
        verhniy_ryad.addWidget(label_monety)
        layout.addLayout(verhniy_ryad)

        self.otobrazhenie_skina = QLabel("СКИН")
        self.otobrazhenie_skina.setAlignment(Qt.AlignCenter)
        self.otobrazhenie_skina.setFont(QFont(self.svoy_font, 48, QFont.Bold))
        self.otobrazhenie_skina.setStyleSheet("""
            background-color: #dcdcdc;
            border: 2px solid #888;
            border-radius: 100px;
            padding: 50px;
            color: black;
        """)
        layout.addWidget(self.otobrazhenie_skina)

        navigatsiya = QHBoxLayout()
        knopka_nazad_skin = self.sozdat_knopku("◀", razmer_fonta=32, otstup=10, shirina=80, visota=80)
        knopka_vpered_skin = self.sozdat_knopku("▶", razmer_fonta=32, otstup=10, shirina=80, visota=80)

        knopka_nazad_skin.clicked.connect(self.predydushiy_skin)
        knopka_vpered_skin.clicked.connect(self.sleduyushiy_skin)

        navigatsiya.addWidget(knopka_nazad_skin)
        navigatsiya.addSpacing(20)
        navigatsiya.addWidget(knopka_vpered_skin)
        layout.addLayout(navigatsiya)

        podpisi = QHBoxLayout()
        for tekst in ["Смена скина\nназад", "Смена скина\nвперед"]:
            podpis = QLabel(tekst)
            podpis.setAlignment(Qt.AlignCenter)
            podpis.setFont(QFont(self.svoy_font, 12))
            podpisi.addWidget(podpis)
        layout.addLayout(podpisi)

        self.widget_magazin.setLayout(layout)

    def sozdat_tablitsu_rekordov(self):
        self.widget_rekordy = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        zagolovok = QLabel("ТАБЛИЦА РЕКОРДОВ")
        zagolovok.setAlignment(Qt.AlignCenter)
        zagolovok.setFont(QFont(self.svoy_font, 36, QFont.Bold))
        zagolovok.setStyleSheet("""
            color: #ff00ff;
            text-shadow: 0 0 10px #ff00ff, 0 0 20px #ff00ff;
        """)
        layout.addWidget(zagolovok)

        self.soderzhanie_rekordov = QWidget()
        self.layout_rekordov = QVBoxLayout()
        self.layout_rekordov.setAlignment(Qt.AlignCenter)
        self.soderzhanie_rekordov.setLayout(self.layout_rekordov)
        layout.addWidget(self.soderzhanie_rekordov)

        knopka_nazad = self.sozdat_knopku("Назад")
        knopka_nazad.clicked.connect(self.pokazat_glavnoe_menyu)
        layout.addWidget(knopka_nazad)

        self.widget_rekordy.setLayout(layout)
        self.obnovit_rekordy()

    def obnovit_rekordy(self):
        while self.layout_rekordov.count():
            child = self.layout_rekordov.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.rekordy = self.zagruzit_rekordy()

        if not self.rekordy:
            nadpis = QLabel("Нет рекордов")
            nadpis.setAlignment(Qt.AlignCenter)
            nadpis.setFont(QFont(self.svoy_font, 20))
            nadpis.setStyleSheet("color: white;")
            self.layout_rekordov.addWidget(nadpis)
        else:
            for imya, ochki in self.rekordy:
                nadpis = QLabel(f"{imya} — {ochki}")
                nadpis.setAlignment(Qt.AlignCenter)
                nadpis.setFont(QFont(self.svoy_font, 20))
                nadpis.setStyleSheet("color: white; background-color: rgba(255, 105, 180, 0.2); padding: 10px; border-radius: 10px;")
                self.layout_rekordov.addWidget(nadpis)

    def sozdat_ekran_igry(self):
        self.widget_igra = QWidget()
        self.widget_igra.setFocusPolicy(Qt.StrongFocus)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.scena = QGraphicsScene()
        self.vid = QGraphicsView(self.scena)
        self.vid.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.vid.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.vid.setStyleSheet("background: transparent; border: none;")
        self.vid.setRenderHint(QPainter.Antialiasing)

        layout.addWidget(self.vid)
        self.widget_igra.setLayout(layout)

    def pokazat_ekran_imya(self):
        self.widget_imya.setVisible(True)
        self.widget_menyu.setVisible(False)
        self.widget_magazin.setVisible(False)
        self.widget_rekordy.setVisible(False)
        self.widget_igra.setVisible(False)

    def pokazat_glavnoe_menyu(self):
        self.zvuk_knopki.play()
        self.ochistit_igru()
        self.widget_imya.setVisible(False)
        self.widget_menyu.setVisible(True)
        self.widget_magazin.setVisible(False)
        self.widget_rekordy.setVisible(False)
        self.widget_igra.setVisible(False)
        self.obnovit_rekordy()

    def pokazat_magazin(self):
        self.zvuk_knopki.play()
        self.widget_imya.setVisible(False)
        self.widget_menyu.setVisible(False)
        self.widget_magazin.setVisible(True)
        self.widget_rekordy.setVisible(False)
        self.widget_igra.setVisible(False)
        self.obnovit_skiny()
        label = self.widget_magazin.findChild(QLabel, "label_monety")
        if label:
            label.setText(f"Монеты: {self.monety}")

    def pokazat_rekordy(self):
        self.zvuk_knopki.play()
        self.widget_imya.setVisible(False)
        self.widget_menyu.setVisible(False)
        self.widget_magazin.setVisible(False)
        self.widget_rekordy.setVisible(True)
        self.widget_igra.setVisible(False)

    def pokazat_igru(self):
        self.zvuk_knopki.play()
        self.widget_imya.setVisible(False)
        self.widget_menyu.setVisible(False)
        self.widget_magazin.setVisible(False)
        self.widget_rekordy.setVisible(False)
        self.widget_igra.setVisible(True)
        self.nachat_igru_vnutri()

    def obnovit_pozitsiyu_scheta(self):
        if hasattr(self, 'tekst_scheta'):
            w = self.scena.width()
            rect = self.tekst_scheta.boundingRect()
            self.tekst_scheta.setPos(w - rect.width() - 20, 20)

    def nachat_igru_vnutri(self):
        self.scena.clear()
        w, h = self.width(), self.height()
        self.vid.setFixedSize(w, h)
        self.scena.setSceneRect(0, 0, w, h)

        self.GRAVITATSIYA = 0.6
        self.SILA_PRYZHKA = -7
        self.SKOROST_TRUB = 3
        self.SHIRINA_TRUBY = 52
        self.VYSOTA_PROREZI = 20
        self.OTSTUP_SVERHU = 60
        self.SCHET = 0

        radius_ptitsy = 16
        perо = QPen(QColor("white"), 3)
        kist = QBrush(QColor("#ff69b4"))
        self.ptitsa = self.scena.addEllipse(0, 0, radius_ptitsy * 2, radius_ptitsy * 2, pen=perо, brush=kist)
        self.ptitsa.setPos(100, h // 2)

        self.skorost_ptitsy = 0
        self.truby = []

        font = QFont(self.svoy_font, 28, QFont.Bold)
        self.tekst_scheta = self.scena.addText("0", font)
        self.tekst_scheta.setDefaultTextColor(QColor("white"))
        self.tekst_scheta.setZValue(100)
        self.obnovit_pozitsiyu_scheta()

        self.knopka_nazad_v_igre = self.sozdat_knopku("Назад", razmer_fonta=16, otstup=6, shirina=90, visota=35)
        self.knopka_nazad_v_igre.clicked.connect(self.pokazat_glavnoe_menyu)
        self.knopka_nazad_v_igre.setParent(self.vid)
        self.knopka_nazad_v_igre.move(20, 20)
        self.knopka_nazad_v_igre.show()

        self.timer_trub = QTimer()
        self.timer_trub.timeout.connect(self.sozydat_trubu)
        self.timer_trub.start(2800)

        self.timer_igry = QTimer()
        self.timer_igry.timeout.connect(self.obnovlenie_igry)
        self.timer_igry.start(30)

        self.widget_igra.setFocus()
        self.widget_igra.setFocusPolicy(Qt.StrongFocus)
        self.widget_igra.setFocus(Qt.OtherFocusReason)
        self.activateWindow()

        if self.fon_muzika:
            self.fon_muzika.play()

    def sozydat_trubu(self):
        h = self.scena.height()
        if h <= self.OTSTUP_SVERHU + self.VYSOTA_PROREZI:
            return

        MIN_VYSOTA_PROREZI = 16 * 3

        realnaya_vysota = max(self.VYSOTA_PROREZI, MIN_VYSOTA_PROREZI)

        min_vverhu = self.OTSTUP_SVERHU + 40
        max_vverhu = int(h - realnaya_vysota - 20)

        if max_vverhu <= min_vverhu:
            vverhu = min_vverhu
        else:
            vverhu = random.randint(min_vverhu, max_vverhu)

        vnizu = vverhu + realnaya_vysota

        tsvet_truby = QColor("#ff69b4")
        pero_truby = QPen(tsvet_truby, 2)
        kist_truby = QBrush(tsvet_truby)

        truba_verh = self.scena.addRect(0, 0, self.SHIRINA_TRUBY, vverhu, pen=pero_truby, brush=kist_truby)
        truba_niz = self.scena.addRect(0, vnizu, self.SHIRINA_TRUBY, h - vnizu, pen=pero_truby, brush=kist_truby)

        truba_verh.setPos(self.scena.width(), 0)
        truba_niz.setPos(self.scena.width(), vnizu)

        truba_verh.setData(0, False)
        self.truby.append((truba_verh, truba_niz))

    def obnovlenie_igry(self):
        if not self.widget_igra.isVisible():
            return

        self.skorost_ptitsy += self.GRAVITATSIYA
        self.ptitsa.moveBy(0, self.skorost_ptitsy)

        tsentr_x = self.ptitsa.x() + 16
        tsentr_y = self.ptitsa.y() + 16
        visota_sceny = self.scena.height()

        if tsentr_y - 16 <= 0 or tsentr_y + 16 >= visota_sceny:
            self.konets_igry()
            return

        udalit_truby = []
        for verh, niz in self.truby:
            verh.moveBy(-self.SKOROST_TRUB, 0)
            niz.moveBy(-self.SKOROST_TRUB, 0)

            if not verh.data(0) and (verh.x() + self.SHIRINA_TRUBY < tsentr_x):
                verh.setData(0, True)
                self.SCHET += 1
                self.tekst_scheta.setPlainText(str(self.SCHET))
                self.obnovit_pozitsiyu_scheta()

            ptitsa_rect = QRectF(tsentr_x - 16, tsentr_y - 16, 32, 32)
            rect_verh = verh.boundingRect().translated(verh.pos())
            rect_niz = niz.boundingRect().translated(niz.pos())

            if ptitsa_rect.intersects(rect_verh) or ptitsa_rect.intersects(rect_niz):
                self.konets_igry()
                return

            if verh.x() + self.SHIRINA_TRUBY < 0:
                self.scena.removeItem(verh)
                self.scena.removeItem(niz)
                udalit_truby.append((verh, niz))

        for para in udalit_truby:
            self.truby.remove(para)

    def konets_igry(self):
        if self.SCHET > 0:
            zarabotano = self.SCHET // 5
            self.monety += zarabotano
            self.sohranit_monety()

            if self.imya_igroka:
                self.rekordy = self.zagruzit_rekordy()
                novaya_zapis = (self.imya_igroka, self.SCHET)

                est_li = any(imya == self.imya_igroka and ochki == self.SCHET for imya, ochki in self.rekordy)

                if not est_li:
                    self.rekordy.append(novaya_zapis)
                    self.rekordy.sort(key=lambda x: x[1], reverse=True)
                    self.rekordy = self.rekordy[:5]
                    self.sohranit_rekordy(self.rekordy)

        self.timer_igry.stop()
        self.timer_trub.stop()
        self.pokazat_ekran_konca()

    def pokazat_ekran_konca(self):
        if hasattr(self, 'widget_konca') and self.widget_konca:
            self.nadpis_konca.setText(f"Игра окончена!\nСчёт: {self.SCHET}")
            self.widget_konca.show()
            if hasattr(self, 'knopka_nazad_v_igre'):
                self.knopka_nazad_v_igre.hide()
            return

        self.widget_konca = QWidget(self.vid)
        self.widget_konca.setGeometry(0, 0, self.width(), self.height())
        self.widget_konca.setStyleSheet("background-color: rgba(0, 0, 0, 180);")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)

        self.nadpis_konca = QLabel(f"Игра окончена!\nСчёт: {self.SCHET}")
        self.nadpis_konca.setFont(QFont(self.svoy_font, 32, QFont.Bold))
        self.nadpis_konca.setStyleSheet("color: white;")
        self.nadpis_konca.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.nadpis_konca)

        knopka_esche = self.sozdat_knopku("Повторить", razmer_fonta=24)
        knopka_esche.clicked.connect(self.zanovo)
        layout.addWidget(knopka_esche)

        knopka_menyu = self.sozdat_knopku("Меню", razmer_fonta=24)
        knopka_menyu.clicked.connect(self.pokazat_glavnoe_menyu)
        layout.addWidget(knopka_menyu)

        self.widget_konca.setLayout(layout)
        self.widget_konca.show()

        if hasattr(self, 'knopka_nazad_v_igre'):
            self.knopka_nazad_v_igre.hide()

    def zanovo(self):
        if hasattr(self, 'widget_konca') and self.widget_konca:
            self.widget_konca.hide()
        self.pokazat_igru()

    def ochistit_igru(self):
        if self.fon_muzika:
            self.fon_muzika.pause()
            self.fon_muzika.setPosition(0)
        if hasattr(self, 'knopka_nazad_v_igre'):
            self.knopka_nazad_v_igre.hide()
        if hasattr(self, 'widget_konca') and self.widget_konca:
            self.widget_konca.hide()

    def nachat_igru(self):
        self.pokazat_igru()

    def nazhat_dalee(self):
        imya = self.pole_imya.text().strip()
        if imya:
            self.imya_igroka = imya
            self.pokazat_glavnoe_menyu()

    def obnovit_skiny(self):
        nazvanie = self.skiny[self.indeks_skina]
        self.otobrazhenie_skina.setText(nazvanie)

    def predydushiy_skin(self):
        self.zvuk_knopki.play()
        self.indeks_skina = (self.indeks_skina - 1) % len(self.skiny)
        self.obnovit_skiny()

    def sleduyushiy_skin(self):
        self.zvuk_knopki.play()
        self.indeks_skina = (self.indeks_skina + 1) % len(self.skiny)
        self.obnovit_skiny()

    def vyiti(self):
        self.zvuk_knopki.play()
        QApplication.quit()

    def ustanovit_fon(self):
        palitra = QPalette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#ffafcc"))
        gradient.setColorAt(1, QColor("#bde0fe"))
        palitra.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palitra)

    def resizeEvent(self, event):
        self.ustanovit_fon()
        super().resizeEvent(event)

    def keyPressEvent(self, event):
        if self.widget_igra.isVisible():
            if event.key() == Qt.Key_Space:
                self.skorost_ptitsy = self.SILA_PRYZHKA
                self.zvuk_knopki.play()
            elif event.key() == Qt.Key_Escape:
                self.pokazat_glavnoe_menyu()
        else:
            super().keyPressEvent(event)

    def zagruzit_rekordy(self):
        zapisi = []
        if os.path.exists("leaderboard.txt"):
            with open("leaderboard.txt", "r", encoding="utf-8") as f:
                for stroka in f:
                    stroka = stroka.strip()
                    if stroka:
                        try:
                            imya, ochki = stroka.rsplit(" — ", 1)
                            zapisi.append((imya, int(ochki)))
                        except ValueError:
                            continue
        zapisi.sort(key=lambda x: x[1], reverse=True)
        return zapisi[:5]

    def sohranit_rekordy(self, zapisi):
        with open("leaderboard.txt", "w", encoding="utf-8") as f:
            for imya, ochki in zapisi:
                f.write(f"{imya} — {ochki}\n")

    def zagruzit_monety(self):
        if os.path.exists("user.txt"):
            try:
                with open("user.txt", "r") as f:
                    return int(f.read().strip())
            except ValueError:
                return 0
        return 0

    def sohranit_monety(self):
        with open("user.txt", "w") as f:
            f.write(str(self.monety))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    okno = GlavnoeMenyu()
    okno.show()
    sys.exit(app.exec_())