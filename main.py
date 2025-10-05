# მთავარი გამშვები ფაილი

import sys
from PyQt5.QtWidgets import QApplication
from database import Database
from PyQT_data import MyApp

app = QApplication(sys.argv)
db = Database()
window = MyApp(db)
window.show()
sys.exit(app.exec())
