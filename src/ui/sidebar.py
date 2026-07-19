from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QGroupBox, QRadioButton, 
                             QPushButton, QSpinBox, QLabel, QFormLayout, QLineEdit)

class Sidebar(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(300)
        self.layout = QVBoxLayout(self)

        # --- Grupo de Algoritmos ---
        self.group_algo = QGroupBox("Algoritmos e Transformações")
        self.algo_layout = QVBoxLayout()
        
        # Primitivas
        self.rb_dda = QRadioButton("Linha DDA")
        self.rb_dda.setChecked(True)
        self.rb_bresenham = QRadioButton("Linha Bresenham")
        self.rb_circle = QRadioButton("Círculo")
        self.rb_ellipse = QRadioButton("Elipse")
        self.rb_bezier2 = QRadioButton("Bézier (Grau 2)")
        self.rb_bezier3 = QRadioButton("Bézier (Grau 3)")
        self.rb_polyline = QRadioButton("Polilinha (N pontos)")
        self.rb_scanline = QRadioButton("Varredura (Scanline)")
        self.rb_floodfill = QRadioButton("Recursivo (Flood Fill)")
        
        # Transformações
        self.rb_translate = QRadioButton("Translação")
        self.rb_rotate = QRadioButton("Rotação")
        self.rb_scale = QRadioButton("Escala")
        
        # Adicionando todos ao layout
        self.algo_layout.addWidget(self.rb_dda)
        self.algo_layout.addWidget(self.rb_bresenham)
        self.algo_layout.addWidget(self.rb_circle)
        self.algo_layout.addWidget(self.rb_ellipse)
        self.algo_layout.addWidget(self.rb_bezier2)
        self.algo_layout.addWidget(self.rb_bezier3)
        self.algo_layout.addWidget(self.rb_polyline)
        self.algo_layout.addWidget(self.rb_scanline)
        self.algo_layout.addWidget(self.rb_floodfill)
        self.algo_layout.addWidget(self.rb_translate)
        self.algo_layout.addWidget(self.rb_rotate)
        self.algo_layout.addWidget(self.rb_scale)
        
        self.group_algo.setLayout(self.algo_layout)
        self.layout.addWidget(self.group_algo)

        # --- Grupo de Coordenadas ---
        self.group_coords = QGroupBox("Parâmetros (Entrada)")
        self.coords_layout = QFormLayout()
        
        self.spin_x1 = self.create_spinbox()
        self.spin_y1 = self.create_spinbox()
        self.spin_x2 = self.create_spinbox()
        self.spin_y2 = self.create_spinbox()
        self.spin_x3 = self.create_spinbox()
        self.spin_y3 = self.create_spinbox()
        self.spin_x4 = self.create_spinbox()
        self.spin_y4 = self.create_spinbox()
        
        self.spin_r = self.create_spinbox()
        self.spin_r.setMinimum(0) 
        
        self.input_polyline = QLineEdit()
        self.input_polyline.setPlaceholderText("Ex: -5,-5; 5,-5; 0,5")
        
        # Labels para orientar o usuário (Reutilização de campos)
        self.coords_layout.addRow(QLabel("P0 X (X1/Ângulo/TransX/Sx):"), self.spin_x1)
        self.coords_layout.addRow(QLabel("P0 Y (Y1/TransY/Sy):"), self.spin_y1)
        self.coords_layout.addRow(QLabel("P1 X (X2/PivôX/FixoX):"), self.spin_x2)
        self.coords_layout.addRow(QLabel("P1 Y (Y2/PivôY/FixoY):"), self.spin_y2)
        self.coords_layout.addRow(QLabel("P2 X:"), self.spin_x3)
        self.coords_layout.addRow(QLabel("P2 Y:"), self.spin_y3)
        self.coords_layout.addRow(QLabel("P3 X:"), self.spin_x4)
        self.coords_layout.addRow(QLabel("P3 Y:"), self.spin_y4)
        self.coords_layout.addRow(QLabel("Raio (Círculos):"), self.spin_r)
        self.coords_layout.addRow(QLabel("Polígono (N pontos):"), self.input_polyline)
        
        self.group_coords.setLayout(self.coords_layout)
        self.layout.addWidget(self.group_coords)

        # --- Botões de Ação ---
        self.btn_draw = QPushButton("Desenhar")
        self.btn_clear = QPushButton("Limpar")
        self.layout.addWidget(self.btn_draw)
        self.layout.addWidget(self.btn_clear)
        self.layout.addStretch()

    def create_spinbox(self):
        spinbox = QSpinBox()
        spinbox.setRange(-1000, 1000) # Aumentado range para aceitar translações maiores
        return spinbox

    def get_selected_algorithm(self):
        if self.rb_dda.isChecked(): return "dda"
        elif self.rb_bresenham.isChecked(): return "bresenham"
        elif self.rb_circle.isChecked(): return "circle"
        elif self.rb_ellipse.isChecked(): return "ellipse"
        elif self.rb_bezier2.isChecked(): return "bezier_quad"
        elif self.rb_bezier3.isChecked(): return "bezier_cubic"
        elif self.rb_polyline.isChecked(): return "polyline"
        elif self.rb_scanline.isChecked(): return "scanline"
        elif self.rb_floodfill.isChecked(): return "flood_fill"
        elif self.rb_translate.isChecked(): return "translate"
        elif self.rb_rotate.isChecked(): return "rotate"
        elif self.rb_scale.isChecked(): return "scale"