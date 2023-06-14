# delete_window.py
# 15-06-2023

from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QVBoxLayout, QApplication, QLabel, QMessageBox
from PyQt5.QtCore import Qt


class DeleteWindow(QWidget):
    def __init__(self, conn, cursor, update_table_callback, id, parent=None):
        super().__init__(parent)
        self.conn = conn
        self.cursor = cursor
        self.update_table = update_table_callback
        self.id = id

        # Инициализируем UI
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Удаление записей")
        self.resize(350, 140)

        self.cursor.execute("SELECT * FROM people WHERE id = ?", (self.id,))
        result = self.cursor.fetchone()
        if result is not None:
            # Создание и настройка меток и полей ввода
            self.id_label = QLabel('Id: ' + str(result[0]), self)
            self.person_label = QLabel('Person: ' + str(result[1]), self)
            self.year_label = QLabel('Year: ' + str(result[2]), self)
            
            self.layout = QVBoxLayout(self)
            self.layout.addWidget(self.id_label)
            self.layout.addWidget(self.person_label)
            self.layout.addWidget(self.year_label)

            self.delete_button = QPushButton('Delete', self)
            self.delete_button.clicked.connect(self.delete_entry)
            self.layout.addWidget(self.delete_button)
        
            self.setLayout(self.layout)
        else:
            QMessageBox.warning(self, 'Error', 'No entry with such ID exists.')

        self.center_on_screen()


    def delete_entry(self):
        try:
            self.cursor.execute("DELETE FROM people WHERE id = ?", (self.id,))
            self.conn.commit()

            # Обновление таблицы после удаления записи
            self.update_table()

            # Закрытие окна после удаления записи
            self.close()
        except Exception as e:
            QMessageBox.warning(self, 'Error', str(e))


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
    
