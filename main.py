import sys

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget, QMessageBox
from PyQt5.Qt import QAbstractItemView
import sqlite3
from mainForm import Ui_MainWindow
from addEditCoffeeForm import Ui_Form


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # uic.loadUi('main.ui', self)  # Загружаем дизайн
        self.setupUi(self)
        self.connection = None

        self.addentry.setText('Новая запись / редактирование')
        self.addentry.clicked.connect(self.open_add_form)
        self.load_data()

    def open_add_form(self):
        self.second_form = SecondForm(self)
        self.second_form.show()

    def load_data(self):
        self.connection = sqlite3.connect("data/coffee.sqlite")
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

        self.tableWidget.setColumnWidth(0, 25)
        self.tableWidget.setColumnWidth(2, 120)
        self.tableWidget.setColumnWidth(3, 120)
        self.tableWidget.setColumnWidth(4, 480)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)


class SecondForm(QWidget, Ui_Form):
    def __init__(self, *args):
        super().__init__()
        # uic.loadUi('addEditCoffeeForm.ui', self)
        self.setupUi(self)
        self.add_button.clicked.connect(self.add_coffee)
        self.edit_button.clicked.connect(self.edit_coffee)
        self.show_id.clicked.connect(self.load_current)
        self.connection = None
        self.default_load()

    def error_msg(self, msg_text):
        msg = QMessageBox()
        msg.setWindowTitle("Ошибка")
        msg.setText(msg_text)
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()

    def sucsess_msg(self, msg_text):
        msg = QMessageBox()
        msg.setWindowTitle("Успех")
        msg.setText(msg_text)
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def add_coffee(self):
        self.connection = sqlite3.connect("data/coffee.sqlite")
        data = []
        try:
            data.append(self.lineEdit_1.text())
            data.append(self.lineEdit_2.text())
            data.append(self.lineEdit_3.text())
            data.append(self.lineEdit_4.text())
            data.append(int(self.lineEdit_5.text()))
            data.append(int(self.lineEdit_6.text()))
        except Exception:
            data.clear()
            self.error_msg("Некорректные данные")
        query = "INSERT INTO coffee (name_of_the_variety, degree_of_roasting, ground_in_grains, taste, price, volume)  VALUES (?, ?, ?, ?, ?, ?)"

        if data:
            self.connection.cursor().execute(query, data)
            self.connection.commit()
            ####################
            self.lineEdit_1.setText('')
            self.lineEdit_2.setText('')
            self.lineEdit_3.setText('')
            self.lineEdit_4.setText('')
            self.lineEdit_5.setText('')
            self.lineEdit_6.setText('')
            ###############
            ex.load_data()
            self.sucsess_msg("Данные успешно добавлены")
        self.connection.close()

    def default_load(self):
        self.connection = sqlite3.connect("data/coffee.sqlite")
        query1 = f"SELECT * FROM coffee"
        load = self.connection.cursor().execute(query1).fetchone()
        # print(load)
        self.lineEdit_e_id.setText(str(load[0]))
        self.lineEdit_e_1.setText(load[1])
        self.lineEdit_e_2.setText(load[2])
        self.lineEdit_e_3.setText(load[3])
        self.lineEdit_e_4.setText(load[4])
        self.lineEdit_e_5.setText(str(load[5]))
        self.lineEdit_e_6.setText(str(load[6]))

    def load_current(self):
        self.connection = sqlite3.connect("data/coffee.sqlite")
        id = self.lineEdit_e_id.text()
        query = f"SELECT * FROM coffee WHERE ID=={str(id)}"
        load = []
        try:
            load = self.connection.cursor().execute(query).fetchone()
            # print(load)
        except Exception:
            self.error_msg("ошибка ввода ID")
        if load:
            self.lineEdit_e_1.setText(load[1])
            self.lineEdit_e_2.setText(load[2])
            self.lineEdit_e_3.setText(load[3])
            self.lineEdit_e_4.setText(load[4])
            self.lineEdit_e_5.setText(str(load[5]))
            self.lineEdit_e_6.setText(str(load[6]))

        else:
            self.lineEdit_e_1.setText('')
            self.lineEdit_e_2.setText('')
            self.lineEdit_e_3.setText('')
            self.lineEdit_e_4.setText('')
            self.lineEdit_e_5.setText('')
            self.lineEdit_e_6.setText('')
            self.error_msg("запись в указанным ID не найдена")

    def edit_coffee(self):
        self.connection = sqlite3.connect("data/coffee.sqlite")
        id = self.lineEdit_e_id.text()
        data = []
        try:
            data.append(self.lineEdit_e_1.text())
            data.append(self.lineEdit_e_2.text())
            data.append(self.lineEdit_e_3.text())
            data.append(self.lineEdit_e_4.text())
            data.append(int(self.lineEdit_e_5.text()))
            data.append(int(self.lineEdit_e_6.text()))

            query = f"""UPDATE coffee SET name_of_the_variety = '{data[0]}',
                                   degree_of_roasting = '{data[1]}',
                                   ground_in_grains = '{data[2]}',
                                   taste = '{data[3]}',
                                   price = {data[4]},
                                   volume={data[5]}
                                   WHERE ID=={int(id)}"""
            self.connection.cursor().execute(query)
            self.connection.commit()
            ex.load_data()
            self.sucsess_msg('данные успешно изменены')

        except Exception:
            self.error_msg('что-то пошло не так. попроверьте корректность введенных данных')
            data.clear()
        self.connection.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
