import sys
from PyQt5.QtWidgets import QApplication
from converter_window import ConverterWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ConverterWindow()
    window.show()
    sys.exit(app.exec_())
