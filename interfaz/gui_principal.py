import tkinter as tk
from tkinter import messagebox, ttk

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from funciones.definiciones import (
    derivada_escalabilidad_newton,
    derivada_newton_threads,
    funcion_balanceo_carga,
    funcion_escalabilidad_cloud,
    funcion_hash_table,
    funcion_newton_threads,
    g_crecimiento_db,
)
from metodos.biseccion import metodo_biseccion
from metodos.falsa_posicion import metodo_falsa_posicion
from metodos.interpolacion_polinomica import metodo_interpolacion_polinomica
from metodos.newton import metodo_newton_raphson
from metodos.punto_fijo import metodo_punto_fijo
from metodos.secante import metodo_secante


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Software Metodos Numericos - Dashboard de Ingenieria")
        self.geometry("1550x920")
        self.configure(bg="#0f172a")

        self.metodo_actual = "Ex1"
        self.historial = {
            "Ex1": {"data": {}, "last_time": 0.0, "time_detail": ""},
            "Ex2": {"Falsa": None, "Bisec": None, "last_time": 0.0, "time_detail": ""},
            "Ex3": {"data": {}, "last_time": 0.0, "time_detail": ""},
            "Ex4": {"data": {}, "last_time": 0.0, "time_detail": ""},
            "Ex5": {"data": {}, "last_time": 0.0, "time_detail": ""},
            "Ex6": {"data": {}, "last_time": 0.0, "time_detail": ""},
        }
        self.paleta = ["#38bdf8", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2"]

        self._configurar_estilos()
        self._crear_layout_base()
        self._cargar_componentes()

    def _configurar_estilos(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#1e293b", foreground="white", fieldbackground="#1e293b", rowheight=30)
        style.configure("Treeview.Heading", background="#334155", foreground="white", font=("Segoe UI", 10, "bold"))

    def _crear_layout_base(self) -> None:
        self.sidebar = tk.Frame(self, bg="#0b1120", width=260)
        self.sidebar.pack(side="left", fill="y")
        self.main_area = tk.Frame(self, bg="#0f172a")
        self.main_area.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    def _cargar_componentes(self) -> None:
        for child in self.main_area.winfo_children():
            child.destroy()
        for child in self.sidebar.winfo_children():
            child.destroy()

        self._crear_menu_lateral()
        self._crear_cabecera()
        self._crear_panel_entrada()

        self.frame_tiempo = tk.Frame(self.main_area, bg="#1e293b", bd=2, relief="groove")
        self.frame_tiempo.pack(fill="x", pady=10)

        self.lbl_status = tk.Label(
            self.frame_tiempo,
            text="Tiempo de ejecucion: 0.00000000 s",
            bg="#1e293b",
            fg="#38bdf8",
            font=("Segoe UI", 12, "bold"),
            pady=10,
        )
        self.lbl_status.pack()

        dashboard = tk.Frame(self.main_area, bg="#0f172a")
        dashboard.pack(fill="both", expand=True)

        self.frame_tabla = tk.Frame(dashboard, bg="#1e293b", padx=10, pady=10)
        self.frame_tabla.pack(side="left", fill="both", expand=True, padx=(0, 10))
        self._crear_tabla()

        self.frame_grafica = tk.Frame(dashboard, bg="#1e293b", padx=10, pady=10)
        self.frame_grafica.pack(side="right", fill="both", expand=True)
        self._inicializar_matplotlib()

        self._recuperar_estado_persistente()

    def _crear_menu_lateral(self) -> None:
        tk.Label(self.sidebar, text="METODOS", bg="#0b1120", fg="#64748b", font=("Segoe UI", 10, "bold")).pack(pady=20)

        opciones = [
            ("Ejercicio 1 - Biseccion", "Ex1"),
            ("Ejercicio 2 - Falsa Posicion", "Ex2"),
            ("Ejercicio 3 - Punto Fijo", "Ex3"),
            ("Ejercicio 4 - Newton Raphson", "Ex4"),
            ("Ejercicio 5 - Secante", "Ex5"),
            ("Ejercicio 6 - Interpolacion", "Ex6"),
        ]

        for texto, id_metodo in opciones:
            boton = tk.Button(
                self.sidebar,
                text=texto,
                bg="#1e293b",
                fg="white",
                relief="flat",
                pady=12,
                command=lambda metodo=id_metodo: self._cambiar_metodo(metodo),
            )
            boton.pack(fill="x", pady=1, padx=15)

    def _crear_cabecera(self) -> None:
        titulos = {
            "Ex1": "Ejercicio 1 - Biseccion Hash",
            "Ex2": "Ejercicio 2 - Comparativa",
            "Ex3": "Ejercicio 3 - Punto Fijo",
            "Ex4": "Ejercicio 4 - Newton",
            "Ex5": "Ejercicio 5 - Secante",
            "Ex6": "Ejercicio 6 - Interpolacion Polinomica",
        }
        descripciones = {
            "Ex1": "CONTEXTO: Optimizacion de cache distribuido.\nT(l) = 2.5 + 0.8l^2 - 3.2l + ln(l + 1)",
            "Ex2": "CONTEXTO: Balanceo de carga en servidores.\nE(x) = x^3 - 6x^2 + 11x - 6.5",
            "Ex3": "CONTEXTO: Crecimiento de base de datos.\ng(x) = 0.5cos(x) + 1.5",
            "Ex4": "CONTEXTO: Overhead de sincronizacion en threads.\nT(n) = n^3 - 8n^2 + 20n - 16",
            "Ex5": "CONTEXTO: Escalabilidad cloud.\nP(x) = x*e^(-x/2) - 0.3",
            "Ex6": "CONTEXTO: Ajuste exacto de datos por interpolacion.\nUse x como lista CSV, y como lista CSV y el tercer campo como x a evaluar.",
        }

        tk.Label(
            self.main_area,
            text=titulos.get(self.metodo_actual, ""),
            font=("Segoe UI", 20, "bold"),
            bg="#0f172a",
            fg="#38bdf8",
        ).pack()

        tk.Label(
            self.main_area,
            text=descripciones.get(self.metodo_actual, ""),
            font=("Consolas", 10),
            bg="#0f172a",
            fg="#94a3b8",
            justify="center",
        ).pack(pady=(0, 10))

    def _defaults_por_metodo(self):
        return {
            "Ex1": {
                "labels": ("x0 / a:", "b / x1:", "Tol:"),
                "values": ("-0.999", "1.0", "1e-6"),
            },
            "Ex2": {
                "labels": ("a:", "b:", "Tol:"),
                "values": ("2.0", "4.0", "1e-7"),
            },
            "Ex3": {
                "labels": ("x0:", "Reservado:", "Tol:"),
                "values": ("1.0", "0", "1e-8"),
            },
            "Ex4": {
                "labels": ("x0:", "Reservado:", "Tol:"),
                "values": ("5.0", "0", "1e-10"),
            },
            "Ex5": {
                "labels": ("x0:", "x1:", "Tol:"),
                "values": ("0.5", "1.0", "1e-9"),
            },
            "Ex6": {
                "labels": ("x puntos:", "y puntos:", "x eval:"),
                "values": ("0,1,2,3", "1,3,2,5", "1.5"),
            },
        }

    def _crear_panel_entrada(self) -> None:
        card = tk.LabelFrame(
            self.main_area,
            text=" PARAMETROS ",
            bg="#1e293b",
            fg="#94a3b8",
            font=("Segoe UI", 9, "bold"),
            padx=15,
            pady=15,
            relief="flat",
        )
        card.pack(fill="x", pady=(0, 15))

        definicion = self._defaults_por_metodo()[self.metodo_actual]
        labels = definicion["labels"]
        values = definicion["values"]

        params = [("ent_a", labels[0], values[0]), ("ent_b", labels[1], values[1]), ("ent_tol", labels[2], values[2])]
        for i, (attr, texto, valor) in enumerate(params):
            tk.Label(card, text=texto, bg="#1e293b", fg="white").grid(row=0, column=i * 2, padx=5)
            entry = tk.Entry(card, width=28 if self.metodo_actual == "Ex6" and i < 2 else 12, bg="#0f172a", fg="white", insertbackground="white")
            entry.insert(0, valor)
            entry.grid(row=0, column=i * 2 + 1, padx=5)
            setattr(self, attr, entry)

        tk.Button(card, text="CALCULAR", bg="#2563eb", fg="white", command=self.calcular, relief="flat", padx=20).grid(
            row=0, column=6, padx=15
        )
        tk.Button(card, text="BORRAR ACTUAL", bg="#ef4444", fg="white", command=self._limpiar_actual, relief="flat", padx=20).grid(
            row=0, column=7
        )

    def _crear_tabla(self) -> None:
        columnas = {
            "Ex1": (("n", "a", "b", "x_n", "f_xn", "e_abs", "e_rel"), ("n", "a", "b", "x_n", "f(x_n)", "|Err Abs|", "Err Rel %")),
            "Ex2": (("n", "a", "b", "x_n", "f_xn", "e_abs", "e_rel"), ("n", "a", "b", "x_n", "f(x_n)", "|Err Abs|", "Err Rel %")),
            "Ex3": (("n", "x_n", "g_xn", "e_abs", "e_rel"), ("n", "x_n", "g(x_n)", "|x_n-g|", "Err Rel %")),
            "Ex4": (("n", "x_n", "f_xn", "df_xn", "e_abs", "e_rel"), ("n", "x_n", "f(x_n)", "f'(x_n)", "|Err Abs|", "Err Rel %")),
            "Ex5": (("n", "xn_1", "xn", "fxn_1", "fxn", "xn_mas1", "e_abs"), ("n", "x_{n-1}", "x_n", "f(x_{n-1})", "f(x_n)", "x_{n+1}", "|Err Abs|")),
            "Ex6": (("n", "x_i", "y_i", "l_i", "contribucion"), ("i", "x_i", "y_i", "L_i(x)", "y_i*L_i(x)")),
        }

        cols, titulos = columnas[self.metodo_actual]
        self.tree = ttk.Treeview(self.frame_tabla, columns=cols, show="headings", height=12)
        for columna, titulo in zip(cols, titulos):
            self.tree.heading(columna, text=titulo)
            self.tree.column(columna, width=110, anchor="center")
        self.tree.pack(fill="both", expand=True)

    def _inicializar_matplotlib(self) -> None:
        self.fig = Figure(figsize=(6, 7), facecolor="#1e293b")
        self.ax1 = self.fig.add_subplot(211)
        self.ax2 = self.fig.add_subplot(212)

        for ax in (self.ax1, self.ax2):
            ax.set_facecolor("#0f172a")
            ax.tick_params(colors="white")
            ax.xaxis.label.set_color("white")
            ax.yaxis.label.set_color("white")
            ax.title.set_color("white")

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_grafica)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.fig.canvas.mpl_connect("scroll_event", self._zoom_2d)

    def _zoom_2d(self, event) -> None:
        if event.inaxes != self.ax1:
            return

        base = 1.5
        factor = 1 / base if event.button == "up" else base

        for axis, coord in ((self.ax1.get_xlim(), event.xdata), (self.ax1.get_ylim(), event.ydata)):
            new_w = (axis[1] - axis[0]) * factor
            rel = (axis[1] - coord) / (axis[1] - axis[0])
            if axis == self.ax1.get_xlim():
                self.ax1.set_xlim([coord - new_w * (1 - rel), coord + new_w * rel])
            else:
                self.ax1.set_ylim([coord - new_w * (1 - rel), coord + new_w * rel])

        self.canvas.draw()

    def _parse_lista_numerica(self, texto: str):
        partes = [parte.strip() for parte in texto.split(",") if parte.strip()]
        if not partes:
            raise ValueError("Debe ingresar al menos un valor numerico.")
        return [float(parte) for parte in partes]

    def _formatear_tiempo(self, segundos: float) -> str:
        if segundos < 1e-3:
            return f"{segundos * 1_000_000:.3f} us"
        if segundos < 1:
            return f"{segundos * 1000:.3f} ms"
        return f"{segundos:.6f} s"

    def _actualizar_tiempo_label(self, total: float, detalle: str = "") -> None:
        texto = f"Tiempo de ejecucion: {self._formatear_tiempo(total)}"
        if detalle:
            texto = f"{texto} | {detalle}"
        self.lbl_status.config(text=texto)

    def _configurar_grafica_eficiencia(self, titulo: str) -> None:
        self.ax2.set_title(titulo)
        self.ax2.set_xlabel("Iteracion")
        self.ax2.set_ylabel("Error absoluto")

    def calcular(self) -> None:
        try:
            metodo = self.metodo_actual
            t_proceso = 0.0
            detalle_tiempo = ""

            if metodo == "Ex6":
                x_puntos = self._parse_lista_numerica(self.ent_a.get())
                y_puntos = self._parse_lista_numerica(self.ent_b.get())
                x_eval = float(self.ent_tol.get())
                resultado = metodo_interpolacion_polinomica(x_puntos, y_puntos, x_eval)
                clave = f"x={x_eval} | puntos={len(x_puntos)}"
                self.historial["Ex6"]["data"][clave] = resultado
                t_proceso = resultado["tiempo"]
                detalle_tiempo = f"grado {resultado['grado']}"
            else:
                a = float(self.ent_a.get())
                b = float(self.ent_b.get())
                tol = float(self.ent_tol.get())

                if metodo == "Ex1":
                    resultado = metodo_biseccion(funcion_hash_table, a, b, tol, 100)
                    self.historial["Ex1"]["data"][f"[{a},{b}]"] = resultado
                    t_proceso = resultado["tiempo"]

                elif metodo == "Ex2":
                    res_falsa = metodo_falsa_posicion(funcion_balanceo_carga, a, b, tol, 100)
                    res_biseccion = metodo_biseccion(funcion_balanceo_carga, a, b, tol, 100)
                    self.historial["Ex2"]["Falsa"] = res_falsa
                    self.historial["Ex2"]["Bisec"] = res_biseccion
                    t_proceso = res_falsa["tiempo"] + res_biseccion["tiempo"]
                    detalle_tiempo = (
                        f"Falsa: {self._formatear_tiempo(res_falsa['tiempo'])} | "
                        f"Biseccion: {self._formatear_tiempo(res_biseccion['tiempo'])}"
                    )

                elif metodo == "Ex3":
                    resultado = metodo_punto_fijo(g_crecimiento_db, a, tol, 100)
                    self.historial["Ex3"]["data"][f"x0={a}"] = resultado
                    t_proceso = resultado["tiempo"]

                elif metodo == "Ex4":
                    resultado = metodo_newton_raphson(funcion_newton_threads, derivada_newton_threads, a, tol, 100)
                    self.historial["Ex4"]["data"][f"n0={a}"] = resultado
                    t_proceso = resultado["tiempo"]

                elif metodo == "Ex5":
                    res_secante = metodo_secante(funcion_escalabilidad_cloud, a, b, tol, 100)
                    res_newton = metodo_newton_raphson(funcion_escalabilidad_cloud, derivada_escalabilidad_newton, a, tol, 100)
                    self.historial["Ex5"]["data"][f"[{a},{b}]"] = {"Sec": res_secante, "New": res_newton}
                    t_proceso = res_secante["tiempo"] + res_newton["tiempo"]
                    detalle_tiempo = (
                        f"Secante: {self._formatear_tiempo(res_secante['tiempo'])} | "
                        f"Newton: {self._formatear_tiempo(res_newton['tiempo'])}"
                    )

            self.historial[metodo]["last_time"] = t_proceso
            self.historial[metodo]["time_detail"] = detalle_tiempo
            self._actualizar_tiempo_label(t_proceso, detalle_tiempo)
            self._recuperar_estado_persistente()

        except Exception as error:
            messagebox.showerror("Error de calculo", f"El proceso se detuvo: {error}")

    def _recuperar_estado_persistente(self) -> None:
        self.ax1.clear()
        self.ax2.clear()

        for ax in (self.ax1, self.ax2):
            ax.set_facecolor("#0f172a")
            ax.tick_params(colors="white")
            ax.xaxis.label.set_color("white")
            ax.yaxis.label.set_color("white")
            ax.title.set_color("white")

        for item in self.tree.get_children():
            self.tree.delete(item)

        metodo = self.metodo_actual
        t_guardado = self.historial[metodo].get("last_time", 0.0)
        detalle_tiempo = self.historial[metodo].get("time_detail", "")
        self._actualizar_tiempo_label(t_guardado, detalle_tiempo)

        if metodo == "Ex1":
            self._dibujar_ex1()
        elif metodo == "Ex2":
            self._dibujar_ex2()
        elif metodo == "Ex3":
            self._dibujar_ex3()
        elif metodo == "Ex4":
            self._dibujar_ex4()
        elif metodo == "Ex5":
            self._dibujar_ex5()
        elif metodo == "Ex6":
            self._dibujar_ex6()

        self.canvas.draw()

    def _dibujar_ex1(self) -> None:
        historial = self.historial["Ex1"]["data"]
        x = np.linspace(-0.999, 4.5, 500)
        self.ax1.plot(x, funcion_hash_table(x), color="#38bdf8", label="T(l)")
        self.ax1.axhline(0, color="white", lw=0.8)
        self.ax1.axvline(-1.0, color="#ef4444", ls="--", label="Asintota")
        self._configurar_grafica_eficiencia("Eficiencia del metodo de biseccion")

        if historial:
            ultimo = list(historial.values())[-1]
            for it in ultimo["iteraciones"]:
                self.tree.insert("", "end", values=(it["n"], f"{it['a']:.4f}", f"{it['b']:.4f}", f"{it['x_n']:.8f}", f"{it['f_xn']:.4e}", f"{it['error_abs']:.4e}", f"{it['error_rel']:.4f}%"))
            self._marcar_raiz(ultimo["raiz"])
            for i, (label, resultado) in enumerate(historial.items()):
                errores = [it["error_abs"] for it in resultado["iteraciones"]]
                self.ax2.semilogy(range(1, len(errores) + 1), errores, "o-", color=self.paleta[i % len(self.paleta)], label=label)

        self._set_legends()

    def _dibujar_ex2(self) -> None:
        historial = self.historial["Ex2"]
        x = np.linspace(0.5, 4.5, 500)
        self.ax1.plot(x, funcion_balanceo_carga(x), color="#38bdf8", label="E(x)")
        self.ax1.axhline(0, color="white", lw=0.8)
        self.ax1.set_title("Comportamiento de la funcion E(x)")
        self._configurar_grafica_eficiencia("Eficiencia comparativa: Falsa Posicion vs Biseccion")

        if historial["Falsa"]:
            res_falsa = historial["Falsa"]
            for it in res_falsa["iteraciones"]:
                self.tree.insert("", "end", values=(it["n"], f"{it['a']:.4f}", f"{it['b']:.4f}", f"{it['x_n']:.8f}", f"{it['f_xn']:.4e}", f"{it['error_abs']:.4e}", f"{it['error_rel']:.4f}%"))

            self._marcar_raiz(res_falsa["raiz"])
            errores_falsa = [it["error_abs"] for it in res_falsa["iteraciones"]]
            self.ax2.semilogy(range(1, len(errores_falsa) + 1), errores_falsa, "o-", color=self.paleta[1], label="Falsa Posicion")

            if historial["Bisec"]:
                errores_bisec = [it["error_abs"] for it in historial["Bisec"]["iteraciones"]]
                self.ax2.semilogy(range(1, len(errores_bisec) + 1), errores_bisec, "s-", color=self.paleta[2], label="Biseccion")

        self._set_legends()

    def _dibujar_ex3(self) -> None:
        historial = self.historial["Ex3"]["data"]
        x = np.linspace(0.5, 2.5, 500)
        self.ax1.plot(x, g_crecimiento_db(x), color="#38bdf8", label="g(x)")
        self.ax1.plot(x, x, "w--", alpha=0.5, label="y=x")
        self._configurar_grafica_eficiencia("Eficiencia del metodo de punto fijo")

        if historial:
            ultimo = list(historial.values())[-1]
            for it in ultimo["iteraciones"]:
                self.tree.insert("", "end", values=(it["n"], f"{it['x_n']:.8f}", f"{it['g_xn']:.8f}", f"{it['error_abs']:.4e}", f"{it['error_rel']:.4f}%"))

            self._marcar_raiz(ultimo["raiz"], ultimo["raiz"])
            for i, (label, resultado) in enumerate(historial.items()):
                color = self.paleta[i % len(self.paleta)]
                for it in resultado["iteraciones"][:10]:
                    xn = it["x_n"]
                    g_xn = it["g_xn"]
                    self.ax1.plot([xn, xn], [xn, g_xn], color=color, alpha=0.4)
                    self.ax1.plot([xn, g_xn], [g_xn, g_xn], color=color, alpha=0.4)
                errores = [it["error_abs"] for it in resultado["iteraciones"]]
                self.ax2.semilogy(range(1, len(errores) + 1), errores, "o-", color=color, label=label)

        self._set_legends()

    def _dibujar_ex4(self) -> None:
        historial = self.historial["Ex4"]["data"]
        x = np.linspace(0, 6, 500)
        self.ax1.plot(x, funcion_newton_threads(x), color="#38bdf8", label="T(n)")
        self.ax1.axhline(0, color="white", lw=0.8)
        self._configurar_grafica_eficiencia("Eficiencia del metodo de Newton-Raphson")

        if historial:
            ultimo = list(historial.values())[-1]
            for it in ultimo["iteraciones"]:
                self.tree.insert("", "end", values=(it["n"], f"{it['x_n']:.6f}", f"{it['f_xn']:.4e}", f"{it['df_xn']:.4e}", f"{it['error_abs']:.4e}", f"{it['error_rel']:.4f}%"))

            for it in ultimo["iteraciones"][:4]:
                xn = it["x_n"]
                fxn = it["f_xn"]
                dfxn = it["df_xn"]
                xt = np.linspace(xn - 1, xn + 1, 10)
                yt = fxn + dfxn * (xt - xn)
                self.ax1.plot(xt, yt, "y--", alpha=0.3)

            self._marcar_raiz(ultimo["raiz"])
            for i, (label, resultado) in enumerate(historial.items()):
                errores = [it["error_abs"] for it in resultado["iteraciones"]]
                self.ax2.semilogy(range(1, len(errores) + 1), errores, "o-", color=self.paleta[i % len(self.paleta)], label=label)

        self._set_legends()

    def _dibujar_ex5(self) -> None:
        historial = self.historial["Ex5"]["data"]
        x = np.linspace(0, 10, 500)
        self.ax1.plot(x, funcion_escalabilidad_cloud(x), color="#38bdf8", label="P(x)")
        self.ax1.axhline(0, color="white", lw=0.8)
        self._configurar_grafica_eficiencia("Eficiencia comparativa: Secante vs Newton")

        if historial:
            ultimo = list(historial.values())[-1]
            secante = ultimo["Sec"]
            newton = ultimo["New"]

            for it in secante["iteraciones"]:
                self.tree.insert("", "end", values=(it["n"], f"{it['xn_1']:.4f}", f"{it['xn']:.4f}", f"{it['fxn_1']:.4e}", f"{it['f_xn']:.4e}", f"{it['x_mas1']:.4f}", f"{it['error_abs']:.4e}"))

            for it in secante["iteraciones"][:4]:
                self.ax1.plot([it["xn_1"], it["xn"]], [it["fxn_1"], it["f_xn"]], "y--", alpha=0.4)

            self._marcar_raiz(secante["raiz"])
            self.ax2.semilogy(range(1, len(secante["iteraciones"]) + 1), [it["error_abs"] for it in secante["iteraciones"]], "o-", label="Secante")
            self.ax2.semilogy(range(1, len(newton["iteraciones"]) + 1), [it["error_abs"] for it in newton["iteraciones"]], "s-", label="Newton")

        self._set_legends()

    def _dibujar_ex6(self) -> None:
        historial = self.historial["Ex6"]["data"]
        self.ax1.set_title("Polinomio interpolante")
        self.ax2.set_title("Eficiencia del ensamblaje del polinomio")
        self.ax2.set_xlabel("Base de Lagrange")
        self.ax2.set_ylabel("Error absoluto parcial")

        if not historial:
            return

        ultimo = list(historial.values())[-1]
        x_puntos = np.asarray(ultimo["x_puntos"], dtype=float)
        y_puntos = np.asarray(ultimo["y_puntos"], dtype=float)
        x_eval = ultimo["x_eval"]
        y_eval = ultimo["y_eval"]
        coeficientes = np.asarray(ultimo["coeficientes"], dtype=float)
        polinomio = np.poly1d(coeficientes)

        x_min = min(np.min(x_puntos), x_eval) - 1
        x_max = max(np.max(x_puntos), x_eval) + 1
        x_grid = np.linspace(x_min, x_max, 400)

        self.ax1.plot(x_grid, polinomio(x_grid), color="#38bdf8", label="P(x)")
        self.ax1.scatter(x_puntos, y_puntos, color="#f59e0b", s=50, label="Puntos")
        self.ax1.plot(x_eval, y_eval, "ro", markersize=8, label="Evaluacion")
        self.ax1.annotate(f"P({x_eval:.4f}) = {y_eval:.6f}", (x_eval, y_eval), xytext=(10, 10), textcoords="offset points", color="white")

        for it in ultimo["iteraciones"]:
            self.tree.insert("", "end", values=(it["n"], f"{it['x_i']:.4f}", f"{it['y_i']:.4f}", f"{it['l_i']:.6f}", f"{it['contribucion']:.6f}"))

        indices = [it["n"] for it in ultimo["iteraciones"]]
        errores = [it["error_abs"] for it in ultimo["iteraciones"]]
        self.ax2.semilogy(indices, errores, "o-", color="#22c55e", label="Error parcial")

        texto_polinomio = "Coef: " + ", ".join(f"{coef:.4f}" for coef in coeficientes)
        self.ax2.text(0.02, 0.95, texto_polinomio, transform=self.ax2.transAxes, va="top", ha="left", color="white", fontsize=9)
        self._set_legends()

    def _marcar_raiz(self, rx, ry=0):
        self.ax1.plot(rx, ry, "ro", markersize=8)
        self.ax1.annotate(f"Raiz: {rx:.6f}", (rx, ry), xytext=(0, 10), textcoords="offset points", ha="center", color="white", weight="bold")

    def _set_legends(self) -> None:
        for ax in (self.ax1, self.ax2):
            handles, labels = ax.get_legend_handles_labels()
            if labels:
                ax.legend(fontsize=8, facecolor="#1e293b", labelcolor="white")

    def _limpiar_actual(self) -> None:
        metodo = self.metodo_actual
        if metodo == "Ex2":
            self.historial[metodo] = {"Falsa": None, "Bisec": None, "last_time": 0.0, "time_detail": ""}
        else:
            self.historial[metodo] = {"data": {}, "last_time": 0.0, "time_detail": ""}
        self._recuperar_estado_persistente()

    def _cambiar_metodo(self, metodo: str) -> None:
        self.metodo_actual = metodo
        self._cargar_componentes()


if __name__ == "__main__":
    App().mainloop()
