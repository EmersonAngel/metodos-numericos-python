import time
from typing import Dict, List

import numpy as np

from utils.validaciones import validar_puntos_interpolacion


def metodo_interpolacion_polinomica(
    x_puntos: List[float],
    y_puntos: List[float],
    x_eval: float
) -> Dict:
    """
    Construye el polinomio interpolante de Lagrange y lo evalua en x_eval.
    """
    validar_puntos_interpolacion(x_puntos, y_puntos)

    inicio = time.perf_counter()

    x_arr = np.asarray(x_puntos, dtype=float)
    y_arr = np.asarray(y_puntos, dtype=float)

    polinomio = np.poly1d([0.0])
    iteraciones = []

    for i, (x_i, y_i) in enumerate(zip(x_arr, y_arr), start=1):
        base = np.poly1d([1.0])
        divisor = 1.0

        for j, x_j in enumerate(x_arr):
            if i - 1 == j:
                continue
            base *= np.poly1d([1.0, -x_j])
            divisor *= (x_i - x_j)

        base = base / divisor
        contribucion = float(y_i * base(x_eval))
        polinomio += y_i * base

        iteraciones.append({
            "n": i,
            "x_i": float(x_i),
            "y_i": float(y_i),
            "l_i": float(base(x_eval)),
            "contribucion": contribucion
        })

    y_eval = float(polinomio(x_eval))
    coeficientes = [float(coef) for coef in polinomio.c]

    acumulado = 0.0
    for it in iteraciones:
        acumulado += it["contribucion"]
        it["acumulado"] = acumulado
        it["error_abs"] = abs(y_eval - acumulado)

    return {
        "x_puntos": x_arr.tolist(),
        "y_puntos": y_arr.tolist(),
        "x_eval": float(x_eval),
        "y_eval": y_eval,
        "coeficientes": coeficientes,
        "polinomio_str": str(np.poly1d(coeficientes)),
        "iteraciones": iteraciones,
        "iteraciones_totales": len(iteraciones),
        "grado": len(x_arr) - 1,
        "tiempo": time.perf_counter() - inicio
    }
