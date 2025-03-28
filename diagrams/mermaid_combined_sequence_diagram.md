# PyAlgGraph Combined Sequence Diagram

```mermaid
sequenceDiagram
    actor User
    participant App
    participant GW as GraphWindow
    participant BGW as BipartiteGraphWindow
    participant GC as GraphColorer
    participant GV as GraphVisualizer
    participant ROD as RearrangeOrderDialog
    participant SW as StatisticsWindow
    participant AEW as AlgorithmExplanationWindow

    %% Application start
    User->>App: Start application
    App->>App: Initialize
    
    %% Graph type selection
    User->>App: Select graph type
    
    %% Branch: Regular Graph
    alt Regular Graph
        App->>GW: Create and open
        GW-->>App: Window opened
        
        User->>GW: Add vertices
        User->>GW: Add edges
        
        User->>GW: Finalize graph
        GW->>GW: Create graph
        GW->>App: Return graph data
        
        %% Regular graph coloring options
        alt Default Order Coloring
            User->>App: Select sequential coloring default order
            App->>GC: secuencial_coloring(graph, edges)
        else User Order Coloring
            User->>App: Select sequential coloring user order
            App->>GC: sequential_user_order_coloring(graph)
        end
        
        GC->>GC: Execute algorithm
        GC-->>App: Return edge_colors
        
        %% Optional order rearrangement for regular graph
        opt Rearrange Edge Order
            User->>App: Request to rearrange edge order
            App->>ROD: Create(current_edges)
            ROD-->>User: Show rearrangement dialog
            User->>ROD: Rearrange edges and confirm
            ROD-->>App: Return new edge order
            App->>GC: sequential_user_order_coloring(graph) with new order
            GC-->>App: Return updated edge_colors
        end
        
        App->>GV: draw_graph(graph, edge_colors)
    
    %% Branch: Bipartite Graph
    else Bipartite Graph
        App->>BGW: Create and open
        BGW-->>App: Window opened
        
        User->>BGW: Add left vertices
        User->>BGW: Add right vertices
        User->>BGW: Add edges
        
        User->>BGW: Finalize graph
        BGW->>BGW: Create bipartite graph
        BGW->>App: Return graph data
        
        User->>App: Select coloring algorithm
        
        alt Standard Bipartite
            App->>GC: bipartite_coloring(graph)
        else Degree-based
            App->>GC: bipartite_degree_coloring(graph)
        else User Order
            App->>GC: bipartite_user_order_coloring(graph, edge_order)
        end
        
        GC->>GC: Execute algorithm
        GC-->>App: Return edge_colors
        
        %% Optional order rearrangement for bipartite graph
        opt Rearrange Edge Order
            User->>App: Request to rearrange edge order
            App->>ROD: Create(current_edges)
            ROD-->>User: Show rearrangement dialog
            User->>ROD: Rearrange edges and confirm
            ROD-->>App: Return new edge order
            App->>GC: bipartite_user_order_coloring(graph, new_order)
            GC-->>App: Return updated edge_colors
        end
        
        App->>GV: draw_bipartite_graph(graph, edge_colors)
        
        opt Step-by-Step View
            User->>App: Request step-by-step view
            App->>App: display_matching_groups()
            App->>App: create_step_buttons()
            User->>App: Click "Next Step"
            App->>App: show_next_step()
            App->>GV: Update visualization for step
        end
    end
    
    %% Common path after coloring
    GV->>GV: Render visualization
    GV-->>App: Display updated
    
    %% Statistics
    User->>App: Request statistics
    App->>SW: Create and show
    SW->>SW: update_statistics()
    SW-->>App: Statistics shown
    
    %% Algorithm explanation
    User->>App: Request algorithm explanation
    App->>AEW: Create with algorithm details
    AEW-->>App: Explanation window shown
```

This comprehensive sequence diagram illustrates both the regular graph and bipartite graph workflows in a single diagram, showing how the application handles both paths. The diagram uses "alt", "else", and "opt" sections to represent the branching paths, and includes:

1. Initial application setup
2. User selecting between regular and bipartite graph types
3. Different graph creation processes for each type
4. Different coloring algorithms for each type:
   - Regular graph: Default order and user order options
   - Bipartite graph: Standard, degree-based, and user order options
5. Optional order rearrangement functionality for both graph types
6. Common visualization, statistics, and explanation components
7. Optional step-by-step visualization for bipartite graphs

The arrows indicate the direction of function calls and information flow, with solid arrows representing function calls and dashed arrows representing returns or responses. 