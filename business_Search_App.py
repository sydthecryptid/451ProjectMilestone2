# business search app prototype, connects to .ui file

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QWidget

class BusinessSearchApp(QWidget): #test app loading
    def __init__(self):
        super().__init__()
        uic.loadUi("business_search.ui", self)

if __name__ == "__main__": 
    app = QApplication([])
    window = BusinessSearchApp()
    window.show()
    app.exec()