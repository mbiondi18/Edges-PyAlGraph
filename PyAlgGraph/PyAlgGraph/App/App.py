from PyQt5.QtWidgets import (
    QVBoxLayout, QMainWindow, QPushButton, QGraphicsScene, QGraphicsView, 
    QGraphicsEllipseItem, QComboBox, QGraphicsTextItem, QLabel, QGraphicsLineItem, 
    QWidget, QHBoxLayout, QDialog, QMessageBox, QScrollArea  # Add this import at the top of the file
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
from RearrangeOrderDialog import RearrangeOrderDialog
import networkx as nx
from StatisticsWindow import StatisticsWindow
from AlgorithmExplanationWindow import AlgorithmExplanationWindow

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
        # Replace the Color Bipartite Graph button with a dropdown
        app.color_bipartite_graph_button = QComboBox()
        app.color_bipartite_graph_button.addItems([
            "Color Bipartite Graph (Step by Step)", 
            "Color Bipartite Graph (Final State)",
            "Color Bipartite Graph (Degree-Based)",
            "Color Bipartite Graph (User Order)"
        ])
        app.color_bipartite_graph_button.activated[str].connect(app.on_color_bipartite_graph_selected)
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

        # Create right sidebar for sorted edges with scroll area
        right_sidebar = QWidget()
        right_sidebar.setFixedWidth(220)
        
        # Create a scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Create a widget to hold the content
        scroll_content = QWidget()
        right_sidebar_layout = QVBoxLayout(scroll_content)
        right_sidebar_layout.setSpacing(0)
        right_sidebar_layout.setContentsMargins(5, 5, 5, 5)
        
        # Set up the scroll area
        scroll.setWidget(scroll_content)
        
        # Add scroll area to right sidebar
        right_sidebar_vbox = QVBoxLayout(right_sidebar)
        right_sidebar_vbox.addWidget(scroll)
        right_sidebar_vbox.setContentsMargins(0, 0, 0, 0)
        
        app.right_sidebar = right_sidebar
        app.right_sidebar.setVisible(False)
        app.right_sidebar_layout = right_sidebar_layout

        main_layout.addWidget(right_sidebar)

    def open_graph_window(app):
        # Remove the redundant dialog
        app.graph_window = GraphWindow(app, app.graph, False)  # Always use default ordering initially
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
        self.graph = graph
        
        # Create the coloring method combo box if it doesn't exist
        if not hasattr(self, 'bipartite_coloring_combo'):
            self.bipartite_coloring_combo = QComboBox()
            self.bipartite_coloring_combo.addItems([
                "Color Bipartite Graph (Step by Step)",
                "Color Bipartite Graph (Final State)",
                "Color Bipartite Graph (Degree-Based)"  # New option
            ])
            self.bipartite_coloring_combo.currentTextChanged.connect(self.on_color_bipartite_graph_selected)
            self.right_sidebar_layout.addWidget(self.bipartite_coloring_combo)
        
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
            self.right_sidebar.setVisible(True)
            self.show_rearrange_button()
        elif text == "Secuencial coloring user order":
            if hasattr(self.graph_window, 'edge_creation_order'):
                self.colorer.sorted_edges = self.graph_window.edge_creation_order
                edge_colors = self.colorer.sequential_user_order_coloring(self.graph)
                self.print(edge_colors)
                self.display_sorted_edges()
                self.display_algorithm_process("user")
                self.display_color_classes(edge_colors)
                self.right_sidebar.setVisible(True)
                self.show_rearrange_button()

    def bipartite_coloring(app):
        edge_colors = app.colorer.bipartite_coloring(app.graph)
        app.print(edge_colors)        


    def secuencial_coloring(app, edges):
        edge_colors = app.colorer.secuencial_coloring(app.graph, edges)
        app.print(edge_colors)
        app.display_sorted_edges()
        app.display_algorithm_process("default")
        app.display_color_classes(edge_colors)
        app.right_sidebar.setVisible(True)

    def format_bipartite_edge(self, edge):
        """Format bipartite edge for display: convert 'left_X-right_Y' to 'LX-RY'."""
        u, v = edge
        
        # Convert left_X to LX
        if isinstance(u, str) and u.startswith('left_'):
            u = 'L' + u[5:]  # Replace 'left_' with 'L'
        elif isinstance(u, str) and u.startswith('right_'):
            u = 'R' + u[6:]  # Replace 'right_' with 'R'
        
        # Convert right_Y to RY
        if isinstance(v, str) and v.startswith('left_'):
            v = 'L' + v[5:]  # Replace 'left_' with 'L'
        elif isinstance(v, str) and v.startswith('right_'):
            v = 'R' + v[6:]  # Replace 'right_' with 'R'
        
        return f"{u}-{v}"

    def display_sorted_edges(self):
        # Create a single string with header and content
        sorted_edges_text = "Sorted Edges:\n\n"
        
        if hasattr(self.colorer, 'sorted_edges'):
            for edge in self.colorer.sorted_edges:
                # Format the edge for display
                formatted_edge = self.format_bipartite_edge(edge)
                sorted_edges_text += formatted_edge + "\n"
        
        # Clear existing content if needed
        if hasattr(self, 'sorted_edges_combined'):
            self.right_sidebar_layout.removeWidget(self.sorted_edges_combined)
            self.sorted_edges_combined.deleteLater()
        
        # Create a single label with both title and content
        self.sorted_edges_combined = QLabel(sorted_edges_text)
        self.sorted_edges_combined.setWordWrap(True)
        self.sorted_edges_combined.setContentsMargins(0, 0, 0, 0)
        self.right_sidebar_layout.addWidget(self.sorted_edges_combined)

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

    def on_color_bipartite_graph_selected(self, text):
        if text == "Color Bipartite Graph (Step by Step)":
            self.color_bipartite_graph()
        elif text == "Color Bipartite Graph (Final State)":
            self.color_bipartite_graph_final()
        elif text == "Color Bipartite Graph (Degree-Based)":
            self.color_bipartite_graph_degree_based()
        elif text == "Color Bipartite Graph (User Order)":
            self.color_bipartite_graph_user_order()

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
                    
                    # Create new simplified states sequence
                    self.matching_states = []
                    
                    # Track colors and matchings for each iteration
                    current_color = None
                    iteration_matchings = {}
                    
                    # Process the original states to create our simplified sequence
                    for state in matching_states:
                        if isinstance(state, dict):
                            color = state["color"]
                            
                            # If this is a new color (new iteration)
                            if color != current_color:
                                if current_color is None:
                                    # First iteration - include augmenting path state
                                    if state.get("augmenting_path"):
                                        self.matching_states.append(state)
                                current_color = color
                                iteration_matchings[color] = state["matching"]
                            else:
                                # Update the matching for current color
                                iteration_matchings[color] = state["matching"]
                    
                    # Add final state for each iteration
                    for color, matching in iteration_matchings.items():
                        final_iteration_state = {
                            "matching": matching,
                            "augmenting_path": None,
                            "color": color,
                            "show_all_colors": False
                        }
                        self.matching_states.append(final_iteration_state)
                    
                    # Add the final state showing all colors
                    final_state = {
                        "matching": self.edge_colors,
                        "augmenting_path": None,
                        "color": "final",
                        "show_all_colors": True
                    }
                    self.matching_states.append(final_state)
                    
                    # Hide the right sidebar initially
                    self.right_sidebar.setVisible(False)
                    
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
                        current_state,
                        set(),
                        set(),
                        pos=self.visualizer.positions,
                        augmenting_path=None,
                        color="final"
                    )
                    
                    # Clear previous content first
                    self.clear_right_sidebar()
                    
                    # For final state, only show matching groups and color classes
                    self.display_matching_groups()
                    
                    # Display color classes
                    edge_colors = {}
                    matching_data = current_state["matching"]
                    
                    # Check what format the matching data is in
                    if matching_data:
                        # Sample first item to determine format
                        sample_key, sample_value = next(iter(matching_data.items()))
                        
                        if isinstance(sample_value, str) and sample_value in ["Red", "Green", "Blue", "Yellow", "Orange", "Violet", "Brown"]:
                            # This is already in the edge:color format (from final state)
                            print("Final state matching data is already in edge:color format")
                            edge_colors = matching_data
                        else:
                            # This is in the left:right node format (from intermediate steps)
                            print("Converting left:right format to edge:color format")
                            for edge, color in current_state["matching"].items():
                                if isinstance(edge, tuple):
                                    edge_colors[edge] = color
                    
                    print(f"Final state edge_colors: {edge_colors}")
                    self.display_color_classes(edge_colors)
                    
                    # Add the explanation button
                    if not hasattr(self, 'explanation_button'):
                        self.explanation_button = QPushButton("Show Algorithm Explanation")
                        self.explanation_button.clicked.connect(self.show_algorithm_explanation)
                        self.explanation_button.setContentsMargins(0, 0, 0, 0)
                        self.right_sidebar_layout.addWidget(self.explanation_button)
                    self.explanation_button.setVisible(True)
                    
                    self.right_sidebar.setVisible(True)
                    
                    # Update step indicator (if it's the final state show proper step number)
                    if hasattr(self, 'current_step') and hasattr(self, 'matching_states'):
                        total_steps = len(self.matching_states)
                        current = self.current_step + 1  # Add 1 since we're using 1-indexed display
                        self.visualizer.update_step_info(current, total_steps)
                    
                    return
                else:
                    # For non-final states, still show color information
                    # But clear previous content first
                    self.clear_right_sidebar()
                    
                    # Show current matchings for this step
                    step_info = f"Step {self.current_step + 1}/{len(self.matching_states)}\n\n"
                    step_info += f"Color: {color}\n\n"
                    
                    # Create matching info for this step
                    matching_text = "Current Matching:\n\n"
                    sorted_matches = []
                    for left, right in current_matching.items():
                        if isinstance(left, str) and isinstance(right, str):
                            left_label = f"L{left.split('_')[1]}" if '_' in left else left
                            right_label = f"R{right.split('_')[1]}" if '_' in right else right
                            sorted_matches.append((left_label, right_label))
                    sorted_matches.sort()
                    
                    for left, right in sorted_matches:
                        matching_text += f"{left}-{right}\n"
                    
                    # Add step info and matching info labels to sidebar
                    step_label = QLabel(step_info)
                    self.right_sidebar_layout.addWidget(step_label)
                    
                    matching_label = QLabel(matching_text)
                    matching_label.setWordWrap(True)
                    self.right_sidebar_layout.addWidget(matching_label)
                    
                    # Show color classes for current matching
                    current_colors = {}
                    # Convert current matching to edge:color format
                    for left, right in current_matching.items():
                        current_colors[(left, right)] = color
                        
                    # Also include edges from previous steps that might be colored differently
                    if hasattr(self, 'cumulative_edge_colors'):
                        for edge, edge_color in self.cumulative_edge_colors.items():
                            if edge_color != 'gray' and edge not in current_colors:
                                current_colors[edge] = edge_color
                    
                    # Display color classes for the current step
                    if current_colors:  # Only display if we have colors
                        self.display_color_classes(current_colors)
                    
                    # Show the right sidebar for non-final states too
                    self.right_sidebar.setVisible(True)

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
                # Update step info - ensure it reflects the current step accurately
                if hasattr(self, 'matching_states'):
                    total_steps = len(self.matching_states)
                    current = self.current_step + 1  # Add 1 since we're using 1-indexed display
                    self.visualizer.update_step_info(current, total_steps)
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

    def display_matching_groups(self):
        if hasattr(self, 'matching_states'):
            # Create text for matching groups
            matching_text = "Matching Groups by Iteration:\n\n"
            
            # Track the last seen matching for each iteration color
            color_matchings = {}
            color_order = []  # Keep track of the order colors appear
            
            # Look for iteration matchings in the colorer if available
            if hasattr(self, 'colorer') and hasattr(self.colorer, 'matching_states'):
                print("Using colorer matching states")
                matching_states = self.colorer.matching_states
            else:
                matching_states = self.matching_states
            
            # Process states in order, keeping only the last matching for each color
            for state in matching_states:
                if isinstance(state, dict) and "matching" in state:
                    color = state.get("color", "default")
                    if color != "final":  # Skip the final state in the processing
                        matching = state["matching"]
                        if isinstance(matching, dict) and matching:  # Make sure it's a non-empty dict
                            if color not in color_matchings:
                                color_matchings[color] = matching
                                color_order.append(color)  # Add color to order list when first seen
                            else:
                                # Update with the last matching for this color
                                color_matchings[color] = matching
            
            print(f"Found {len(color_order)} color iterations")
            print(f"Color matchings: {color_matchings}")
            
            # If no iterations found, try to extract data from the final state
            if not color_order and len(matching_states) > 0:
                final_state = matching_states[-1]
                if isinstance(final_state, dict) and "matching" in final_state:
                    matching = final_state["matching"]
                    if isinstance(matching, dict):
                        # Group by color
                        edge_colors = {}
                        for edge, color in matching.items():
                            if isinstance(edge, tuple) and len(edge) == 2:
                                if color not in edge_colors:
                                    edge_colors[color] = []
                                edge_colors[color].append(edge)
                        
                        # Use these color groups as iterations
                        for i, (color, edges) in enumerate(edge_colors.items()):
                            iteration_matching = {}
                            for edge in edges:
                                iteration_matching[edge[0]] = edge[1]
                            color_matchings[color] = iteration_matching
                            color_order.append(color)
                            
            # Display matchings in the order colors appeared
            for i, color in enumerate(color_order):
                matching = color_matchings[color]
                matching_text += f"Iteration {i+1}:\n"
                # Sort the matches for consistent display
                sorted_matches = []
                for left, right in matching.items():
                    try:
                        if isinstance(left, str) and isinstance(right, str):
                            left_label = f"L{left.split('_')[1]}" if '_' in left else left
                            right_label = f"R{right.split('_')[1]}" if '_' in right else right
                            sorted_matches.append((left_label, right_label))
                    except (IndexError, TypeError) as e:
                        print(f"Error processing matching {left}-{right}: {e}")
                sorted_matches.sort()
                
                for left, right in sorted_matches:
                    matching_text += f"{left}-{right}\n"
                matching_text += "\n"  # Add space between iterations
            
            # Don't use the sorted_edges_label which appears below the graph
            # Instead, create a dedicated label in the right sidebar
            
            # Clear existing matching groups label if it exists
            if hasattr(self, 'matching_groups_label'):
                self.right_sidebar_layout.removeWidget(self.matching_groups_label)
                self.matching_groups_label.deleteLater()
            
            # Add the new matching groups label to the right sidebar
            self.matching_groups_label = QLabel(matching_text)
            self.matching_groups_label.setWordWrap(True)
            self.matching_groups_label.setContentsMargins(5, 5, 5, 5)
            self.right_sidebar_layout.addWidget(self.matching_groups_label)
            
            # Make sure the sorted_edges_label is not visible
            if hasattr(self, 'sorted_edges_label'):
                self.sorted_edges_label.setVisible(False)
            
            # Create and show the explanation button if it doesn't exist
            if not hasattr(self, 'explanation_button'):
                self.explanation_button = QPushButton("Show Algorithm Explanation")
                self.explanation_button.clicked.connect(self.show_algorithm_explanation)
                self.explanation_button.setContentsMargins(0, 0, 0, 0)  # Remove margins
                self.right_sidebar_layout.addWidget(self.explanation_button)
            self.explanation_button.setVisible(True)

    def show_algorithm_explanation(self):
        explanation_window = AlgorithmExplanationWindow(self)
        explanation_window.exec_()

    def color_bipartite_graph_final(self):
        if isinstance(self.graph, nx.Graph) and nx.is_bipartite(self.graph):
            try:
                matching_states, edge_colors = self.colorer.maximal_matching_bipartite(self.graph)
                
                # Process all states to build up the final edge colors
                self.visualizer.final_edge_colors = {}  # Store in visualizer instead
                current_color = None
                iteration_matchings = {}
                color_order = []  # Keep track of color order
                
                # Process states to collect all edge colors
                for state in matching_states:
                    if isinstance(state, dict):
                        color = state["color"]
                        matching = state["matching"]
                        
                        # If this is a new color (new iteration)
                        if color != current_color:
                            if color not in color_order:  # Add color to order if new
                                color_order.append(color)
                            current_color = color
                            iteration_matchings[color] = matching
                        else:
                            # Update the matching for current color
                            iteration_matchings[color] = matching
                
                # Build final edge colors from iteration matchings
                for color, matching in iteration_matchings.items():
                    for left, right in matching.items():
                        self.visualizer.final_edge_colors[(left, right)] = color
                
                # Create matching text for display
                matching_text = "Matching Groups by Iteration:\n\n"
                for i, color in enumerate(color_order):
                    if color in iteration_matchings:
                        matching = iteration_matchings[color]
                        matching_text += f"Iteration {i+1}:\n"
                        # Sort the matches for consistent display
                        sorted_matches = sorted([
                            (f"L{left.split('_')[1]}", f"R{right.split('_')[1]}")
                            for left, right in matching.items()
                        ])
                        for left, right in sorted_matches:
                            matching_text += f"{left}-{right}\n"
                        matching_text += "\n"
                
                # Create a list of states for each iteration to be used by display_matching_groups
                self.iteration_states = []
                for color in color_order:
                    if color in iteration_matchings:
                        self.iteration_states.append({
                            "matching": iteration_matchings[color],
                            "color": color
                        })
                
                # Create the final state with all colors
                final_edge_colors = {}
                # Ensure we have the correct format (edge tuple -> color)
                for edge, color in edge_colors.items():
                    if isinstance(edge, tuple):
                        final_edge_colors[edge] = color
                    elif isinstance(color, str) and isinstance(edge, str):
                        # Handle string format if present
                        final_edge_colors[edge] = color
                
                self.matching_states = self.iteration_states + [{
                    "matching": final_edge_colors,  # Use properly formatted edge_colors
                    "augmenting_path": None,
                    "color": "final",
                    "show_all_colors": True
                }]
                
                self.current_step = len(self.matching_states) - 1  # Show the final state
                self.update_bipartite_visualization()
                self.visualizer.draw_execution_time(self.colorer.execution_time)
                
                # Hide navigation buttons
                self.prev_button.setVisible(False)
                self.next_button.setVisible(False)
                
                # Update and show matching groups
                self.display_matching_groups()
                
                # Display color classes
                self.display_color_classes(edge_colors)
                
                self.right_sidebar.setVisible(True)
                
            except Exception as e:
                print(f"Error in maximal_matching_bipartite: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("The current graph is not bipartite or no graph is loaded.")

    def display_algorithm_process(self, mode):
        # Create process title and steps in a single string
        if mode == "default":
            process_text = "Algorithm Process:\n\n"
            process_text += "1. The algorithm starts with the\n   vertex of highest degree\n"
            process_text += "2. Colors all edges connected to\n   this vertex\n"
            process_text += "3. Continues with the next vertex\n   of highest degree\n"
            process_text += "4. Repeats until all edges are\n   colored"
        elif mode == "user":
            process_text = "Algorithm Process:\n\n"
            process_text += "1. The algorithm follows the\n   user-defined order\n"
            process_text += "2. Colors edges in the sequence\n   they were created\n"
            process_text += "3. Assigns colors based on\n   availability\n"
            process_text += "4. Continues until all edges\n   are colored"
        elif mode == "degree":
            process_text = "Algorithm Process:\n\n"
            process_text += "1. The algorithm starts with the\n   vertex of highest degree\n"
            process_text += "2. Colors all edges connected to\n   this vertex\n"
            process_text += "3. Continues with the next vertex\n   of highest degree\n"
            process_text += "4. Ensures bipartite properties\n   are maintained\n"
            process_text += "5. Repeats until all edges are\n   colored"
        
        # Clear existing content if needed
        if hasattr(self, 'algorithm_combined'):
            self.right_sidebar_layout.removeWidget(self.algorithm_combined)
            self.algorithm_combined.deleteLater()
        
        # Create a single label with both title and content
        self.algorithm_combined = QLabel(process_text)
        self.algorithm_combined.setWordWrap(True)
        self.algorithm_combined.setContentsMargins(0, 0, 0, 0)
        self.right_sidebar_layout.addWidget(self.algorithm_combined)

    def display_color_classes(self, edge_colors):
        # Group edges by color
        color_groups = {}
        if not edge_colors:
            print("Warning: No edge colors provided to display_color_classes")
            # Try to get colors from the cumulative_edge_colors if available
            if hasattr(self, 'cumulative_edge_colors') and self.cumulative_edge_colors:
                print("Using cumulative_edge_colors as fallback")
                edge_colors = self.cumulative_edge_colors
            # Try to get colors from visualizer if available
            elif hasattr(self.visualizer, 'final_edge_colors') and self.visualizer.final_edge_colors:
                print("Using visualizer.final_edge_colors as fallback")
                edge_colors = self.visualizer.final_edge_colors
        
        # Now populate the color groups
        for edge, color in edge_colors.items():
            if color not in color_groups:
                color_groups[color] = []
            color_groups[color].append(edge)
        
        # Format text with header and content in one string
        color_text = "Color Classes:\n\n"
        if not color_groups:
            color_text += "No color classes to display.\n"
        else:
            for color, edges in color_groups.items():
                if color == 'gray':  # Skip gray (uncolored) edges
                    continue
                color_text += f"{color} = "
                formatted_edges = []
                for edge in edges:
                    # Format the edge for display
                    try:
                        formatted_edge = self.format_bipartite_edge(edge)
                        formatted_edges.append(formatted_edge)
                    except Exception as e:
                        print(f"Error formatting edge {edge}: {e}")
                color_text += ", ".join(formatted_edges)
                color_text += "\n"
        
        # Clear existing content if needed
        if hasattr(self, 'color_classes_combined'):
            self.right_sidebar_layout.removeWidget(self.color_classes_combined)
            self.color_classes_combined.deleteLater()
        
        # Create a single label with both title and content
        self.color_classes_combined = QLabel(color_text)
        self.color_classes_combined.setWordWrap(True)
        self.color_classes_combined.setContentsMargins(0, 0, 0, 0)
        self.right_sidebar_layout.addWidget(self.color_classes_combined)

        # Calculate maximum degree (∆)
        # For bipartite graphs, we need to be more careful about the degree calculation
        try:
            degrees = dict(self.graph.degree())
            if degrees:
                max_degree = max(degrees.values())
            else:
                max_degree = 0
                
            # For bipartite graphs, also check the maximum number of edges incident to any node
            if nx.is_bipartite(self.graph):
                # Get the maximum number of edges with the same color incident to any node
                node_color_counts = {}
                for edge, color in edge_colors.items():
                    if color != 'gray':  # Skip uncolored edges
                        u, v = edge
                        if u not in node_color_counts:
                            node_color_counts[u] = set()
                        if v not in node_color_counts:
                            node_color_counts[v] = set()
                        node_color_counts[u].add(color)
                        node_color_counts[v].add(color)
                
                if node_color_counts:
                    # The maximum degree is the max number of different colors at any node
                    color_degree = max(len(colors) for colors in node_color_counts.values())
                    max_degree = max(max_degree, color_degree)
        except Exception as e:
            print(f"Error calculating max degree: {e}")
            max_degree = 3  # Default to 3 if we can't calculate (typical for small bipartite graphs)
        
        # Count the actual colors used (excluding 'gray' which is used for uncolored edges)
        # and ensuring we count unique colors
        colors_used = len([c for c in color_groups.keys() if c != 'gray'])
        if colors_used == 0 and edge_colors:
            # Fallback: count unique colors in edge_colors
            colors_used = len(set([c for c in edge_colors.values() if c != 'gray']))
        
        # Create optimality message
        if colors_used > 0:
            if colors_used <= max_degree + 1:
                optimality_text = (f"The graph was colored with {colors_used} "
                                 f"colors which is ∆+1 ({max_degree}+1) or "
                                 f"less therefore the coloration was optimal")
            else:
                optimality_text = (f"The graph was colored with {colors_used} "
                                 f"colors which is more than ∆+1 ({max_degree}+1) "
                                 f"therefore there is a better coloration to this graph")
        else:
            optimality_text = "No colors have been applied yet."
        
        # Clear existing content if needed
        if hasattr(self, 'optimality_label'):
            self.right_sidebar_layout.removeWidget(self.optimality_label)
            self.optimality_label.deleteLater()
        
        # Create the optimality label
        self.optimality_label = QLabel(optimality_text)
        self.optimality_label.setWordWrap(True)
        self.optimality_label.setContentsMargins(0, 0, 0, 0)
        self.optimality_label.setStyleSheet("""
            QLabel {
                margin-top: 3px;
                padding: 5px;
                background-color: #f0f0f0;
                border-radius: 5px;
                font-weight: bold;
            }
        """)
        self.right_sidebar_layout.addWidget(self.optimality_label)

    def show_rearrange_button(self):
        # Clear existing button if needed
        if hasattr(self, 'rearrange_button'):
            self.right_sidebar_layout.removeWidget(self.rearrange_button)
            self.rearrange_button.deleteLater()
        
        # Create a new button
        self.rearrange_button = QPushButton("Rearrange Coloring Order")
        self.rearrange_button.clicked.connect(self.show_rearrange_dialog)
        self.rearrange_button.setContentsMargins(0, 0, 0, 0)
        self.right_sidebar_layout.addWidget(self.rearrange_button)

    def show_rearrange_dialog(self):
        current_edges = self.colorer.sorted_edges
        dialog = RearrangeOrderDialog(current_edges, self)
        if dialog.exec_() == QDialog.Accepted:
            # Update the edge order and recolor
            self.colorer.sorted_edges = dialog.new_edge_order
            
            # Determine if we're working with a bipartite graph
            is_bipartite = nx.is_bipartite(self.graph)
            
            if is_bipartite:
                # Use the bipartite coloring algorithm
                edge_colors = self.colorer.bipartite_user_order_coloring(self.graph)
                self.visualizer.draw_bipartite_degree_coloring(
                    self.graph,
                    edge_colors,
                    self.visualizer.positions
                )
            else:
                # Use the regular coloring algorithm
                edge_colors = self.colorer.sequential_user_order_coloring(self.graph)
                self.print(edge_colors)
            
            # Clear the layout first to ensure correct order
            self.clear_right_sidebar()
            
            # Re-add all widgets in the correct order
            self.display_sorted_edges()
            self.display_algorithm_process("user")
            self.display_color_classes(edge_colors)
            self.show_rearrange_button()  # Now this will be added at the end
            self.right_sidebar.setVisible(True)

    def clear_right_sidebar(self):
        # Remove all widgets from the layout
        while self.right_sidebar_layout.count():
            item = self.right_sidebar_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def color_bipartite_graph_degree_based(self):
        print("Starting degree-based coloring")
        if isinstance(self.graph, nx.Graph) and nx.is_bipartite(self.graph):
            try:
                print("Graph is bipartite")
                # Initialize colorer if not already done
                if not hasattr(self, 'colorer'):
                    self.colorer = GraphColorer(self.graph)
                
                # Color the graph using the degree-based algorithm
                edge_colors = self.colorer.bipartite_degree_coloring(self.graph)
                print(f"Coloring complete. Edge colors: {edge_colors}")
                
                # Update visualization using the new method
                self.visualizer.draw_bipartite_degree_coloring(
                    self.graph,
                    edge_colors,
                    self.visualizer.positions
                )
                
                # Update the right sidebar
                self.display_sorted_edges()
                self.display_algorithm_process("degree")
                self.display_color_classes(edge_colors)
                self.right_sidebar.setVisible(True)
                
            except Exception as e:
                print(f"Error in bipartite_degree_coloring: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("Graph is not bipartite or no graph is loaded")
            QMessageBox.warning(self, "Error", "The current graph is not bipartite or no graph is loaded.")

    def color_bipartite_graph_user_order(self):
        """Color bipartite graph edges based on user-defined creation order."""
        print("Starting user order bipartite coloring")
        if isinstance(self.graph, nx.Graph) and nx.is_bipartite(self.graph):
            try:
                print("Graph is bipartite")
                # Initialize colorer if not already done
                if not hasattr(self, 'colorer'):
                    self.colorer = GraphColorer(self.graph)
                
                # Get the edge creation order from the bipartite graph window
                if hasattr(self.bipartite_graph_window, 'edge_creation_order'):
                    # Transform the edge creation order to match the graph node format
                    transformed_edges = []
                    for u, v in self.bipartite_graph_window.edge_creation_order:
                        # Check if u is in left or right set
                        u_side = 'left' if u in self.bipartite_graph_window.nodes_left else 'right'
                        v_side = 'right' if v in self.bipartite_graph_window.nodes_right else 'left'
                        
                        # Add the appropriate prefix
                        transformed_u = f"{u_side}_{u}"
                        transformed_v = f"{v_side}_{v}"
                        
                        transformed_edges.append((transformed_u, transformed_v))
                    
                    print(f"Original edges: {self.bipartite_graph_window.edge_creation_order}")
                    print(f"Transformed edges: {transformed_edges}")
                    
                    # Apply user order coloring with transformed edges
                    self.colorer.sorted_edges = transformed_edges
                    edge_colors = self.colorer.bipartite_user_order_coloring(self.graph)
                    print(f"Coloring complete. Edge colors: {edge_colors}")
                    
                    # Update visualization
                    self.visualizer.draw_bipartite_degree_coloring(
                        self.graph,
                        edge_colors,
                        self.visualizer.positions
                    )
                    
                    # Clear the layout first to ensure correct order
                    self.clear_right_sidebar()
                    
                    # Update the right sidebar
                    self.display_sorted_edges()
                    self.display_algorithm_process("user")
                    self.display_color_classes(edge_colors)
                    self.show_rearrange_button()  # Now this will be added at the end
                    self.right_sidebar.setVisible(True)
                else:
                    print("No edge creation order found")
                    QMessageBox.warning(self, "Error", "No edge creation order available. Please create a bipartite graph first.")
                
            except Exception as e:
                print(f"Error in color_bipartite_graph_user_order: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("Graph is not bipartite or no graph is loaded")
            QMessageBox.warning(self, "Error", "The current graph is not bipartite or no graph is loaded.")
