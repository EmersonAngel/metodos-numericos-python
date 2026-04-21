import time
from typing import Callable, Dict

from utils.validaciones import validar_intervalo, validar_max_iter, validar_tolerancia


def metodo_biseccion(
    f: Callable[[float], float],
    a: float,
    b: float,
    tol: float = 1e-6,
    max_iter: int = 100
) -> Dict:
    """
    Implementacion del metodo de biseccion con trazabilidad de iteraciones.
    """
    validar_tolerancia(tol)
    validar_max_iter(max_iter)
    validar_intervalo(f, a, b)

    inicio = time.perf_counter()
    fa, fb = f(a), f(b)
    iteraciones = []
    x_n_ant = a

    for n in range(1, max_iter + 1):
        x_n = (a + b) / 2.0
        f_xn = f(x_n)

        error_abs = abs(x_n - x_n_ant) if n > 1 else abs(b - a)
        error_rel = (error_abs / abs(x_n)) * 100 if x_n != 0 else 0.0

        iteraciones.append({
            "n": n,
            "a": a,
            "b": b,
            "x_n": x_n,
            "f_xn": f_xn,
            "error_abs": error_abs,
            "error_rel": error_rel
        })

        if error_abs < tol or abs(f_xn) < 1e-15:
            break

        if fa * f_xn < 0:
            b, fb = x_n, f_xn
        else:
            a, fa = x_n, f_xn

        x_n_ant = x_n

    return {
        "raiz": x_n,
        "iteraciones": iteraciones,
        "iteraciones_totales": len(iteraciones),
        "tiempo": time.perf_counter() - inicio
    }
