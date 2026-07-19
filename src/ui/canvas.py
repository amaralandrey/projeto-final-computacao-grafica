from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QPen, QFont, QBrush
from PyQt6.QtCore import Qt
from core.viewport import Viewport

class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(661, 661) 
        self.setAutoFillBackground(True)
        
        # Cor de fundo padrão
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(200, 235, 235))
        self.setPalette(palette)
        
        self.viewport = Viewport(self.width(), self.height())
        self.pixels_to_draw = [] 

    def set_pixels(self, pixels):
        self.pixels_to_draw = pixels
        self.update() 

    def clear_canvas(self):
        self.pixels_to_draw = []
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False) 
        
        self.draw_pixels(painter)
        
        self.draw_grid(painter)
        
    def draw_pixels(self, painter):
        painter.setPen(QPen(QColor(50, 50, 50), 1, Qt.PenStyle.SolidLine))
        painter.setBrush(QBrush(QColor(255, 0, 0))) 
        
        cell_size = self.width() / 22
        
        for x, y in self.pixels_to_draw:
            if -11 <= x <= 11 and -11 <= y <= 11:
                cx, cy = self.viewport.math_to_screen(x, y)
                
                painter.drawRect(
                    int(cx - (cell_size / 2)), 
                    int(cy - (cell_size / 2)), 
                    int(cell_size), 
                    int(cell_size)
                )

    def draw_grid(self, painter):
        pen_pixel_inativo = QPen(QColor(180, 180, 180), 1, Qt.PenStyle.SolidLine)
        painter.setPen(pen_pixel_inativo)
        painter.setBrush(Qt.BrushStyle.NoBrush) 
        
        cell_size = self.width() / 22
        
        for x in range(-11, 12):
            for y in range(-11, 12):
                cx, cy = self.viewport.math_to_screen(x, y)
                painter.drawRect(
                    int(cx - (cell_size / 2)), 
                    int(cy - (cell_size / 2)), 
                    int(cell_size), 
                    int(cell_size)
                )

        pen_axis = QPen(QColor(0, 0, 0), 2, Qt.PenStyle.SolidLine)
        painter.setPen(pen_axis)
        
        x1, y1 = self.viewport.math_to_screen(0, -11)
        x2, y2 = self.viewport.math_to_screen(0, 11)
        painter.drawLine(int(x1), int(y1), int(x2), int(y2))
        
        x3, y3 = self.viewport.math_to_screen(-11, 0)
        x4, y4 = self.viewport.math_to_screen(11, 0)
        painter.drawLine(int(x3), int(y3), int(x4), int(y4))

        font = QFont("Arial", 8)
        painter.setFont(font)
        pen_text = QPen(QColor(50, 50, 50))
        painter.setPen(pen_text)
      
        for i in range(-11, 12):
            if i == 0:
                x_pos, y_pos = self.viewport.math_to_screen(0, 0)
                painter.drawText(int(x_pos + 5), int(y_pos + 15), "0")
                continue
            
            x_pos, y_pos = self.viewport.math_to_screen(i, 0)
            painter.drawText(int(x_pos - 5), int(y_pos + 15), str(i))
            
            x_pos, y_pos = self.viewport.math_to_screen(0, i)
            painter.drawText(int(x_pos + 5), int(y_pos + 4), str(i))