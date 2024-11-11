# PyAlgGraph

PyAlgGraph is a Python-based application for visualizing and analyzing graph algorithms, particularly focusing on bipartite graphs and graph coloring.

## Features

- **Graph Coloring**: Implements sequential and user-order graph coloring algorithms.
- **Bipartite Matching**: Visualizes bipartite graph matching and augmenting paths.
- **Interactive Visualization**: Provides a GUI for creating and manipulating graphs.
- **Statistics**: Displays execution time, number of colors used, and algorithm details.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/PyAlgGraph.git
   ```
2. Navigate to the project directory:
   ```bash
   cd PyAlgGraph
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python main.py
   ```
2. Use the GUI to create graphs, apply algorithms, and visualize results.

## Code Structure

- `App/GraphColorer.py`: Contains graph coloring algorithms.
  - Sequential coloring: 
    ```python:PyAlgGraph/PyAlgGraph/App/GraphColorer.py
    startLine: 14
    endLine: 193
    ```
  - Augmenting path finding:
    ```python:PyAlgGraph/PyAlgGraph/App/GraphColorer.py
    startLine: 134
    endLine: 162
    ```

- `App/GraphVisualizer.py`: Handles graph visualization.
  - Bipartite matching visualization:
    ```python:PyAlgGraph/PyAlgGraph/App/GraphVisualizer.py
    startLine: 127
    endLine: 200
    ```

- `App/App.py`: Main application logic and GUI handling.
  - Sequential coloring activation:
    ```python:PyAlgGraph/PyAlgGraph/App/App.py
    startLine: 148
    endLine: 176
    ```
  - Bipartite graph coloring:
    ```python:PyAlgGraph/PyAlgGraph/App/App.py
    startLine: 187
    endLine: 228
    ```
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

