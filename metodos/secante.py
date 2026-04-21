import time

from utils.validaciones import validar_max_iter, validar_tolerancia


def metodo_secante(f, x0, x1, tol, max_iter):
    validar_tolerancia(tol)
    validar_max_iter(max_iter)

    inicio = time.perf_counter()
    iteraciones = []
    xn_1, xn = x0, x1

    for n in range(1, max_iter + 1):
        fxn_1 = f(xn_1)
        fxn = f(xn)

        if abs(fxn - fxn_1) < 1e-15:
            raise ValueError("Division por cero en el metodo de la secante.")

        x_mas1 = xn - fxn * (xn - xn_1) / (fxn - fxn_1)
        error_abs = abs(x_mas1 - xn)
        error_rel = (error_abs / abs(x_mas1)) * 100 if x_mas1 != 0 else 0.0

        iteraciones.append({
            "n": n,
            "xn_1": xn_1,
            "xn": xn,
            "fxn_1": fxn_1,
            "f_xn": fxn,
            "x_mas1": x_mas1,
            "error_abs": error_abs,
            "error_rel": error_rel
        })

        xn_1, xn = xn, x_mas1
        if error_abs < tol:
            break

    return {
        "raiz": xn,
        "iteraciones": iteraciones,
        "iteraciones_totales": len(iteraciones),
        "tiempo": time.perf_counter() - inicio
    }
