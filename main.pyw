# ↓   MaxSl - DobermanNotepad 1.0   ↓


all_classes = []
# ↓ Функция возвращающая все алгоритмы шифрования ↓
def all_encryption_functions_to_aefpy():
    aefdir = []
    for i in os.listdir("encryption_functions"):
        if i[-3:] == ".py":
            aefdir.append(i)
    to_print_into_aef = []
    all_alg = []
    for i in aefdir:
        with open("encryption_functions/" + i, "r") as f:
            data = f.read()
            if data[-1:] == "\n":
                data = data[:-1]
            data = f"class {i[:-3]}():" + "\n    ".join(("\n" + data).split("\n"))
            to_print_into_aef.append(data)
            all_alg.append(i[:-3])
    to_print_into_aef = "\n\n\n".join(to_print_into_aef)
    to_print_into_aef += "\n\n\nall_classes = {" + ", ".join(['"' + i + '": ' + i + '' for i in all_alg]) + "}\n"
    return to_print_into_aef


from time import monotonic as monotonic

time_a = monotonic()

import sys, PyQt5
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QFileDialog, QLineEdit, QCheckBox, \
    QPushButton, QLabel, QAction, QMenu
from PyQt5.QtGui import QIcon, QFont
import os
import sqlite3

con = sqlite3.connect("programdata.sqlite")
cur = con.cursor()
time_b = monotonic()

