# PyAlgGraph Regular Graph Sequence Diagram

```mermaid
sequenceDiagram
    actor User
    participant App
    participant GW as GraphWindow
    participant GC as GraphColorer
    participant GV as GraphVisualizer
    participant ROD as RearrangeOrderDialog
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
    
    %% Default Order Coloring
    User->>App: Select sequential coloring default order
    App->>GC: secuencial_coloring(graph, edges)
    GC->>GC: Execute algorithm
    GC-->>App: Return edge_colors
    
    %% Visualizing
    App->>GV: draw_graph(graph, edge_colors)
    GV->>GV: Render visualization
    GV-->>App: Display updated
    
    %% Optional: User Order Coloring
    alt User Order Coloring
        User->>App: Select sequential coloring user order
        App->>GC: sequential_user_order_coloring(graph)
        GC->>GC: Execute algorithm with creation order
        GC-->>App: Return edge_colors
        App->>GV: Update visualization
        GV-->>App: Display updated with new coloring
    end
    
    %% Optional: Rearrange Order
    alt Rearrange Edge Order
        User->>App: Request to rearrange edge order
        App->>ROD: Create(current_edges)
        ROD-->>User: Show rearrangement dialog
        User->>ROD: Rearrange edges and confirm
        ROD-->>App: Return new edge order
        App->>GC: sequential_user_order_coloring(graph) with new order
        GC->>GC: Execute algorithm with new order
        GC-->>App: Return edge_colors
        App->>GV: Update visualization
        GV-->>App: Display updated with new coloring
    end
    
    %% Statistics and explanation
    User->>App: Request statistics
    App->>SW: Create and show
    SW->>SW: update_statistics()
    SW-->>App: Statistics shown
    
    User->>App: Request algorithm explanation
    App->>AEW: Create with algorithm details
    AEW-->>App: Explanation window shown
```

This sequence diagram illustrates the interaction flow between the main components during a typical operation of creating and coloring a regular graph. It shows:

1. Initial application setup
2. Creating a regular graph through the GraphWindow
3. Default sequential coloring with degree-based ordering
4. Optional user order coloring based on creation/user-specified order
5. Optional rearrangement of edge order through the RearrangeOrderDialog
6. Visualizing the colored graph with GraphVisualizer
7. Displaying statistics through StatisticsWindow
8. Showing algorithm explanations via AlgorithmExplanationWindow

The arrows indicate the direction of function calls and information flow, with solid arrows representing function calls and dashed arrows representing returns or responses. 