from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QApplication

# Color scheme - Updated with darker colors
PRIMARY_COLOR = "#3498db"  # Keep blue for primary actions
SECONDARY_COLOR = "#2ecc71"  # Keep green for secondary actions
BACKGROUND_COLOR = "#3a3a3a"  # Darker grey background
BUTTON_COLOR = "#555555"  # Darker grey for buttons
BUTTON_HOVER_COLOR = "#666666"  # Slightly lighter on hover
TEXT_COLOR = "#ffffff"  # White text for better contrast on dark background
CANVAS_BACKGROUND = "#ffffff"  # Keep canvas white
CANVAS_BORDER_COLOR = "#000000"  # Black border for canvas

def set_app_style(app: QApplication):
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(BACKGROUND_COLOR))
    palette.setColor(QPalette.WindowText, QColor(TEXT_COLOR))
    palette.setColor(QPalette.Base, QColor(CANVAS_BACKGROUND))
    palette.setColor(QPalette.AlternateBase, QColor(BACKGROUND_COLOR))
    palette.setColor(QPalette.ToolTipBase, QColor(PRIMARY_COLOR))
    palette.setColor(QPalette.ToolTipText, QColor(TEXT_COLOR))
    palette.setColor(QPalette.Text, QColor(TEXT_COLOR))
    palette.setColor(QPalette.Button, QColor(BUTTON_COLOR))
    palette.setColor(QPalette.ButtonText, QColor("white"))
    palette.setColor(QPalette.BrightText, QColor("red"))
    palette.setColor(QPalette.Highlight, QColor(SECONDARY_COLOR))
    palette.setColor(QPalette.HighlightedText, QColor("black"))
    app.setPalette(palette)

    app.setStyleSheet(f"""
        /* Main application styling */
        QMainWindow {{
            background-color: {BACKGROUND_COLOR};
        }}
        
        QWidget {{
            background-color: {BACKGROUND_COLOR};
            color: {TEXT_COLOR};
        }}
        
        /* Button styling */
        QPushButton {{
            background-color: {BUTTON_COLOR};
            color: white;
            border: none;
            padding: 8px;
            border-radius: 4px;
            font-weight: bold;
        }}
        
        QPushButton:hover {{
            background-color: {BUTTON_HOVER_COLOR};
        }}
        
        /* Primary action buttons */
        QPushButton#primary {{
            background-color: {PRIMARY_COLOR};
        }}
        
        QPushButton#primary:hover {{
            background-color: #2980b9;
        }}
        
        /* Canvas styling */
        QGraphicsView {{
            background-color: {CANVAS_BACKGROUND};
            border: 2px solid {CANVAS_BORDER_COLOR};
            border-radius: 2px;
        }}
        
        /* Matplotlib canvas (FigureCanvas) */
        FigureCanvas {{
            border: 2px solid {CANVAS_BORDER_COLOR};
        }}
        
        /* Dropdown styling */
        QComboBox {{
            background-color: {BUTTON_COLOR};
            color: {TEXT_COLOR};
            border: 1px solid #666666;
            border-radius: 4px;
            padding: 5px 10px;
            min-width: 6em;
        }}
        
        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 15px;
            border-left-width: 1px;
            border-left-color: #666666;
            border-left-style: solid;
            border-top-right-radius: 3px;
            border-bottom-right-radius: 3px;
        }}
        
        QComboBox::item {{
            background-color: {BACKGROUND_COLOR};
            color: {TEXT_COLOR};
        }}
        
        QComboBox::item:selected {{
            background-color: {PRIMARY_COLOR};
        }}
        
        /* Ensure dropdown shows full text */
        QComboBox QAbstractItemView {{
            background-color: {BUTTON_COLOR};
            color: {TEXT_COLOR};
            border: 1px solid #777777;
            selection-background-color: {PRIMARY_COLOR};
            min-width: 300px;
            padding: 5px;
        }}
        
        /* Label styling */
        QLabel {{
            color: {TEXT_COLOR};
        }}
        
        /* Text styling */
        QTextEdit, QLineEdit {{
            background-color: #444444;
            color: {TEXT_COLOR};
            border: 1px solid #666666;
            border-radius: 4px;
            padding: 4px;
        }}
    """)

# Additional styles for specific components
def get_graph_window_style():
    return f"""
        QMainWindow {{
            background-color: {BACKGROUND_COLOR};
        }}
        
        QPushButton {{
            background-color: {BUTTON_COLOR};
            color: white;
            padding: 8px;
            border-radius: 4px;
        }}
        
        QGraphicsView {{
            background-color: {CANVAS_BACKGROUND};
            border: 2px solid {CANVAS_BORDER_COLOR};
        }}
    """

def get_bipartite_window_style():
    return f"""
        QMainWindow {{
            background-color: {BACKGROUND_COLOR};
        }}
        
        QPushButton {{
            background-color: {BUTTON_COLOR};
            color: white;
            padding: 8px;
            border-radius: 4px;
        }}
        
        QGraphicsView {{
            background-color: {CANVAS_BACKGROUND};
            border: 2px solid {CANVAS_BORDER_COLOR};
        }}
    """
