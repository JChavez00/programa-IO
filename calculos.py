# calculos.py

def calcular_probabilidades(prob_demanda, prob_demora):
    """Calcula la probabilidad total y acumulada de la demanda durante el tiempo de espera."""
    prob_total = {i: 0.0 for i in range(10)}

    # Demora 1 día
    for d1, p_d1 in prob_demanda.items():
        prob_total[d1] += p_d1 * prob_demora[1]

    # Demora 2 días
    for d1, p_d1 in prob_demanda.items():
        for d2, p_d2 in prob_demanda.items():
            prob_total[d1 + d2] += p_d1 * p_d2 * prob_demora[2]

    # Demora 3 días
    for d1, p_d1 in prob_demanda.items():
        for d2, p_d2 in prob_demanda.items():
            for d3, p_d3 in prob_demanda.items():
                prob_total[d1 + d2 + d3] += p_d1 * p_d2 * p_d3 * prob_demora[3]

    prob_acumulada = {}
    acumulado = 0.0
    for i in range(9, -1, -1):
        acumulado += prob_total[i]
        prob_acumulada[i] = acumulado

    return prob_total, prob_acumulada


def calcular_esperanza_y_costos(prob_total, q1, q2, q3, beta, y, delta_y):
    """Calcula E(D) y el Costo Total para cada Punto de Reorden (R)."""
    resultados = {}
    
    for r in range(9, 0, -1):
        # 1. Calcular Esperanza de Desabastecimiento E(D)
        esperanza_d = 0.0
        for demanda in range(r + 1, 10):  # Solo evalúa cuando Demanda > R
            esperanza_d += (demanda - r) * prob_total[demanda]
        
        # 2. Calcular Costo Total según la fórmula de la pizarra
        costo_almacenamiento = ((y / 2) + r - delta_y) * q1
        costo_pedido = (beta / y) * q2
        costo_escasez = esperanza_d * q3 * (beta / y)
        
        costo_total = costo_almacenamiento + costo_pedido + costo_escasez
        
        resultados[r] = {
            "E(D)": esperanza_d,
            "Costo": costo_total
        }
        
    return resultados