import time
from typing import Callable, Dict


def metodo_falsa_posicion(
        f: Callable[[float], float],
        a: float,
        b: float,
        tol: float = 1e-7,
        max_iter: int = 100
) -> Dict:
    """
    Implementación del método de Falsa Posición con captura de límites a y b.
    Soluciona el error de ceros en la tabla del Ejercicio 2.
    """
    inicio = time.perf_counter()
    fa, fb = f(a), f(b)

    # Validación técnica de signos opuestos
    if fa * fb > 0:
        raise ValueError(f"f(a) y f(b) deben tener signos opuestos. f({a})={fa:.4f}, f({b})={fb:.4f}")

    iteraciones = []
    x_n_ant = a

    for n in range(1, max_iter + 1):
        # Fórmula de la Falsa Posición (Interpolación lineal)
        # x_n = b - (f(b)*(b - a)) / (f(b) - f(a))
        divisor = fb - fa
        if abs(divisor) < 1e-15:
            break

        x_n = b - (fb * (b - a)) / divisor
        f_xn = f(x_n)

        # Cálculo de errores para la tabla
        error_abs = abs(x_n - x_n_ant) if n > 1 else abs(b - a)
        error_rel = (error_abs / abs(x_n)) * 100 if x_n != 0 else 0

        # REQUISITO: Guardar a y b para evitar los ceros en la tabla
        iteraciones.append({
            "n": n,
            "a": float(a),  # Valor actual del límite izquierdo
            "b": float(b),  # Valor actual del límite derecho
            "x_n": x_n,
            "f_xn": f_xn,
            "error_abs": error_abs,
            "error_rel": error_rel
        })

        # Criterio de parada
        if error_abs < tol or abs(f_xn) < 1e-15:
            break

        # Actualización del intervalo
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
        "tiempo": tiempo_total  # Variable para el cronómetro
    }