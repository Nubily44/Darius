import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt

class CounterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cute Counter ♡")
        self.setFixedSize(300, 200)

        # Counter variable
        self.counter = 0

        # Layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Counter display
        self.label = QLabel(str(self.counter))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 40px;")
        self.layout.addWidget(self.label)

        # Increment button
        self.increment_btn = QPushButton("Increment ♡")
        self.increment_btn.clicked.connect(self.increment)
        self.layout.addWidget(self.increment_btn)

        # Decrement button
        self.decrement_btn = QPushButton("Decrement ♡")
        self.decrement_btn.clicked.connect(self.decrement)
        self.layout.addWidget(self.decrement_btn)

        # Reset button
        self.reset_btn = QPushButton("Reset ♡")
        self.reset_btn.clicked.connect(self.reset)
        self.layout.addWidget(self.reset_btn)

    def increment(self):
        self.counter += 1
        self.update_label()

    def decrement(self):
        self.counter -= 1
        self.update_label()

    def reset(self):
        self.counter = 0
        self.update_label()

    def update_label(self):
        self.label.setText(str(self.counter))

class FlavorTextApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flavour Text Example")
        self.setFixedSize(400, 200)

        self.layout = QVBoxLayout(self)

        # Flavour text label
        self.text_label = QLabel("The wind is calm today.")
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setWordWrap(True)
        self.text_label.setStyleSheet("font-size: 16px;")

        # Button
        self.change_button = QPushButton("Change text")
        self.change_button.clicked.connect(self.change_text)

        self.layout.addWidget(self.text_label)
        self.layout.addWidget(self.change_button)

        # List of possible texts
        self.texts = [
            "The wind is calm today.",
            "Dark clouds gather on the horizon.",
            "A soft light fills the room.",
            "You feel like something is about to happen.",
            "Everything is quiet. Too quiet."
        ]

        self.current_index = 0

    def change_text(self):
        self.current_index = (self.current_index + 1) % len(self.texts)
        self.text_label.setText(self.texts[self.current_index])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FlavorTextApp()
    window.show()
    sys.exit(app.exec())
