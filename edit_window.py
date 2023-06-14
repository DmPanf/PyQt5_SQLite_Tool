# edit_window.py
# 15-06-2023

from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QVBoxLayout, QApplication, QFormLayout, QLabel, QMessageBox
from PyQt5.QtCore import Qt


class EditWindow(QWidget):
    def __init__(self, conn, cursor, update_table_callback, id, parent=None):
        super().__init__(parent)
        self.conn = conn
        self.cursor = cursor
        self.update_table = update_table_callback
        self.id = id

        # Инициализируем UI
        self.initUI()

        # Устанавливаем фокус на person_input
        self.person_input.setFocus()

    def initUI(self):
        self.setWindowTitle("Редактирование записей")
        self.resize(400, 190)

        self.cursor.execute("SELECT * FROM people WHERE id = ?", (self.id,))
        result = self.cursor.fetchone()
        if result is not None:
            # Создание и настройка меток и полей ввода
            self.id_label = QLabel(' ID: ', self)
            self.person_label = QLabel(' Person: ', self)
            self.year_label = QLabel(' Year: ', self)

            self.id_input = QLineEdit(str(result[0]), self)
            self.id_input.setReadOnly(True)  # Пользователь не может изменить это поле
            self.person_input = QLineEdit(str(result[1]), self)
            self.year_input = QLineEdit(str(result[2]), self)

            # Создание кнопки для сохранения исправленной записи
            self.edit_button = QPushButton('Save', self)
            self.edit_button.setFixedWidth(320)
            self.edit_button.clicked.connect(self.edit_entry)

            # Размещение виджетов в вертикальном layout
            self.layout = QFormLayout(self)
            self.layout.addRow(self.id_label, self.id_input)
            self.layout.addRow(self.person_label, self.person_input)
            self.layout.addRow(self.year_label, self.year_input)
            self.layout.addWidget(self.edit_button)
        else:
            QMessageBox.warning(self, 'Error', 'No entry with such ID exists.')
        
        self.center_on_screen()

    def edit_entry(self):
        try:
            person = self.person_input.text()
            year = self.year_input.text()
            self.cursor.execute("UPDATE people SET person=?, year=? WHERE id=?", (person, year, self.id))
            self.conn.commit()

            # Обновление таблицы после корректировки записи
            self.update_table()

            # Закрытие окна после корректировки записи
            self.close()
        except Exception as e:
            QMessageBox.warning(self, 'Error', str(e))


        #id = self.id_input.text()
        # person = self.person_input.text()
        # year = self.year_input.text()
        # self.cursor.execute("UPDATE people SET person=?, year=? WHERE id=?", (person, year, self.id))


    def center_on_screen(self):
        # Получаем геометрию экрана
        screen_geometry = QApplication.desktop().availableGeometry()
        # Получаем геометрию окна
        window_geometry = self.frameGeometry()
        # Устанавливаем центр окна в центр экрана
        window_geometry.moveCenter(screen_geometry.center())
        # Добавляем смещение: отодвигаем окно вверх на 90 пикселей
        window_geometry.moveTop(window_geometry.top() + 90)
        # Перемещаем главное окно по этим координатам
        self.move(window_geometry.topLeft())
