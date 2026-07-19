from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from ui.canvas import Canvas
from ui.sidebar import Sidebar
from core.rasterization import Rasterization 
from core.transformations import Transformations

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Trabalho Final Computação Gráfica - Algoritmos")
        self.resize(1100, 800) 

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.main_layout = QHBoxLayout(central_widget)
     
        self.sidebar = Sidebar()
        self.canvas = Canvas()
        
        self.main_layout.addWidget(self.canvas)
        self.main_layout.addWidget(self.sidebar)

        self.sidebar.btn_draw.clicked.connect(self.handle_draw)
        self.sidebar.btn_clear.clicked.connect(self.canvas.clear_canvas)

    def get_parsed_points(self):
        """Helper para ler os pontos da caixa de texto da Polilinha"""
        raw_text = self.sidebar.input_polyline.text()
        str_points = raw_text.split(';')
        points = []
        for pt in str_points:
            if pt.strip(): 
                coords = pt.split(',')
                if len(coords) == 2:
                    px = max(-11, min(11, int(coords[0].strip())))
                    py = max(-11, min(11, int(coords[1].strip())))
                    points.append((px, py))
        return points

    def handle_draw(self):
        algo = self.sidebar.get_selected_algorithm()
        
        # Parâmetros gerais dos Spinboxes
        x1, y1 = self.sidebar.spin_x1.value(), self.sidebar.spin_y1.value()
        x2, y2 = self.sidebar.spin_x2.value(), self.sidebar.spin_y2.value()
        x3, y3 = self.sidebar.spin_x3.value(), self.sidebar.spin_y3.value()
        x4, y4 = self.sidebar.spin_x4.value(), self.sidebar.spin_y4.value()
        r = self.sidebar.spin_r.value()
        
        pixels = []
        points = self.get_parsed_points()

        # Algoritmos de Desenho Primitivo
        if algo == "bresenham":
            pixels = Rasterization.bresenham_line(x1, y1, x2, y2)
        elif algo == "circle":
            pixels = Rasterization.bresenham_circle(x1, y1, r)
        elif algo == "ellipse":
            pixels = Rasterization.midpoint_ellipse(x1, y1, abs(x2), abs(y2))
        elif algo == "bezier_quad":
            pixels = Rasterization.bezier_quad(x1, y1, x2, y2, x3, y3)
        elif algo == "bezier_cubic":
            pixels = Rasterization.bezier_cubic(x1, y1, x2, y2, x3, y3, x4, y4)
        
        # Algoritmos de Preenchimento / Polilinha
        elif algo == "polyline":
            if len(points) >= 2:
                pixels = Rasterization.polyline(points)
        elif algo == "scanline":
            if len(points) >= 3:
                pixels = Rasterization.scanline_fill(points)
        elif algo == "flood_fill":
            if len(points) >= 3:
                pixels = Rasterization.flood_fill_recursive(points, x1, y1)
                
        # Transformações Geométricas
        elif algo == "translate":
            if len(points) >= 2:
                final_points = Transformations.translate(points, x1, y1)
                pixels = Rasterization.polyline(final_points)
        elif algo == "rotate":
            if len(points) >= 2:
                # x1 = angulo, x2/y2 = pivô
                final_points = Transformations.rotate(points, x1, x2, y2)
                pixels = Rasterization.polyline(final_points)
        elif algo == "scale":
            if len(points) >= 2:
                # x1/y1 = sx/sy, x2/y2 = ponto fixo
                final_points = Transformations.scale(points, x1, y1, x2, y2)
                pixels = Rasterization.polyline(final_points)
            
        self.canvas.set_pixels(pixels)