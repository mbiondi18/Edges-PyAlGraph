import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import networkx as nx

class GraphVisualizer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure()
        self.figure.set_size_inches(10, 8)
        self.canvas = FigureCanvas(self.figure)
        self.label = QLabel(self)
        self.step_label = QLabel(self)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.label)
        layout.addWidget(self.step_label)
        self.setLayout(layout)
        self.positions = None

    def create_graph(self, graph):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        if self.positions is None:
            self.positions = nx.spring_layout(graph, k=0.5, iterations=50)
        
        # Draw nodes with white background and black border
        nx.draw_networkx_nodes(graph, self.positions, ax=ax,
                          node_color='white',
                          edgecolors='black',
                          node_size=500)  # Increased node size
        
        # Draw edges
        nx.draw_networkx_edges(graph, self.positions, ax=ax)
        
        # Draw labels in black
        labels = {node: str(node) for node in graph.nodes()}
        nx.draw_networkx_labels(graph, self.positions, labels, ax=ax,
                          font_size=8,
                          font_color='black')
        
        ax.set_title("Graph")
        ax.set_axis_off()
        # Set fixed limits to maintain consistent size
        #ax.set_xlim(-1.2, 1.2)
        #ax.set_ylim(-1.2, 1.2)
        self.figure.tight_layout()
        self.canvas.draw()

    def draw_graph(self, graph, edge_colors):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        if self.positions is None:
            self.positions = nx.spring_layout(graph)
        
        # Draw nodes with white background and black border
        nx.draw_networkx_nodes(graph, self.positions, ax=ax, 
                              node_color='white', 
                              edgecolors='black',
                              node_size=300)
        
        for edge, color in edge_colors.items():
            nx.draw_networkx_edges(graph, self.positions, edgelist=[edge], edge_color=color, ax=ax)
        
        # Modified this part to handle both string and integer node labels
        labels = {}
        for node in graph.nodes():
            if isinstance(node, str) and '_' in node:
                labels[node] = node.split('_')[1]
            else:
                labels[node] = str(node)

        nx.draw_networkx_labels(graph, self.positions, labels, ax=ax, font_size=8)
        
        ax.set_title("Graph Coloring")
        ax.set_axis_off()
        self.figure.tight_layout()
        self.canvas.draw()

    def draw_execution_time(self, execution_time):
        formatted_time = f"{execution_time:.10f}".rstrip('0').rstrip('.')
        self.label.setText(f"Tiempo de ejecución: {formatted_time} segundos")

    def create_bipartite_graph(self, graph):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        left_nodes = [n for n, d in graph.nodes(data=True) if d['bipartite'] == 0]
        right_nodes = [n for n, d in graph.nodes(data=True) if d['bipartite'] == 1]
        
        max_count = max(len(left_nodes), len(right_nodes))
        
        pos = {}
        for i, node in enumerate(left_nodes):
            pos[node] = (-0.45, 1 - (i / (max_count - 1)) if max_count > 1 else 0.5)
        for i, node in enumerate(right_nodes):
            pos[node] = (0.45, 1 - (i / (max_count - 1)) if max_count > 1 else 0.5)

        nx.draw_networkx_nodes(graph, pos, nodelist=left_nodes, node_color='r', ax=ax, node_size=300)
        nx.draw_networkx_nodes(graph, pos, nodelist=right_nodes, node_color='b', ax=ax, node_size=300)

        nx.draw_networkx_edges(graph, pos, ax=ax, edge_color='gray', width=0.5)

        labels = {node: node.split('_')[1] for node in graph.nodes()}
        nx.draw_networkx_labels(graph, pos, labels, ax=ax, font_size=10, font_color='white')

        ax.set_axis_off()
        ax.set_xlim(-0.5, 0.5)
        ax.set_ylim(-0.05, 1.05)

        self.figure.tight_layout()
        self.canvas.draw()
        self.positions = pos

    def draw_bipartite_graph(self, graph, edge_colors, pos=None):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        if pos is None:
            pos = self.positions
        
        left_nodes = [n for n, d in graph.nodes(data=True) if d['bipartite'] == 0]
        right_nodes = [n for n, d in graph.nodes(data=True) if d['bipartite'] == 1]
        
        nx.draw_networkx_nodes(graph, pos, nodelist=left_nodes, node_color='r', ax=ax, node_size=300)
        nx.draw_networkx_nodes(graph, pos, nodelist=right_nodes, node_color='b', ax=ax, node_size=300)
        
        edge_colors_list = [edge_colors.get(edge, 'gray') for edge in graph.edges()]
        nx.draw_networkx_edges(graph, pos, ax=ax, edge_color=edge_colors_list, width=2.0)
        
        labels = {node: node.split('_')[1] for node in graph.nodes()}
        nx.draw_networkx_labels(graph, pos, labels, ax=ax, font_size=10, font_color='white')

        ax.set_axis_off()
        ax.set_xlim(-0.5, 0.5)
        ax.set_ylim(-0.05, 1.05)  # Adjusted to show full graph with a small margin

        self.figure.tight_layout()
        self.canvas.draw()
        self.positions = pos

    def draw_bipartite_matching(self, graph, assignments, unassigned_left, unassigned_right, pos, augmenting_path=None):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        left_nodes = [n for n in graph.nodes() if n.startswith('left_')]
        right_nodes = [n for n in graph.nodes() if n.startswith('right_')]

        # Adjust node positions
        max_nodes = max(len(left_nodes), len(right_nodes))
        for i, node in enumerate(left_nodes):
            pos[node] = (-0.35, 1 - (i / (max_nodes - 1)) if max_nodes > 1 else 0.5)
        for i, node in enumerate(right_nodes):
            pos[node] = (0.35, 1 - (i / (max_nodes - 1)) if max_nodes > 1 else 0.5)

        # Draw nodes
        node_size = 1000
        nx.draw_networkx_nodes(graph, pos, nodelist=left_nodes, node_color='lightblue', ax=ax, node_size=node_size)
        nx.draw_networkx_nodes(graph, pos, nodelist=right_nodes, node_color='lightgreen', ax=ax, node_size=node_size)
        nx.draw_networkx_nodes(graph, pos, nodelist=list(unassigned_left) + list(unassigned_right), node_color='red', ax=ax, node_size=node_size)

        # Draw edges
        all_edges = list(graph.edges())
        matched_edges = [(left, right) for left, right in assignments.items()]
        unmatched_edges = [edge for edge in all_edges if edge not in matched_edges and edge[::-1] not in matched_edges]

        # Draw unmatched edges
        nx.draw_networkx_edges(graph, pos, edgelist=unmatched_edges, edge_color='gray', style='dashed', ax=ax, width=1.0)

        if augmenting_path:
            # Create path edges
            path_edges = list(zip(augmenting_path[:-1], augmenting_path[1:]))
            
            # Separate matched edges into those in the augmenting path and those not
            matched_edges_in_path = [edge for edge in matched_edges if edge in path_edges or edge[::-1] in path_edges]
            matched_edges_not_in_path = [edge for edge in matched_edges if edge not in matched_edges_in_path and edge[::-1] not in matched_edges_in_path]
            
            # Draw matched edges not in path
            nx.draw_networkx_edges(graph, pos, edgelist=matched_edges_not_in_path, edge_color='r', ax=ax, width=2.0)
            
            # Draw augmenting path with blue dotted lines first
            nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color='b', ax=ax, width=1.5, style='--')
            
            # Draw matched edges in path with orange color last (on top)
            nx.draw_networkx_edges(graph, pos, edgelist=matched_edges_in_path, edge_color='orange', ax=ax, width=3.5)
        else:
            # Draw all matched edges in red if no augmenting path
            nx.draw_networkx_edges(graph, pos, edgelist=matched_edges, edge_color='r', ax=ax, width=2.0)

        # Draw labels
        labels = {node: node.split('_')[1] for node in graph.nodes()}
        for node, (x, y) in pos.items():
            label = labels[node]
            ax.text(x, y, label, fontsize=14, ha='center', va='center', color='black', fontweight='bold')

        ax.set_title("Bipartite Matching", fontsize=16)
        ax.set_axis_off()
        ax.set_xlim(-0.5, 0.5)
        ax.set_ylim(-0.1, 1.1)

        # Update legend
        ax.plot([], [], 'o', color='lightblue', label='Left Nodes', markersize=10)
        ax.plot([], [], 'o', color='lightgreen', label='Right Nodes', markersize=10)
        ax.plot([], [], 'o', color='red', label='Unassigned Nodes', markersize=10)
        ax.plot([], [], '-r', label='Matched Edges', linewidth=2)
        ax.plot([], [], '--', color='gray', label='Unmatched Edges', linewidth=1)
        if augmenting_path:
            ax.plot([], [], '-', color='orange', label='Previous Matching in Path', linewidth=2.5)
            ax.plot([], [], '--b', label='Augmenting Path', linewidth=2)
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=12)

        # Add augmenting path text description
        if augmenting_path:
            path_description = " → ".join(f"{'L' if node.startswith('left') else 'R'}{node.split('_')[1]}" for node in augmenting_path)
            ax.text(0, -0.1, f"Augmenting Path: {path_description}", ha='center', va='center', fontsize=12, fontweight='bold')

        self.figure.tight_layout()
        self.canvas.draw()

    def update_step_info(self, current_step, total_steps):
        self.step_label.setText(f"Step: {current_step}/{total_steps}")

    def get_graph_layout(self, graph):
        if self.positions is None:
            self.positions = nx.spring_layout(graph)
        return self.positions




