from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QApplication
import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        for i in range(5):
            button = QPushButton(f"Button {i}")
            self.layout.addWidget(button)

        remove_btn = QPushButton("Remove Last")
        remove_btn.clicked.connect(self.remove_last)
        self.layout.addWidget(remove_btn)

    def remove_last(self):
        # remove widget before the remove button
        index = self.layout.count() - 2

        if index >= 0:
            item = self.layout.takeAt(index)

            widget = item.widget()

            if widget:
                widget.deleteLater()


app = QApplication(sys.argv)

window = Window()
window.show()

app.exec()