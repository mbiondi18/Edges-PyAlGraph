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
        edge_colors = {}

        def edge_weight(edge):
            return graph.degree(edge[0]) + graph.degree(edge[1])

        # Sort edges based on the sum of degrees of incident vertices (descending order)
        self.sorted_edges = sorted(edges, key=edge_weight, reverse=True)

        for u, v in self.sorted_edges:
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
        self.algorithm_used = "Sequential Coloring with Degree Ordering"
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


    def maximal_matching_bipartite(self, graph: nx.Graph):
        start_time = time.perf_counter()
        
        left_nodes, right_nodes = nx.bipartite.sets(graph)
        print("Left nodes:", left_nodes)
        print("Right nodes:", right_nodes)
        
        matching = {}
        matching_states = []

        # Initial greedy matching
        for left in left_nodes:
            for right in graph.neighbors(left):
                if left not in matching and right not in matching.values():
                    matching[left] = right
                    break
        
        print("Initial matching:", matching)
        matching_states.append({"matching": matching.copy(), "augmenting_path": None})

        while True:
            path = self.find_augmenting_path(graph, matching, left_nodes, right_nodes)
            if not path:
                break
            
            print("Augmenting path found:", path)
            
            # Store the state with the augmenting path
            matching_states.append({"matching": matching.copy(), "augmenting_path": path})
            
            # Update the matching
            for i in range(0, len(path), 2):
                left, right = path[i], path[i+1]
                if left in matching:
                    del matching[left]
                if right in matching.values():
                    del matching[list(matching.keys())[list(matching.values()).index(right)]]
                matching[left] = right
            
            print("Updated matching:", matching)
            
        # Add the final matching state without an augmenting path
        matching_states.append({"matching": matching.copy(), "augmenting_path": None})
        
        end_time = time.perf_counter()
        self.execution_time = end_time - start_time
        self.colors_used = len(set(matching.values()))
        self.algorithm_used = "Augmenting Path Algorithm"
        
        return matching_states

    def find_augmenting_path(self, graph, matching, left_nodes, right_nodes):
        queue = [(left, [left]) for left in left_nodes if left not in matching]
        visited = set()
        
        while queue:
            node, path = queue.pop(0)
            if node not in visited:
                visited.add(node)
                
                if node in right_nodes and node not in matching.values():
                    return path
                
                neighbors = set(graph.neighbors(node)) - visited
                for neighbor in neighbors:
                    if (node in matching and neighbor != matching[node]) or (node not in matching):
                        new_path = path + [neighbor]
                        queue.append((neighbor, new_path))
        
        return None

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
