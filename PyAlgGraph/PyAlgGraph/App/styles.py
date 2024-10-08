from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QApplication

# Color scheme
PRIMARY_COLOR = "#3498db"
SECONDARY_COLOR = "#2ecc71"
BACKGROUND_COLOR = "#ecf0f1"
TEXT_COLOR = "#2c3e50"

def set_app_style(app: QApplication):
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(BACKGROUND_COLOR))
    palette.setColor(QPalette.WindowText, QColor(TEXT_COLOR))
    palette.setColor(QPalette.Base, QColor(BACKGROUND_COLOR))
    palette.setColor(QPalette.AlternateBase, QColor(BACKGROUND_COLOR))
    palette.setColor(QPalette.ToolTipBase, QColor(PRIMARY_COLOR))
    palette.setColor(QPalette.ToolTipText, QColor(TEXT_COLOR))
    palette.setColor(QPalette.Text, QColor(TEXT_COLOR))
    palette.setColor(QPalette.Button, QColor(PRIMARY_COLOR))
    palette.setColor(QPalette.ButtonText, QColor("white"))
    palette.setColor(QPalette.BrightText, QColor("red"))
    palette.setColor(QPalette.Highlight, QColor(SECONDARY_COLOR))
    palette.setColor(QPalette.HighlightedText, QColor("black"))
    app.setPalette(palette)

    app.setStyleSheet(f"""
        QPushButton {{
            background-color: {PRIMARY_COLOR};
            color: white;
            border: none;
            padding: 5px;
            border-radius: 3px;
        }}
        QPushButton:hover {{
            background-color: {SECONDARY_COLOR};
        }}
        QComboBox {{
            border: 1px solid {PRIMARY_COLOR};
            border-radius: 3px;
            padding: 1px 18px 1px 3px;
            min-width: 6em;
        }}
        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 15px;
            border-left-width: 1px;
            border-left-color: darkgray;
            border-left-style: solid;
            border-top-right-radius: 3px;
            border-bottom-right-radius: 3px;
        }}
    """)
