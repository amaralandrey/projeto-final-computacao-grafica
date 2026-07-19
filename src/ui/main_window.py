from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from ui.canvas import Canvas
from ui.sidebar import Sidebar
from core.rasterization import Rasterization 
from core.transformations import Transformations
from core.clipping import cohen_sutherland_clip, sutherland_hodgman_clip
from core.projections import Projections  

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Computação Gráfica - Trabalho Prático")
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

    def get_parsed_3d_points(self):
        """Helper para ler os pontos 3D da caixa de texto"""
        raw_text = self.sidebar.input_polyline.text()
        str_points = raw_text.split(';')
        points = []
        for pt in str_points:
            if pt.strip(): 
                coords = pt.split(',')
                if len(coords) == 3: 
                    px = float(coords[0].strip())
                    py = float(coords[1].strip())
                    pz = float(coords[2].strip())
                    points.append((px, py, pz))
        return points

    def handle_draw(self):
        algo = self.sidebar.get_selected_algorithm()
        
        x1, y1 = self.sidebar.spin_x1.value(), self.sidebar.spin_y1.value()
        x2, y2 = self.sidebar.spin_x2.value(), self.sidebar.spin_y2.value()
        x3, y3 = self.sidebar.spin_x3.value(), self.sidebar.spin_y3.value()
        x4, y4 = self.sidebar.spin_x4.value(), self.sidebar.spin_y4.value()
        r = self.sidebar.spin_r.value()
        
        pixels = []
        points = self.get_parsed_points()

        self.canvas.clip_area = None

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
        
        elif algo == "polyline":
            if len(points) >= 2:
                pixels = Rasterization.polyline(points)
        elif algo == "scanline":
            if len(points) >= 3:
                pixels = Rasterization.scanline_fill(points)
        elif algo == "flood_fill":
            if len(points) >= 3:
                pixels = Rasterization.flood_fill_recursive(points, x1, y1)
                
        elif algo == "translate":
            if len(points) >= 2:
                final_points = Transformations.translate(points, x1, y1)
                pixels = Rasterization.polyline(final_points)
        elif algo == "rotate":
            if len(points) >= 2:
                final_points = Transformations.rotate(points, x1, x2, y2)
                pixels = Rasterization.polyline(final_points)
        elif algo == "scale":
            if len(points) >= 2:
                final_points = Transformations.scale(points, x1, y1, x2, y2)
                pixels = Rasterization.polyline(final_points)
        
        elif algo == "clip_line":
            self.canvas.set_clipping_area(x3, y3, x4, y4)

            clipped_line = cohen_sutherland_clip(x1, y1, x2, y2, x3, y3, x4, y4)
            if clipped_line:
                pixels = Rasterization.bresenham_line(*clipped_line)
        
        elif algo == "clip_poly":
            self.canvas.set_clipping_area(x3, y3, x4, y4)
            if len(points) >= 3:
                clipped_points = sutherland_hodgman_clip(points, x3, y3, x4, y4)
                if clipped_points and len(clipped_points) >= 3:
                    if clipped_points[0] != clipped_points[-1]:
                        clipped_points.append(clipped_points[0])
                    pixels = Rasterization.polyline(clipped_points)
                    
        elif algo in ["proj_ortho", "proj_oblique", "proj_persp"]:
            points_3d = self.get_parsed_3d_points() # Lê pontos (X, Y, Z)
            projected_2d_points = []
            
            if len(points_3d) >= 2:
                if algo == "proj_ortho":
                    plano = x1 
                    projected_2d_points = Projections.orthographic(points_3d, plano)
                    
                elif algo == "proj_oblique":
                    angle = x1
                    fator = 1 if x2 == 1 else 0.5 
                    projected_2d_points = Projections.oblique(points_3d, angle, fator)
                    
                elif algo == "proj_persp":
                    d = x1 
                    projected_2d_points = Projections.perspective(points_3d, d)

                if projected_2d_points and len(projected_2d_points) >= 2:
                    
                    projected_2d_points_int = [(int(round(pt[0])), int(round(pt[1]))) for pt in projected_2d_points]
                    
                    if projected_2d_points_int[0] != projected_2d_points_int[-1]:
                        projected_2d_points_int.append(projected_2d_points_int[0])
                        
                    pixels = Rasterization.polyline(projected_2d_points_int)

        self.canvas.set_pixels(pixels)