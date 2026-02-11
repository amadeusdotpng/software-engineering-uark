from PySide6 import QtWidgets, QtCore, QtGui

import sys

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.resize(720, 643)
        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World",
                                     alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.text)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def showEvent(self, event: QtGui.QShowEvent):
        super().showEvent(event)

        # show splash screen when the main window is shown
        label = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap('res/splash_screen.jpg').scaled(725, 648)
        label.setPixmap(pixmap)
        label.resize(720, 643)
        label.show()

        # close splash screen after 3 seconds
        QtCore.QTimer.singleShot(3000, label.close)
        pass

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow();
    window.show()  # IMPORTANT!!!!! Windows are hidden by default.

    sys.exit(app.exec())

