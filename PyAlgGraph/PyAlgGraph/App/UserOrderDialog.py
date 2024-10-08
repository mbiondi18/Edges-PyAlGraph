from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

class UserOrderDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("User Order")
        layout = QVBoxLayout()
        
        label = QLabel("Do you want to use User Order?")
        layout.addWidget(label)
        
        self.yes_button = QPushButton("Yes")
        self.yes_button.clicked.connect(self.accept)
        layout.addWidget(self.yes_button)
        
        self.no_button = QPushButton("No")
        self.no_button.clicked.connect(self.reject)
        layout.addWidget(self.no_button)
        
        self.setLayout(layout)
