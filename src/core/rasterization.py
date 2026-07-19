class Rasterization:
    @staticmethod
    def bresenham_line(x1, y1, x2, y2):
        pixels = []
        
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        
        err = dx - dy

        while True:
            pixels.append((x1, y1))
            
            if x1 == x2 and y1 == y2:
                break
                
            e2 = 2 * err
            
            if e2 > -dy:
                err -= dy
                x1 += sx
                
            if e2 < dx:
                err += dx
                y1 += sy
                
        return pixels

    @staticmethod
    def bresenham_circle(xc, yc, r):
        pixels = []
        x = 0
        y = r
        d = 3 - 2 * r

        def add_circle_points(xc, yc, x, y):
            pixels.extend([
                (xc + x, yc + y), (xc - x, yc + y),
                (xc + x, yc - y), (xc - x, yc - y),
                (xc + y, yc + x), (xc - y, yc + x),
                (xc + y, yc - x), (xc - y, yc - x)
            ])

        add_circle_points(xc, yc, x, y)
        
        while y >= x:
            x += 1
            if d > 0:
                y -= 1
                d = d + 4 * (x - y) + 10
            else:
                d = d + 4 * x + 6
            add_circle_points(xc, yc, x, y)
            
        return list(set(pixels))
    
    @staticmethod
    def midpoint_ellipse(xc, yc, rx, ry):
        pixels = []
        rx2 = rx * rx
        ry2 = ry * ry
        two_rx2 = 2 * rx2
        two_ry2 = 2 * ry2
        
        x = 0
        y = ry
        p = ry2 - (rx2 * ry) + (0.25 * rx2)
        px = 0
        py = two_rx2 * y
        
        def add_ellipse_points(xc, yc, x, y):
            pixels.extend([
                (xc + x, yc + y), (xc - x, yc + y),
                (xc + x, yc - y), (xc - x, yc - y)
            ])
            
        while px < py:
            add_ellipse_points(xc, yc, x, y)
            x += 1
            px += two_ry2
            if p < 0:
                p += ry2 + px
            else:
                y -= 1
                py -= two_rx2
                p += ry2 + px - py
        
        p = ry2 * (x + 0.5)**2 + rx2 * (y - 1)**2 - rx2 * ry2
        while y >= 0:
            add_ellipse_points(xc, yc, x, y)
            y -= 1
            py -= two_rx2
            if p > 0:
                p += rx2 - py
            else:
                x += 1
                px += two_ry2
                p += rx2 - py + px
                
        return list(set(pixels))

    @staticmethod
    def bezier_quad(x0, y0, x1, y1, x2, y2, steps=20):
        pixels = []
        last_x, last_y = x0, y0
        
        for i in range(1, steps + 1):
            t = i / steps
            
            curr_x = int(round((1 - t)**2 * x0 + 2 * (1 - t) * t * x1 + t**2 * x2))
            curr_y = int(round((1 - t)**2 * y0 + 2 * (1 - t) * t * y1 + t**2 * y2))
            
            pixels.extend(Rasterization.bresenham_line(last_x, last_y, curr_x, curr_y))
            
            last_x, last_y = curr_x, curr_y
            
        return list(set(pixels)) 

    @staticmethod
    def bezier_cubic(x0, y0, x1, y1, x2, y2, x3, y3, steps=20):
        pixels = []
        last_x, last_y = x0, y0
        
        for i in range(1, steps + 1):
            t = i / steps
            
            curr_x = int(round((1 - t)**3 * x0 + 3 * (1 - t)**2 * t * x1 + 3 * (1 - t) * t**2 * x2 + t**3 * x3))
            curr_y = int(round((1 - t)**3 * y0 + 3 * (1 - t)**2 * t * y1 + 3 * (1 - t) * t**2 * y2 + t**3 * y3))
            
            pixels.extend(Rasterization.bresenham_line(last_x, last_y, curr_x, curr_y))
            last_x, last_y = curr_x, curr_y
            
        return list(set(pixels))
    
    @staticmethod
    def polyline(points):
        pixels = []
        for i in range(len(points) - 1):
            p1 = points[i]
            p2 = points[i+1]
            pixels.extend(Rasterization.bresenham_line(p1[0], p1[1], p2[0], p2[1]))
            
        return list(set(pixels))
    
    @staticmethod
    def scanline_fill(points):
        if len(points) < 3:
            return []
            
        pixels = set()
        
        closed_points = points + [points[0]]
        pixels.update(Rasterization.polyline(closed_points))
        
        min_y = min(p[1] for p in points)
        max_y = max(p[1] for p in points)
        
        for y in range(min_y, max_y + 1):
            intersections = []
            for i in range(len(points)):
                p1 = points[i]
                p2 = points[(i + 1) % len(points)]
                
                if p1[1] == p2[1]:
                    continue
                
                if min(p1[1], p2[1]) <= y < max(p1[1], p2[1]):
                    x = p1[0] + (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1])
                    intersections.append(x)
            
            intersections.sort()
            
            for i in range(0, len(intersections), 2):
                if i + 1 < len(intersections):
                    x_start = int(round(intersections[i]))
                    x_end = int(round(intersections[i+1]))
                    for x in range(x_start, x_end + 1):
                        pixels.add((x, y))
                        
        return list(pixels)

    @staticmethod
    def flood_fill_recursive(points, seed_x, seed_y):
        if len(points) < 3:
            return []
            
        closed_points = points + [points[0]]
        boundary = set(Rasterization.polyline(closed_points))
        
        pixels = set(boundary)
        visited = set()
        
        def fill(x, y):
            if x < -11 or x > 11 or y < -11 or y > 11:
                return
            if (x, y) in pixels or (x, y) in visited:
                return
            
            visited.add((x, y))
            pixels.add((x, y))
            
            fill(x + 1, y) # Direita
            fill(x - 1, y) # Esquerda
            fill(x, y + 1) # Cima
            fill(x, y - 1) # Baixo
            
        fill(seed_x, seed_y)
        return list(pixels)