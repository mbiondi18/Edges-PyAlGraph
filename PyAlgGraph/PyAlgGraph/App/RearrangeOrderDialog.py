from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QListWidget, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt

class RearrangeOrderDialog(QDialog):
    def __init__(self, current_edges, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Rearrange Coloring Order")
        self.setMinimumWidth(500)
        self.current_edges = current_edges
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout()

        # Left side - Current Order
        left_layout = QVBoxLayout()
        left_label = QLabel("Current Order:")
        self.current_list = QListWidget()
        for edge in self.current_edges:
            self.current_list.addItem(f"{edge[0]}-{edge[1]}")
        left_layout.addWidget(left_label)
        left_layout.addWidget(self.current_list)

        # Right side - New Order
        right_layout = QVBoxLayout()
        right_label = QLabel("New Order:")
        self.new_list = QListWidget()
        self.new_list.setAcceptDrops(True)
        self.new_list.setDragDropMode(QListWidget.DragDrop)
        right_layout.addWidget(right_label)
        right_layout.addWidget(self.new_list)

        # Add layouts to main layout
        layout.addLayout(left_layout)
        layout.addLayout(right_layout)

        # Button layout
        button_layout = QVBoxLayout()
        self.move_right_button = QPushButton("→")
        self.move_left_button = QPushButton("←")
        self.validate_button = QPushButton("Validate Rearrangement")
        
        button_layout.addWidget(self.move_right_button)
        button_layout.addWidget(self.move_left_button)
        button_layout.addStretch()
        button_layout.addWidget(self.validate_button)

        # Connect buttons
        self.move_right_button.clicked.connect(self.move_to_right)
        self.move_left_button.clicked.connect(self.move_to_left)
        self.validate_button.clicked.connect(self.validate_order)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def move_to_right(self):
        current_item = self.current_list.currentItem()
        if current_item:
            self.new_list.addItem(current_item.text())
            self.current_list.takeItem(self.current_list.row(current_item))

    def move_to_left(self):
        current_item = self.new_list.currentItem()
        if current_item:
            self.current_list.addItem(current_item.text())
            self.new_list.takeItem(self.new_list.row(current_item))

    def validate_order(self):
        if self.new_list.count() != len(self.current_edges):
            QMessageBox.warning(self, "Invalid Order", 
                              "Please include all edges in the new order!")
            return

        new_order = []
        for i in range(self.new_list.count()):
            edge_str = self.new_list.item(i).text()
            v1, v2 = map(int, edge_str.split('-'))
            new_order.append((v1, v2))

        self.new_edge_order = new_order
        self.accept() 