import time

from utils.validaciones import validar_max_iter, validar_tolerancia


def metodo_punto_fijo(g, x0, tol, max_iter):
    validar_tolerancia(tol)
    validar_max_iter(max_iter)

    inicio = time.perf_counter()
    iteraciones = []
    x_n = x0

    h = 1e-5
    derivada_x0 = (g(x0 + h) - g(x0 - h)) / (2 * h)

    for n in range(1, max_iter + 1):
        g_xn = g(x_n)
        error_abs = abs(g_xn - x_n)
        error_rel = (error_abs / abs(g_xn)) * 100 if g_xn != 0 else 0.0

        iteraciones.append({
            "n": n,
            "x_n": x_n,
            "g_xn": g_xn,
            "error_abs": error_abs,
            "error_rel": error_rel
        })

        if abs(g_xn) > 1e6:
            raise ValueError("El metodo esta divergiendo. Verifique que |g'(x)| < 1.")

        x_n = g_xn
        if error_abs < tol:
            break

    return {
        "raiz": x_n,
        "derivada_inicial": derivada_x0,
        "iteraciones": iteraciones,
        "iteraciones_totales": len(iteraciones),
        "tiempo": time.perf_counter() - inicio
    }
