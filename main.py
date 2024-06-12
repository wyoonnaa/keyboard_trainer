from PyQt6.QtWidgets import QApplication
from src.main2 import WelcomeWidget


def get_style() -> str:
    with open('src/gui/resources/style.css', 'r') as file:
        return file.read()


if __name__ == '__main__':

    application = QApplication([])
    application.setApplicationName('Клавиатурный тренажёр')
    application.setStyleSheet(get_style())
    main_widget = WelcomeWidget()


    main_widget.show()
    application.exec()


