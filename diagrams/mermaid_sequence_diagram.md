# PyAlgGraph Sequence Diagram

```mermaid
sequenceDiagram
    actor User
    participant App
    participant BGW as BipartiteGraphWindow
    participant GC as GraphColorer
    participant GV as GraphVisualizer
    participant SW as StatisticsWindow
    participant AEW as AlgorithmExplanationWindow

    %% Creating the bipartite graph
    User->>App: Start application
    App->>App: Initialize
    User->>App: Request bipartite graph window
    App->>BGW: Create and open
    BGW-->>App: Window opened
    
    User->>BGW: Add left vertices
    User->>BGW: Add right vertices
    User->>BGW: Add edges
    
    User->>BGW: Finalize graph
    BGW->>BGW: Create bipartite graph
    BGW->>App: Return graph data
    
    %% Coloring the graph
    User->>App: Select coloring algorithm
    App->>GC: bipartite_coloring(graph)
    GC->>GC: Execute algorithm
    GC-->>App: Return edge_colors
    
    %% Visualizing
    App->>GV: draw_bipartite_graph(graph, edge_colors)
    GV->>GV: Render visualization
    GV-->>App: Display updated
    
    %% Statistics and explanation
    User->>App: Request statistics
    App->>SW: Create and show
    SW->>SW: update_statistics()
    SW->>SW: add_matching_statistics()
    SW-->>App: Statistics shown
    
    User->>App: Request algorithm explanation
    App->>AEW: Create with algorithm details
    AEW-->>App: Explanation window shown
    
    %% Step-by-step navigation (optional flow)
    User->>App: Request step-by-step view
    App->>App: display_matching_groups()
    App->>App: create_step_buttons()
    App-->>User: Step UI displayed
    
    User->>App: Click "Next Step"
    App->>App: show_next_step()
    App->>GV: Update visualization for step
    GV-->>App: Step visualization shown
    App-->>User: Updated display
```

This sequence diagram illustrates the interaction flow between the main components during a typical operation of creating and coloring a bipartite graph. It shows:

1. Initial application setup
2. Creating a bipartite graph through the BipartiteGraphWindow
3. Coloring the graph using GraphColorer
4. Visualizing the colored graph with GraphVisualizer
5. Displaying statistics through StatisticsWindow
6. Showing algorithm explanations via AlgorithmExplanationWindow
7. The optional step-by-step navigation flow

The arrows indicate the direction of function calls and information flow, with solid arrows representing function calls and dashed arrows representing returns or responses. 