import sys
import random
import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QDesktopWidget, QLineEdit, QGraphicsView, QGraphicsScene, QGraphicsTextItem
from PyQt5.QtCore import Qt, QUrl, QTimer, QRectF
from PyQt5.QtGui import QFont, QFontDatabase, QPalette, QColor, QLinearGradient, QBrush, QPainter, QPen
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.player_name = None
        self.current_skin_index = 0
        self.coins = self.load_coins()
        self.skins = ["Скин 1", "Скин 2", "Скин 3"]
        self.bg_music = None
        self.clck = None
        self.leaderboard_records = self.load_leaderboard()
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

        self.bg_music = QMediaPlayer()
        self.bg_music.setMedia(QMediaContent(QUrl.fromLocalFile("mat/mus/muslo.mp3")))
        self.bg_music.setVolume(20)
        self.bg_music.mediaStatusChanged.connect(self.on_media_status_changed)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setSpacing(30)
        central_widget.setLayout(self.main_layout)

        self.create_name_screen()
        self.create_main_menu()
        self.create_shop_screen()
        self.create_leaderboard_screen()
        self.create_game_screen()

        self.main_layout.addWidget(self.name_widget)
        self.main_layout.addWidget(self.main_menu_widget)
        self.main_layout.addWidget(self.shop_widget)
        self.main_layout.addWidget(self.leaderboard_widget)
        self.main_layout.addWidget(self.game_widget)

        self.show_name_screen()
        self.set_back()

    def on_media_status_changed(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.bg_music.setPosition(0)
            self.bg_music.play()

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

    def create_name_screen(self):
        self.name_widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(30)

        title = QLabel("ВВЕДИТЕ ИМЯ")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont(self.custom_font, 48, QFont.Bold))
        title.setStyleSheet("""
            color: #ff00ff;
            text-shadow: 0 0 10px #ff00ff, 0 0 20px #ff00ff;
        """)
        layout.addWidget(title)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Ваше имя")
        self.name_input.setAlignment(Qt.AlignCenter)
        self.name_input.setFont(QFont(self.custom_font, 24))
        self.name_input.setStyleSheet("""
            padding: 15px;
            border: 2px solid #ff69b4;
            border-radius: 15px;
            background-color: rgba(255, 255, 255, 0.2);
            color: white;
        """)
        self.name_input.setMaxLength(15)
        layout.addWidget(self.name_input)

        continue_btn = self.create_button("Продолжить")
        continue_btn.clicked.connect(self.on_continue_name)
        layout.addWidget(continue_btn)

        self.name_widget.setLayout(layout)

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
        coins_label.setObjectName("coins_label")
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

        self.leaderboard_content = QWidget()
        self.leaderboard_content_layout = QVBoxLayout()
        self.leaderboard_content_layout.setAlignment(Qt.AlignCenter)
        self.leaderboard_content.setLayout(self.leaderboard_content_layout)
        layout.addWidget(self.leaderboard_content)

        back_btn = self.create_button("Назад")
        back_btn.clicked.connect(self.show_main_menu)
        layout.addWidget(back_btn)

        self.leaderboard_widget.setLayout(layout)
        self.update_leaderboard_display()

    def update_leaderboard_display(self):
        # Очистка старых записей
        while self.leaderboard_content_layout.count():
            child = self.leaderboard_content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.leaderboard_records = self.load_leaderboard()

        if not self.leaderboard_records:
            no_records = QLabel("Нет рекордов")
            no_records.setAlignment(Qt.AlignCenter)
            no_records.setFont(QFont(self.custom_font, 20))
            no_records.setStyleSheet("color: white;")
            self.leaderboard_content_layout.addWidget(no_records)
        else:
            for name, score in self.leaderboard_records:
                label = QLabel(f"{name} — {score}")
                label.setAlignment(Qt.AlignCenter)
                label.setFont(QFont(self.custom_font, 20))
                label.setStyleSheet("color: white; background-color: rgba(255, 105, 180, 0.2); padding: 10px; border-radius: 10px;")
                self.leaderboard_content_layout.addWidget(label)

    def create_game_screen(self):
        self.game_widget = QWidget()
        self.game_widget.setFocusPolicy(Qt.StrongFocus)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setStyleSheet("background: transparent; border: none;")
        self.view.setRenderHint(QPainter.Antialiasing)

        layout.addWidget(self.view)
        self.game_widget.setLayout(layout)

    def show_name_screen(self):
        self.name_widget.setVisible(True)
        self.main_menu_widget.setVisible(False)
        self.shop_widget.setVisible(False)
        self.leaderboard_widget.setVisible(False)
        self.game_widget.setVisible(False)

    def show_main_menu(self):
        self.clck.play()
        self.cleanup_game_ui()
        self.name_widget.setVisible(False)
        self.main_menu_widget.setVisible(True)
        self.shop_widget.setVisible(False)
        self.leaderboard_widget.setVisible(False)
        self.game_widget.setVisible(False)
        self.update_leaderboard_display()

    def show_shop(self):
        self.clck.play()
        self.name_widget.setVisible(False)
        self.main_menu_widget.setVisible(False)
        self.shop_widget.setVisible(True)
        self.leaderboard_widget.setVisible(False)
        self.game_widget.setVisible(False)
        self.update_skin_display()
        coins_label = self.shop_widget.findChild(QLabel, "coins_label")
        if coins_label:
            coins_label.setText(f"Монеты: {self.coins}")

    def show_leaderboard(self):
        self.clck.play()
        self.name_widget.setVisible(False)
        self.main_menu_widget.setVisible(False)
        self.shop_widget.setVisible(False)
        self.leaderboard_widget.setVisible(True)
        self.game_widget.setVisible(False)

    def show_game(self):
        self.clck.play()
        self.name_widget.setVisible(False)
        self.main_menu_widget.setVisible(False)
        self.shop_widget.setVisible(False)
        self.leaderboard_widget.setVisible(False)
        self.game_widget.setVisible(True)
        self.init_game()

    def update_score_position(self):
        if hasattr(self, 'score_text'):
            w = self.scene.width()
            text_rect = self.score_text.boundingRect()
            self.score_text.setPos(w - text_rect.width() - 20, 20)

    def init_game(self):
        self.scene.clear()
        w, h = self.width(), self.height()
        self.view.setFixedSize(w, h)
        self.scene.setSceneRect(0, 0, w, h)

        self.GRAVITY = 0.6
        self.JUMP_STRENGTH = -7
        self.PIPE_SPEED = 3
        self.PIPE_WIDTH = 52
        self.GAP_HEIGHT = 20
        self.TOP_MARGIN = 60
        self.SCORE = 0

        self.bird_radius = 16
        pen = QPen(QColor("white"), 3)
        brush = QBrush(QColor("#ff69b4"))
        self.bird = self.scene.addEllipse(0, 0, self.bird_radius * 2, self.bird_radius * 2, pen=pen, brush=brush)
        self.bird.setPos(100, h // 2)

        self.bird_velocity = 0
        self.pipes = []

        font = QFont(self.custom_font, 28, QFont.Bold)
        self.score_text = self.scene.addText("0", font)
        self.score_text.setDefaultTextColor(QColor("white"))
        self.score_text.setZValue(100)
        self.update_score_position()

        self.back_button_game = self.create_button("Назад", font_size=16, padding=6, width=90, height=35)
        self.back_button_game.clicked.connect(self.show_main_menu)
        self.back_button_game.setParent(self.view)
        self.back_button_game.move(20, 20)
        self.back_button_game.show()

        self.pipe_timer = QTimer()
        self.pipe_timer.timeout.connect(self.spawn_pipe)
        self.pipe_timer.start(2800)

        self.game_timer = QTimer()
        self.game_timer.timeout.connect(self.update_game)
        self.game_timer.start(30)

        self.game_widget.setFocus()
        self.game_widget.setFocusPolicy(Qt.StrongFocus)
        self.game_widget.setFocus(Qt.OtherFocusReason)
        self.activateWindow()

        if self.bg_music:
            self.bg_music.play()

    def spawn_pipe(self):
        h = self.scene.height()
        if h <= self.TOP_MARGIN + self.GAP_HEIGHT:
            return

        MIN_GAP_HEIGHT = self.bird_radius * 3

        actual_gap_height = max(self.GAP_HEIGHT, MIN_GAP_HEIGHT)

        min_gap_top = self.TOP_MARGIN + 40
        max_gap_top = int(h - actual_gap_height - 20)

        if max_gap_top <= min_gap_top:
            gap_top = min_gap_top
        else:
            gap_top = random.randint(min_gap_top, max_gap_top)

        gap_bottom = gap_top + actual_gap_height

        pipe_color = QColor("#ff69b4")
        pipe_pen = QPen(pipe_color, 2)
        pipe_brush = QBrush(pipe_color)

        top_pipe = self.scene.addRect(0, 0, self.PIPE_WIDTH, gap_top, pen=pipe_pen, brush=pipe_brush)
        bottom_pipe = self.scene.addRect(0, gap_bottom, self.PIPE_WIDTH, h - gap_bottom, pen=pipe_pen, brush=pipe_brush)

        top_pipe.setPos(self.scene.width(), 0)
        bottom_pipe.setPos(self.scene.width(), gap_bottom)

        top_pipe.setData(0, False)
        self.pipes.append((top_pipe, bottom_pipe))

    def update_game(self):
        if not self.game_widget.isVisible():
            return

        self.bird_velocity += self.GRAVITY
        self.bird.moveBy(0, self.bird_velocity)

        bird_center_x = self.bird.x() + self.bird_radius
        bird_center_y = self.bird.y() + self.bird_radius
        scene_h = self.scene.height()

        if bird_center_y - self.bird_radius <= 0 or bird_center_y + self.bird_radius >= scene_h:
            self.game_over()
            return

        pipes_to_remove = []
        for top_pipe, bottom_pipe in self.pipes:
            top_pipe.moveBy(-self.PIPE_SPEED, 0)
            bottom_pipe.moveBy(-self.PIPE_SPEED, 0)

            if not top_pipe.data(0) and (top_pipe.x() + self.PIPE_WIDTH < bird_center_x):
                top_pipe.setData(0, True)
                self.SCORE += 1
                self.score_text.setPlainText(str(self.SCORE))
                self.update_score_position()

            bird_rect = QRectF(bird_center_x - self.bird_radius, bird_center_y - self.bird_radius,
                               self.bird_radius * 2, self.bird_radius * 2)
            top_rect = top_pipe.boundingRect().translated(top_pipe.pos())
            bottom_rect = bottom_pipe.boundingRect().translated(bottom_pipe.pos())

            if bird_rect.intersects(top_rect) or bird_rect.intersects(bottom_rect):
                self.game_over()
                return

            if top_pipe.x() + self.PIPE_WIDTH < 0:
                self.scene.removeItem(top_pipe)
                self.scene.removeItem(bottom_pipe)
                pipes_to_remove.append((top_pipe, bottom_pipe))

        for pipe_pair in pipes_to_remove:
            self.pipes.remove(pipe_pair)

    def game_over(self):
        if self.SCORE > 0:
            earned_coins = self.SCORE // 5
            self.coins += earned_coins
            self.save_coins()

            if self.player_name:
                self.leaderboard_records = self.load_leaderboard()
                new_record = (self.player_name, self.SCORE)

                exists = any(name == self.player_name and score == self.SCORE for name, score in self.leaderboard_records)

                if not exists:
                    self.leaderboard_records.append(new_record)
                    self.leaderboard_records.sort(key=lambda x: x[1], reverse=True)
                    self.leaderboard_records = self.leaderboard_records[:5]
                    self.save_leaderboard(self.leaderboard_records)

        self.game_timer.stop()
        self.pipe_timer.stop()
        self.show_game_over_screen()

    def show_game_over_screen(self):
        if hasattr(self, 'game_over_widget') and self.game_over_widget:
            self.game_over_widget.show()
            return

        self.game_over_widget = QWidget(self.view)
        self.game_over_widget.setGeometry(0, 0, self.width(), self.height())
        self.game_over_widget.setStyleSheet("background-color: rgba(0, 0, 0, 180);")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)

        label = QLabel(f"Игра окончена!\nСчёт: {self.SCORE}")
        label.setFont(QFont(self.custom_font, 32, QFont.Bold))
        label.setStyleSheet("color: white;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        retry_btn = self.create_button("Повторить", font_size=24)
        retry_btn.clicked.connect(self.restart_game)
        layout.addWidget(retry_btn)

        back_btn = self.create_button("Меню", font_size=24)
        back_btn.clicked.connect(self.show_main_menu)
        layout.addWidget(back_btn)

        self.game_over_widget.setLayout(layout)
        self.game_over_widget.show()

        if hasattr(self, 'back_button_game'):
            self.back_button_game.hide()

    def restart_game(self):
        if hasattr(self, 'game_over_widget') and self.game_over_widget:
            self.game_over_widget.hide()
        self.show_game()

    def cleanup_game_ui(self):
        if self.bg_music:
            self.bg_music.pause()
            self.bg_music.setPosition(0)
        if hasattr(self, 'back_button_game'):
            self.back_button_game.hide()
        if hasattr(self, 'game_over_widget') and self.game_over_widget:
            self.game_over_widget.hide()

    def start_game(self):
        self.show_game()

    def on_continue_name(self):
        name = self.name_input.text().strip()
        if name:
            self.player_name = name
            self.show_main_menu()

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

    def keyPressEvent(self, event):
        if self.game_widget.isVisible():
            if event.key() == Qt.Key_Space:
                self.bird_velocity = self.JUMP_STRENGTH
                self.clck.play()
            elif event.key() == Qt.Key_Escape:
                self.show_main_menu()
        else:
            super().keyPressEvent(event)

    def load_leaderboard(self):
        records = []
        if os.path.exists("leaderboard.txt"):
            with open("leaderboard.txt", "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            name, score = line.rsplit(" — ", 1)
                            records.append((name, int(score)))
                        except ValueError:
                            continue
        records.sort(key=lambda x: x[1], reverse=True)
        return records[:5]

    def save_leaderboard(self, records):
        with open("leaderboard.txt", "w", encoding="utf-8") as f:
            for name, score in records:
                f.write(f"{name} — {score}\n")

    def load_coins(self):
        if os.path.exists("user.txt"):
            try:
                with open("user.txt", "r") as f:
                    return int(f.read().strip())
            except ValueError:
                return 0
        return 0

    def save_coins(self):
        with open("user.txt", "w") as f:
            f.write(str(self.coins))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainMenu()
    window.show()
    sys.exit(app.exec_())