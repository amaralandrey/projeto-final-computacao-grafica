class Viewport:
    def __init__(self, width, height, min_val=-11, max_val=11):
        self.width = width
        self.height = height
        self.range_val = max_val - min_val
        
        self.scale_x = self.width / self.range_val
        self.scale_y = self.height / self.range_val
        
        self.center_x = self.width / 2
        self.center_y = self.height / 2

    def math_to_screen(self, x, y):
        screen_x = self.center_x + (x * self.scale_x)
        screen_y = self.center_y - (y * self.scale_y)
        return int(round(screen_x)), int(round(screen_y))