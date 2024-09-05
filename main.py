import sys
from PyQt5 import QtWidgets, QtCore
from utilities import Listener
from gui import QtWindow

class TranscriptionApp(QtWidgets.QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.listener = Listener()
        self.window = QtWindow()
        self.window.show()

        # Timer to regularly update the label with the transcribed text
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_transcription)
        self.timer.start(1000)  # Update every second

        # Start the recording
        self.listener.start_recording()

    def update_transcription(self):
        transcribed_text = self.listener.get_transcribed_text()
        self.window.label.setText(transcribed_text)

if __name__ == '__main__':
    app = TranscriptionApp(sys.argv)
    sys.exit(app.exec_())
