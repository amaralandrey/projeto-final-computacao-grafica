from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from ui.canvas import Canvas

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Trabalho Final Computação Gráfica")
        self.resize(1100, 800) 

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.main_layout = QHBoxLayout(central_widget)
     
        self.canvas = Canvas()
        self.main_layout.addWidget(self.canvas)