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
        self.edge_colors = {}  # Store edge colors as class attribute

        def edge_weight(edge):
            return graph.degree(edge[0]) + graph.degree(edge[1])

        # Sort edges based on the sum of degrees of incident vertices (descending order)
        self.sorted_edges = sorted(edges, key=edge_weight, reverse=True)

        for u, v in self.sorted_edges:
            available_colors = [True] * len(colors)

            # Check colors of adjacent edges
            for w in graph.neighbors(u):
                edge = (u, w) if u < w else (w, u)
                if edge in self.edge_colors:
                    color_index = colors.index(self.edge_colors[edge])
                    available_colors[color_index] = False
            for w in graph.neighbors(v):
                edge = (v, w) if v < w else (w, v)
                if edge in self.edge_colors:
                    color_index = colors.index(self.edge_colors[edge])
                    available_colors[color_index] = False

            # Assign the first available color
            for i, is_available in enumerate(available_colors):
                if is_available:
                    edge_color = colors[i]
                    self.edge_colors[(u, v)] = edge_color
                    break

        end_time = time.time()
        self.execution_time = end_time - start_time
        self.colors_used = len(set(self.edge_colors.values()))
        self.algorithm_used = "Sequential Coloring with Degree Ordering"
        return self.edge_colors
    
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
        matching_states = []
        edge_colors = {}
        color_index = 0

        while True:
            matching = {}
            # Initial greedy matching
            for left in left_nodes:
                for right in graph.neighbors(left):
                    if left not in matching and right not in matching.values():
                        matching[left] = right
                        break
            
            if not matching:
                break

            matching_states.append({"matching": matching.copy(), "augmenting_path": None, "color": colors[color_index]})

            while True:
                path = self.find_augmenting_path(graph, matching, left_nodes, right_nodes)
                if not path:
                    break
                
                matching_states.append({"matching": matching.copy(), "augmenting_path": path, "color": colors[color_index]})
                
                # Update the matching
                for i in range(0, len(path), 2):
                    left, right = path[i], path[i+1]
                    if left in matching:
                        del matching[left]
                    if right in matching.values():
                        del matching[list(matching.keys())[list(matching.values()).index(right)]]
                    matching[left] = right
            
            matching_states.append({"matching": matching.copy(), "augmenting_path": None, "color": colors[color_index]})
            
            # Color the matched edges
            for left, right in matching.items():
                edge_colors[(left, right)] = colors[color_index]
            
            color_index += 1

            # Remove matched edges from the graph
            for left, right in matching.items():
                graph.remove_edge(left, right)
            
            if not graph.edges():
                break
        
        end_time = time.perf_counter()
        self.execution_time = end_time - start_time
        self.colors_used = color_index
        self.algorithm_used = "Augmenting Path Algorithm"
        
        return matching_states, edge_colors

    def find_augmenting_path(self, graph, matching, left_nodes, right_nodes):
        all_augmenting_paths = []
        queue = [(left, [left]) for left in left_nodes if left not in matching]
        visited_per_path = {left: {left} for left in left_nodes if left not in matching}
        
        while queue:
            node, path = queue.pop(0)
            visited = visited_per_path[path[0]]
            
            if node in right_nodes and node not in matching.values():
                all_augmenting_paths.append(path)
                continue
            
            neighbors = set(graph.neighbors(node)) - visited
            for neighbor in neighbors:
                if (node in matching and neighbor != matching[node]) or (node not in matching):
                    new_path = path + [neighbor]
                    new_visited = visited_per_path[path[0]].copy()
                    new_visited.add(neighbor)
                    visited_per_path[path[0]] = new_visited
                    queue.append((neighbor, new_path))
        
        if not all_augmenting_paths:
            return None
        
        # Return the shortest augmenting path
        shortest_path = min(all_augmenting_paths, key=len)
        print(f"Found {len(all_augmenting_paths)} augmenting paths. Choosing shortest: {shortest_path}")
        return shortest_path

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
