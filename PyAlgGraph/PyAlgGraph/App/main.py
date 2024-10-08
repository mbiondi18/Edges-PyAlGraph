from PyQt5.QtWidgets import QApplication
from App import App
import sys
from styles import set_app_style

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    window.setWindowTitle('PyAlgGraph')
    set_app_style(app)
    sys.exit(app.exec_())