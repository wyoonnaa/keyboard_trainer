import os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QDialog, QScrollArea, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit
import src.globals as globals
from src.globals import user_nickname
from src.trainer import TypingTest
from src.trainer import max_elapsed_time_easy, max_elapsed_time_hard

class MainWidget(QWidget):

    def __init__(self,  parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):


        self.setFixedSize(600, 400)
        layout = QVBoxLayout(self)
        layout.addStretch(1)

        difficulty_btn_easy = QPushButton("    Легкий режим    ", self)
        difficulty_btn_easy.setFixedSize(600, 200)
        difficulty_btn_easy.clicked.connect(lambda: self.start_training('easy'))
        layout.addWidget(difficulty_btn_easy, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch(2)

        font = QFont("Arial", 14, QFont.Weight.Bold)
        greeting_label = QLabel(f"\n Ваша статистика в легком режиме: \n лучшее время {max_elapsed_time_easy} \n", self)
        greeting_label.setFont(font)
        greeting_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(greeting_label)
        layout.addStretch(1)

        difficulty_btn_hard = QPushButton("     Сложный режим     ", self)
        difficulty_btn_hard.setFixedSize(600, 200)
        difficulty_btn_hard.clicked.connect(lambda: self.start_training('easy'))
        layout.addWidget(difficulty_btn_hard, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch(2)

        font = QFont("Arial", 14, QFont.Weight.Bold)
        greeting_label = QLabel(f"\n  Ваша статистика в сложном режиме: \n лучшее время {max_elapsed_time_hard} \n", self)
        greeting_label.setFont(font)
        greeting_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(greeting_label)
        layout.addStretch(1)

        stat = QPushButton(" Посмотреть всю статистику ", self)
        stat.setFixedSize(600, 200)
        stat.clicked.connect(self.stat)
        layout.addWidget(stat, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch(2)

        add_text_btn = QPushButton("      Добавить свой текст      ", self)
        add_text_btn.setFixedSize(600, 200)
        add_text_btn.clicked.connect(self.save_text)
        layout.addWidget(add_text_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch(2)

    def handle_typing(self):
        pass

    def start_training(self, difficulty):

        self.typing_test_dialog = TypingTest(self)
        self.setup_training(difficulty)

        # self.typing_test_dialog.show()

    def setup_training(self, difficulty):
        if difficulty == "easy":
            text = self.load_text("text.txt")
        elif difficulty == "hard":
            text = self.load_text("text.txt")

        self.typing_test_dialog.set_training_text(text)

    def load_text(self, file_name):
        try:
            with open(f"src/texts/{file_name}", "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            return "Ошибка: файл не найден."

    def save_text(self):
        if not hasattr(self, 'text_edit'):
            self.text_edit = QTextEdit(self)
            self.layout().addWidget(self.text_edit)
        text = self.text_edit.toPlainText()

        filename = f"src/texts/text_{globals.user_nickname}.txt"

        if os.path.exists(filename):
            with open(filename, 'a') as file:
                file.write(text + '\n')
        else:
            with open(filename, 'w') as file:
                file.write(text + '\n')

        self.text_edit.clear()

    def stat(self):

        print("Метод stat был вызван")
        print(globals.user_nickname)
        filename = f"src/stat/stats_{globals.user_nickname}.txt"
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                stats_data = file.read()

                dialog = QDialog()
                dialog.setWindowTitle("Статистика")
                dialog_layout = QVBoxLayout(dialog)

                scroll_area = QScrollArea()
                content_widget = QWidget()
                content_layout = QVBoxLayout(content_widget)

                font = QFont("Arial", 14, weight=QFont.Weight.Bold)
                stats_label = QLabel(stats_data)
                stats_label.setFont(font)
                content_layout.addWidget(stats_label)
                content_widget.setLayout(content_layout)

                scroll_area.setWidget(content_widget)
                dialog_layout.addWidget(scroll_area)

                close_button = QPushButton("Закрыть")
                close_button.clicked.connect(dialog.close)
                dialog_layout.addWidget(close_button)

                dialog.setLayout(dialog_layout)
                dialog.exec()


