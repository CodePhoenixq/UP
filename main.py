import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QDesktopWidget
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QFont, QFontDatabase, QPalette, QColor, QLinearGradient, QBrush
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.click_sound = None
        self.current_skin_index = 0
        self.coins = 50
        self.skins = ["Скин 1", "Скин 2", "Скин 3"]
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
        central_widget.setLayout(self.main_layout)

        self.create_main_menu()
        self.create_shop_screen()
        self.create_leaderboard_screen()

        self.main_layout.addWidget(self.main_menu_widget)
        self.main_layout.addWidget(self.shop_widget)
        self.main_layout.addWidget(self.leaderboard_widget)

        self.show_main_menu()
        self.set_back()

    def create_button(self, text, font_size=24, padding=15, width=None, height=None):
        button = QPushButton(text)
        style = f"""
            QPushButton {{
                background-color: rgba(255, 105, 180, 0.3);
                color: white;
                border: 2px solid #ff69b4;
                border-radius: 15px;
                padding: {padding}px;
                font-size: {font_size}px;
                font-family: "{self.custom_font}";
                text-shadow: 0 0 8px #ff69b4;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 105, 180, 0.6);
                border: 2px solid #ff1493;
            }}
        """
        button.setStyleSheet(style)
        if width and height:
            button.setFixedSize(width, height)
        return button

    def create_main_menu(self):
        self.main_menu_widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(30)

        title = QLabel("FLAPPY BIRD")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont(self.custom_font, 48, QFont.Bold))
        title.setStyleSheet("""
            color: #ff00ff;
            text-shadow: 0 0 10px #ff00ff, 0 0 20px #ff00ff;
        """)
        layout.addWidget(title)

        buttons = [
            ("Играть", self.start_game),
            ("Магазин", self.show_shop),
            ("Таблица рекордов", self.show_leaderboard),
            ("Выход", self.on_exit_click)
        ]

        for text, handler in buttons:
            button = self.create_button(text)
            button.clicked.connect(handler)
            layout.addWidget(button)

        self.main_menu_widget.setLayout(layout)

    def create_shop_screen(self):
        self.shop_widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        top_bar = QHBoxLayout()
        back_btn = self.create_button("Вернуться", font_size=18, padding=10)
        back_btn.clicked.connect(self.show_main_menu)

        coins_label = QLabel(f"Монеты: {self.coins}")
        coins_label.setFont(QFont(self.custom_font, 18))
        coins_label.setStyleSheet("color: yellow; font-weight: bold;")

        top_bar.addWidget(back_btn)
        top_bar.addStretch()
        top_bar.addWidget(coins_label)
        layout.addLayout(top_bar)

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
        layout.addWidget(self.skin_display)

        nav_layout = QHBoxLayout()
        prev_btn = self.create_button("◀", font_size=32, padding=10, width=80, height=80)
        next_btn = self.create_button("▶", font_size=32, padding=10, width=80, height=80)

        prev_btn.clicked.connect(self.prev_skin)
        next_btn.clicked.connect(self.next_skin)

        nav_layout.addWidget(prev_btn)
        nav_layout.addSpacing(20)
        nav_layout.addWidget(next_btn)
        layout.addLayout(nav_layout)

        labels_layout = QHBoxLayout()
        for text in ["Смена скина\nназад", "Смена скина\nвперед"]:
            label = QLabel(text)
            label.setAlignment(Qt.AlignCenter)
            label.setFont(QFont(self.custom_font, 12))
            labels_layout.addWidget(label)
        layout.addLayout(labels_layout)

        self.shop_widget.setLayout(layout)

    def create_leaderboard_screen(self):
        self.leaderboard_widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        title = QLabel("ТАБЛИЦА РЕКОРДОВ")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont(self.custom_font, 36, QFont.Bold))
        title.setStyleSheet("""
            color: #ff00ff;
            text-shadow: 0 0 10px #ff00ff, 0 0 20px #ff00ff;
        """)
        layout.addWidget(title)

        scores = [
            "Александр — 42",
            "Вика — 665",
            "Олег — 21",
            "Сосунок — 3",
            "с? — 41"
        ]

        for score in scores:
            label = QLabel(score)
            label.setAlignment(Qt.AlignCenter)
            label.setFont(QFont(self.custom_font, 20))
            label.setStyleSheet("color: white; background-color: rgba(255, 105, 180, 0.2); padding: 10px; border-radius: 10px;")
            layout.addWidget(label)

        back_btn = self.create_button("Назад")
        back_btn.clicked.connect(self.show_main_menu)
        layout.addWidget(back_btn)

        self.leaderboard_widget.setLayout(layout)

    def show_main_menu(self):
        self.clck.play()
        self.main_menu_widget.setVisible(True)
        self.shop_widget.setVisible(False)
        self.leaderboard_widget.setVisible(False)

    def show_shop(self):
        self.clck.play()
        self.main_menu_widget.setVisible(False)
        self.shop_widget.setVisible(True)
        self.leaderboard_widget.setVisible(False)
        self.update_skin_display()

    def show_leaderboard(self):
        self.clck.play()
        self.main_menu_widget.setVisible(False)
        self.shop_widget.setVisible(False)
        self.leaderboard_widget.setVisible(True)

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

    def start_game(self):
        print("Запуск игры...")

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainMenu()
    window.show()
    sys.exit(app.exec_())