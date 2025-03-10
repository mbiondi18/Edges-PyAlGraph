# PyAlgGraph Diagram Documentation

This directory contains various diagrams that document the structure and flow of the PyAlgGraph application.

## Available Diagrams

1. **Class Diagram** - Shows the class structure and relationships between classes
   - Available as text-based ASCII art (`class_diagram.txt`) 
   - Available as Mermaid markup (`mermaid_class_diagram.md`)

2. **Component Interaction Diagram** - Shows how components interact during operations
   - Available as text-based illustration (`component_interaction.txt`)

3. **Sequence Diagrams** - Show the sequence of operations for different workflows
   - Bipartite graph workflow (`mermaid_sequence_diagram.md`)
   - Regular graph workflow (`mermaid_sequence_diagram_regular.md`)
   - Combined workflow diagram (`mermaid_combined_sequence_diagram.md`)

4. **Flowchart** - Shows the algorithmic flow of the application
   - Available as Mermaid markup (`mermaid_flowchart.md`)

## How to View the Diagrams

### Text-based Diagrams
The text-based diagrams (`*.txt` files) can be viewed in any text editor.

### Mermaid Diagrams
The Mermaid-based diagrams (`*.md` files) can be viewed in several ways:

1. **GitHub** - If you push these files to GitHub, the Mermaid diagrams will render automatically in the repository.

2. **VS Code** - Install the "Markdown Preview Mermaid Support" extension to view Mermaid diagrams directly in VS Code.

3. **Mermaid Live Editor** - Copy the content between the \`\`\`mermaid and \`\`\` tags and paste it into the [Mermaid Live Editor](https://mermaid.live/).

4. **Export as Images** - Use the Mermaid CLI tool to convert these diagrams to images:
   ```bash
   npm install -g @mermaid-js/mermaid-cli
   mmdc -i mermaid_class_diagram.md -o class_diagram.png
   ```

## Diagram Description

### Class Diagram
Shows the main classes and their relationships in the PyAlgGraph application:
- `App`: The main application class that coordinates everything
- `GraphColorer`: Handles the graph coloring algorithms
- `GraphVisualizer`: Manages visualization of graphs
- `BipartiteGraphWindow`: UI for creating bipartite graphs
- `GraphWindow`: UI for creating regular graphs
- `StatisticsWindow`: Displays statistics about colorings

### Component Interaction Diagram
Illustrates how the different components interact during key operations, showing the flow of data and control between classes.

### Sequence Diagrams
Three separate sequence diagrams are provided:
1. **Bipartite Graph Workflow** - Shows the step-by-step sequence of operations when a user creates and colors a bipartite graph.
2. **Regular Graph Workflow** - Shows the step-by-step sequence of operations when a user creates and colors a regular graph.
3. **Combined Workflow** - Shows both workflows in a single diagram with branches, allowing for easy comparison.

### Flowchart
Depicts the algorithmic flow of the application, from start to finish, for coloring both regular and bipartite graphs. 