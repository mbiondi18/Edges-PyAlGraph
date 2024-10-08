from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QIntValidator

class WeightDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(300, 150)
        
        self.setWindowTitle("Asignar peso al vértice")
        self.layout = QVBoxLayout()
        self.label = QLabel("Ingrese el peso del vértice:")
        self.text_field = QLineEdit()
        self.button = QPushButton("Aceptar")
        self.button.clicked.connect(self.accept)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.text_field)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

    def get_weight(self):
        
        if self.text_field.text() == "":
            return 0
        else:
            return int(self.text_field.text())

class OrderDialog(QDialog):
    def __init__(self, parent=None, used_orders=None):
        super(OrderDialog, self).__init__(parent)
        self.setWindowTitle("Edge Order")
        self.used_orders = used_orders or []

        layout = QVBoxLayout()

        self.label = QLabel("Insert edge order:")
        layout.addWidget(self.label)

        self.order_input = QLineEdit()
        self.order_input.setValidator(QIntValidator())
        layout.addWidget(self.order_input)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        layout.addWidget(self.error_label)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.validate_and_accept)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

    def validate_and_accept(self):
        order = int(self.order_input.text())
        if order in self.used_orders:
            self.error_label.setText("This order number is used already")
        elif order != len(self.used_orders) + 1:
            self.error_label.setText(f"Number out of order, it should be {len(self.used_orders) + 1}")
        else:
            self.accept()

    def get_order(self):
        return int(self.order_input.text())