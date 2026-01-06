import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize


class ImageButtonExample(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PNG Button")
        self.resize(300, 200)

        layout = QVBoxLayout(self)

        button = QPushButton()
        button.setText("")
        button.setIcon(QIcon("Kojima.png"))  # path to your PNG
        button.setIconSize(QSize(300, 300))  # size of the image
        button.setFixedSize(400, 400)        # size of the button

        button.setStyleSheet("""
            QPushButton {
                padding: 8px;
            }
        """)

        layout.addWidget(button)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageButtonExample()
    window.show()
    sys.exit(app.exec())