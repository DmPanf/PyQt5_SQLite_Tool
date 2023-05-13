import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QHeaderView, QLabel, QMessageBox, QFormLayout, QFileDialog
from PyQt5.QtGui import QFont
import sqlite3
import csv
import os
from add_window import AddWindow
from delete_window import DeleteWindow
from edit_window import EditWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Создание базы данных
        self.db_path = "sqlite_database.db"
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        try:
            # Создание таблицы
            self.cursor.execute("""
            CREATE TABLE people
            (id INTEGER PRIMARY KEY, 
            person TEXT, 
            year INTEGER)
            """)
        except sqlite3.OperationalError:
            pass

        # Инициализируем UI
        self.initUI()

        # размер файла в байтах
        file_size = round(os.path.getsize(self.db_path) / 1024, 1)
        db_info = f'DB: {os.path.abspath(self.db_path)} [{file_size} KB]'
        self.setWindowTitle(db_info)

    def initUI(self):
        # self.setWindowTitle("Пример простой таблицы SQLite")
        self.resize(720, 480)

        # Виджет для отображения таблицы
        self.table_widget = QTableWidget()
        # self.table_widget.setFixedWidth(300)
        # self.table_widget.setFixedHeight(200)
        #self.table_widget.setRowCount(0)
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["ID", "Person", "Year"])
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.update_table()

        # Кнопки: 1 row
        self.button_layout = QHBoxLayout()
        self.add_button = QPushButton('Add', self)
        self.add_button.clicked.connect(self.open_add)
        self.button_layout.addWidget(self.add_button)

        self.delete_button = QPushButton('Delete', self)
        self.delete_button.clicked.connect(self.open_delete)
        self.button_layout.addWidget(self.delete_button)

        self.edit_button = QPushButton('Edit', self)
        self.edit_button.clicked.connect(self.open_edit)
        self.button_layout.addWidget(self.edit_button)

        # Кнопки: 2 row
        self.files_button_layout = QHBoxLayout()
        self.open_db_button = QPushButton('Open Database', self)
        self.open_db_button.clicked.connect(self.open_database)
        self.files_button_layout.addWidget(self.open_db_button)

        self.import_from_csv_button = QPushButton('Import CSV', self)
        self.import_from_csv_button.clicked.connect(self.import_from_csv)
        self.files_button_layout.addWidget(self.import_from_csv_button)

        self.export_to_csv_button = QPushButton('Export CSV', self)
        self.export_to_csv_button.clicked.connect(self.export_to_csv)
        self.files_button_layout.addWidget(self.export_to_csv_button)
        
        # Формирование вида окна с размещением виджетов
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.table_widget)
        self.layout.addLayout(self.button_layout)
        self.layout.addLayout(self.files_button_layout)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.center_on_screen()


    def open_add(self):
        self.add_window = AddWindow(self.conn, self.cursor, self.update_table)
        self.add_window.show()

    def open_delete(self):
        #self.delete_window = DeleteWindow(self.conn, self.cursor, self.update_table)
        #self.delete_window.show()
        selected_items = self.table_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, 'Warning', 'No items selected')
            return

        # Получить уникальные id из выделенных строк
        selected_ids = list(set(item.text() for item in selected_items if item.column() == 0))

        # Создать и открыть окно удаления для каждого id
        for id in selected_ids:
            self.delete_window = DeleteWindow(self.conn, self.cursor, self.update_table, id)
            self.delete_window.show()

    def open_edit(self):
        selected_items = self.table_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, 'Warning', 'No items selected')
            return

        # Получить уникальные id из выделенных строк
        selected_ids = list(set(item.text() for item in selected_items if item.column() == 0))

        # Создать и открыть окно удаления для каждого id
        for id in selected_ids:
            self.edit_window = EditWindow(self.conn, self.cursor, self.update_table, id)
            self.edit_window.show()

    def update_table(self):
        self.cursor.execute("SELECT * FROM people")
        rows = self.cursor.fetchall()
        
        self.table_widget.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table_widget.setItem(i, j, QTableWidgetItem(str(val)))

    def open_database(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open Database', '', 'SQLite Database Files (*.db);;All Files (*)', options=options)
        if file_name:
            self.load_database(file_name)
            # размер файла в байтах
            file_size = round(os.path.getsize(file_name) / 1024, 1)
            db_info = f'DB: {os.path.abspath(file_name)} [{file_size} KB]'
            self.setWindowTitle(db_info)

    def load_database(self, file_name):
        self.conn = sqlite3.connect(file_name)
        self.cursor = self.conn.cursor()
        self.update_table()


    def export_to_csv(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save to CSV', '', 'CSV Files (*.csv);;All Files (*)', options=options)
        if file_name:
            with open(file_name, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                self.cursor.execute("SELECT * FROM people")
                rows = self.cursor.fetchall()
                writer.writerow(['id', 'person', 'year'])  # header
                writer.writerows(rows)


    def import_from_csv(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open CSV', '', 'CSV Files (*.csv);;All Files (*)', options=options)
        if file_name:
            with open(file_name, 'r', newline='') as csv_file:
                reader = csv.reader(csv_file)
                next(reader, None)  # skip the header
                for row in reader:
                    self.cursor.execute("INSERT OR REPLACE INTO people VALUES (?, ?, ?)", (row[0], row[1], row[2]))
                self.conn.commit()
                self.update_table()


    def center_on_screen(self):
        # Получаем геометрию экрана
        screen_geometry = QApplication.desktop().availableGeometry()
        # Получаем геометрию окна
        window_geometry = self.frameGeometry()
        # Устанавливаем центр окна в центр экрана
        window_geometry.moveCenter(screen_geometry.center())
        # Добавляем смещение: отодвигаем окно вверх на 50 пикселей
        window_geometry.moveTop(window_geometry.top() - 50)
        # Перемещаем главное окно по этим координатам
        self.move(window_geometry.topLeft())

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Устанавливаем размер шрифта для всего приложения
    font = QFont()
    font.setPointSize(12)
    app.setFont(font)

    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
