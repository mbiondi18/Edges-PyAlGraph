import networkx as nx
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QMessageBox, QScrollArea, QGroupBox, QFrame
from PyQt5.QtCore import Qt
import os

class StatisticsWindow(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("Graph Coloring Statistics")
        self.setGeometry(300, 300, 650, 700)
        
        # Apply dark theme styling
        self.setStyleSheet("""
            QWidget {
                background-color: #3a3a3a;
                color: white;
            }
            QGroupBox {
                border: 1px solid #555555;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                padding: 0 3px;
                color: #4a86e8;
            }
            QPushButton {
                background-color: #555555;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #666666;
            }
            QTextEdit {
                background-color: #444444;
                color: white;
                border: 1px solid #555555;
                border-radius: 4px;
            }
            QLabel {
                padding: 2px;
            }
            QScrollArea {
                border: none;
            }
        """)

        # Create a scroll area for the content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Create the main container widget
        container = QWidget()
        self.layout = QVBoxLayout(container)
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(15, 15, 15, 15)
        
        # Create a header section with key stats
        header_group = QGroupBox("Performance Metrics")
        header_layout = QVBoxLayout()
        
        self.execution_time_label = QLabel(f"Execution Time: {self.app.colorer.execution_time:.6f} seconds")
        header_layout.addWidget(self.execution_time_label)
        
        self.colors_used_label = QLabel(f"Number of Colors Used: {self.get_colors_used()}")
        header_layout.addWidget(self.colors_used_label)
        
        self.algorithm_label = QLabel(f"Algorithm Used: {self.get_algorithm_used()}")
        header_layout.addWidget(self.algorithm_label)
        
        header_group.setLayout(header_layout)
        self.layout.addWidget(header_group)
        
        # Create a graph connections section
        connections_group = QGroupBox("Graph Connections")
        connections_layout = QVBoxLayout()
        
        self.connections_text = QTextEdit()
        self.connections_text.setPlainText(self.get_connections())
        self.connections_text.setReadOnly(True)
        self.connections_text.setMaximumHeight(150)
        connections_layout.addWidget(self.connections_text)
        
        connections_group.setLayout(connections_layout)
        self.layout.addWidget(connections_group)
        
        # Edge sorting information
        edges_group = QGroupBox("Edge Processing Order")
        edges_layout = QVBoxLayout()
        
        self.sorted_edges_label = QLabel(self.get_sorted_edges())
        self.sorted_edges_label.setWordWrap(True)
        edges_layout.addWidget(self.sorted_edges_label)
        
        edges_group.setLayout(edges_layout)
        self.layout.addWidget(edges_group)
        
        # Color distribution information
        color_group = QGroupBox("Color Distribution")
        color_layout = QVBoxLayout()
        
        self.color_distribution_label = QLabel(self.get_color_distribution())
        self.color_distribution_label.setWordWrap(True)
        color_layout.addWidget(self.color_distribution_label)
        
        color_group.setLayout(color_layout)
        self.layout.addWidget(color_group)
        
        # Add matching statistics
        self.add_matching_statistics()
        
        # Add export button at the bottom
        self.import_button = QPushButton('Export Statistics', self)
        self.import_button.setMinimumHeight(40)
        self.import_button.clicked.connect(self.import_statistics)
        self.layout.addWidget(self.import_button)
        
        # Set the container as the scroll area widget
        scroll.setWidget(container)
        
        # Main layout for the window
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
        
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
                try:
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
                    
                    if connections:
                        return "\n".join(sorted(connections))
                    else:
                        return "No connection data available"
                except Exception as e:
                    # Instead of showing the technical error, display a generic message
                    print(f"Debug - Bipartite graph error: {str(e)}")
                    return "No valid data available for this graph structure"
            else:
                connections = [f"{u}-{v}" for u, v in self.app.graph.edges()]
                if connections:
                    return "\n".join(sorted(connections))
                else:
                    return "No connections in graph"
        return "No graph available"

    def import_statistics(self):
        filename = 'graph_statistics.txt'
        try:
            with open(filename, 'w') as f:
                f.write(f"{self.execution_time_label.text()}\n")
                f.write(f"{self.colors_used_label.text()}\n")
                f.write(f"{self.algorithm_label.text()}\n")
                f.write("Graph Connections:\n")
                f.write(self.connections_text.toPlainText())
                f.write("\n\nEdge Processing Order:\n")
                f.write(self.get_sorted_edges())
            
            abs_path = os.path.abspath(filename)
            QMessageBox.information(self, "Statistics Exported", f"Statistics have been exported to:\n{abs_path}")
        except IOError as e:
            QMessageBox.warning(self, "Error", f"An error occurred while writing the file:\n{str(e)}")

    def get_sorted_edges(self):
        if hasattr(self.app.colorer, 'sorted_edges') and self.app.colorer.sorted_edges:
            try:
                edges = [f"{u}-{v}" for u, v in self.app.colorer.sorted_edges]
                if edges:
                    return "\n".join(edges)
                return "No edge processing order available"
            except Exception as e:
                print(f"Debug - Error displaying sorted edges: {str(e)}")
                return "No valid edge processing data available"
        return "No edge processing order available"

    def add_matching_statistics(self):
        """Add statistics about bipartite matching iterations."""
        # Create a group box for matching statistics
        matching_group = QGroupBox("Bipartite Matching Statistics")
        matching_layout = QVBoxLayout()
        
        # First check if this is a bipartite graph
        if not hasattr(self.app, 'graph') or not nx.is_bipartite(self.app.graph):
            message_label = QLabel("No bipartite matching data available for this graph type.")
            message_label.setStyleSheet("padding: 10px;")
            matching_layout.addWidget(message_label)
            matching_group.setLayout(matching_layout)
            self.layout.addWidget(matching_group)
            return
        
        # Process matching states to extract matching data by iteration
        if hasattr(self.app, 'matching_states') and self.app.matching_states:
            # Track the last seen matching for each iteration color
            color_matchings = {}
            color_order = []  # Keep track of the order colors appear
            
            try:
                # Process states in order, keeping only the last matching for each color
                for state in self.app.matching_states:
                    if isinstance(state, dict) and "matching" in state:
                        color = state.get("color")
                        
                        # Skip the final state or states without color
                        if color is None or color == "final" or state.get("show_all_colors", False):
                            continue
                        
                        if color not in color_matchings:
                            color_matchings[color] = state["matching"]
                            color_order.append(color)  # Add color to order list when first seen
                        else:
                            # Update with the last matching for this color
                            color_matchings[color] = state["matching"]
                
                # If no iterations were found, show a message
                if not color_order:
                    message_label = QLabel("No iteration data available for this graph.")
                    message_label.setStyleSheet("padding: 10px;")
                    matching_layout.addWidget(message_label)
                else:
                    # Display matchings in the order colors appeared
                    for i, color in enumerate(color_order):
                        matching = color_matchings[color]
                        
                        # Add iteration header with color
                        iteration_label = QLabel(f"<b>Iteration {i+1} ({color}):</b>")
                        matching_layout.addWidget(iteration_label)
                        
                        # Sort the matches for consistent display
                        try:
                            sorted_matches = []
                            for left, right in matching.items():
                                if isinstance(left, str) and isinstance(right, str):
                                    left_label = f"L{left.split('_')[1]}" if '_' in left else left
                                    right_label = f"R{right.split('_')[1]}" if '_' in right else right
                                    sorted_matches.append((left_label, right_label))
                            sorted_matches.sort()
                            
                            if not sorted_matches:
                                no_matches = QLabel("    No valid matches in this iteration")
                                matching_layout.addWidget(no_matches)
                            else:
                                # Add each match as a separate label
                                for left, right in sorted_matches:
                                    match_label = QLabel(f"    {left}-{right}")
                                    matching_layout.addWidget(match_label)
                        except Exception as e:
                            print(f"Debug - Error processing matches: {str(e)}")
                            error_label = QLabel("    Cannot display matches for this iteration")
                            matching_layout.addWidget(error_label)
                        
                        # Add some spacing between iterations
                        spacer = QLabel("")
                        matching_layout.addWidget(spacer)
            except Exception as e:
                print(f"Debug - Error in bipartite matching statistics: {str(e)}")
                message_label = QLabel("Unable to process matching data for this graph structure.")
                message_label.setStyleSheet("padding: 10px;")
                matching_layout.addWidget(message_label)
        else:
            message_label = QLabel("No bipartite matching data has been generated yet.")
            message_label.setStyleSheet("padding: 10px;")
            matching_layout.addWidget(message_label)
        
        matching_group.setLayout(matching_layout)
        self.layout.addWidget(matching_group)

    def get_color_distribution(self):
        try:
            if not hasattr(self.app.colorer, 'color_counts') or not self.app.colorer.color_counts:
                return "No color distribution data available"
            
            distribution = []
            for color, count in self.app.colorer.color_counts.items():
                if color != "None":  # Skip uncolored nodes
                    distribution.append(f"{color}: {count}")
            
            if distribution:
                return "\n".join(distribution)
            return "No color distribution data available"
        except Exception as e:
            print(f"Debug - Error displaying color distribution: {str(e)}")
            return "Unable to process color distribution data"