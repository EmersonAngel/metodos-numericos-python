import time
from typing import Callable, Dict

from utils.validaciones import validar_intervalo, validar_max_iter, validar_tolerancia


def metodo_falsa_posicion(
    f: Callable[[float], float],
    a: float,
    b: float,
    tol: float = 1e-7,
    max_iter: int = 100
) -> Dict:
    """
    Implementacion del metodo de falsa posicion con captura completa del intervalo.
    """
    validar_tolerancia(tol)
    validar_max_iter(max_iter)
    validar_intervalo(f, a, b)

    inicio = time.perf_counter()
    fa, fb = f(a), f(b)
    iteraciones = []
    x_n_ant = a

    for n in range(1, max_iter + 1):
        divisor = fb - fa
        if abs(divisor) < 1e-15:
            raise ValueError("No es posible continuar: f(b) - f(a) es demasiado pequeno.")

        x_n = b - (fb * (b - a)) / divisor
        f_xn = f(x_n)
        error_abs = abs(x_n - x_n_ant) if n > 1 else abs(b - a)
        error_rel = (error_abs / abs(x_n)) * 100 if x_n != 0 else 0.0

        iteraciones.append({
            "n": n,
            "a": float(a),
            "b": float(b),
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
