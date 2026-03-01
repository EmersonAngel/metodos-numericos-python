import time

def metodo_newton_raphson(f, df, x0, tol, max_iter):
    inicio = time.perf_counter()
    iteraciones = []
    x_n = x0
    for n in range(1, max_iter + 1):
        fxn, dfxn = f(x_n), df(x_n)
        if abs(dfxn) < 1e-15: raise ValueError(f"Derivada nula en x={x_n}")
        x_sig = x_n - fxn / dfxn
        error_abs = abs(x_sig - x_n)
        iteraciones.append({"n": n, "x_n": x_n, "f_xn": fxn, "df_xn": dfxn,
                            "error_abs": error_abs, "error_rel": (error_abs/abs(x_sig))*100 if x_sig!=0 else 0})
        if error_abs < tol: break
        x_n = x_sig
    return {"raiz": x_n, "iteraciones": iteraciones, "tiempo": time.perf_counter() - inicio}