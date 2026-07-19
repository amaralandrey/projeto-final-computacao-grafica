from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QGroupBox, QComboBox, 
                             QPushButton, QSpinBox, QLabel, QFormLayout, 
                             QLineEdit, QTabWidget)
from PyQt6.QtCore import Qt

class Sidebar(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(320)
        self.layout = QVBoxLayout(self)

        # --- Abas (Organização por categorias) ---
        self.tabs = QTabWidget()
        
        self.tab_primitivas = QWidget()
        self.tab_preenchimento = QWidget()
        self.tab_transformacoes = QWidget()
        
        self.tabs.addTab(self.tab_primitivas, "Formas")
        self.tabs.addTab(self.tab_preenchimento, "Pintura")
        self.tabs.addTab(self.tab_transformacoes, "Transf.")
        
        self.setup_tab_primitivas()
        self.setup_tab_preenchimento()
        self.setup_tab_transformacoes()
        
        self.layout.addWidget(self.tabs)

        # --- Grupo de Parâmetros (Dinâmico) ---
        self.group_coords = QGroupBox("Parâmetros do Algoritmo")
        self.coords_layout = QFormLayout()
        
        # Criação das entradas
        self.spin_x1, self.spin_y1 = self.create_spinbox(), self.create_spinbox()
        self.spin_x2, self.spin_y2 = self.create_spinbox(), self.create_spinbox()
        self.spin_x3, self.spin_y3 = self.create_spinbox(), self.create_spinbox()
        self.spin_x4, self.spin_y4 = self.create_spinbox(), self.create_spinbox()
        self.spin_r = self.create_spinbox()
        self.input_polyline = QLineEdit()
        self.input_polyline.setPlaceholderText("Ex: -5,5; 0,0; 5,5")
        
        # Labels para renomear dinamicamente
        self.lbl_x1, self.lbl_y1 = QLabel("X1:"), QLabel("Y1:")
        self.lbl_x2, self.lbl_y2 = QLabel("X2:"), QLabel("Y2:")
        self.lbl_x3, self.lbl_y3 = QLabel("X3:"), QLabel("Y3:")
        self.lbl_x4, self.lbl_y4 = QLabel("X4:"), QLabel("Y4:")
        self.lbl_r, self.lbl_poly = QLabel("Raio:"), QLabel("Dados:")
        
        # Adicionar ao layout
        self.coords_layout.addRow(self.lbl_x1, self.spin_x1)
        self.coords_layout.addRow(self.lbl_y1, self.spin_y1)
        self.coords_layout.addRow(self.lbl_x2, self.spin_x2)
        self.coords_layout.addRow(self.lbl_y2, self.spin_y2)
        self.coords_layout.addRow(self.lbl_x3, self.spin_x3)
        self.coords_layout.addRow(self.lbl_y3, self.spin_y3)
        self.coords_layout.addRow(self.lbl_x4, self.spin_x4)
        self.coords_layout.addRow(self.lbl_y4, self.spin_y4)
        self.coords_layout.addRow(self.lbl_r, self.spin_r)
        self.coords_layout.addRow(self.lbl_poly, self.input_polyline)
        
        self.group_coords.setLayout(self.coords_layout)
        self.layout.addWidget(self.group_coords)

        # --- Ações ---
        self.btn_draw = QPushButton("Desenhar / Aplicar")
        self.btn_clear = QPushButton("Limpar Tela")
        self.layout.addWidget(self.btn_draw)
        self.layout.addWidget(self.btn_clear)
        self.layout.addStretch()

        # Conexões
        self.combo_prim.currentIndexChanged.connect(self.update_fields)
        self.combo_preench.currentIndexChanged.connect(self.update_fields)
        self.combo_transf.currentIndexChanged.connect(self.update_fields)
        self.tabs.currentChanged.connect(self.update_fields)
        
        self.update_fields()

    # --- Configuração das Abas ---
    def setup_tab_primitivas(self):
        layout = QVBoxLayout(self.tab_primitivas)
        self.combo_prim = QComboBox()
        self.combo_prim.addItem("Linha Bresenham", "bresenham")
        self.combo_prim.addItem("Círculo", "circle")
        self.combo_prim.addItem("Elipse", "ellipse")
        self.combo_prim.addItem("Bézier (Grau 2)", "bezier_quad")
        self.combo_prim.addItem("Bézier (Grau 3)", "bezier_cubic")
        self.combo_prim.addItem("Polilinha", "polyline")
        layout.addWidget(self.combo_prim)

    def setup_tab_preenchimento(self):
        layout = QVBoxLayout(self.tab_preenchimento)
        self.combo_preench = QComboBox()
        self.combo_preench.addItem("Varredura (Scanline)", "scanline")
        self.combo_preench.addItem("Recursivo (Flood Fill)", "flood_fill")
        layout.addWidget(self.combo_preench)

    def setup_tab_transformacoes(self):
        layout = QVBoxLayout(self.tab_transformacoes)
        self.combo_transf = QComboBox()
        self.combo_transf.addItem("Translação", "translate")
        self.combo_transf.addItem("Rotação", "rotate")
        self.combo_transf.addItem("Escala", "scale")
        layout.addWidget(self.combo_transf)

    # --- Lógica de Interface ---
    def create_spinbox(self):
        spin = QSpinBox()
        spin.setRange(-1000, 1000)
        return spin

    def get_selected_algorithm(self):
        tab_idx = self.tabs.currentIndex()
        if tab_idx == 0: return self.combo_prim.currentData()
        if tab_idx == 1: return self.combo_preench.currentData()
        return self.combo_transf.currentData()

    def set_row(self, label, field, visible, text=""):
        label.setVisible(visible)
        field.setVisible(visible)
        if visible: label.setText(text)

    def update_fields(self):
        # Esconde tudo
        campos = [
            (self.lbl_x1, self.spin_x1), (self.lbl_y1, self.spin_y1),
            (self.lbl_x2, self.spin_x2), (self.lbl_y2, self.spin_y2),
            (self.lbl_x3, self.spin_x3), (self.lbl_y3, self.spin_y3),
            (self.lbl_x4, self.spin_x4), (self.lbl_y4, self.spin_y4),
            (self.lbl_r, self.spin_r), (self.lbl_poly, self.input_polyline)
        ]
        for lbl, fld in campos: self.set_row(lbl, fld, False)

        algo = self.get_selected_algorithm()

        # Configura visibilidade baseada no algoritmo
        if algo == "bresenham":
            self.set_row(self.lbl_x1, self.spin_x1, True, "X Inicial:")
            self.set_row(self.lbl_y1, self.spin_y1, True, "Y Inicial:")
            self.set_row(self.lbl_x2, self.spin_x2, True, "X Final:")
            self.set_row(self.lbl_y2, self.spin_y2, True, "Y Final:")
        elif algo == "circle":
            self.set_row(self.lbl_x1, self.spin_x1, True, "Centro X:")
            self.set_row(self.lbl_y1, self.spin_y1, True, "Centro Y:")
            self.set_row(self.lbl_r, self.spin_r, True, "Raio:")
        elif algo == "ellipse":
            self.set_row(self.lbl_x1, self.spin_x1, True, "Centro X:")
            self.set_row(self.lbl_y1, self.spin_y1, True, "Centro Y:")
            self.set_row(self.lbl_x2, self.spin_x2, True, "Raio X:")
            self.set_row(self.lbl_y2, self.spin_y2, True, "Raio Y:")
        elif algo == "bezier_quad":
            self.set_row(self.lbl_x1, self.spin_x1, True, "P0 X:")
            self.set_row(self.lbl_y1, self.spin_y1, True, "P0 Y:")
            self.set_row(self.lbl_x2, self.spin_x2, True, "P1 X:")
            self.set_row(self.lbl_y2, self.spin_y2, True, "P1 Y:")
            self.set_row(self.lbl_x3, self.spin_x3, True, "P2 X:")
            self.set_row(self.lbl_y3, self.spin_y3, True, "P2 Y:")
        elif algo == "bezier_cubic":
            self.set_row(self.lbl_x1, self.spin_x1, True, "P0 X:")
            self.set_row(self.lbl_y1, self.spin_y1, True, "P0 Y:")
            self.set_row(self.lbl_x2, self.spin_x2, True, "P1 X:")
            self.set_row(self.lbl_y2, self.spin_y2, True, "P1 Y:")
            self.set_row(self.lbl_x3, self.spin_x3, True, "P2 X:")
            self.set_row(self.lbl_y3, self.spin_y3, True, "P2 Y:")
            self.set_row(self.lbl_x4, self.spin_x4, True, "P3 X:")
            self.set_row(self.lbl_y4, self.spin_y4, True, "P3 Y:")
        elif algo in ["polyline", "scanline"]:
            self.set_row(self.lbl_poly, self.input_polyline, True, "Vértices:")
        elif algo == "flood_fill":
            self.set_row(self.lbl_poly, self.input_polyline, True, "Polígono:")
            self.set_row(self.lbl_x1, self.spin_x1, True, "Semente X:")
            self.set_row(self.lbl_y1, self.spin_y1, True, "Semente Y:")
        elif algo == "translate":
            self.set_row(self.lbl_poly, self.input_polyline, True, "Vértices:")
            self.set_row(self.lbl_x1, self.spin_x1, True, "Desl X:")
            self.set_row(self.lbl_y1, self.spin_y1, True, "Desl Y:")
        elif algo == "rotate":
            self.set_row(self.lbl_poly, self.input_polyline, True, "Vértices:")
            self.set_row(self.lbl_x1, self.spin_x1, True, "Ângulo:")
            self.set_row(self.lbl_x2, self.spin_x2, True, "Pivô X:")
            self.set_row(self.lbl_y2, self.spin_y2, True, "Pivô Y:")
        elif algo == "scale":
            self.set_row(self.lbl_poly, self.input_polyline, True, "Vértices:")
            self.set_row(self.lbl_x1, self.spin_x1, True, "Escala X:")
            self.set_row(self.lbl_y1, self.spin_y1, True, "Escala Y:")
            self.set_row(self.lbl_x2, self.spin_x2, True, "Ponto Fixo X:")
            self.set_row(self.lbl_y2, self.spin_y2, True, "Ponto Fixo Y:")