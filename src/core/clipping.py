INSIDE = 0  # 0000
LEFT   = 1  # 0001
RIGHT  = 2  # 0010
BOTTOM = 4  # 0100
TOP    = 8  # 1000

def compute_code(x, y, x_min, y_min, x_max, y_max):
    """Calcula o código de região para um ponto (x, y)."""
    code = INSIDE
    if x < x_min:      # À esquerda da janela
        code |= LEFT
    elif x > x_max:    # À direita da janela
        code |= RIGHT
        
    if y < y_min:      # Abaixo da janela
        code |= BOTTOM
    elif y > y_max:    # Acima da janela
        code |= TOP
        
    return code

def cohen_sutherland_clip(x1, y1, x2, y2, x_min, y_min, x_max, y_max):
    """
    Recorta uma linha delimitada por (x1, y1) e (x2, y2) 
    usando a janela de recorte [x_min, y_min, x_max, y_max].
    """
    code1 = compute_code(x1, y1, x_min, y_min, x_max, y_max)
    code2 = compute_code(x2, y2, x_min, y_min, x_max, y_max)
    accept = False

    while True:
        # Caso 1: Ambos os pontos estão dentro da janela (Trivialmente aceito)
        if code1 == 0 and code2 == 0:
            accept = True
            break
        
        # Caso 2: Ambos os pontos compartilham uma região exterior (Trivialmente rejeitado)
        elif (code1 & code2) != 0:
            break
            
        # Caso 3: A linha cruza a janela, precisamos calcular a interseção
        else:
            x = 0.0
            y = 0.0
            
            # Escolhe um ponto que está fora da janela
            code_out = code1 if code1 != 0 else code2

            # Encontra a interseção usando a fórmula da reta:
            # y = y1 + m * (x - x1)  OU  x = x1 + (1/m) * (y - y1)
            
            if code_out & TOP:
                x = x1 + (x2 - x1) * (y_max - y1) / (y2 - y1)
                y = y_max
            elif code_out & BOTTOM:
                x = x1 + (x2 - x1) * (y_min - y1) / (y2 - y1)
                y = y_min
            elif code_out & RIGHT:
                y = y1 + (y2 - y1) * (x_max - x1) / (x2 - x1)
                x = x_max
            elif code_out & LEFT:
                y = y1 + (y2 - y1) * (x_min - x1) / (x2 - x1)
                x = x_min

            # Substitui o ponto fora da janela pelo ponto de interseção
            if code_out == code1:
                x1, y1 = x, y
                code1 = compute_code(x1, y1, x_min, y_min, x_max, y_max)
            else:
                x2, y2 = x, y
                code2 = compute_code(x2, y2, x_min, y_min, x_max, y_max)
                
    if accept:
        # Retorna as coordenadas arredondadas para manter a integridade da grade de inteiros
        return (round(x1), round(y1), round(x2), round(y2))
    else:
        # Retorna None se a linha foi totalmente rejeitada (invisível)
        return None
    
# Mantenha o código de linha (cohen_sutherland_clip) intacto acima desta parte

def sutherland_hodgman_clip(polygon, x_min, y_min, x_max, y_max):
    """
    Recorta um polígono (lista de pontos) usando a janela [x_min, y_min, x_max, y_max].
    """
    def clip_edge(poly, edge):
        new_poly = []
        if not poly: 
            return new_poly
        
        # Função auxiliar para verificar se um ponto está "dentro" da área útil
        def inside(p):
            x, y = p
            if edge == 'LEFT': return x >= x_min
            if edge == 'RIGHT': return x <= x_max
            if edge == 'BOTTOM': return y >= y_min
            if edge == 'TOP': return y <= y_max

        # Função auxiliar para encontrar a interseção entre p1-p2 e a borda atual
        def intersect(p1, p2):
            x1, y1 = p1
            x2, y2 = p2
            if edge == 'LEFT':
                x = x_min
                y = y1 + (y2 - y1) * (x_min - x1) / (x2 - x1)
            elif edge == 'RIGHT':
                x = x_max
                y = y1 + (y2 - y1) * (x_max - x1) / (x2 - x1)
            elif edge == 'BOTTOM':
                y = y_min
                x = x1 + (x2 - x1) * (y_min - y1) / (y2 - y1)
            elif edge == 'TOP':
                y = y_max
                x = x1 + (x2 - x1) * (y_max - y1) / (y2 - y1)
            return (round(x), round(y))

        # Percorre as arestas do polígono
        p1 = poly[-1] # O último ponto se liga ao primeiro (fecha o polígono)
        for p2 in poly:
            if inside(p2):
                if not inside(p1):
                    # Se p2 tá dentro e p1 tá fora, adiciona a interseção
                    new_poly.append(intersect(p1, p2))
                # Adiciona o próprio ponto p2
                new_poly.append(p2)
            elif inside(p1):
                # Se p2 tá fora mas p1 tá dentro, adiciona apenas a interseção
                new_poly.append(intersect(p1, p2))
            p1 = p2
            
        return new_poly

    # Aplica o recorte para as quatro bordas, usando o resultado anterior
    clipped = polygon
    for edge_name in ['LEFT', 'RIGHT', 'BOTTOM', 'TOP']:
        clipped = clip_edge(clipped, edge_name)
        
    return clipped