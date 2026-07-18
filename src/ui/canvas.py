from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QPen, QFont
from PyQt6.QtCore import Qt
from core.viewport import Viewport

class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(660, 660) 
        
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(255, 255, 255))
        self.setPalette(palette)
        
        self.viewport = Viewport(self.width(), self.height())

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing) 
        self.draw_grid(painter)
        
    def draw_grid(self, painter):
        pen_grid = QPen(QColor(220, 220, 220), 1, Qt.PenStyle.SolidLine)
        painter.setPen(pen_grid)
        
        for i in range(-11, 12):
            x1, y1 = self.viewport.math_to_screen(i, -11)
            x2, y2 = self.viewport.math_to_screen(i, 11)
            painter.drawLine(x1, y1, x2, y2)
            
            x3, y3 = self.viewport.math_to_screen(-11, i)
            x4, y4 = self.viewport.math_to_screen(11, i)
            painter.drawLine(x3, y3, x4, y4)

        pen_axis = QPen(QColor(0, 0, 0), 2, Qt.PenStyle.SolidLine)
        painter.setPen(pen_axis)
        
        x1, y1 = self.viewport.math_to_screen(0, -11)
        x2, y2 = self.viewport.math_to_screen(0, 11)
        painter.drawLine(x1, y1, x2, y2)
        
        x3, y3 = self.viewport.math_to_screen(-11, 0)
        x4, y4 = self.viewport.math_to_screen(11, 0)
        painter.drawLine(x3, y3, x4, y4)

        font = QFont("Arial", 8)
        painter.setFont(font)
        pen_text = QPen(QColor(50, 50, 50))
        painter.setPen(pen_text)

        for i in range(-11, 12):
            if i == 0:
                x_pos, y_pos = self.viewport.math_to_screen(0, 0)
                painter.drawText(x_pos + 5, y_pos + 15, "0")
                continue
                
            x_pos, y_pos = self.viewport.math_to_screen(i, 0)
            painter.drawText(x_pos - 5, y_pos + 15, str(i))
            
            x_pos, y_pos = self.viewport.math_to_screen(0, i)
            painter.drawText(x_pos + 5, y_pos + 4, str(i))