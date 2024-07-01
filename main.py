import sys
from PyQt5.QtWidgets import *
from login import Ui_MainWindow
from lib_gui import lib_gui_MainWindow
import psycopg2
from psycopg2 import Error

class LoginWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.login)


    def connect_bd(self, username, password):
        try:
            conn = psycopg2.connect(
                dbname='kr1',
                user=username,
                password=password,
                host='localhost'
            )

            return conn
        except psycopg2.Error:
            QMessageBox.warning(self, 'Ошибка!', 'Не удалось подключится к БД.')
            return None

    def aut_user(self, conn, username):
        if conn is None:
            return None

        values = ('lib1', 'rea1', 'adm1')

        cursor = conn.cursor()
        for value in values:
            cursor.execute(
                f"SELECT rolname FROM pg_roles WHERE pg_has_role(rolname, '{value}', 'member') and rolname = '{username}';")
            result = cursor.fetchone()
            if result is not None:
                role = value
                break
        cursor.close()
        return role

    def login(self):
        username = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()

        conn = self.connect_bd(username, password)
        role = self.aut_user(conn, username)
        if conn is not None:
            if role == 'lib1' or role == 'rea1' or role == 'adm1':
                self.act_win = lib_gui_Window(conn, self)
                self.act_win.show()
                self.hide()
            else:
                QMessageBox.warning(self, 'Ошибка!', 'Такой роли не существует.')
        else:
            QMessageBox.warning(self, 'Ошибка!', 'Неверный логин или пароль.')

