import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QDesktopWidget
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QFont, QFontDatabase, QPalette, QColor, QLinearGradient, QBrush, QPixmap, QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.click_sound = None
        self.current_skin_index = 0
        self.coins = 50  # от болды пока
        self.skins = ["Скин 1", "Скин 2", "Скин 3"]  # тож самое
        self.is_shop_visible = False
        self.init_ui()

    def init_ui(self):
        screen = QDesktopWidget().screenGeometry()
        screen_width = screen.width()
        screen_height = screen.height()

        window_width = int(screen_width * 0.6)
        window_height = int(screen_height * 0.7)
        self.setFixedSize(window_width, window_height)

        self.move(
            (screen_width - window_width) // 2,
            (screen_height - window_height) // 2
        )
        self.setWindowTitle("Flappy Bird")

        font_path = "mat/f/Comfortaa.ttf"
        font_id = QFontDatabase.addApplicationFont(font_path)
        self.custom_font = QFontDatabase.applicationFontFamilies(font_id)[0]

        self.clck = QMediaPlayer()
        self.clck.setMedia(QMediaContent(QUrl.fromLocalFile("mat/s/hump.mp3")))
        self.clck.setVolume(50)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setSpacing(30)

        self.title = QLabel("FLAPPY BIRD")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont(self.custom_font, 48, QFont.Bold))
        self.title.setStyleSheet("""
            color: #ff00ff;
            text-shadow: 0 0 10px #ff00ff, 0 0 20px #ff00ff;
        """)
        self.main_layout.addWidget(self.title)

        button_style = f"""
            QPushButton {{
                background-color: rgba(255, 105, 180, 0.3);
                color: white;
                border: 2px solid #ff69b4;
                border-radius: 15px;
                padding: 15px;
                font-size: 24px;
                font-family: "{self.custom_font}";
                text-shadow: 0 0 8px #ff69b4;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 105, 180, 0.6);
                border: 2px solid #ff1493;
            }}
        """

        self.play_btn = QPushButton("Играть")
        self.shop_btn = QPushButton("Магазин")
        self.leaderboard_btn = QPushButton("Таблица рекордов")
        self.exit_btn = QPushButton("Выход")

        for btn in [self.play_btn, self.shop_btn, self.leaderboard_btn, self.exit_btn]:
            btn.setStyleSheet(button_style)
            self.main_layout.addWidget(btn)

        self.shop_layout = QVBoxLayout()
        self.shop_layout.setAlignment(Qt.AlignCenter)
        self.shop_layout.setSpacing(20)

        top_bar = QHBoxLayout()
        back_btn = QPushButton("Вернуться")
        coins_label = QLabel(f"Монеты: {self.coins}")
        coins_label.setFont(QFont(self.custom_font, 18))
        coins_label.setStyleSheet("color: yellow; font-weight: bold;")
        back_btn.setStyleSheet(button_style.replace("font-size: 24px;", "font-size: 18px;"))
        coins_label.setStyleSheet("color: yellow; font-weight: bold;")

        back_btn.clicked.connect(self.hide_shop)
        top_bar.addWidget(back_btn)
        top_bar.addStretch()
        top_bar.addWidget(coins_label)
        self.shop_layout.addLayout(top_bar)

        self.skin_display = QLabel("СКИН")
        self.skin_display.setAlignment(Qt.AlignCenter)
        self.skin_display.setFont(QFont(self.custom_font, 48, QFont.Bold))
        self.skin_display.setStyleSheet("""
            background-color: #dcdcdc;
            border: 2px solid #888;
            border-radius: 100px;
            padding: 50px;
            color: black;
        """)
        self.shop_layout.addWidget(self.skin_display)


        # как вариант, седлать через фигуры, но тоже хз
        nav_layout = QHBoxLayout()
        prev_btn = QPushButton("◀")
        next_btn = QPushButton("▶")
        prev_btn.setStyleSheet(button_style.replace("font-size: 24px;", "font-size: 32px;"))
        next_btn.setStyleSheet(button_style.replace("font-size: 24px;", "font-size: 32px;"))
        prev_btn.setFixedSize(80, 80)
        next_btn.setFixedSize(80, 80)

        prev_btn.clicked.connect(self.prev_skin)
        next_btn.clicked.connect(self.next_skin)

        nav_layout.addWidget(prev_btn)
        nav_layout.addSpacing(20)
        nav_layout.addWidget(next_btn)
        self.shop_layout.addLayout(nav_layout)

        labels_layout = QHBoxLayout()
        prev_label = QLabel("Смена скина\nназад")
        next_label = QLabel("Смена скина\nвперед")
        prev_label.setAlignment(Qt.AlignCenter)
        next_label.setAlignment(Qt.AlignCenter)
        prev_label.setFont(QFont(self.custom_font, 12))
        next_label.setFont(QFont(self.custom_font, 12))
        labels_layout.addWidget(prev_label)
        labels_layout.addWidget(next_label)
        self.shop_layout.addLayout(labels_layout)

        #магазик
        self.main_layout.addLayout(self.shop_layout)
        self.shop_layout.setParent(None)
        self.central_widget = central_widget
        self.central_widget.setLayout(self.main_layout)
        self.set_back()

        self.play_btn.clicked.connect(self.on_button_click)
        self.shop_btn.clicked.connect(self.show_shop)
        self.leaderboard_btn.clicked.connect(self.on_button_click)
        self.exit_btn.clicked.connect(self.on_exit_click)

    def show_shop(self):
        self.clck.play()
        self.is_shop_visible = True
        self.main_layout.removeWidget(self.title)
        self.main_layout.removeWidget(self.play_btn)
        self.main_layout.removeWidget(self.shop_btn)
        self.main_layout.removeWidget(self.leaderboard_btn)
        self.main_layout.removeWidget(self.exit_btn)
        self.main_layout.insertLayout(0, self.shop_layout)
        self.update_skin_display()

    def hide_shop(self):
        self.clck.play()
        self.is_shop_visible = False
        self.main_layout.removeItem(self.shop_layout)
        self.main_layout.insertWidget(0, self.title)
        self.main_layout.insertWidget(1, self.play_btn)
        self.main_layout.insertWidget(2, self.shop_btn)
        self.main_layout.insertWidget(3, self.leaderboard_btn)
        self.main_layout.insertWidget(4, self.exit_btn)

    def update_skin_display(self):
        current_skin_name = self.skins[self.current_skin_index]
        self.skin_display.setText(current_skin_name)

    def prev_skin(self):
        self.clck.play()
        self.current_skin_index = (self.current_skin_index - 1) % len(self.skins)
        self.update_skin_display()

    def next_skin(self):
        self.clck.play()
        self.current_skin_index = (self.current_skin_index + 1) % len(self.skins)
        self.update_skin_display()

    def on_button_click(self):
        self.clck.play()
        sender = self.sender()
        if sender.text() == "Играть":
            self.start_game()
        elif sender.text() == "Таблица рекордов":
            self.show_leaderboard()

    def on_exit_click(self):
        self.clck.play()
        QApplication.quit()

    def set_back(self):
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#ffafcc"))
        gradient.setColorAt(1, QColor("#bde0fe"))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

    def resizeEvent(self, event):
        self.set_back()
        super().resizeEvent(event)

    def start_game(self):
        print("Запуск игры...")

    def show_leaderboard(self):
        print("Показ таблицы рекордов...")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainMenu()
    window.show()
    sys.exit(app.exec_())