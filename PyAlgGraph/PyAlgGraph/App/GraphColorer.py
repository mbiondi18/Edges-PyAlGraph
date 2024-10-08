import networkx as nx
import time

colors = ["Red", "Green", "Blue", "Yellow", "Orange", "Violet", "Brown", "Gray", "Black", "White", "Pink", "Cyan", "Magenta", "Lime", "Teal", "Indigo", "Maroon", "Olive", "Navy", "Purple", "Silver", "Aqua", "Fuchsia", "WhiteSmoke", "AliceBlue", "AntiqueWhite", "Azure", "Beige", "Bisque", "BlanchedAlmond", "BurlyWood", "Coral", "CornflowerBlue", "Cornsilk", "Crimson", "DarkGoldenRod", "DarkKhaki", "DarkOrange", "DarkOrchid", "DarkSalmon", "DarkSeaGreen", "DarkTurquoise", "DarkViolet", "DeepPink", "DeepSkyBlue", "DimGray", "DodgerBlue", "FireBrick", "FloralWhite", "ForestGreen", "Gainsboro", "GhostWhite", "Gold", "GoldenRod", "GreenYellow", "HoneyDew", "HotPink", "IndianRed", "Ivory", "Khaki", "Lavender", "LavenderBlush", "LawnGreen", "LemonChiffon", "LightBlue", "LightCoral", "LightCyan", "LightGoldenRodYellow", "LightGray", "LightGreen", "LightPink", "LightSalmon", "LightSeaGreen", "LightSkyBlue", "LightSlateGray", "LightSteelBlue", "LightYellow", "LimeGreen", "Linen", "MediumAquaMarine", "MediumOrchid", "MediumPurple", "MediumSeaGreen", "MediumSlateBlue", "MediumSpringGreen", "MediumTurquoise", "MediumVioletRed", "MintCream", "MistyRose", "Moccasin", "NavajoWhite", "OldLace", "OrangeRed", "Orchid", "PaleGoldenRod", "PaleGreen", "PaleTurquoise", "PaleVioletRed", "PapayaWhip", "PeachPuff", "Peru", "Pink", "Plum", "PowderBlue", "RosyBrown", "RoyalBlue", "SaddleBrown", "Salmon", "SandyBrown", "SeaGreen", "SeaShell", "Sienna", "SkyBlue", "SlateBlue", "SlateGray", "Snow", "SpringGreen", "SteelBlue"]

class GraphColorer:

    def __init__(self, graph: nx.Graph):
        self.execution_time = 0
        self.color = {}
        self.dsatur = {}


    def secuencial_coloring(self, graph: nx.Graph, edges: list):
        start_time = time.time()
        # Diccionario para guardar el color asignado a cada arista
        edge_colors = {}

        for u, v in edges:
            print("Edge: ", (u, v))
            available_colors = [True] * len(colors)

            # Verificar colores de aristas adyacentes
            for w in graph.neighbors(u):
                edge = (u, w) if u < w else (w, u)
                if edge in edge_colors:
                    color_index = colors.index(edge_colors[edge])
                    available_colors[color_index] = False
            for w in graph.neighbors(v):
                edge = (v, w) if (v, w) in edge_colors else (w, v)
                if edge in edge_colors:
                    color_index = colors.index(edge_colors[edge])
                    available_colors[color_index] = False

            # Assign the first available color
            for i, is_available in enumerate(available_colors):
                if is_available:
                    edge_color = colors[i]
                    edge_colors[(u, v)] = edge_color
                    break
        print("Greedy Coloring edge colors: ", edge_colors)
        end_time = time.time()
        self.execution_time = end_time - start_time
        print("Execution time: ", self.execution_time, " seconds")
        self.colors_used = len(set(edge_colors.values()))
        self.algorithm_used = "Sequential Coloring"
        return edge_colors
    
    def bipartite_coloring(self, graph: nx.Graph):
        start_time = time.time()
        left_nodes = {n for n, d in graph.nodes(data=True) if d['bipartite'] == 0}
        right_nodes = set(graph) - left_nodes

        edge_colors = {}
        for left_node in left_nodes:
            available_colors = set(colors)
            for neighbor in graph[left_node]:
                if (left_node, neighbor) in edge_colors:
                    available_colors.discard(edge_colors[(left_node, neighbor)])
                elif (neighbor, left_node) in edge_colors:
                    available_colors.discard(edge_colors[(neighbor, left_node)])
            
            for neighbor in graph[left_node]:
                if (left_node, neighbor) not in edge_colors and (neighbor, left_node) not in edge_colors:
                    edge_color = min(available_colors, key=lambda c: sum(graph.nodes[n]['weight'] for n in [left_node, neighbor]))
                    edge_colors[(left_node, neighbor)] = edge_color
                    available_colors.discard(edge_color)

        end_time = time.time()
        self.execution_time = end_time - start_time
        print("Execution time: ", self.execution_time, " seconds")
        self.colors_used = len(set(edge_colors.values()))
        self.algorithm_used = "Bipartite Coloring"
        return edge_colors


    def maximal_matching_bipartite(self, graph: nx.Graph, iterations=100):
        total_time = 0
        for _ in range(iterations):
            start_time = time.perf_counter()
            
            left_nodes, right_nodes = nx.bipartite.sets(graph)
            matching = set()
            self.assignments = {}

            for left_node in left_nodes:
                for right_node in graph.neighbors(left_node):
                    if right_node not in self.assignments.values():
                        self.assignments[left_node] = right_node
                        matching.add((left_node, right_node))
                        break

            unassigned_left = set(left_nodes) - set(self.assignments.keys())
            unassigned_right = set(right_nodes) - set(self.assignments.values())

            end_time = time.perf_counter()
            total_time += (end_time - start_time)

        self.execution_time = total_time / iterations
        print(f"Average execution time over {iterations} iterations: {self.execution_time:.6f} seconds")
        self.colors_used = len(set(self.assignments.values()))
        self.algorithm_used = "Maximal Pairing Algorithm"
        return self.assignments, unassigned_left, unassigned_right

    def sequential_user_order_coloring(self, graph: nx.Graph):
        start_time = time.perf_counter()
        edge_colors = {}
        ordered_edges = sorted(graph.edges(data=True), key=lambda x: x[2]['order'])

        for u, v, _ in ordered_edges:
            available_colors = [True] * len(colors)

            for w in graph.neighbors(u):
                edge = (u, w) if u < w else (w, u)
                if edge in edge_colors:
                    color_index = colors.index(edge_colors[edge])
                    available_colors[color_index] = False
            for w in graph.neighbors(v):
                edge = (v, w) if v < w else (w, v)
                if edge in edge_colors:
                    color_index = colors.index(edge_colors[edge])
                    available_colors[color_index] = False

            for i, is_available in enumerate(available_colors):
                if is_available:
                    edge_color = colors[i]
                    edge_colors[(u, v)] = edge_color
                    break

        end_time = time.perf_counter()
        self.execution_time = end_time - start_time
        self.colors_used = len(set(edge_colors.values()))
        self.algorithm_used = "Sequential User Order Coloring"
        return edge_colors
