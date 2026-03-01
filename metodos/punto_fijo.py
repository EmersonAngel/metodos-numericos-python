import time


def metodo_punto_fijo(g, x0, tol, max_iter):
    inicio = time.perf_counter()
    iteraciones = []
    x_n = x0

    # Cálculo automático de la derivada numérica para validación
    h = 1e-5
    derivada_x0 = (g(x0 + h) - g(x0 - h)) / (2 * h)

    for n in range(1, max_iter + 1):
        g_xn = g(x_n)
        error_abs = abs(g_xn - x_n)

        iteraciones.append({
            "n": n,
            "x_n": x_n,
            "g_xn": g_xn,
            "error_abs": error_abs
        })

        # Detección de divergencia según consideraciones técnicas
        if abs(g_xn) > 1e6:
            raise ValueError("El método está divergiendo. Verifique que |g'(x)| < 1.")

        if error_abs < tol:
            break
        x_n = g_xn

    return {
        "raiz": g_xn,
        "derivada_inicial": derivada_x0,
        "iteraciones": iteraciones,
        "iteraciones_totales": n,
        "tiempo": time.perf_counter() - inicio
    }