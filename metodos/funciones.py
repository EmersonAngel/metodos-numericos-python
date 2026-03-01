import numpy as np
from utils.evaluador import evaluar_funcion


def evaluar_en_punto(funcion_str, x):

    resultado = evaluar_funcion(funcion_str, x)

    return {
        "x": x,
        "f(x)": resultado
    }


def analizar_intervalo(funcion_str, a, b):

    fa = evaluar_funcion(funcion_str, a)
    fb = evaluar_funcion(funcion_str, b)

    cambio_signo = fa * fb < 0

    return {
        "a": a,
        "f(a)": fa,
        "b": b,
        "f(b)": fb,
        "cambio_signo": cambio_signo
    }


def generar_datos_grafica(funcion_str, x_min=-10, x_max=10, puntos=400):

    x_vals = np.linspace(x_min, x_max, puntos)
    y_vals = []

    for x in x_vals:
        try:
            y = evaluar_funcion(funcion_str, x)
        except:
            y = np.nan
        y_vals.append(y)

    return x_vals, np.array(y_vals)