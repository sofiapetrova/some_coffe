import sys

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)  # Загружаем дизайн
        self.connection = []
        self.load_data()

    def load_data(self):
        self.connection = sqlite3.connect("coffee.sqlite")
        query = f"""SELECT * FROM coffee"""
        res = self.connection.cursor().execute(query).fetchall()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(
            ['ID', 'Название сорта', 'Степень обжарки', 'Молотый/в зернах', 'Описание вкуса', 'Цена',
             'Объем упаковки'])
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
