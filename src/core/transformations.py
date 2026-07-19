import math

class Transformations:
    @staticmethod
    def translate(points, dx, dy):
        return [(p[0] + dx, p[1] + dy) for p in points]

    @staticmethod
    def rotate(points, angle_deg, px, py):
        angle_rad = math.radians(angle_deg)
        cos_val = math.cos(angle_rad)
        sin_val = math.sin(angle_rad)
        
        rotated = []
        for x, y in points:
            # Transladar para a origem do pivô
            tx, ty = x - px, y - py
            # Rotacionar
            rx = tx * cos_val - ty * sin_val
            ry = tx * sin_val + ty * cos_val
            # Transladar de volta
            rotated.append((int(round(rx + px)), int(round(ry + py))))
        return rotated

    @staticmethod
    def scale(points, sx, sy, fx, fy):
        scaled = []
        for x, y in points:
            # Escalar em relação ao ponto fixo (fx, fy)
            sx_val = fx + (x - fx) * sx
            sy_val = fy + (y - fy) * sy
            scaled.append((int(round(sx_val)), int(round(sy_val))))
        return scaled