from PyQt6 import QtCore, QtWidgets
import sys, time

print(QtCore.PYQT_VERSION_STR)

class MyWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self,parent)

        self.label = QtWidgets.QLabel('Первое название')
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        self.btnQuit = QtWidgets.QPushButton('&Закрыть')
        self.btnStartTread = QtWidgets.QPushButton('Старт Потока')

        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self.label)
        self.vbox.addWidget(self.btnQuit)
        self.vbox.addWidget(self.btnStartTread)

        self.setLayout(self.vbox)

        self.newThread = QmyThread()

        self.btnQuit.clicked.connect(QtWidgets.QApplication.instance().quit)
        self.btnStartTread. connect(self.on_clicked)
        self.newThread.started.connect(self.on_started)
        self.newThread.finished.connect(self.on_finished)
        self.newThread.mysignal.connect(self.on_change,QtCore.Qt.ConnectionType.QueuedConnection)

    def on_clicked(self):
        self.btnStartTread.setDisabled(True)
        self.newThread.start()
    def on_started(self):
        self.label.setText('Запущено')
    def on_finished(self):
        self.label.setText('Завершино')
        self.btnStartTread.setDisabled(False)
    def on_change(self,s):
        self.label.setText(s)


class QmyThread(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self,parent)
    def run(self):
        for i in range(1,21):
            self.sleep(2)
            # передача данных через сигнал
            self.mysignal.emit(f'i = {i}')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.setWindowTitle('Заголовок окна')
    window.resize(300,70)
    window.show()
    sys.exit(app.exec())

