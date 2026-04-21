from typing import Callable


def validar_intervalo(
    funcion: Callable[[float], float],
    a: float,
    b: float
) -> None:
    """
    Verifica que el intervalo [a, b] tenga cambio de signo.
    """

    f_a = funcion(a)
    f_b = funcion(b)

    if f_a * f_b > 0:
        raise ValueError(
            "El intervalo no contiene una raíz (no hay cambio de signo)."
        )


def validar_division_por_cero(valor: float) -> None:
    """
    Verifica que un valor no sea cero para evitar división por cero.
    """

    if valor == 0:
        raise ZeroDivisionError("División por cero detectada.")


def validar_convergencia(
    error: float,
    tolerancia: float,
    iteracion: int,
    max_iter: int
) -> None:
    """
    Verifica si se alcanzó la convergencia o se excedió el máximo de iteraciones.
    """

    if iteracion >= max_iter and error > tolerancia:
        raise ValueError(
            "El método no convergió dentro del número máximo de iteraciones."
        )


def validar_tolerancia(tolerancia: float) -> None:
    """
    Verifica que la tolerancia sea positiva.
    """

    if tolerancia <= 0:
        raise ValueError("La tolerancia debe ser mayor que cero.")


def validar_max_iter(max_iter: int) -> None:
    """
    Verifica que el maximo de iteraciones sea positivo.
    """

    if max_iter <= 0:
        raise ValueError("El numero maximo de iteraciones debe ser mayor que cero.")


def validar_puntos_interpolacion(x_puntos, y_puntos) -> None:
    """
    Verifica la integridad de los puntos usados para interpolacion.
    """

    if len(x_puntos) != len(y_puntos):
        raise ValueError("Las listas de x e y deben tener la misma cantidad de elementos.")

    if len(x_puntos) < 2:
        raise ValueError("Se requieren al menos dos puntos para interpolar.")

    if len(set(x_puntos)) != len(x_puntos):
        raise ValueError("Los valores de x no pueden repetirse en interpolacion.")
