# ============
# EJERCICIO 1
# ============

import numpy as np


def funcion_hash_table(lam):
    """
    Calcula T(λ) = 2.5 + 0.8λ² - 3.2λ + ln(λ + 1).
    Soporta tanto escalares como arrays de NumPy.
    """
    # Convertimos a array de numpy si no lo es para asegurar compatibilidad
    lam = np.asanyarray(lam)

    # Usamos np.errstate para que no ensucie la consola con advertencias de log(-1)
    with np.errstate(invalid='ignore'):
        # np.log devolverá NaN donde lam + 1 <= 0
        resultado = 2.5 + 0.8 * (lam ** 2) - 3.2 * lam + np.log(lam + 1)

    return resultado

# ============
# EJERCICIO 2
# ============

def funcion_balanceo_carga(x: float) -> float:
    """E(x) = x^3 - 6x^2 + 11x - 6.5."""
    x = np.asanyarray(x)
    return x**3 - 6*x**2 + 11*x - 6.5

# ============
# EJERCICIO 3
# ============

# Ejercicio 3: Crecimiento de Base de Datos
def g_crecimiento_db(x):
    return 0.5 * np.cos(x) + 1.5

def dg_crecimiento_db(x):
    return -0.5 * np.sin(x)

# ============
# EJERCICIO 4
# ============

def funcion_newton_threads(n):
    return n**3 - 8*n**2 + 20*n - 16 # T(n)

def derivada_newton_threads(n):
    return 3*n**2 - 16*n + 20 # T'(n)

# ============
# EJERCICIO 5
# ============

def funcion_escalabilidad_cloud(x):
    """
    P(x) = x * e^(-x/2) - 0.3
    Modelo de probabilidad de éxito en peticiones cloud.
    """
    return x * np.exp(-x / 2) - 0.3

def derivada_escalabilidad_newton(x):
    """
    P'(x) = e^(-x/2) * (1 - x/2)
    Derivada necesaria para comparar Newton vs Secante en el Ex 5.
    """
    return np.exp(-x / 2) * (1 - x / 2)