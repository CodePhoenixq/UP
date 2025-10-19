import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QDesktopWidget
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QFont, QFontDatabase, QPalette, QColor, QLinearGradient, QBrush
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.click_sound = None
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

        play_btn = QPushButton("Играть")
        shop_btn = QPushButton("Магазин")
        leaderboard_btn = QPushButton("Таблица рекордов")
        exit_btn = QPushButton("Выход")

        for btn in [play_btn, shop_btn, leaderboard_btn, exit_btn]:
            btn.setStyleSheet(button_style)
            layout.addWidget(btn)

        play_btn.clicked.connect(self.on_button_click)
        shop_btn.clicked.connect(self.on_button_click)
        leaderboard_btn.clicked.connect(self.on_button_click)
        exit_btn.clicked.connect(self.on_exit_click)

        central_widget.setLayout(layout)
        self.set_back()

    def on_button_click(self):
        self.clck.play()
        sender = self.sender()
        if sender.text() == "Играть":
            self.start_game()
        elif sender.text() == "Магазин":
            self.open_shop()
        elif sender.text() == "Таблица рекордов":
            self.show_leaderboard()

    def on_exit_click(self):
        if self.click_sound:
            self.click_sound.play()
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

    def open_shop(self):
        print("Открытие магазина...")

    def show_leaderboard(self):
        print("Показ таблицы рекордов...")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainMenu()
    window.show()
    sys.exit(app.exec_())