#   ↓ Основное окно ↓
class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./ui/main.ui', self)
        self.setWindowTitle("Doberman Notepad - 1.0")
        self.setWindowIcon(QIcon("./icons/icon4.png"))
        self.nws = False
        self.saved = True
        self.parameter_names = ["Предупреждать о несохранённом файле при выходе",
                                "Предупреждать о несохранённом файле при открытии другого файла",
                                "Отображать путь к файлу на statusbar", "Отображать в заголовке окна путь к файлу"]
        self.parameter_action_refs = [self.action_settings1, self.action_settings2, self.action_settings3,
                                      self.action_settings4]
        self.parameter_action_names = ["action_settings1", "action_settings2", "self.action_settings3",
                                       "self.action_settings4"]
        self.settings = {}
        # ↓ Проверка необходимости пересоздания БД ↓
        try:
            firt_open = cur.execute("SELECT parameter_value FROM settings WHERE parameter_name = 'first_open'")
            if firt_open.fetchall()[0][0] == "True":
                print("first open!")
                self.rebuild_programdatasqlite()
        except BaseException as f:
            print("first open! With error")
            self.rebuild_programdatasqlite()
        self.update_settings()
        self.working_folder = \
        cur.execute("SELECT parameter_value FROM settings WHERE parameter_name = 'working_folder'").fetchall()[0][0]
        self.file = os.path.realpath(__file__).split(":")[0] + ":/untitled.txt"

        # ↓ Изменение позиции курсора/Изменение содержимого рабочей зоны ↓
        self.textEdit.textChanged.connect(self.text_changed)
        self.textEdit.cursorPositionChanged.connect(self.update_statusbar)


        # ↓ ↓ ↓ ↓        Привязка нажатия на кнопки на menubar        ↓ ↓ ↓ ↓

        # ↓ Файл ↓
        self.action_NewWinow.triggered.connect(lambda: os.startfile(os.path.realpath(__file__)))
        self.action_Open.triggered.connect(self.openFile)
        self.action_Save.triggered.connect(self.click_action_Save)
        self.action_SaveAs.triggered.connect(self.click_action_SaveAs)
        self.action_OpenInExplorer.triggered.connect(self.click_action_OpenInExplorer)
        self.action_Exit.triggered.connect(self.click_action_Exit)

        # ↓ Редактировать ↓
        self.action_Font.triggered.connect(self.click_action_Font)
        self.action_ResizeUp.triggered.connect(lambda: self.textEdit.zoomIn(2))
        self.action_ResizeDown.triggered.connect(lambda: self.textEdit.zoomOut(2))

        # ↓ Настройки ↓
        self.action_settings1.changed.connect(
            lambda: self.change_settings("Предупреждать о несохранённом файле при выходе",
                                         self.action_settings1.isChecked()))
        self.action_settings2.changed.connect(
            lambda: self.change_settings("Предупреждать о несохранённом файле при открытии другого файла",
                                         self.action_settings2.isChecked()))
        self.action_settings3.changed.connect(
            lambda: self.change_settings("Отображать путь к файлу на statusbar", self.action_settings3.isChecked()))
        self.action_settings4.changed.connect(
            lambda: self.change_settings("Отображать в заголовке окна путь к файлу", self.action_settings4.isChecked()))
        self.action_forgetAll.triggered.connect(self.click_action_forgetAll)

        # ↓ Шифрование ↓
        self.action_EncryptThisFile.triggered.connect(self.click_action_EncryptThisFile)
        self.action_EncryptAnotherFile.triggered.connect(self.click_action_EncryptAnotherFile)
        self.action_DecryptThisFile.triggered.connect(self.click_action_DecryptThisFile)
        self.action_DecryptAnotherFile.triggered.connect(self.click_action_DecryptAnotherFile)

        # ↓ Запустить ↓
        self.action_Python.triggered.connect(self.click_action_Python)
        self.action_Html.triggered.connect(self.click_action_Html)

        # ↓ Итоговоя настройка ↓
        self.statusbar.showMessage(f"запуск программы за: {int((monotonic() - time_a) * 1000)}ms")
        self.update_WorkingFolder()
        self.update_bookmarks()
        print(f"Импорт библеотек: {int((time_b - time_a) * 1000) / 1000}")
        print(f"Запуск программы: {int((monotonic() - time_b) * 1000) / 1000}")

    def change_settings(self, parametr_name, value):
        cur.execute(f"UPDATE settings SET parameter_value = '{value}' WHERE parameter_name='{parametr_name}'")
        con.commit()
        self.update_settings()
        if parametr_name == "Отображать в заголовке окна путь к файлу":
            self.setWindowTitle(self.WindowTitleText())

    def update_settings(self):
        for i in self.parameter_names:
            new_value = "True" == \
                        cur.execute(f'SELECT parameter_value FROM settings WHERE parameter_name = "{i}"').fetchall()[0][0]
            self.parameter_action_refs[self.parameter_names.index(i)].setChecked(new_value)
            self.settings[i] = new_value

    #   ↓ обновление statusbar ↓
    def update_statusbar(self):
        text_cursor = self.textEdit.textCursor()
        way = self.file
        if not self.nws:
            way = "файл не сохранён"
        self.statusbar.showMessage(
            f" строка {text_cursor.blockNumber()+1}, столбец {self.textEdit.textCursor().columnNumber()+1}  |  {way} ")

    #   ↓ обновление рабочей папки ↓
    def update_WorkingFolder(self):
        result = os.listdir(self.working_folder)
        self.menu_8.clear()
        action = QAction("Сменить рабочую папку", self)
        action.triggered.connect(self.ChangeWorkingFolder)
        self.menu_8.addAction(action)
        self.menu_8.addSeparator()

        for i in result:
            if "." not in i:
                continue
            file_menu = QAction(i, self)
            file_menu.triggered.connect(lambda _, file=i: self.openFile(self.working_folder + "/" + file))
            self.menu_8.addAction(file_menu)

    #   ↓ Обновление закладок ↓
    def update_bookmarks(self):
        result = cur.execute("SELECT file_path FROM files").fetchall()
        self.menu_3.clear()
        if self.file in [i[0] for i in result] and self.nws:
            action = QAction("Удалить файл из закладок", self)
        else:
            action = QAction("Добавить файл в закладки", self)
        action.triggered.connect(self.click_action_AddToBookmarks)
        self.menu_3.addAction(action)
        self.menu_3.addSeparator()
        self.menu_3.setVisible(False)

        for i in result:
            file_menu = QMenu(i[0].split("/")[-1], self)
            action = QAction("Открыть", self)
            action.triggered.connect(lambda _, file=i[0]: self.openFile(file))
            file_menu.addAction(action)
            action = QAction("Открыть в проводнике", self)
            action.triggered.connect(lambda _, file=i[0]: os.system("explorer " + "\\".join(file.split("/")[:-1])))
            file_menu.addAction(action)
            self.menu_3.addMenu(file_menu)

    def text_changed(self):
        self.saved = False
        self.setWindowTitle(self.WindowTitleText())

    def WindowTitleText(self):
        text = ""
        if not self.nws:
            return "файл не сохранён"
        elif self.settings["Отображать в заголовке окна путь к файлу"]:
            text = self.file
        else:
            text = self.file.split("/")[-1]
        if not self.saved:
            text += "*"
        return text

    #   ↓ Событие отрисовки ↓
    def paintEvent(self, event):
        self.textEdit.setLineWrapMode(int(self.action_AutomaticWordTransfer.isChecked()))
        self.textEdit.setGeometry(0, 0, self.geometry().size().width(), self.geometry().size().height() - 50)

    def openFile(self, file=None):
        if not self.saved and self.settings["Предупреждать о несохранённом файле при открытии другого файла"]:
            self.file_to_open = file
            ChangeFileWarningWidget(self).show()
            self.saved = True
        else:
            if type(file) == str:
                with open(file, "r", encoding="utf-8", errors="ignore") as f:
                    self.textEdit.setPlainText(f.read())
                    self.file = file
                    self.nws = True
                    self.saved = True
                    self.setWindowTitle(self.WindowTitleText())
                    self.update_statusbar()
                self.update_bookmarks()
            else:
                self.file_to_open = QFileDialog.getOpenFileName(
                    self, 'Выбрать файл', self.file, 'Текстовый файл (*.txt);;Все файлы (*)')[0]
                if self.file_to_open != "":
                    self.openFile(self.file_to_open)

    def click_action_Save(self):
        if not self.nws:
            self.click_action_SaveAs()
        else:
            with open(self.file, "w+", encoding="utf-8") as f:
                f.write(self.textEdit.toPlainText())
                self.saved = True
                self.setWindowTitle(self.WindowTitleText())
                self.update_statusbar()

    def click_action_SaveAs(self):
        self.file_to_save = QFileDialog.getSaveFileName(
            self, 'Сохранить как', os.path.realpath(__file__).split(":")[0] + ":/untitled.txt",
            'Все файлы (*);;Текстовый файл (*.txt);;Изображение (*.png, *.jpg)')[0]
        if self.file_to_save != "":
            with open(self.file_to_save, "w+", encoding="utf-8") as f:
                f.write(self.textEdit.toPlainText())
                self.file = self.file_to_save
                self.nws = True
                self.saved = True
                self.setWindowTitle(self.WindowTitleText())
                self.update_statusbar()
                self.update_bookmarks()

    def click_action_OpenInExplorer(self):
        os.system("explorer " + "\\".join(self.file.split("/")[:-1]))

    def click_action_Exit(self):
        if not self.saved:
            ExitWarningWidget(self).show()
        else:
            con.commit()
            sys.exit()

    def click_action_Font(self):
        font, ok_pressed = PyQt5.QtWidgets.QFontDialog.getFont()
        if ok_pressed:
            font = QFont(font.family(), 16)
            self.textEdit.setFont(font)

    def ChangeWorkingFolder(self):
        self.working_folder = QFileDialog.getExistingDirectory(self, 'Выбрать рабочую папку',
                                                               os.path.realpath(__file__).split(":")[0] + ":/")
        cur.execute(f"UPDATE settings SET parameter_value = '{self.working_folder}' "
                    f"WHERE parameter_name='working_folder'")
        self.update_WorkingFolder()

    def click_action_AddToBookmarks(self):
        if self.nws:
            if self.file not in [i[0] for i in cur.execute("SELECT file_path FROM files").fetchall()]:
                cur.execute(f"INSERT INTO files (file_path) VALUES('{self.file}')")
                con.commit()
            else:
                cur.execute("DELETE FROM files WHERE file_path = '" + self.file + "'")
                con.commit()
            self.update_bookmarks()
        else:
            pass

    def click_action_EncryptThisFile(self):
        EncryptWindow(self, self.textEdit.toPlainText().encode("utf-8"), True).show()

    def click_action_EncryptAnotherFile(self):
        with open(QFileDialog.getOpenFileName(self, 'Выбрать файл', self.file)[0], "rb") as f:
            text = f.read()
        EncryptWindow(self, text, True).show()

    def click_action_DecryptThisFile(self):
        EncryptWindow(self, self.textEdit.toPlainText().encode("utf-8"), False).show()

    def click_action_DecryptAnotherFile(self):
        with open(QFileDialog.getOpenFileName(self, 'Выбрать файл', self.file)[0], "rb") as f:
            text = f.read()
        EncryptWindow(self, text, False).show()

    def close(self):
        sys.exit()

    def save(self):
        self.click_action_Save()

    def click_action_Python(self):
        if self.nws:
            comand = 'python "' + self.file + '"'
            os.system('start cmd /c "' + comand + '"')

    def click_action_Html(self):
        if self.nws:
            os.system('start iexplore "' + self.file + '"')

    def closeEvent(self, event):
        event.ignore()
        self.click_action_Exit()

    # ↓ Пересоздание БД ↓
    def rebuild_programdatasqlite(self):
        cur.execute('CREATE TABLE IF NOT EXISTS files (file_path TEXT)')
        cur.execute("DELETE FROM files")
        cur.execute("CREATE TABLE IF NOT EXISTS files (file_path TEXT)")
        cur.execute('CREATE TABLE IF NOT EXISTS settings (parameter_name TEXT, parameter_value TEXT)')
        cur.execute("DELETE FROM settings")
        cur.execute("CREATE TABLE IF NOT EXISTS settings (parameter_name TEXT, parameter_value TEXT)")

        cur.execute(
            f"INSERT INTO settings (parameter_name, parameter_value) VALUES ('working_folder', "
            f"'{os.path.realpath(__file__).split(':')[0] + ':/'}') ")
        cur.execute("INSERT INTO settings (parameter_name, parameter_value) VALUES"
                    " ('first_open', 'False') ")
        cur.execute("INSERT INTO settings (parameter_name, parameter_value) VALUES"
                    " ('Предупреждать о несохранённом файле при выходе', 'True')")
        cur.execute("INSERT INTO settings (parameter_name, parameter_value) VALUES"
                    " ('Предупреждать о несохранённом файле при открытии другого файла', 'True')")
        cur.execute("INSERT INTO settings (parameter_name, parameter_value) VALUES"
                    " ('Отображать путь к файлу на statusbar', 'True')")
        cur.execute("INSERT INTO settings (parameter_name, parameter_value) VALUES"
                    " ('Отображать в заголовке окна путь к файлу', 'False')")
        self.update_settings()

    def click_action_forgetAll(self):
        cur.execute(f"UPDATE settings SET parameter_value = 'True' WHERE parameter_name='first_open'")
        con.commit()
        sys.exit()


