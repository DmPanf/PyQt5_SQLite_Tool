# add_window.py
# 15-06-2023

from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QVBoxLayout, QApplication, QFormLayout, QLabel
from PyQt5.QtCore import Qt


class AddWindow(QWidget):
    def __init__(self, conn, cursor, update_table):
        super().__init__()
        self.conn = conn
        self.cursor = cursor
        self.update_table = update_table

        # Получаем новый ID для сотрудника
        self.cursor.execute("SELECT max(id) FROM people")
        max_id = self.cursor.fetchone()[0]
        self.id = max_id + 1 if max_id is not None else 1

        # Инициализируем UI
        self.initUI()

        # Задаем новый ID
        self.id_input.setText(str(self.id))
        # Устанавливаем фокус на person_input
        self.person_input.setFocus()


    def initUI(self):
        self.setWindowTitle("Добавление записей")
        self.resize(400, 190)

        # Создание и настройка меток и полей ввода
        self.id_label = QLabel(' ID: ')
        self.person_label = QLabel(' Person: ')
        self.year_label = QLabel(' Year: ')

        self.id_input = QLineEdit()
        self.id_input.setReadOnly(True)  # Пользователь не может изменить это поле
        self.person_input = QLineEdit()
        self.year_input = QLineEdit()
        
        # Создание кнопки для сохранения новой записи
        self.add_button = QPushButton('Save', self)
        self.add_button.setFixedWidth(320)
        self.add_button.clicked.connect(self.add_entry)

        #self.layout = QVBoxLayout(self)
        # Размещение виджетов в вертикальном layout
        self.layout = QFormLayout(self)
        self.layout.addRow(self.id_label, self.id_input)
        self.layout.addRow(self.person_label, self.person_input)
        self.layout.addRow(self.year_label, self.year_input)
        self.layout.addWidget(self.add_button)

        self.center_on_screen()

    def add_entry(self):
        # id = self.id_input.text()
        person = self.person_input.text()
        year = self.year_input.text()

        # Проверка, что поле Person не пустое
        if person.strip() == '':
            QMessageBox.warning(self, 'Warning', 'Person field must not be empty')
            return

        self.cursor.execute("INSERT INTO people VALUES (?, ?, ?)", (self.id, person, year))
        self.conn.commit()

        # Обновление таблицы после добавления записи
        self.update_table()

        # Закрытие окна после удаления записи
        self.close()

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
    
