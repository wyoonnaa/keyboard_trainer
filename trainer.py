# лучшая версия
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QLineEdit, QLabel, QGridLayout, QPushButton, QWidget, \
    QApplication, QMessageBox
from PyQt6.QtCore import QUrl, QTimer, Qt
from PyQt6.QtGui import QTextCursor, QTextCharFormat, QFont, QColor
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
import random
import os
import time
import src.globals as globals


class GameStatistics(QDialog):
    def __init__(self, stats, parent=None):
        super(GameStatistics, self).__init__(parent)
        self.setWindowTitle("Статистика игры")
        self.stats = stats
        layout = QVBoxLayout(self)
        statistics_label = QLabel(f"Тут будет статистика: {self.stats}")
        layout.addWidget(statistics_label)
        self.setLayout(layout)


class VirtualKeyboard(QWidget):
    def __init__(self, input_widget, parent=None):
        super(VirtualKeyboard, self).__init__(parent)
        self.input_widget = input_widget
        self._initUI()
        self.music_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.music_player.setAudioOutput(self.audio_output)
        sound_file = QUrl.fromLocalFile("src/gui/resources/keyb.mp3")
        self.music_player.setSource(sound_file)

    def _createButtonMap(self):
        self.qtKeyMap = {}
        flatten_board = [key for row in self.keyBoard for key in row]

        for key in flatten_board:
            if key == ' ':
                qt_key_enum = Qt.Key.Key_Space
            else:
                qt_key_enum = getattr(Qt, 'Key_{}'.format(key.upper()), Qt.Key.Key_Space)
            self.qtKeyMap[qt_key_enum] = key

    def _initUI(self):
        self.generalLayout = QVBoxLayout(self)
        self._createButtons()

    def _createButtons(self):
        self.keyBoard = [
            ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
            ["a", "s", "d", "f", "g", "h", "j", "k", "l"],
            ["z", "x", "c", "v", "b", "n", "m", ".", ",", "?", "!", ],
            [" "]
        ]
        self._createButtonMap()
        self.buttonsLayout = QGridLayout()
        self.buttonMap = {}
        for row_index, row in enumerate(self.keyBoard):
            for col_index, key in enumerate(row):
                button = QPushButton(key.upper())
                button.setEnabled(False)
                button.setStyleSheet("background-color: lightblue;")
                self.buttonsLayout.addWidget(button, row_index, col_index)
                self.buttonMap[key.upper()] = button
        self.generalLayout.addLayout(self.buttonsLayout)

    def play_key_sound(self):
        if not self.music_player.source().isEmpty():
            self.music_player.stop()
        self.music_player.play()

    def highlight_key(self, key, color):
        button = self.buttonMap.get(key.upper())
        if button:
            button.setStyleSheet(f"background-color: {color};")
            QTimer.singleShot(500, lambda: button.setStyleSheet("background-color: lightblue;"))


class TypingTest(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_word_index = 0
        self.typo = 0
        self.init_ui()
        # Таймер
        self.timer = QTimer()
        self.start_time = 0
        self.elapsed_time = 0
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

    def init_ui(self):
        self.setWindowTitle("Тренажёр печати")
        layout = QVBoxLayout(self)

        self.text_to_type = QTextEdit()
        self.text_to_type.setReadOnly(True)
        self.text_to_type.setFont(QFont("Arial", 32))
        layout.addWidget(self.text_to_type)

        self.user_input = QLineEdit()
        self.user_input.setFont(QFont("Arial", 32))
        layout.addWidget(self.user_input)

        self.timer_label = QLabel("Time elapsed: 0 seconds")
        layout.addWidget(self.timer_label)
        self.typo_count_label = QLabel("Typo count: 0")
        layout.addWidget(self.typo_count_label)

        keyboard = VirtualKeyboard(self.user_input, self)
        self.keyboard = keyboard
        layout.addWidget(keyboard)

        self.user_input.textChanged.connect(self.check_typing)

        self.setLayout(layout)
        self.load_text()

    def update_timer(self):
        self.elapsed_time += 1
        self.timer_label.setText(f"Time elapsed: {self.elapsed_time} seconds")

    def set_training_text(self, text):
        self.words = text.split()
        self.text_to_type.setPlainText(text)
        self.highlight_current_word()

    def highlight_current_word(self):
        cursor = QTextCursor(self.text_to_type.document())
        cursor.movePosition(QTextCursor.MoveOperation.Start)
        format = QTextCharFormat()
        format.setBackground(QColor("lightgreen"))

        for i, word in enumerate(self.words):
            if i == self.current_word_index:
                cursor.movePosition(QTextCursor.MoveOperation.EndOfWord, QTextCursor.MoveMode.KeepAnchor)
                cursor.setCharFormat(format)
                break
            cursor.movePosition(QTextCursor.MoveOperation.EndOfWord)
            cursor.movePosition(QTextCursor.MoveOperation.NextWord)

    def check_typing(self):
        user_text = self.user_input.text()
        original_text = self.text_to_type.toPlainText()
        cursor_position = len(user_text)

        if cursor_position <= len(original_text):
            expected_char = original_text[cursor_position - 1] if cursor_position > 0 else ''
            input_char = user_text[-1] if user_text else ''

            if input_char == expected_char:
                color = "lightgreen"
            else:
                color = "pink"
                self.typo += 1
                self.typo_count_label.setText(f"Typo count: {self.typo}")

            self.keyboard.play_key_sound()
            self.keyboard.highlight_key(input_char, color)

            if user_text == original_text:
                self.timer.stop()
                elapsed_time = self.elapsed_time

                self.user_input.setStyleSheet(f"background-color: lightgreen;")
                QMessageBox.information(self, "Поздравления", f"Вы ввели весь текст за {elapsed_time} секунд! Совершили {self.typo} ошиб-ку/ок")
                self.save_statistics(elapsed_time, self.typo, original_text)
                # os.system(f'open src/stat/stats_{globals.user_nickname}.txt')
                self.close()
            else:
                self.user_input.setStyleSheet("background-color: white;")
        else:
            self.user_input.setStyleSheet("background-color: white;")

    def load_text(self):
        lines = []
        paths = ["src/texts/text.txt", f"src/texts/text_{globals.user_nickname}.txt"]
        for path in paths:
            try:
                with open(path, "r", encoding="utf-8") as file:
                    lines += file.read().splitlines()
            except FileNotFoundError:
                continue

        if lines:
            random_line = random.choice(lines).strip()
            self.set_training_text(random_line)
            print(f"Random line: {random_line}")
            self.start_time = time.time()
            self.elapsed_time = 0
        else:
            self.set_training_text("Ошибка: файл не найден или пустой.")

    def save_statistics(self, elapsed_time, typo_count, text_line):
        stats_file_path = f"src/stat/stats_{globals.user_nickname}.txt"
        with open(stats_file_path, 'a', encoding='utf-8') as f:
            f.write(f"\n--- Новая запись ---\n")
            f.write(f"Строка для ввода: {text_line}\n")
            f.write(f"Время: {elapsed_time} секунд\n")
            f.write(f"Количество опечаток: {typo_count}\n")


def main():
    app = QApplication([])
    window = TypingTest()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
