import networkx as nx
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QMessageBox
import os

class StatisticsWindow(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("Graph Statistics")
        self.setGeometry(300, 300, 400, 300)

        layout = QVBoxLayout()

        self.execution_time_label = QLabel(f"Execution Time: {self.app.colorer.execution_time:.6f} seconds")
        layout.addWidget(self.execution_time_label)

        self.colors_used_label = QLabel(f"Number of Colors Used: {self.get_colors_used()}")
        layout.addWidget(self.colors_used_label)

        self.algorithm_label = QLabel(f"Algorithm Used: {self.get_algorithm_used()}")
        layout.addWidget(self.algorithm_label)

        self.connections_label = QLabel("Graph Connections:")
        layout.addWidget(self.connections_label)

        self.connections_text = QTextEdit()
        self.connections_text.setPlainText(self.get_connections())
        self.connections_text.setReadOnly(True)
        layout.addWidget(self.connections_text)

        self.import_button = QPushButton('Import Statistics', self)
        self.import_button.clicked.connect(self.import_statistics)
        layout.addWidget(self.import_button)

        self.sorted_edges_label = QLabel()
        layout.addWidget(self.sorted_edges_label)

        self.setLayout(layout)

    def get_colors_used(self):
        if nx.is_bipartite(self.app.graph):
            return 1
        elif hasattr(self.app.colorer, 'colors_used'):
            return self.app.colorer.colors_used
        else:
            return len(set(nx.get_edge_attributes(self.app.graph, 'color').values()))

    def get_algorithm_used(self):
        if hasattr(self.app.colorer, 'algorithm_used'):
            return self.app.colorer.algorithm_used
        elif nx.is_bipartite(self.app.graph):
            return "Maximal Pairing Algorithm"
        else:
            return "Unknown Algorithm"

    def get_connections(self):
        if hasattr(self.app, 'graph'):
            if nx.is_bipartite(self.app.graph):
                left, right = nx.bipartite.sets(self.app.graph)
                colored_edges = self.app.graph.edges()
                connections = []
                for u, v in colored_edges:
                    if u in left:
                        u_label = f"L{u}" if isinstance(u, int) else f"L{u.split('_')[1]}"
                        v_label = f"R{v}" if isinstance(v, int) else f"R{v.split('_')[1]}"
                    else:
                        u_label = f"R{u}" if isinstance(u, int) else f"R{u.split('_')[1]}"
                        v_label = f"L{v}" if isinstance(v, int) else f"L{v.split('_')[1]}"
                    connections.append(f"{u_label}-{v_label}")
            else:
                connections = [f"{u}-{v}" for u, v in self.app.graph.edges()]
            return "\n".join(sorted(connections))
        return ""

    def import_statistics(self):
        filename = 'graph_statistics.txt'
        try:
            with open(filename, 'w') as f:
                f.write(f"{self.execution_time_label.text()}\n")
                f.write(f"{self.colors_used_label.text()}\n")
                f.write(f"{self.algorithm_label.text()}\n")
                f.write(f"{self.connections_label.text()}\n")
                f.write(self.connections_text.toPlainText())
            
            abs_path = os.path.abspath(filename)
            QMessageBox.information(self, "Statistics Imported", f"Statistics have been imported to:\n{abs_path}")
        except IOError as e:
            QMessageBox.warning(self, "Error", f"An error occurred while writing the file:\n{str(e)}")

    def get_sorted_edges(self):
        if hasattr(self.app.colorer, 'sorted_edges'):
            return "\n".join([f"{u}-{v}" for u, v in self.app.colorer.sorted_edges])
        return "Not available"

    def update_statistics(self):
        # ... (existing update code)
        
        sorted_edges = self.get_sorted_edges()
        self.sorted_edges_label.setText(f"Sorted Edges:\n{sorted_edges}")