class lib_gui_Window(QMainWindow):
    def __init__(self, conn, parent=None):
        super().__init__(parent)
        self.lib_gui_ui = lib_gui_MainWindow()
        self.lib_gui_ui.setupUi(self)

        self.conn = conn

        self.lib_gui_ui.comboBox.textActivated.connect(self.onActivated)
        self.masks_for_tables = [["Авторы", "author"],
                                 ["Жанры", "genre"],
                                 ["Библиотекари", "librarian"],
                                 ["Литература", "literature"],
                                 ["Движение книг", "literature_movement"],
                                 ["Пени", "penalties"],
                                 ["Издательство", "publishing_house"],
                                 ["Читатели", "reader"]]
        self.setCombo()

        self.lib_gui_ui.pushButton_and_or_2.clicked.connect(lambda: self.change_button(self.lib_gui_ui.pushButton_and_or_2))
        self.lib_gui_ui.pushButton_and_or_3.clicked.connect(lambda: self.change_button(self.lib_gui_ui.pushButton_and_or_3))
        self.lib_gui_ui.pushButton_and_or_4.clicked.connect(lambda: self.change_button(self.lib_gui_ui.pushButton_and_or_4))
        self.lib_gui_ui.pushButton_and_or_5.clicked.connect(lambda: self.change_button(self.lib_gui_ui.pushButton_and_or_5))
        self.lib_gui_ui.pushButton_and_or_6.clicked.connect(lambda: self.change_button(self.lib_gui_ui.pushButton_and_or_6))
        self.lib_gui_ui.pushButton_and_or_7.clicked.connect(lambda: self.change_button(self.lib_gui_ui.pushButton_and_or_7))
        self.lib_gui_ui.pushButton_and_or_8.clicked.connect(lambda: self.change_button(self.lib_gui_ui.pushButton_and_or_8))
        self.lib_gui_ui.pushButton_and_or_9.clicked.connect(lambda: self.change_button(self.lib_gui_ui.pushButton_and_or_9))

        self.Button_and_or = ([self.lib_gui_ui.pushButton_and_or_2,
                               self.lib_gui_ui.pushButton_and_or_3,
                               self.lib_gui_ui.pushButton_and_or_4,
                               self.lib_gui_ui.pushButton_and_or_5,
                               self.lib_gui_ui.pushButton_and_or_6,
                               self.lib_gui_ui.pushButton_and_or_7,
                               self.lib_gui_ui.pushButton_and_or_8,
                               self.lib_gui_ui.pushButton_and_or_9])

        self.textEdit = [self.lib_gui_ui.textEdit_1,
                         self.lib_gui_ui.textEdit_2,
                         self.lib_gui_ui.textEdit_3,
                         self.lib_gui_ui.textEdit_4,
                         self.lib_gui_ui.textEdit_5,
                         self.lib_gui_ui.textEdit_6,
                         self.lib_gui_ui.textEdit_7,
                         self.lib_gui_ui.textEdit_8,
                         self.lib_gui_ui.textEdit_9]


        self.textBrowser = [self.lib_gui_ui.textBrowser_1,
                            self.lib_gui_ui.textBrowser_2,
                            self.lib_gui_ui.textBrowser_3,
                            self.lib_gui_ui.textBrowser_4,
                            self.lib_gui_ui.textBrowser_5,
                            self.lib_gui_ui.textBrowser_6,
                            self.lib_gui_ui.textBrowser_7,
                            self.lib_gui_ui.textBrowser_8,
                            self.lib_gui_ui.textBrowser_9]

        self.lib_gui_ui.pushButton_filter.clicked.connect(self.filter_table)
        self.lib_gui_ui.pushButton_add.clicked.connect(self.add_table)
        self.lib_gui_ui.pushButton_delete.clicked.connect(self.delete_table)
        self.lib_gui_ui.pushButton_update.clicked.connect(self.update_table)

    def change_button(self, button):
        if button.text() == "AND":
            button.setText("OR")
        elif button.text() == "OR":
            button.setText("")
        else:
            button.setText("AND")

    def do_show(self, element):
        element.show()

    def do_hide(self, element):
        element.hide()

    def setCombo(self):
        for i in range(len(self.masks_for_tables)):
            self.lib_gui_ui.comboBox.addItem(self.masks_for_tables[i][0])

    def onActivated(self):
        text = self.lib_gui_ui.comboBox.currentText()
        for i in range(len(self.masks_for_tables)):
            if text == self.masks_for_tables[i][0]:
                self.table_n = i
                self.lib_gui_ui.tableWidget.setSortingEnabled(False)
                self.show_table()
                self.lib_gui_ui.tableWidget.setSortingEnabled(True)

    def show_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"SAVEPOINT SP1")
            sql_colum_name = (
                f"SELECT column_name FROM information_schema.columns WHERE table_name = '{self.masks_for_tables[self.table_n][1]}' ORDER BY ordinal_position;")
            cursor.execute(sql_colum_name)
            colum_name = cursor.fetchall()

            if self.table_n == 0:
                row_labels = ["id", "Фамилия", "Имя", "Отчество", "Дата рождения"]
            elif self.table_n == 1:
                row_labels = ["id", "Жанр"]
            elif self.table_n == 2:
                row_labels = ["id", "Фамилия", "Имя", "Отчество", "Дата рождения", "Телефон"]
            elif self.table_n == 3:
                row_labels = ["id", "Название", "Жанр", "Автор", "Издательство", "Дата печати", "Возраст", "Стоимость"]
            elif self.table_n == 4:
                row_labels = ["id", "Библиотекарь", "Читатель", "Литература", "Дата выдачи",
                            "Дата предполагаемого возврата", "Дата фактического возврата"]
            elif self.table_n == 5:
                row_labels = ["id", "Читатель", "Библиотекарь", "Движение книги", "Сумма", "Основание", "Статус оплаты"]
            elif self.table_n == 6:
                row_labels = ["id", "Название", "Адресс", "Телефон", "Электронная почта"]
            elif self.table_n == 7:
                row_labels = ["id", "Фамилия", "Имя", "Отчество", "Дата рождения", "Дата регистрации", "Алресс", "Телефон",
                            "Пасспорт"]

            for i in range(len(row_labels)):
                self.textBrowser[i].setText(row_labels[i])

            self.lib_gui_ui.tableWidget.setColumnCount(len(colum_name))
            self.lib_gui_ui.tableWidget.setHorizontalHeaderLabels(row_labels)

            for i in range(len(self.Button_and_or)):
                self.do_hide(self.Button_and_or[i])
            for i in range(len(colum_name) - 1):
                self.do_show(self.Button_and_or[i])

            for i in range(len(self.textEdit)):
               self.do_hide(self.textEdit[i])
            for i in range(len(colum_name)):
                self.do_show(self.textEdit[i])

            for i in range(len(self.textBrowser)):
                self.do_hide(self.textBrowser[i])
            for i in range(len(colum_name)):
                self.do_show(self.textBrowser[i])

            cursor = self.conn.cursor()

            cursor.execute(f"select * from current_user")
            username = cursor.fetchall()
            if  str(username)[3:6] == 'rea' and (self.masks_for_tables[self.table_n][1] == 'literature_movement'
                                                or self.masks_for_tables[self.table_n][1] == 'reader'
                                                or self.masks_for_tables[self.table_n][1] == 'penalties'):

                cursor.execute(f"SELECT * FROM " + self.masks_for_tables[self.table_n][1] + " where rea_id = '" + str(username)[6:-4] + "'")
            else:
                cursor.execute(f"SELECT * FROM " + self.masks_for_tables[self.table_n][1])
            bib = cursor.fetchall()

            self.lib_gui_ui.tableWidget.setRowCount(len(bib))
            for i in range(len(bib)):
                for j in range(len(colum_name)):
                    self.lib_gui_ui.tableWidget.setItem(i, j, QTableWidgetItem(str(bib[i][j])))

            self.lib_gui_ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

            cursor.execute(f"RELEASE SAVEPOINT SP1")

        except(Exception, Error) as error:
            QMessageBox.warning(self, 'Ошибка!', str(error))
            cursor.execute(f"ROLLBACK TO SAVEPOINT SP1")

    def filter_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"SAVEPOINT SP1")
            sql_colum_name = (
                f"SELECT column_name FROM information_schema.columns WHERE table_name = '{self.masks_for_tables[self.table_n][1]}' ORDER BY ordinal_position;")
            cursor.execute(sql_colum_name)
            colum_name = cursor.fetchall()

            sql = (f"SELECT * FROM " + self.masks_for_tables[self.table_n][1] + " WHERE (")
            for i in range(len(colum_name)):
                if self.textEdit[i].toPlainText():
                    if self.Button_and_or[i - 1].text() != '':
                        sql = sql + " " + self.Button_and_or[i - 1].text() + " "
                    sql = sql + colum_name[i][0] + " = '" + str(self.textEdit[i].toPlainText()) + "'"

            sql = sql.replace(';', '')
            sql = sql + "');"

            cursor.execute(sql)
            filter_result = cursor.fetchall()

            self.lib_gui_ui.tableWidget.setRowCount(len(filter_result))
            for i in range(len(filter_result)):
                for j in range(len(colum_name)):
                    self.lib_gui_ui.tableWidget.setItem(i, j, QTableWidgetItem(str(filter_result[i][j])))
            self.lib_gui_ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

            cursor.execute(f"RELEASE SAVEPOINT SP1")

        except(Exception, Error) as error:
            QMessageBox.warning(self, 'Ошибка!', str(error))
            cursor.execute(f"ROLLBACK TO SAVEPOINT SP1")

    def add_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"SAVEPOINT SP1")
            sql = (f"INSERT INTO  " + self.masks_for_tables[self.table_n][1] + " VALUES ('")

            if self.lib_gui_ui.textEdit_1.toPlainText():
                sql = sql + self.lib_gui_ui.textEdit_1.toPlainText()
            if self.lib_gui_ui.textEdit_2.toPlainText():
                sql = sql  + "', '" + self.lib_gui_ui.textEdit_2.toPlainText()
            if self.lib_gui_ui.textEdit_3.isVisible() and self.lib_gui_ui.textEdit_3.toPlainText():
                sql = sql  + "', '" + self.lib_gui_ui.textEdit_3.toPlainText()
            if self.lib_gui_ui.textEdit_4.isVisible() and self.lib_gui_ui.textEdit_4.toPlainText():
                sql = sql  + "', '" + self.lib_gui_ui.textEdit_4.toPlainText()
            if self.lib_gui_ui.textEdit_5.isVisible() and self.lib_gui_ui.textEdit_5.toPlainText():
                sql = sql  + "', '" + self.lib_gui_ui.textEdit_5.toPlainText()
            if self.lib_gui_ui.textEdit_6.isVisible() and self.lib_gui_ui.textEdit_6.toPlainText():
                sql = sql  + "', '" + self.lib_gui_ui.textEdit_6.toPlainText()
            if self.lib_gui_ui.textEdit_7.isVisible() and self.lib_gui_ui.textEdit_7.toPlainText():
                sql = sql  + "', '" + self.lib_gui_ui.textEdit_7.toPlainText()
            if self.lib_gui_ui.textEdit_8.isVisible() and self.lib_gui_ui.textEdit_8.toPlainText():
                sql = sql  + "', '" + self.lib_gui_ui.textEdit_8.toPlainText()
            if self.lib_gui_ui.textEdit_9.isVisible() and self.lib_gui_ui.textEdit_9.toPlainText():
                sql = sql  + "', '" + self.lib_gui_ui.textEdit_9.toPlainText()

            sql = sql.replace(';', '')
            sql = sql + "');"

            cursor.execute(sql)
            self.conn.commit()

            cursor.execute(f"RELEASE SAVEPOINT SP1")

        except(Exception, Error) as error:
            QMessageBox.warning(self, 'Ошибка!', str(error))
            cursor.execute(f"ROLLBACK TO SAVEPOINT SP1")

    def delete_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"SAVEPOINT SP1")
            sql_colum_name = (
                f"SELECT column_name FROM information_schema.columns WHERE table_name = '{self.masks_for_tables[self.table_n][1]}' ORDER BY ordinal_position;")
            cursor.execute(sql_colum_name)
            colum_name = cursor.fetchall()

            sql = (f"DELETE FROM " + self.masks_for_tables[self.table_n][1] + " WHERE (")

            if self.lib_gui_ui.textEdit_1.toPlainText():
                sql = sql + str(colum_name[0])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_1.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_2.toPlainText():
                if self.lib_gui_ui.textEdit_1.toPlainText():
                    sql = sql + " " + str(self.lib_gui_ui.pushButton_and_or_2.text()) + " "
                sql = sql + str(colum_name[1])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_2.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_3.toPlainText():
                if self.lib_gui_ui.textEdit_2.toPlainText():
                    sql = sql + " " + str(self.lib_gui_ui.pushButton_and_or_3.text()) + " "
                sql = sql + str(colum_name[2])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_3.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_4.toPlainText():
                if self.lib_gui_ui.textEdit_3.toPlainText():
                    sql = sql + " " + str(self.lib_gui_ui.pushButton_and_or_4.text()) + " "
                sql = sql + str(colum_name[3])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_4.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_5.toPlainText():
                if self.lib_gui_ui.textEdit_4.toPlainText():
                    sql = sql + " " + str(self.lib_gui_ui.pushButton_and_or_5.text()) + " "
                sql = sql + str(colum_name[4])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_5.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_6.toPlainText():
                if self.lib_gui_ui.textEdit_5.toPlainText():
                    sql = sql + " " + str(self.lib_gui_ui.pushButton_and_or_6.text()) + " "
                sql = sql + str(colum_name[5])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_6.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_7.toPlainText():
                if self.lib_gui_ui.textEdit_6.toPlainText():
                    sql = sql + " " + str(self.lib_gui_ui.pushButton_and_or_7.text()) + " "
                sql = sql + str(colum_name[6])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_7.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_8.toPlainText():
                if self.lib_gui_ui.textEdit_7.toPlainText():
                    sql = sql + " " + str(self.lib_gui_ui.pushButton_and_or_8.text()) + " "
                sql = sql + str(colum_name[7])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_8.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_9.toPlainText():
                if self.lib_gui_ui.textEdit_8.toPlainText():
                    sql = sql + " " + str(self.lib_gui_ui.pushButton_and_or_9.text()) + " "
                sql = sql + str(colum_name[8])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_9.toPlainText()) + "'"

            sql = sql.replace(';', '')
            sql = sql + "');"

            cursor.execute(sql)

            cursor.execute(f"RELEASE SAVEPOINT SP1")

        except(Exception, Error) as error:
            QMessageBox.warning(self, 'Ошибка!', str(error))
            cursor.execute(f"ROLLBACK TO SAVEPOINT SP1")

    def update_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"SAVEPOINT SP1")
            sql_colum_name = (
                f"SELECT column_name FROM information_schema.columns WHERE table_name = '{self.masks_for_tables[self.table_n][1]}' ORDER BY ordinal_position;")
            cursor.execute(sql_colum_name)
            colum_name = cursor.fetchall()

            sql = (f"UPDATE " + self.masks_for_tables[self.table_n][1] + " SET ")

            if self.lib_gui_ui.textEdit_1.toPlainText():
                sql = sql + str(colum_name[0])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_1.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_2.toPlainText():
                if self.lib_gui_ui.textEdit_1.toPlainText():
                    sql = sql + ", "
                sql = sql + str(colum_name[1])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_2.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_3.toPlainText():
                if self.lib_gui_ui.textEdit_2.toPlainText():
                    sql = sql + ", "
                sql = sql + str(colum_name[2])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_3.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_4.toPlainText():
                if self.lib_gui_ui.textEdit_3.toPlainText():
                    sql = sql + ", "
                sql = sql + str(colum_name[3])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_4.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_5.toPlainText():
                if self.lib_gui_ui.textEdit_4.toPlainText():
                    sql = sql + ", "
                sql = sql + str(colum_name[4])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_5.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_6.toPlainText():
                if self.lib_gui_ui.textEdit_5.toPlainText():
                    sql = sql + ", "
                sql = sql + str(colum_name[5])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_6.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_7.toPlainText():
                if self.lib_gui_ui.textEdit_6.toPlainText():
                    sql = sql + ", "
                sql = sql + str(colum_name[6])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_7.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_8.toPlainText():
                if self.lib_gui_ui.textEdit_7.toPlainText():
                    sql = sql + ", "
                sql = sql + str(colum_name[7])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_8.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_9.toPlainText():
                if self.lib_gui_ui.textEdit_8.toPlainText():
                    sql = sql + ", "
                sql = sql + str(colum_name[8])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_9.toPlainText()) + "'"

            sql = sql + " WHERE (" + str(colum_name[0])[2:-3] + " = '" + (self.lib_gui_ui.tableWidget.item(self.lib_gui_ui.tableWidget.currentRow(), 0).text())

            sql = sql.replace(';', '')
            sql = sql + "');"

            cursor.execute(sql)

            cursor.execute(f"RELEASE SAVEPOINT SP1")

        except(Exception, Error) as error:
            QMessageBox.warning(self, 'Ошибка!', str(error))
            cursor.execute(f"ROLLBACK TO SAVEPOINT SP1")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
