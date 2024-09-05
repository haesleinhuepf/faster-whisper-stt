from PyQt5 import QtWidgets, QtCore

class QtWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('GUI Text Output')
        self.showFullScreen()
        
        # Create label
        self.label = QtWidgets.QLabel('Your Text Here', self)
        self.label.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter)
        self.label.setStyleSheet("color: white; background-color: black")
        
        # Set layout
        layout = QtWidgets.QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.label)
        self.setLayout(layout)

    def set_label_text(self, text):
        self.label.setText(text)

    def update_label(self, text):
        self.label.setText(text)
