import numpy as np


def evaluar_funcion(funcion_str, x):
    """
    Evalúa la función ingresada por el usuario.
    Permite usar numpy como np.
    """
    try:
        return eval(funcion_str, {"np": np, "x": x})
    except Exception:
        raise ValueError("Error al evaluar la función.")