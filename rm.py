from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from random import choice
from shutil import copy
from fnmatch import fnmatch
from psutil import disk_usage
from os import walk, path


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(495, 110)
        MainWindow.setStyleSheet("background-color: rgb(60, 60, 60);\n"
                                 "font: 12pt \"Calibri\";\n"
                                 "")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.source = QtWidgets.QLineEdit(self.centralwidget)
        self.source.setStyleSheet("color: rgb(180, 180, 180); border: 1px solid rgb(40, 40, 40)")
        self.source.setGeometry(QtCore.QRect(5, 5, 400, 30))
        self.source.setText("")
        self.source.setObjectName("source")
        self.btn_source = QtWidgets.QPushButton(self.centralwidget)
        self.btn_source.setGeometry(QtCore.QRect(410, 5, 80, 30))
        self.btn_source.setStyleSheet("color: rgb(180, 180, 180);")
        self.btn_source.setObjectName("btn_source")

        self.destination = QtWidgets.QLineEdit(self.centralwidget)
        self.destination.setGeometry(QtCore.QRect(5, 40, 400, 30))
        self.destination.setStyleSheet("color: rgb(180, 180, 180); border: 1px solid rgb(40, 40, 40)")
        self.destination.setObjectName("destination")
        self.btn_destination = QtWidgets.QPushButton(self.centralwidget)
        self.btn_destination.setGeometry(QtCore.QRect(410, 40, 80, 30))
        self.btn_destination.setStyleSheet("color: rgb(180, 180, 180);")
        self.btn_destination.setObjectName("btn_destination")

        self.size = QtWidgets.QLineEdit(self.centralwidget)
        self.size.setGeometry(QtCore.QRect(5, 75, 80, 30))
        self.size.setStyleSheet("color: rgb(180, 180, 180); border: 1px solid rgb(40, 40, 40)")
        self.size.setObjectName("size")
        self.btn_ok = QtWidgets.QPushButton(self.centralwidget)
        self.btn_ok.setGeometry(QtCore.QRect(410, 75, 80, 30))
        self.btn_ok.setStyleSheet("selection-color: rgb(255, 255, 255);")
        self.btn_ok.setStyleSheet("color: rgb(180, 180, 180);")
        self.btn_ok.setObjectName("btn_ok")

        self.size2 = QtWidgets.QLabel(self.centralwidget)
        self.size2.setGeometry(QtCore.QRect(90, 75, 315, 30))
        self.size2.setStyleSheet("color: rgb(180, 180, 180);")
        self.size2.setText("")
        self.size2.setObjectName("size2")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.btn_source.clicked.connect(self.select_source)
        self.btn_destination.clicked.connect(self.select_destination)
        self.btn_ok.clicked.connect(self.copy_pack)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "randomusic"))
        self.btn_source.setText(_translate("MainWindow", "..."))
        self.btn_destination.setText(_translate("MainWindow", "..."))
        self.btn_ok.setText(_translate("MainWindow", "ok"))
        self.source.setPlaceholderText(_translate("MainWindow", "  откуда"))
        self.destination.setPlaceholderText(_translate("MainWindow", "  куда"))
        self.size.setPlaceholderText(_translate("MainWindow", "  мб"))

    def select_source(self):
        source_file = QFileDialog.getExistingDirectory()
        self.source.setText(source_file)

    def select_destination(self):
        destination_file = QFileDialog.getExistingDirectory()
        self.destination.setText(destination_file)
        if destination_file:
            DISK = destination_file[:destination_file.find('/')]  # свободное место на диске (destination)
            free = disk_usage(DISK).free / (1024 * 1024 * 1024)
            self.size2.setText(f"{free:.4} Гб свободно на диске {DISK}")

    def copy_pack(self):
        if path.isdir(self.source.text()) and path.isdir(self.destination.text()) and self.size.text().isdigit():
            file_size, file_list = 0, []
            pack_size = int(self.size.text()) * 1000000
            pattern = "*.mp3"

            for root, dirs, files in walk(self.source.text()):
                for filename in files:
                    if fnmatch(filename, pattern):
                        file_list.append(path.join(root, filename))

            while file_size < pack_size:
                if file_list == []:
                    break
                a = choice(file_list)
                file_list.remove(a)
                file_size += path.getsize(a)
                copy(a, self.destination.text())

            ok = QMessageBox()
            ok.setWindowTitle('Готово!')
            ok.setStandardButtons(QMessageBox.Cancel | QMessageBox.Retry)
            ok.setDefaultButton(QMessageBox.Cancel)

            ok.buttonClicked.connect(self.action)

            ok.exec_()

        else:
            error = QMessageBox()
            error.setWindowTitle('Ошибка')
            error.setText('Проверьте окна ввода, возможно нет такой папки\nили не введен объем')
            error.setIcon(QMessageBox.Warning)
            error.setStandardButtons(QMessageBox.Ok)

            error.exec_()

    def action(self, btn):
        if btn.text() == 'Cancel':
            self.close()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())