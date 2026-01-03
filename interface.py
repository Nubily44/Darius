import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QPoint, QSize, QTimer

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


class MovingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smooth Move Example")
        self.setFixedSize(400, 200)

        layout = QVBoxLayout(self)

        self.button = QPushButton("Move left")
        self.button.clicked.connect(self.move_left)

        layout.addWidget(self.button)

        # Keep a reference to the animation
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(600)  # milliseconds

    def move_left(self):
        start_pos = self.pos()
        end_pos = QPoint(start_pos.x() - 100, start_pos.y())

        self.animation.stop()
        self.animation.setStartValue(start_pos)
        self.animation.setEndValue(end_pos)
        self.animation.start()

class ResizingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smooth Resize Example")
        self.resize(300, 200)  # ← allow resizing

        layout = QVBoxLayout(self)

        self.button = QPushButton("Grow")
        self.button.clicked.connect(self.resize_widget)
        layout.addWidget(self.button)

        self.animation = QPropertyAnimation(self, b"size")
        self.animation.setDuration(600)

        self.expanded = False

    def resize_widget(self):
        start_size = self.size()

        if not self.expanded:
            end_size = QSize(2560, 1)
            self.button.setText("Shrink")
        else:
            end_size = QSize(300, 200)
            self.button.setText("Grow")

        self.expanded = not self.expanded

        self.animation.stop()
        self.animation.setStartValue(start_size)
        self.animation.setEndValue(end_size)
        self.animation.start()

class DvdBounce(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DVD Bounce")
        self.resize(200, 100)

        layout = QVBoxLayout(self)
        label = QLabel("DVD")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 32px; font-weight: bold;")
        layout.addWidget(label)

        # Movement vector (pixels per tick)
        self.velocity = QPoint(3, 3)

        # Timer for animation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_position)
        self.timer.start(16)  # ~60 FPS

    def update_position(self):
        screen = QApplication.primaryScreen().availableGeometry()
        pos = self.pos()
        size = self.size()

        next_x = pos.x() + self.velocity.x()
        next_y = pos.y() + self.velocity.y()

        # Bounce horizontally
        if next_x <= screen.left() or next_x + size.width() >= screen.right():
            self.velocity.setX(-self.velocity.x())

        # Bounce vertically
        if next_y <= screen.top() or next_y + size.height() >= screen.bottom():
            self.velocity.setY(-self.velocity.y())

        self.move(pos + self.velocity)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multiple Interfaces")
        self.resize(400, 250)

        self.stack = QStackedWidget(self)

        # --- Screen 1 ---
        screen1 = QWidget()
        layout1 = QVBoxLayout(screen1)

        label1 = QLabel("This is the first screen")
        label1.setAlignment(Qt.AlignCenter)

        to_screen2 = QPushButton("Go to second screen")
        to_screen2.clicked.connect(lambda: self.stack.setCurrentIndex(1))

        layout1.addWidget(label1)
        layout1.addWidget(to_screen2)

        # --- Screen 2 ---
        screen2 = QWidget()
        layout2 = QVBoxLayout(screen2)

        label2 = QLabel("Second screen ♡")
        label2.setAlignment(Qt.AlignCenter)

        back_button = QPushButton("Back")
        back_button.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        layout2.addWidget(label2)
        layout2.addWidget(back_button)

        # Add screens to stack
        self.stack.addWidget(screen1)
        self.stack.addWidget(screen2)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.stack)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
