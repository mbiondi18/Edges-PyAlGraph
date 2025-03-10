from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QScrollArea, QWidget
from PyQt5.QtCore import Qt

class AlgorithmExplanationWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Bipartite Matching Algorithm Explanation")
        self.setMinimumSize(600, 400)
        
        # Create layout
        layout = QVBoxLayout()
        
        # Create a scroll area
        scroll = QScrollArea()
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        # Create explanation text
        explanation = """
        <h2>How the Bipartite Matching Algorithm Works</h2>

        <h3>1. Augmenting Path Search</h3>
        • An augmenting path is a path that can increase the size of the current matching
        • The path must start at an unmatched left vertex and end at an unmatched right vertex
        • The path alternates between:
          - Unmatched edges (potential new matches)
          - Matched edges (edges we might need to unmatch)
        
        <h3>2. Path Finding Process</h3>
        • The algorithm starts from an unmatched left vertex
        • For each unmatched edge from this vertex:
          - If it leads to an unmatched right vertex: Path found!
          - If it leads to a matched right vertex:
            * Follow the matched edge back to its left vertex
            * Continue searching from this new left vertex
        • The search uses a breadth-first approach to find the shortest augmenting path
        • When a path is found, it represents the optimal way to increase the matching

        <h3>3. Path Usage</h3>
        • When an augmenting path is found:
          - Unmatched edges in the path become matched
          - Matched edges in the path become unmatched
        • This process:
          - Increases the total number of matches by 1
          - Maintains the matching property (no vertex has multiple matches)
          - Guarantees progress toward the maximum matching

        <h3>4. Coloring Process</h3>
        • Each iteration (successful augmenting path) uses a new color
        • The color shows which edges were matched together
        • Colors help visualize how the matching was built up over time
        • Each color represents an independent set of matches

        <h3>5. Algorithm Completion</h3>
        • The algorithm continues until no augmenting paths exist
        • When no paths are found, we have reached a maximum matching because:
          - Any potential improvement would create an augmenting path
          - We've proven no such paths exist
        • The final matching is optimal (maximum size possible)
        • The combination of all colored edges gives us the maximum matching
        """
        
        # Create and style the label
        explanation_label = QLabel(explanation)
        explanation_label.setWordWrap(True)
        explanation_label.setTextFormat(Qt.RichText)
        explanation_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                line-height: 1.5;
                padding: 20px;
            }
        """)
        
        # Add label to scroll area
        scroll_layout.addWidget(explanation_label)
        scroll_content.setLayout(scroll_layout)
        scroll.setWidget(scroll_content)
        scroll.setWidgetResizable(True)
        
        # Add scroll area to main layout
        layout.addWidget(scroll)
        self.setLayout(layout) 