#   ↓ Предупреждение о несохранённом файле перед выходом ↓
class ExitWarningWidget(QDialog):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)
        uic.loadUi('./ui/ExitWarning.ui', self)
        self.Button_Save.clicked.connect(self.click_Button_Save)
        self.Button_NoSave.clicked.connect(self.click_Button_NoSave)
        self.Button_Cancel.clicked.connect(self.click_Button_Cancel)
        self.isWarn()

    def isWarn(self):
        if not self.parent.settings["Предупреждать о несохранённом файле при выходе"]:
            self.click_Button_NoSave()

    def click_Button_Save(self):
        self.parent.save()
        self.parent.close()

    def click_Button_NoSave(self):
        self.parent.close()

    def click_Button_Cancel(self):
        self.destroy()


#   ↓ Предупреждение о несохранённом файле перед открытием другого файла ↓
class ChangeFileWarningWidget(ExitWarningWidget):
    def isWarn(self):
        pass

    def click_Button_Save(self):
        self.destroy()
        self.parent.save()
        self.parent.openFile(self.parent.file_to_open)

    def click_Button_NoSave(self):
        self.parent.saved = True
        self.destroy()
        self.parent.openFile(self.parent.file_to_open)

    def click_Button_Cancel(self):
        self.destroy()


#   ↓ Окно настроек шифрования ↓
class EncryptWindow(QDialog):
    def __init__(self, parent, text, encrypt=True):
        self.parent = parent
        super().__init__(parent)
        uic.loadUi('./ui/encrypt.ui', self)
        self.setWindowIcon(QIcon("./icons/icon.png"))

        self.text = text
        self.encrypt = encrypt
        if not self.encrypt:
            self.setWindowTitle("Окно расшифрования")

        class aef:
            exec(all_encryption_functions_to_aefpy())

        self.aef = aef
        AlgorithmTypes = [i[0] for i in self.aef.all_classes.items()]

        self.AlgorithmType.clear()
        self.AlgorithmType.addItems(AlgorithmTypes)
        self.AlgorithmType.currentIndexChanged.connect(self.change_AlgorithmType)
        self.widgets = []
        self.change_AlgorithmType(
            True)  # Вызов функции выбора алгоритма шифрования(что-бы она там всё отрисовала красиво)

        self.toThisFileButton.clicked.connect(self.click_toThisFileButton)
        self.toAnotherFileButton.clicked.connect(self.click_toAnotherFileButton)

    #   ↓ Смена алгоритма шифрования ↓
    def change_AlgorithmType(self, first=False):
        self.algorithm = self.aef.all_classes[self.AlgorithmType.currentText()]
        for widget in self.widgets:  # Удаление виджетов
            widget.setVisible(False)
        self.widgets = []
        #   ↓ Добавление виджетов ↓
        for y, widget_parameters in enumerate(self.algorithm.settings(self.algorithm)[0]):
            widget = None
            if widget_parameters[0] == "LineEdit":
                widget = QLineEdit(self)
                widget.setPlaceholderText(widget_parameters[1])
                widget.textChanged.connect(self.check_data)
            elif widget_parameters[0] == "CheckBox":
                widget = QCheckBox(self)
                widget.setText(widget_parameters[1])
                widget.stateChanged.connect(self.check_data)
            elif widget_parameters[0] == "Label":
                widget = QLabel(self)
                widget.setText(widget_parameters[1])
            elif widget_parameters[0] == "ChoiceFile":
                widget = ChoiceFileButton(self)
                widget.setText(widget_parameters[1])
                widget.clicked.connect(self.check_data)
            widget.setGeometry(10, 55 + y * 35, 345, 25)
            widget.show()
            self.widgets.append(widget)

        #   ↓ Геометрия окна настройки шифрования ↓
        space = len(self.widgets) * 35 + 20
        scaleY = space + 160
        if first == True:
            x = int(self.parent.geometry().x() + (self.parent.geometry().width() / 2) - 287.5)
            y = int(self.parent.geometry().y() + (self.parent.geometry().height() / 2) - scaleY / 2)
        else:
            x, y = self.geometry().x(), self.geometry().y()
        self.setGeometry(x, y, 575, scaleY)

        #   ↓ Сдвиг виджетов, что-бы красиво было ↓
        self.line_2.setGeometry(0, space + 80, 365, 3)
        self.line_3.setGeometry(364, 0, 4, scaleY)
        self.toThisFileButton.setGeometry(180, space + 90, 170, 30)
        self.toAnotherFileButton.setGeometry(180, space + 125, 170, 30)
        self.errorText.setGeometry(5, space + 60, 355, 16)
        self.encryptToText.setGeometry(15, space + 90, 160, 65)
        self.algDescription.setGeometry(366, 0, 209, scaleY)
        self.algDescription.setPlainText(self.algorithm.settings(self.algorithm)[1])
        self.check_data()

    #   ↓ Сбор и отправка данных с виджетов в алгоритм шифрования на проверку ↓
    def check_data(self):
        #   ↓ Сбор данных с виджетов ↓
        self.data = []
        for widget in self.widgets:
            if type(widget) == PyQt5.QtWidgets.QLineEdit:
                self.data.append(widget.text())
            if type(widget) == PyQt5.QtWidgets.QCheckBox:
                self.data.append(widget.isChecked())
            if type(widget) == ChoiceFileButton:
                self.data.append(widget.file)

        #   ↓ Отправка данных с виджетов на проверку ↓
        try:
            result = self.algorithm.check_data(self.algorithm, self.data)
            self.errorText.setText(result[1])
            QPushButton().setEnabled(False)
            self.toThisFileButton.setEnabled(result[0])
            self.toAnotherFileButton.setEnabled(result[0])
        except BaseException as f:
            print(f)
            alert = QMessageBox()
            alert.setWindowTitle("Ошибка!")
            if str(f)[-30:] == " has no attribute 'check_data'":
                alert.setText("Ошибка: 2")
            alert.exec()

    def get_encrypted_data(self):
        if self.encrypt:
            return bytes(self.algorithm.encryption_function(self.algorithm, self.text, self.data))
        return bytes(self.algorithm.decryption_function(self.algorithm, self.text, self.data))

    def click_toThisFileButton(self):
        toprint_data = self.get_encrypted_data().decode('utf-8', 'replace')
        self.parent.textEdit.setPlainText(toprint_data)
        self.destroy()

    def click_toAnotherFileButton(self):
        with open(QFileDialog.getSaveFileName(self, 'Сохранить как', self.parent.file)[0], "wb") as f:
            f.write(self.get_encrypted_data())
        self.destroy()


class ProgressBar(QDialog):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)
        uic.loadUi('./ui/ProgressBar.ui', self)
        self.setWindowIcon(QIcon("icon.png"))


class ChoiceFileButton(QPushButton):
    def __init__(self, parent, open=True):
        super().__init__(parent)
        self.open = open
        self.file = os.path.realpath(__file__).split(":")[0] + ":/untitled.txt"

    def mousePressEvent(self, event):
        if self.open:
            self.file = QFileDialog.getOpenFileName(self, 'Выберете файл',
                                                    os.path.realpath(__file__).split(":")[0] + ":/untitled.txt")[0]
        else:
            self.file = QFileDialog.getSaveFileName(self, 'Сохранить как',
                                                    os.path.realpath(__file__).split(":")[0] + ":/untitled.txt")[0]
        self.click()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
