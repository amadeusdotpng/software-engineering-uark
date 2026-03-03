import sys
from PySide6 import QtCore, QtWidgets, QtGui

class CountdownWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # set label to default to 30
        self.label = QtWidgets.QLabel("30")
        self.layout = QtWidgets.QVBoxLayout(self) # create window 

        # sets text color, size, and background color
        self.label.setStyleSheet("color: white; font-size: 48pt")
        self.setStyleSheet("background-color: black;")     

        # put label in center 
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)

        # update widget and window size 
        self.layout.addWidget(self.label)
        self.resize(100, 100)

        # set starting count
        self.countdown = 30
        
        # create timer
        self.timer = QtCore.QTimer(self)
        
        # every 1s (1000ms) the function update_time is called to reduce countdown variable
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time() # this call starts it instantly idk y 

    def update_time(self):
        # update label with new countdown 
        self.label.setText(str(self.countdown))

        # reduce countdown 
        self.countdown = self.countdown - 1

        # close when countdown reaches 0 
        if self.countdown < -1:
            self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CountdownWindow()
    window.show()
    sys.exit(app.exec())
