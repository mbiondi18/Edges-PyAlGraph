from PyQt5.QtWidgets import (
    QVBoxLayout, QMainWindow, QPushButton, QGraphicsScene, QGraphicsView, 
    QGraphicsEllipseItem, QComboBox, QGraphicsTextItem, QLabel, QGraphicsLineItem, 
    QWidget, QHBoxLayout, QDialog  # Add this import at the top of the file
)
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPen, QBrush, QPainter, QFont
from WeightDialog import WeightDialog
from GraphVisualizer import GraphVisualizer
from GraphColorer import GraphColorer
from GraphAnalyzer import GraphAnalyzer
from GraphIO import GraphIO
from Tutorial import Tutorial
from StepByStepSolver import StepByStepSolver
from GraphWindow import GraphWindow
from BipartiteGraphWindow import BipartiteGraphWindow
from UserOrderDialog import UserOrderDialog
import networkx as nx
from StatisticsWindow import StatisticsWindow

class App(QMainWindow):
    def __init__(app):
        super().__init__()
        app.setWindowTitle('PyAlgGraph')
        app.resize(1600, 900)
        app.analyzer = GraphAnalyzer()
        app.graph = nx.Graph()
        app.visualizer = GraphVisualizer(app)
        app.colorer = GraphColorer(app.graph)
        app.analyzer = GraphAnalyzer()
        app.io = GraphIO()
        app.tutorial = Tutorial()
        app.solver = StepByStepSolver()

        central_widget = QWidget()
        app.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        sidebar = QWidget()
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar.setFixedWidth(220)  # Increased width to accommodate larger buttons

        # Make Graph button
        app.paint_graph_button = QPushButton('Make Graph')
        app.paint_graph_button.clicked.connect(app.open_graph_window)
        app.paint_graph_button.setFixedSize(200, 60)
        sidebar_layout.addWidget(app.paint_graph_button)

        # Sequential Coloring dropdown
        app.secuencial_coloring_button = QComboBox()
        app.secuencial_coloring_button.addItems(["Secuencial coloring default order", "Secuencial coloring user order"])
        app.secuencial_coloring_button.activated[str].connect(app.on_secuencial_coloring_button_activated)
        app.secuencial_coloring_button.setFixedSize(200, 60)
        sidebar_layout.addWidget(app.secuencial_coloring_button)

        # Add two empty spaces
        sidebar_layout.addSpacing(60)
        sidebar_layout.addSpacing(60)

        # Make Bipartite Graph button
        app.paint_bipartite_graph_button = QPushButton('Make Bipartite Graph')
        app.paint_bipartite_graph_button.clicked.connect(app.open_bipartite_graph_window)
        app.paint_bipartite_graph_button.setFixedSize(200, 60)
        sidebar_layout.addWidget(app.paint_bipartite_graph_button)

        # Color Bipartite Graph button
        app.color_bipartite_graph_button = QPushButton('Color Bipartite Graph')
        app.color_bipartite_graph_button.clicked.connect(app.color_bipartite_graph)
        app.color_bipartite_graph_button.setFixedSize(200, 60)
        sidebar_layout.addWidget(app.color_bipartite_graph_button)

        # Add four empty spaces
        sidebar_layout.addSpacing(60)
        sidebar_layout.addSpacing(60)
        sidebar_layout.addSpacing(60)
        sidebar_layout.addSpacing(60)

        # See Statistics button
        app.see_statistics_button = QPushButton('See Statistics')
        app.see_statistics_button.clicked.connect(app.show_statistics)
        app.see_statistics_button.setFixedSize(200, 60)
        sidebar_layout.addWidget(app.see_statistics_button)

        sidebar_layout.addStretch(1)
        main_layout.addWidget(sidebar)
        main_layout.addWidget(app.visualizer)

    def open_graph_window(app):
        user_order_dialog = UserOrderDialog(app)
        result = user_order_dialog.exec_()
        use_user_order = result == QDialog.Accepted
        app.graph_window = GraphWindow(app, app.graph, use_user_order)
        app.graph_window.show()

    def unable_modes(app):
        app.select_order_mode = False

    def create_graph(app, graph): 
        print("create_graph method triggered")
        app.unable_modes()
        app.graph = graph.copy()  # Create a copy of the graph
        app.colorer = GraphColorer(app.graph)  # Reset the colorer with the new graph
        app.visualizer.create_graph(app.graph)
        app.visualizer.positions = None  # Reset positions for the new graph

    def create_bipartite_graph(app, graph):
        print("create_bipartite_graph method triggered")
        app.unable_modes()
        app.graph = graph  # Update the app's graph with the bipartite graph
        
        # Ensure all nodes have the 'bipartite' attribute
        left_nodes = set(n for n in app.graph.nodes() if n.startswith('left_'))
        right_nodes = set(app.graph.nodes()) - left_nodes
        nx.set_node_attributes(app.graph, {n: {'bipartite': 0} for n in left_nodes})
        nx.set_node_attributes(app.graph, {n: {'bipartite': 1} for n in right_nodes})
        
        # Ensure all nodes have a 'weight' attribute
        for node in app.graph.nodes():
            if 'weight' not in app.graph.nodes[node]:
                app.graph.nodes[node]['weight'] = 1
        
        app.visualizer.create_bipartite_graph(app.graph)
        app.visualizer.positions = None  # Reset positions for the new graph

    def on_secuencial_coloring_button_activated(self, text):
        if text == "Secuencial coloring default order":
            self.secuencial_coloring(self.graph.edges())
        elif text == "Secuencial coloring user order":
            edge_colors = self.colorer.sequential_user_order_coloring(self.graph)
            self.print(edge_colors)

    def bipartite_coloring(app):
        edge_colors = app.colorer.bipartite_coloring(app.graph)
        app.print(edge_colors)        


    def secuencial_coloring(app, edges):
        edge_colors = app.colorer.secuencial_coloring(app.graph, edges)
        app.print(edge_colors)

    def secuencial_coloring_user_order(app):
        app.unable_modes()
        app.select_order_mode = True
    
    def open_bipartite_graph_window(app):
        app.bipartite_graph_window = BipartiteGraphWindow(app, app.graph)
        app.bipartite_graph_window.show()

    def print(app, edge_colors):
        app.unable_modes()
        app.visualizer.draw_graph(app.graph, edge_colors)
        app.visualizer.draw_execution_time(app.colorer.execution_time)

    def color_bipartite_graph(app):
        if isinstance(app.graph, nx.Graph) and nx.is_bipartite(app.graph):
            if app.visualizer.positions is None:
                left_nodes, right_nodes = nx.bipartite.sets(app.graph)
                max_count = max(len(left_nodes), len(right_nodes))
                current_positions = {}
                for i, node in enumerate(left_nodes):
                    current_positions[node] = (-0.45, 1 - (i / (max_count - 1)) if max_count > 1 else 0.5)
                for i, node in enumerate(right_nodes):
                    current_positions[node] = (0.45, 1 - (i / (max_count - 1)) if max_count > 1 else 0.5)
            else:
                current_positions = app.visualizer.positions

            app.colorer.maximal_matching_bipartite(app.graph, iterations=100)
            
            app.visualizer.draw_bipartite_matching(app.graph, app.colorer.assignments, set(), set(), pos=current_positions)
            app.visualizer.draw_execution_time(app.colorer.execution_time)
        else:
            print("The current graph is not bipartite or no graph is loaded.")


    def show_statistics(app):
        app.statistics_window = StatisticsWindow(app)
        app.statistics_window.show()

