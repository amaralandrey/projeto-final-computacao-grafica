import math

class Projections:

    @staticmethod
    def orthographic(points_3d, plane):
        """
        Projeção Ortográfica (Paralela).
        plane: 1 = Plano XY, 2 = Plano XZ, 3 = Plano YZ
        """
        projected = []
        for x, y, z in points_3d:
            if plane == 1:
                projected.append((x, y))
            elif plane == 2:
                projected.append((x, z))
            elif plane == 3:
                projected.append((z, y))
            else:
                projected.append((x, y)) 
        return projected

    @staticmethod
    def oblique(points_3d, angle_degrees, L):
        """
        Projeção Oblíqua (Cavaleira ou Cabinet).
        angle_degrees: Ângulo das linhas de fuga (ex: 30°, 45°, 60°).
        L: Fator de encurtamento (1.0 para Cavaleira, 0.5 para Cabinet).
        """
        projected = []
        angle_rad = math.radians(angle_degrees)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)

        for x, y, z in points_3d:
            px = x + z * L * cos_a
            py = y + z * L * sin_a
            projected.append((px, py))
            
        return projected

    @staticmethod
    def perspective(points_3d, d):
        """
        Projeção Perspectiva.
        d: Distância focal (distância do centro de projeção até o plano de visão).
        Assume o plano de projeção em Z=0 e o observador em Z = -d.
        """
        projected = []
        for x, y, z in points_3d:
            if d == 0:
                projected.append((x, y))
                continue
                
            denominador = z + d
            
            if denominador == 0:
                denominador = 0.0001 
                
            px = x * (d / denominador)
            py = y * (d / denominador)
            
            projected.append((px, py))
            
        return projected