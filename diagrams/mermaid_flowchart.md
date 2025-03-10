# PyAlgGraph Algorithmic Flowchart

```mermaid
flowchart TD
    %% Main flow
    Start([Start Application]) --> Init[Initialize App]
    Init --> MainMenu[Display Main Interface]
    
    %% Graph creation branch
    MainMenu --> CreateGraph{Create Graph?}
    CreateGraph -->|Regular Graph| OpenGW[Open GraphWindow]
    CreateGraph -->|Bipartite Graph| OpenBGW[Open BipartiteGraphWindow]
    
    %% Regular graph path
    OpenGW --> AddVerticesR[Add Vertices]
    AddVerticesR --> AddEdgesR[Add Edges]
    AddEdgesR --> ColorR{Color Graph?}
    ColorR -->|Yes| SelectAlgoR[Select Coloring Algorithm]
    ColorR -->|No| BackToMainR[Return to Main Menu]
    
    SelectAlgoR --> SeqColoring[Sequential Coloring]
    SeqColoring --> DisplayRegular[Display Colored Graph]
    DisplayRegular --> Stats[View Statistics]
    
    %% Bipartite graph path
    OpenBGW --> AddLeftVertices[Add Left Vertices]
    AddLeftVertices --> AddRightVertices[Add Right Vertices]
    AddRightVertices --> AddEdgesB[Add Edges]
    AddEdgesB --> ColorB{Color Graph?}
    ColorB -->|No| BackToMainB[Return to Main Menu]
    ColorB -->|Yes| SelectAlgoB[Select Bipartite Coloring Algorithm]
    
    SelectAlgoB --> BipartiteChoice{Algorithm Type?}
    BipartiteChoice -->|Standard| StandardBipartite[Standard Bipartite Coloring]
    BipartiteChoice -->|Degree-based| DegreeBipartite[Degree-based Bipartite Coloring]
    BipartiteChoice -->|User Order| UserOrderBipartite[User Order Bipartite Coloring]
    
    StandardBipartite --> MaximalMatching[Find Maximal Matching]
    MaximalMatching --> AugmentPath[Find Augmenting Paths]
    AugmentPath --> ColorEdges[Color Edges]
    
    DegreeBipartite --> SortByDegree[Sort Vertices by Degree]
    SortByDegree --> ProcessByDegree[Process Vertices in Degree Order]
    ProcessByDegree --> ColorEdges
    
    UserOrderBipartite --> GetUserOrder[Get User-defined Edge Order]
    GetUserOrder --> ProcessUserOrder[Process Edges in User Order]
    ProcessUserOrder --> ColorEdges
    
    ColorEdges --> DisplayBipartite[Display Colored Bipartite Graph]
    DisplayBipartite --> StepByStep{Step by Step View?}
    StepByStep -->|Yes| EnableStepping[Enable Step Navigation]
    StepByStep -->|No| Stats
    
    EnableStepping --> NextStep[Show Next Step]
    NextStep -->|More Steps| NextStep
    NextStep -->|No More Steps| Stats
    
    %% Statistics and explanation
    Stats --> AlgoExplain{View Algorithm Explanation?}
    AlgoExplain -->|Yes| ShowExplanation[Show Algorithm Explanation Window]
    AlgoExplain -->|No| End([End])
    ShowExplanation --> End
```

This flowchart illustrates the algorithmic flow of the PyAlgGraph application, showing:

1. Application initialization
2. Main flow branches for regular graphs vs. bipartite graphs
3. The graph creation process
4. Different coloring algorithms:
   - Sequential coloring for regular graphs
   - Standard bipartite coloring
   - Degree-based bipartite coloring
   - User-order bipartite coloring
5. Step-by-step visualization option
6. Statistics and explanation display

The diamond shapes represent decision points, while rectangles show processes or operations. The rounded rectangles indicate the start and end points of the application flow. 