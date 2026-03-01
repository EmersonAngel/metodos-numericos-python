import time

def metodo_secante(f, x0, x1, tol, max_iter):
    inicio = time.perf_counter()
    iteraciones = []
    xn_1, xn = x0, x1
    for n in range(1, max_iter + 1):
        fxn_1, fxn = f(xn_1), f(xn)
        if abs(fxn - fxn_1) < 1e-15: raise ValueError("División por cero")
        x_mas1 = xn - fxn * (xn - xn_1) / (fxn - fxn_1)
        error_abs = abs(x_mas1 - xn)
        iteraciones.append({"n": n, "xn_1": xn_1, "xn": xn, "fxn_1": fxn_1, "f_xn": fxn, "x_mas1": x_mas1, "error_abs": error_abs})
        if error_abs < tol: break
        xn_1, xn = xn, x_mas1
    return {"raiz": xn, "iteraciones": iteraciones, "tiempo": time.perf_counter() - inicio}