# PyAlgGraph Class Diagram

```mermaid
classDiagram
    %% Main classes
    class App {
        +graph: networkx.Graph
        +analyzer: GraphAnalyzer
        +colorer: GraphColorer
        +__init__()
        +open_graph_window()
        +open_bipartite_graph_window()
        +create_graph()
        +create_bipartite_graph()
        +secuencial_coloring()
        +bipartite_coloring()
        +color_bipartite_graph()
        +show_statistics()
        +show_algorithm_explanation()
    }

    class GraphVisualizer {
        +figure: Figure
        +canvas: FigureCanvas
        +positions: dict
        +__init__()
        +create_graph()
        +draw_graph()
        +create_bipartite_graph()
        +draw_bipartite_graph()
        +draw_bipartite_matching()
        +draw_bipartite_degree_coloring()
        +update_step_info()
    }

    class GraphColorer {
        +execution_time: float
        +color: dict
        +dsatur: dict
        +edge_colors: dict
        +__init__(graph)
        +secuencial_coloring(graph, edges)
        +bipartite_coloring(graph)
        +bipartite_degree_coloring(graph)
        +maximal_matching_bipartite(graph)
        +find_augmenting_path(graph, matching, left_nodes, right_nodes)
        +sequential_user_order_coloring(graph)
        +bipartite_user_order_coloring(graph, edge_order)
    }

    class GraphWindow {
        +app: App
        +graph: networkx.Graph
        +__init__(app, graph)
        +add_vertex_mode()
        +add_edge_mode()
        +delete_mode()
        +create_graph()
        +mousePressEvent(event)
    }

    class BipartiteGraphWindow {
        +app: App
        +graph: networkx.DiGraph
        +edge_creation_order: list
        +nodes_left: dict
        +nodes_right: dict
        +__init__(app, graph, parent)
        +add_vertex_left_mode()
        +add_vertex_right_mode()
        +add_edge_mode()
        +delete_mode()
        +create_bipartite_graph()
        +get_positions()
        +mousePressEvent(event)
        +handle_vertex_mode(event, is_left)
        +handle_edge_mode(event)
        +handle_delete_mode(event)
    }

    class StatisticsWindow {
        +app: App
        +__init__(app)
        +get_colors_used()
        +get_algorithm_used()
        +get_connections()
        +import_statistics()
        +get_sorted_edges()
        +update_statistics()
        +add_matching_statistics()
    }

    class AlgorithmExplanationWindow {
        +algorithm_text: str
        +__init__(text)
    }

    %% Utility classes
    class GraphAnalyzer {
        +__init__()
    }

    class GraphIO {
        +__init__()
    }

    class StepByStepSolver {
        +__init__()
    }

    class Tutorial {
        +__init__()
    }

    class UserOrderDialog {
        +__init__()
    }

    class RearrangeOrderDialog {
        +__init__()
    }

    class WeightDialog {
        +__init__()
    }

    %% Relationships
    App "1" *-- "1" GraphColorer : contains
    App "1" *-- "1" GraphAnalyzer : contains
    App "1" *-- "1" GraphVisualizer : uses
    App "1" o-- "*" GraphWindow : creates
    App "1" o-- "*" BipartiteGraphWindow : creates
    App "1" o-- "1" StatisticsWindow : creates
    App "1" o-- "1" AlgorithmExplanationWindow : creates
    App "1" o-- "1" UserOrderDialog : uses
    App "1" o-- "1" RearrangeOrderDialog : uses
    
    GraphWindow "*" --> "1" App : references
    BipartiteGraphWindow "*" --> "1" App : references
    StatisticsWindow "1" --> "1" App : references
    
    GraphColorer --> GraphVisualizer : provides data to
    
    BipartiteGraphWindow --> GraphVisualizer : uses for display
    GraphWindow --> GraphVisualizer : uses for display
```

The class diagram shows the main architectural components of the PyAlgGraph application and how they relate to each other. The key classes are:

- **App**: Central controller class that manages the application flow
- **GraphColorer**: Handles graph coloring algorithms
- **GraphVisualizer**: Manages the visual representation of graphs
- **BipartiteGraphWindow** and **GraphWindow**: UI components for graph creation
- **StatisticsWindow**: Displays coloring statistics
- **AlgorithmExplanationWindow**: Shows algorithm explanations

The relationships shown include:
- Composition relationships (solid diamond)
- Association relationships (arrow)
- Multiplicity (1, *, 1..*) 