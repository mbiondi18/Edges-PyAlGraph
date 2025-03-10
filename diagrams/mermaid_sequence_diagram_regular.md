# PyAlgGraph Regular Graph Sequence Diagram

```mermaid
sequenceDiagram
    actor User
    participant App
    participant GW as GraphWindow
    participant GC as GraphColorer
    participant GV as GraphVisualizer
    participant SW as StatisticsWindow
    participant AEW as AlgorithmExplanationWindow

    %% Creating the regular graph
    User->>App: Start application
    App->>App: Initialize
    User->>App: Request regular graph window
    App->>GW: Create and open
    GW-->>App: Window opened
    
    User->>GW: Add vertices
    User->>GW: Add edges
    
    User->>GW: Finalize graph
    GW->>GW: Create graph
    GW->>App: Return graph data
    
    %% Coloring the graph
    User->>App: Select secuencial coloring
    App->>GC: secuencial_coloring(graph, edges)
    GC->>GC: Execute algorithm
    GC-->>App: Return edge_colors
    
    %% Visualizing
    App->>GV: draw_graph(graph, edge_colors)
    GV->>GV: Render visualization
    GV-->>App: Display updated
    
    %% Statistics and explanation
    User->>App: Request statistics
    App->>SW: Create and show
    SW->>SW: update_statistics()
    SW-->>App: Statistics shown
    
    User->>App: Request algorithm explanation
    App->>AEW: Create with algorithm details
    AEW-->>App: Explanation window shown
    
    %% Optional: User Order
    User->>App: Request custom order coloring
    App->>App: Show UserOrderDialog
    App->>GC: sequential_user_order_coloring(graph)
    GC->>GC: Execute algorithm with custom order
    GC-->>App: Return edge_colors
    App->>GV: Update visualization
    GV-->>App: Display updated with new coloring
```

This sequence diagram illustrates the interaction flow between the main components during a typical operation of creating and coloring a regular graph. It shows:

1. Initial application setup
2. Creating a regular graph through the GraphWindow
3. Coloring the graph using GraphColorer's sequential coloring algorithm
4. Visualizing the colored graph with GraphVisualizer
5. Displaying statistics through StatisticsWindow
6. Showing algorithm explanations via AlgorithmExplanationWindow
7. Optional custom order coloring

The arrows indicate the direction of function calls and information flow, with solid arrows representing function calls and dashed arrows representing returns or responses. 