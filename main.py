import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout,QPushButton, QLabel, QDesktopWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor, QLinearGradient, QBrush


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
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

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(30)

        title = QLabel("FLAPPY BIRD")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Orbitron", 48, QFont.Bold))
        title.setStyleSheet("""
            color: #ff00ff;
            text-shadow: 0 0 10px #ff00ff, 0 0 20px #ff00ff;
        """)
        layout.addWidget(title)


        #хз, сократить может
        button_style = """
            QPushButton {
                background-color: rgba(255, 105, 180, 0.3);
                color: white;
                border: 2px solid #ff69b4;
                border-radius: 15px;
                padding: 15px;
                font-size: 24px;
                font-family: 'Orbitron';
                text-shadow: 0 0 8px #ff69b4;
            }
            QPushButton:hover {
                background-color: rgba(255, 105, 180, 0.6);
                border: 2px solid #ff1493;
            }
        """

        play_btn = QPushButton("Играть")
        shop_btn = QPushButton("Магазин")
        leaderboard_btn = QPushButton("Таблица рекордов")
        exit_btn = QPushButton("Выход")

        for btn in [play_btn, shop_btn, leaderboard_btn, exit_btn]:
            btn.setStyleSheet(button_style)
            layout.addWidget(btn)

        # заглушки
        play_btn.clicked.connect(self.start_game)
        shop_btn.clicked.connect(self.open_shop)
        leaderboard_btn.clicked.connect(self.show_leaderboard)
        exit_btn.clicked.connect(QApplication.quit)

        central_widget.setLayout(layout)

        self.set_back()

    def set_back(self):
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#ffafcc"))
        gradient.setColorAt(1, QColor("#bde0fe"))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

    def start_game(self):
        print("Запуск игры...")

    def open_shop(self):
        print("Открытие магазина...")

    def show_leaderboard(self):
        print("Показ таблицы рекордов...")

    def resizeEvent(self, event):
        self.set_back()
        super().resizeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainMenu()
    window.show()
    sys.exit(app.exec_())