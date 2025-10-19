import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QLabel, QDesktopWidget
)
from PyQt5.QtCore import Qt

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
        layout.setSpacing(20)

        title = QLabel("Flappy Bird")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold;")
        layout.addWidget(title)

        play_btn = QPushButton("Играть")
        shop_btn = QPushButton("Магазин")
        leaderboard_btn = QPushButton("Таблица рекордов")
        exit_btn = QPushButton("Выход")

        for btn in [play_btn, shop_btn, leaderboard_btn, exit_btn]:
            btn.setFixedSize(250, 50)
            layout.addWidget(btn, alignment=Qt.AlignCenter)

        # заглушки
        play_btn.clicked.connect(self.start_game)
        shop_btn.clicked.connect(self.open_shop)
        leaderboard_btn.clicked.connect(self.show_leaderboard)
        exit_btn.clicked.connect(QApplication.quit)

        central_widget.setLayout(layout)

    def start_game(self):
        print("Игра запущена")

    def open_shop(self):
        print("Открыт магазин")

    def show_leaderboard(self):
        print("Показана таблица рекордов")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainMenu()
    window.show()
    sys.exit(app.exec_())