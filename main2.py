from src.globals import user_nickname
import src.globals as app_globals
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel
from PyQt6.QtCore import Qt
import os
from src.widget import MainWidget
from PyQt6.QtGui import QFont
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl
from src.trainer import max_elapsed_time_easy,max_elapsed_time_hard



class WelcomeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedSize(600, 400)

        self.layout = QVBoxLayout(self)

        self.layout.addStretch(1)

        font = QFont("Arial", 20, QFont.Weight.Bold)
        self.greeting_label = QLabel("Добро пожаловать в Клавиатурный тренажёр! \n", self)
        self.greeting_label.setFont(font)
        self.greeting_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.greeting_label)
        self.layout.addStretch()  # Растяжение между виджетами

        self.nickname_input = QLineEdit(self)
        self.nickname_input.setPlaceholderText("Введите ваш ник")
        self.nickname_input.setMinimumWidth(300)
        self.nickname_input.setMinimumHeight(100)
        # self.nickname_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.nickname_input)

        self.start_button = QPushButton("Начать игру", self)
        self.start_button.setFixedSize(600, 200)
        self.start_button.clicked.connect(self.start_game)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.start_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.layout.addStretch(1)

        self.music_player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.music_player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(0.025)
        self.music_player.setSource(QUrl.fromLocalFile("src/gui/resources/zico-jennie-blackpink-spot.mp3"))
        self.music_player.play()

    def start_game(self):
        app_globals.user_nickname = self.nickname_input.text()
        if app_globals.user_nickname:
            stats_file_path = f"src/stat/stats_{app_globals.user_nickname}.txt"
            with open(stats_file_path, 'w') as file:
                file.write("Статистика пользователя\n")
                file.write("\nЛегкий режим\n")
                file.write(f"лучшее время:{max_elapsed_time_easy}сек\n")
                file.write("\nСложный режим\n")
                file.write(f"лучшее время:{max_elapsed_time_hard}сек\n")
            self.main_widget = MainWidget()
            self.main_widget.show()
            self.close()
            self.music_player.stop()



class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.welcome_widget = WelcomeWidget(self)
        self.main_widget = MainWidget(self)
        self.welcome_widget.show()


if __name__ == '__main__':
    app = QApplication([])


    def get_style() -> str:
        with open('src/gui/resources/style.css', 'r') as file:
            return file.read()


    app.setApplicationName('Клавиатурный тренажёр')
    app.setStyleSheet(get_style())

    main_app = MainApp()
    app.exec()
