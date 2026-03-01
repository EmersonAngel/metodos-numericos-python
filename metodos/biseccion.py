import time
from typing import Callable, Dict


def metodo_biseccion(
        f: Callable[[float], float],
        a: float,
        b: float,
        tol: float = 1e-6,
        max_iter: int = 100
) -> Dict:
    """
    Implementación corregida para el Ejercicio 1.
    Incluye cronómetro de alta precisión y validación de intervalo.
    """
    inicio = time.perf_counter()

    fa, fb = f(a), f(b)
    if fa * fb > 0:
        raise ValueError(f"f(a) y f(b) deben tener signos opuestos para encerrar la raíz.")

    iteraciones = []
    x_n_ant = a

    for n in range(1, max_iter + 1):
        x_n = (a + b) / 2.0
        f_xn = f(x_n)

        # Cálculo de errores según especificaciones técnicas
        error_abs = abs(x_n - x_n_ant) if n > 1 else abs(b - a)
        error_rel = (error_abs / abs(x_n)) * 100 if x_n != 0 else 0

        # Importante: Las llaves deben ser exactas para la tabla GUI
        iteraciones.append({
            "n": n,
            "a": a,
            "b": b,
            "x_n": x_n,
            "f_xn": f_xn,
            "error_abs": error_abs,
            "error_rel": error_rel
        })

        # Criterio de convergencia
        if error_abs < tol or abs(f_xn) < 1e-15:
            break

        # Reducción del intervalo
        if fa * f_xn < 0:
            b, fb = x_n, f_xn
        else:
            a, fa = x_n, f_xn
        x_n_ant = x_n

    tiempo_total = time.perf_counter() - inicio

    return {
        "raiz": x_n,
        "iteraciones": iteraciones,
        "iteraciones_totales": n,
        "tiempo": tiempo_total  # Esta es la llave que suma el cronómetro en la app
    }
