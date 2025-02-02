from PyQt5.QtWidgets import (
    QVBoxLayout, QMainWindow, QPushButton, QGraphicsScene, QGraphicsView, 
    QGraphicsEllipseItem, QComboBox, QGraphicsTextItem, QLabel, QGraphicsLineItem, 
    QWidget, QHBoxLayout, QDialog, QMessageBox  # Add this import at the top of the file
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
        sidebar.setFixedWidth(220) 
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
        sidebar_layout.addSpacing(60)
        # See Statistics button
        app.see_statistics_button = QPushButton('See Statistics')
        app.see_statistics_button.clicked.connect(app.show_statistics)
        app.see_statistics_button.setFixedSize(200, 60)
        sidebar_layout.addWidget(app.see_statistics_button)
        sidebar_layout.addStretch(1)
        main_layout.addWidget(sidebar)

        # Create a container for the visualizer, step buttons, and sorted edges label
        visualizer_container = QWidget()
        visualizer_layout = QVBoxLayout(visualizer_container)
        app.visualizer = GraphVisualizer(app)
        visualizer_layout.addWidget(app.visualizer)

        # Create step buttons
        app.create_step_buttons(visualizer_layout)

        # Add the sorted_edges_label to the visualizer container
        app.sorted_edges_label = QLabel("Sorted Edges: Not available")
        app.sorted_edges_label.setAlignment(Qt.AlignTop)
        app.sorted_edges_label.setWordWrap(True)
        app.sorted_edges_label.setVisible(False)  # Hide by default
        visualizer_layout.addWidget(app.sorted_edges_label)

        main_layout.addWidget(visualizer_container, 1)  # Give it a stretch factor of 1

        # Create right sidebar for sorted edges
        right_sidebar = QWidget()
        right_sidebar_layout = QVBoxLayout(right_sidebar)
        right_sidebar.setFixedWidth(220)

        app.sorted_edges_label = QLabel("Sorted Edges:")
        app.sorted_edges_label.setAlignment(Qt.AlignTop)
        app.sorted_edges_label.setWordWrap(True)
        right_sidebar_layout.addWidget(app.sorted_edges_label)
        right_sidebar_layout.addStretch(1)

        app.right_sidebar = right_sidebar  # Store the reference to right_sidebar
        app.right_sidebar.setVisible(False)  # Hide by default

        main_layout.addWidget(right_sidebar)

    def open_graph_window(app):
        user_order_dialog = UserOrderDialog(app)
        result = user_order_dialog.exec_()
        use_user_order = result == QDialog.Accepted
        app.graph_window = GraphWindow(app, app.graph, use_user_order)
        app.graph_window.show()

    def unable_modes(app):
        app.select_order_mode = False

    def create_graph(app, graph, positions=None): 
        print("create_graph method triggered")
        app.unable_modes()
        app.graph = graph.copy()  # Create a copy of the graph
        app.colorer = GraphColorer(app.graph)  # Reset the colorer with the new graph
        app.visualizer.positions = positions  # Set positions before creating graph
        app.visualizer.create_graph(app.graph)

    def create_bipartite_graph(self, graph, positions):
        print("create_bipartite_graph method triggered")
        self.unable_modes()
        self.graph = graph  # Update the app's graph with the bipartite graph
        
        # Ensure all nodes have the 'bipartite' attribute
        left_nodes = set(n for n in self.graph.nodes() if n.startswith('left_'))
        right_nodes = set(self.graph.nodes()) - left_nodes
        nx.set_node_attributes(self.graph, {n: {'bipartite': 0} for n in left_nodes})
        nx.set_node_attributes(self.graph, {n: {'bipartite': 1} for n in right_nodes})
        
        # Ensure all nodes have a 'weight' attribute
        for node in self.graph.nodes():
            if 'weight' not in self.graph.nodes[node]:
                self.graph.nodes[node]['weight'] = 1
        
        self.visualizer.create_bipartite_graph(self.graph)
        self.visualizer.positions = positions  # Set the positions

    def on_secuencial_coloring_button_activated(self, text):
        if text == "Secuencial coloring default order":
            self.secuencial_coloring(self.graph.edges())
            self.right_sidebar.setVisible(True)  # Show the right sidebar
        elif text == "Secuencial coloring user order":
            edge_colors = self.colorer.sequential_user_order_coloring(self.graph)
            self.print(edge_colors)
            self.right_sidebar.setVisible(False)  # Hide the right sidebar

    def bipartite_coloring(app):
        edge_colors = app.colorer.bipartite_coloring(app.graph)
        app.print(edge_colors)        


    def secuencial_coloring(app, edges):
        edge_colors = app.colorer.secuencial_coloring(app.graph, edges)
        app.print(edge_colors)
        app.display_sorted_edges()

    def display_sorted_edges(self):
        if hasattr(self.colorer, 'sorted_edges'):
            sorted_edges_str = "\n".join([f"{u}-{v}" for u, v in self.colorer.sorted_edges])
            
            # Add explanation of the algorithm
            algorithm_explanation = "\n\nAlgorithm Process:\n" + \
                "1. The algorithm starts with the vertex of highest degree\n" + \
                "2. Colors all edges connected to this vertex\n" + \
                "3. Continues with the next vertex of highest degree among the remaining vertices\n" + \
                "4. Repeats until all edges are colored\n"
            
            # Group edges by color
            color_classes = {}
            for (u, v), color in self.colorer.edge_colors.items():
                if color not in color_classes:
                    color_classes[color] = []
                color_classes[color].append(f"{u}-{v}")
            
            # Format color classes string
            color_classes_str = "\nColor Classes:"
            for color, edges in color_classes.items():
                color_classes_str += f"\n{edges} = {color}({len(edges)})"
            
            self.sorted_edges_label.setText(
                f"Sorted Edges:\n\n{sorted_edges_str}{algorithm_explanation}{color_classes_str}"
            )
        else:
            self.sorted_edges_label.setText("Sorted Edges:\n\nNot available")

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

    def color_bipartite_graph(self):
        if isinstance(self.graph, nx.Graph) and nx.is_bipartite(self.graph):
            print("Graph is bipartite")
            
            # Check for connected components
            components = list(nx.connected_components(self.graph))
            if len(components) > 1:
                print("Graph is disconnected, processing each component separately")
            else:
                print("Graph is connected")

            self.matching_states = []
            self.edge_colors = {}
            color_index = 0

            for component in components:
                subgraph = self.graph.subgraph(component).copy()
                left_nodes, right_nodes = nx.bipartite.sets(subgraph)
                
                # Create positions if they don't exist
                if self.visualizer.positions is None:
                    print("Creating new positions")
                    self.visualizer.positions = {}
                    max_count = max(len(left_nodes), len(right_nodes))
                    for i, node in enumerate(left_nodes):
                        self.visualizer.positions[node] = (-0.45, 1 - (i / (max_count - 1)) if max_count > 1 else 0.5)
                    for i, node in enumerate(right_nodes):
                        self.visualizer.positions[node] = (0.45, 1 - (i / (max_count - 1)) if max_count > 1 else 0.5)
                else:
                    print("Using existing positions")
                print("Graph nodes:", subgraph.nodes())
                print("Graph edges:", subgraph.edges())
                print("Positions:", self.visualizer.positions)
                
                # Draw the initial uncolored graph
                self.visualizer.draw_bipartite_matching(subgraph, {}, set(), set(), pos=self.visualizer.positions)
                
                # Initialize colorer if not already done
                if not hasattr(self, 'colorer'):
                    self.colorer = GraphColorer(subgraph)

                try:
                    print("Starting maximal_matching_bipartite")
                    matching_states, edge_colors = self.colorer.maximal_matching_bipartite(subgraph)
                    print("Matching states:", matching_states)
                    self.matching_states.extend(matching_states)
                    self.edge_colors.update(edge_colors)
                    color_index += 1

                    # Add a final state that shows all colors together
                    final_state = {
                        "matching": self.edge_colors,  # Use all colored edges
                        "augmenting_path": None,
                        "color": "final",  # Special marker for final state
                        "show_all_colors": True  # New flag to indicate final state
                    }
                    self.matching_states.append(final_state)
                    
                except Exception as e:
                    print(f"Error in maximal_matching_bipartite: {e}")
                    import traceback
                    traceback.print_exc()

            self.current_step = 0
            self.update_bipartite_visualization()
            self.visualizer.draw_execution_time(self.colorer.execution_time)
            
            self.prev_button.setVisible(True)
            self.next_button.setVisible(True)
        else:
            print("The current graph is not bipartite or no graph is loaded.")

    def update_bipartite_visualization(self):
        if hasattr(self, 'matching_states') and self.matching_states:
            current_state = self.matching_states[self.current_step]
            if isinstance(current_state, dict):
                current_matching = current_state["matching"]
                augmenting_path = current_state.get("augmenting_path")
                color = current_state["color"]
                show_all_colors = current_state.get("show_all_colors", False)
                
                # Handle the final state differently
                if show_all_colors:
                    # For the final state, we pass the state directly
                    self.visualizer.draw_bipartite_matching(
                        self.graph,
                        current_state,  # Pass the entire state
                        set(),  # Empty set for unassigned_left
                        set(),  # Empty set for unassigned_right
                        pos=self.visualizer.positions,
                        augmenting_path=None,
                        color="final"
                    )
                    return

                # Regular state handling
                left_nodes, right_nodes = nx.bipartite.sets(self.graph)
                unassigned_left = set(left_nodes) - set(current_matching.keys())
                unassigned_right = set(right_nodes) - set(current_matching.values())
                
                # Update edge colors
                if not hasattr(self, 'cumulative_edge_colors'):
                    self.cumulative_edge_colors = {}

                for edge in self.graph.edges():
                    if edge in current_matching.items() or (edge[1], edge[0]) in current_matching.items():
                        self.cumulative_edge_colors[edge] = color
                    elif edge not in self.cumulative_edge_colors:
                        self.cumulative_edge_colors[edge] = 'gray'  # Uncolored edges

                self.visualizer.draw_bipartite_matching(
                    self.graph, 
                    current_matching, 
                    unassigned_left, 
                    unassigned_right, 
                    pos=self.visualizer.positions,
                    augmenting_path=augmenting_path,
                    color=color
                )
                self.visualizer.update_step_info(self.current_step + 1, len(self.matching_states))
            else:
                print("Error: current_state is not a dictionary.")
        else:
            print("No matching states available.")

    def show_statistics(app):
        app.statistics_window = StatisticsWindow(app)
        app.statistics_window.show()

    def create_step_buttons(self, layout):
        button_layout = QHBoxLayout()
        self.prev_button = QPushButton("Previous", self)
        self.next_button = QPushButton("Next", self)
        self.prev_button.clicked.connect(self.show_previous_step)
        self.next_button.clicked.connect(self.show_next_step)
        self.prev_button.setVisible(False)
        self.next_button.setVisible(False)
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)
        layout.addLayout(button_layout)

    def show_previous_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.update_bipartite_visualization()

    def show_next_step(self):
        if self.current_step < len(self.matching_states) - 1:
            self.current_step += 1
            self.update_bipartite_visualization()
