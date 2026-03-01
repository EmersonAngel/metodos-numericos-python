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