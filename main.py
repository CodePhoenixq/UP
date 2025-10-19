import sys
import random
import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QDesktopWidget, QLineEdit, QGraphicsView, QGraphicsScene
from PyQt5.QtCore import Qt, QUrl, QTimer, QRectF
from PyQt5.QtGui import QFont, QFontDatabase, QPalette, QColor, QBrush, QPainter, QPen, QPixmap
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer


class Glav(QMainWindow):
    def __init__(self):
        super().__init__()
        self.imya_igroka = None
        self.indeks_skina = 0
        self.tekushiy_skin = 0
        self.kuplennye_skiny = set()
        self.skiny = [
            {"name": "Пушистик", "price": 0, "path": "mat/pl/kap.png"},
            {"name": "Глаз", "price": 50, "path": "mat/pl/eye.png"},
            {"name": "Черный кот", "price": 100, "path": "mat/pl/cat.png"},
            {"name": "Свинка", "price": 150, "path": "mat/pl/pig.png"},
            {"name": "КаĉĉΞĪа", "price": 200, "path": "mat/pl/kass.png"}
        ]
        self.fon_muzika = None
        self.zvuk_knopki = None
        self.rekordy = self.zagruzit_rekordy()
        self.zagruzit_monety()
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
            background-color: rgba(200, 200, 200, 0.5);
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

        self.label_monety = QLabel(f"Монеты: {self.monety}")
        self.label_monety.setFont(QFont(self.svoy_font, 18))
        self.label_monety.setStyleSheet("color: yellow; font-weight: bold;")

        verhniy_ryad.addWidget(knopka_nazad)
        verhniy_ryad.addStretch()
        verhniy_ryad.addWidget(self.label_monety)
        layout.addLayout(verhniy_ryad)

        skin_container = QHBoxLayout()
        skin_container.addStretch()
        self.skin_view = QGraphicsView()
        self.skin_scene = QGraphicsScene()
        self.skin_view.setScene(self.skin_scene)
        self.skin_view.setFixedSize(200, 200)
        self.skin_view.setStyleSheet("background: transparent; border: none;")
        skin_container.addWidget(self.skin_view)
        skin_container.addStretch()
        layout.addLayout(skin_container)

        self.label_skin_name = QLabel("Облик:")
        self.label_skin_name.setAlignment(Qt.AlignCenter)
        self.label_skin_name.setFont(QFont(self.svoy_font, 20))
        self.label_skin_name.setStyleSheet("color: white;")
        layout.addWidget(self.label_skin_name)

        self.label_skin_price = QLabel("Цена:")
        self.label_skin_price.setAlignment(Qt.AlignCenter)
        self.label_skin_price.setFont(QFont(self.svoy_font, 18))
        self.label_skin_price.setStyleSheet("color: yellow;")
        layout.addWidget(self.label_skin_price)

        self.knopka_kupit = self.sozdat_knopku("Применить")
        self.knopka_kupit.clicked.connect(self.kupit_tekushiy_skin)
        layout.addWidget(self.knopka_kupit)

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
        for tekst in ["Смена облика\nназад", "Смена облика\nвперед"]:
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
            nadpis.setStyleSheet("""
                color: white;
                background-color: rgba(0, 0, 0, 150);
                padding: 10px;
                border-radius: 10px;
                border: 1px solid #ff69b4;
            """)
            self.layout_rekordov.addWidget(nadpis)
        else:
            for imya, ochki in self.rekordy:
                nadpis = QLabel(f"{imya} — {ochki}")
                nadpis.setAlignment(Qt.AlignCenter)
                nadpis.setFont(QFont(self.svoy_font, 20))
                nadpis.setStyleSheet("""
                    color: white;
                    background-color: rgba(0, 0, 0, 150);
                    padding: 10px;
                    border-radius: 10px;
                    border: 1px solid #ff69b4;
                """)
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
        if self.tekushiy_skin not in self.kuplennye_skiny:
            self.tekushiy_skin = 0

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

        skin_data = self.skiny[self.tekushiy_skin]
        pixmap = QPixmap(skin_data["path"])

        if not pixmap.isNull():
            self.ptitsa = self.scena.addPixmap(pixmap)
        else:
            pero = QPen(QColor("white"), 3)
            kist = QBrush(QColor("#ff69b4"))
            self.ptitsa = self.scena.addEllipse(0, 0, 32, 32, pen=pero, brush=kist)

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
        if h <= self.OTSTUP_SVERHU + 60:
            return

        self.VYSOTA_PROREZI = random.randint(80, 200)

        min_vverhu = self.OTSTUP_SVERHU + 40
        max_vverhu = int(h - self.VYSOTA_PROREZI - 20)

        if max_vverhu <= min_vverhu:
            vverhu = min_vverhu
        else:
            vverhu = random.randint(min_vverhu, max_vverhu)

        tube_pixmap = QPixmap("mat/i/tube.png")

        vysota_verh = vverhu
        if vysota_verh < 300:
             vysota_verh = 500

        truba_verh_pix = tube_pixmap.scaled(
                int(self.SHIRINA_TRUBY),
                int(vysota_verh),
                Qt.IgnoreAspectRatio,
                Qt.SmoothTransformation
        )
        truba_verh = self.scena.addPixmap(truba_verh_pix)

        truba_verh.setPos(self.scena.width(), -30)

        vnizu = vysota_verh + self.VYSOTA_PROREZI

        vysota_niz = h - vnizu
        if vysota_niz < 300:
            vysota_niz = 500

        truba_niz_pix = tube_pixmap.scaled(
                int(self.SHIRINA_TRUBY),
                int(vysota_niz),
                Qt.IgnoreAspectRatio,
                Qt.SmoothTransformation
        )
        truba_niz = self.scena.addPixmap(truba_niz_pix)
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
        skin_data = self.skiny[self.indeks_skina]
        name = skin_data["name"]
        price = skin_data["price"]

        self.label_skin_name.setText(f"Облик: {name}")
        self.label_skin_price.setText(f"Цена: {price} монет")

        pixmap = QPixmap(skin_data["path"])
        if not pixmap.isNull():
            self.skin_scene.clear()
            item = self.skin_scene.addPixmap(pixmap)
            self.skin_scene.setSceneRect(item.boundingRect())
            self.skin_view.fitInView(item, Qt.KeepAspectRatio)

        if self.indeks_skina in self.kuplennye_skiny:
            self.knopka_kupit.setText("Применить")
            self.knopka_kupit.setEnabled(True)
        else:
            if price == 0:
                self.knopka_kupit.setText("Бесплатно")
            else:
                self.knopka_kupit.setText(f"Купить ({price})")
            self.knopka_kupit.setEnabled(self.monety >= price)

        self.label_monety.setText(f"Монеты: {self.monety}")

    def predydushiy_skin(self):
        self.zvuk_knopki.play()
        self.indeks_skina = (self.indeks_skina - 1) % len(self.skiny)
        self.obnovit_skiny()

    def sleduyushiy_skin(self):
        self.zvuk_knopki.play()
        self.indeks_skina = (self.indeks_skina + 1) % len(self.skiny)
        self.obnovit_skiny()

    def kupit_tekushiy_skin(self):
        skin_index = self.indeks_skina
        skin_data = self.skiny[skin_index]

        if skin_index in self.kuplennye_skiny:
            self.tekushiy_skin = skin_index
            self.zvuk_knopki.play()
            return

        if skin_data["price"] == 0:
            self.kuplennye_skiny.add(skin_index)
            self.tekushiy_skin = skin_index
            self.zvuk_knopki.play()
            self.obnovit_skiny()
            self.sohranit_monety()
            return

        if self.monety >= skin_data["price"]:
            self.monety -= skin_data["price"]
            self.kuplennye_skiny.add(skin_index)
            self.tekushiy_skin = skin_index
            self.zvuk_knopki.play()
            self.sohranit_monety()
            self.obnovit_skiny()

    def vyiti(self):
        self.zvuk_knopki.play()
        QApplication.quit()

    def ustanovit_fon(self):
        fon = QPixmap("mat/i/fon.jpg")
        if fon.isNull():
            fon = QPixmap(self.size())
            fon.fill(Qt.black)

        fon = fon.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        kombinirovannoe = QPixmap(self.size())
        kombinirovannoe.fill(Qt.transparent)

        painter = QPainter(kombinirovannoe)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        x = (self.width() - fon.width()) // 2
        y = (self.height() - fon.height()) // 2
        painter.drawPixmap(x, y, fon)

        scroll = QPixmap("mat/i/scroll.png")
        if not scroll.isNull():
            scroll_scaled = scroll.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            painter.drawPixmap(0, 0, scroll_scaled)

        painter.end()

        palitra = QPalette()
        palitra.setBrush(QPalette.Window, QBrush(kombinirovannoe))
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
                    lines = f.readlines()
                    self.monety = int(lines[0].strip()) if len(lines) > 0 else 0

                    if len(lines) > 1 and lines[1].strip():
                        kuplennye_str = lines[1].strip()
                        self.kuplennye_skiny = set(map(int, kuplennye_str.split(',')))
                    else:
                        self.kuplennye_skiny = set()

                    if len(lines) > 2 and lines[2].strip():
                        tekushiy = int(lines[2].strip())
                        if 0 <= tekushiy < len(self.skiny):
                            self.tekushiy_skin = tekushiy
                        else:
                            self.tekushiy_skin = 0
                    else:
                        self.tekushiy_skin = 0

                    return
            except (ValueError, IndexError, OSError):
                pass

        self.monety = 0
        self.kuplennye_skiny = set()
        self.tekushiy_skin = 0

    def sohranit_monety(self):
        with open("user.txt", "w") as f:
            f.write(str(self.monety) + "\n")
            kuplennye_str = ",".join(map(str, sorted(self.kuplennye_skiny)))
            f.write(kuplennye_str + "\n")
            f.write(str(self.tekushiy_skin) + "\n")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    okno = Glav()
    okno.show()
    sys.exit(app.exec_())