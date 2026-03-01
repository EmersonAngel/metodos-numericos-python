import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# --- IMPORTACIONES DE LÓGICA ---
from metodos.biseccion import metodo_biseccion
from metodos.falsa_posicion import metodo_falsa_posicion
from metodos.punto_fijo import metodo_punto_fijo
from metodos.newton import metodo_newton_raphson
from metodos.secante import metodo_secante

from funciones.definiciones import (
    funcion_hash_table, funcion_balanceo_carga, g_crecimiento_db,
    funcion_newton_threads, derivada_newton_threads,
    funcion_escalabilidad_cloud, derivada_escalabilidad_newton
)


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Software Métodos Numéricos - Dashboard de Ingeniería")
        self.geometry("1550x920")
        self.configure(bg="#0f172a")

        self.metodo_actual = "Ex1"  # Llave corta para evitar KeyError

        # PERSISTENCIA TOTAL
        self.historial = {
            "Ex1": {"data": {}, "last_time": 0.0},
            "Ex2": {"Falsa": None, "Bisec": None, "last_time": 0.0},
            "Ex3": {"data": {}, "last_time": 0.0},
            "Ex4": {"data": {}, "last_time": 0.0},
            "Ex5": {"data": {}, "last_time": 0.0}
        }

        self.paleta = ['#38bdf8', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']
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
        """Organiza la interfaz y asegura que el cronómetro sea actualizable."""
        # Limpieza de seguridad para evitar duplicados en la UI
        for child in self.main_area.winfo_children(): child.destroy()
        for child in self.sidebar.winfo_children(): child.destroy()

        self._crear_menu_lateral()
        self._crear_cabecera()
        self._crear_panel_entrada()

        # --- RECUADRO DEL TIEMPO (Única instancia corregida) ---
        # Se coloca en un Frame dedicado para resaltar como un "instrumento"
        self.frame_tiempo = tk.Frame(self.main_area, bg="#1e293b", bd=2, relief="groove")
        self.frame_tiempo.pack(fill="x", pady=10)

        self.lbl_status = tk.Label(
            self.frame_tiempo,
            text="⏱ Tiempo de ejecución: 0.000000 s",
            bg="#1e293b",
            fg="#38bdf8",
            font=("Segoe UI", 12, "bold"),
            pady=10
        )
        self.lbl_status.pack()

        # Área de Dashboard (Tablas y Gráficas)
        dashboard = tk.Frame(self.main_area, bg="#0f172a")
        dashboard.pack(fill="both", expand=True)

        self.frame_tabla = tk.Frame(dashboard, bg="#1e293b", padx=10, pady=10)
        self.frame_tabla.pack(side="left", fill="both", expand=True, padx=(0, 10))
        self._crear_tabla()

        self.frame_grafica = tk.Frame(dashboard, bg="#1e293b", padx=10, pady=10)
        self.frame_grafica.pack(side="right", fill="both", expand=True)
        self._inicializar_matplotlib()

        # Sincroniza el tiempo guardado si ya hubo un cálculo previo
        self._recuperar_estado_persistente()

    def _crear_menu_lateral(self) -> None:
        tk.Label(self.sidebar, text="MÉTODOS", bg="#0b1120", fg="#64748b", font=("Segoe UI", 10, "bold")).pack(pady=20)
        ops = [("Ejercicio 1 - Bisección", "Ex1"), ("Ejercicio 2 - Falsa Posición", "Ex2"),
               ("Ejercicio 3 - Punto Fijo", "Ex3"), ("Ejercicio 4 - Newton Raphson", "Ex4"), ("Ejercicio 5 - Secante", "Ex5")]
        for texto, id_m in ops:
            btn = tk.Button(self.sidebar, text=texto, bg="#1e293b", fg="white", relief="flat", pady=12,
                            command=lambda m=id_m: self._cambiar_metodo(m))
            btn.pack(fill="x", pady=1, padx=15)

    def _crear_cabecera(self) -> None:
        titulos = {"Ex1": "Ejercicio 1 - Bisección Hash", "Ex2": "Ejercicio 2 - Comparativa",
                   "Ex3": "Ejercicio 3 - Punto Fijo", "Ex4": "Ejercicio 4 - Newton", "Ex5": "Ejercicio 5 - Secante"}
        tk.Label(self.main_area, text=titulos.get(self.metodo_actual), font=("Segoe UI", 20, "bold"), bg="#0f172a",
                 fg="#38bdf8").pack()

        desc = {
            "Ex1":  "CONTEXTO: Optimización de caché distribuido.\n" 
                    "T(λ) = 2.5 + 0.8λ² - 3.2λ + ln(λ + 1) | T'(λ) = 1.6λ - 3.2 + 1/(λ + 1)",
            "Ex2": "CONTEXTO: Balanceo de carga en servidores.\n"
                   "E(x) = x³ - 6x² + 11x - 6.5 | E'(x) = 3x² - 12x + 11",
            "Ex3": "CONTEXTO: Balanceo de carga en servidores.\n"
                   "g(x) = 0.5cos(x) + 1.5 | g'(x) = -0.5sin(x)",
            "Ex4": "CONTEXTO: Overhead de sincronización en threads.\n"
                   "T(n) = n³ - 8n² + 20n - 16 | T'(n) = 3n² - 16n + 20",
            "Ex5": "CONTEXTO: Escalabilidad de infraestructura Cloud.\n"
                   "P(x) = x·e^(-x/2) - 0.3 | P'(x) = e^(-x/2) · (1 - x/2)"
        }
        tk.Label(self.main_area, text=desc.get(self.metodo_actual), font=("Consolas", 10),
                 bg="#0f172a", fg="#94a3b8", justify="center").pack(pady=(0, 10))

    def _crear_panel_entrada(self) -> None:
        card = tk.LabelFrame(self.main_area, text=" PARÁMETROS ", bg="#1e293b", fg="#94a3b8",
                             font=("Segoe UI", 9, "bold"), padx=15, pady=15, relief="flat")
        card.pack(fill="x", pady=(0, 15))

        defaults = {"Ex1": ("-0.999", "1.0", "1e-6"), "Ex2": ("2.0", "4.0", "1e-7"),
                    "Ex3": ("1.0", "0", "1e-8"), "Ex4": ("5.0", "0", "1e-10"), "Ex5": ("0.5", "1.0", "1e-9")}
        v = defaults.get(self.metodo_actual)

        params = [("x0 / a:", "ent_a", v[0]), ("b / x1:", "ent_b", v[1]), ("Tol:", "ent_tol", v[2])]
        for i, (lab, attr, val) in enumerate(params):
            tk.Label(card, text=lab, bg="#1e293b", fg="white").grid(row=0, column=i * 2, padx=5)
            ent = tk.Entry(card, width=12, bg="#0f172a", fg="white", insertbackground="white")
            ent.insert(0, val);
            ent.grid(row=0, column=i * 2 + 1, padx=5);
            setattr(self, attr, ent)

        tk.Button(card, text="CALCULAR", bg="#2563eb", fg="white", command=self.calcular, relief="flat", padx=20).grid(
            row=0, column=6, padx=15)
        tk.Button(card, text="BORRAR ACTUAL", bg="#ef4444", fg="white", command=self._limpiar_actual, relief="flat",
                  padx=20).grid(row=0, column=7)

    def _crear_tabla(self) -> None:
        if self.metodo_actual == "Ex4":
            cols, t = ("n", "x_n", "f_xn", "df_xn", "e_abs", "e_rel"), ["n", "x_n", "f(x_n)", "f'(x_n)", "|Err Abs|",
                                                                        "Err Rel %"]
        elif self.metodo_actual == "Ex5":
            cols, t = ("n", "xn_1", "xn", "fxn_1", "fxn", "xn_mas1", "e_abs"), ["n", "x_{n-1}", "x_n", "f(x_{n-1})",
                                                                                "f(x_n)", "x_{n+1}", "|Err Abs|"]
        elif self.metodo_actual == "Ex3":
            cols, t = ("n", "x_n", "g_xn", "e_abs", "e_rel"), ["n", "x_n", "g(x_n)", "|x_n-g|", "Err Rel %"]
        else:
            cols, t = ("n", "a", "b", "x_n", "f_xn", "e_abs", "e_rel"), ["n", "a", "b", "x_n", "f(x_n)", "|Err Abs|",
                                                                         "Err Rel %"]

        self.tree = ttk.Treeview(self.frame_tabla, columns=cols, show="headings", height=12)
        for c, h in zip(cols, t):
            self.tree.heading(c, text=h);
            self.tree.column(c, width=90, anchor="center")
        self.tree.pack(fill="both", expand=True)

    def _inicializar_matplotlib(self) -> None:
        self.fig = Figure(figsize=(6, 7), facecolor='#1e293b')
        self.ax1 = self.fig.add_subplot(211);
        self.ax2 = self.fig.add_subplot(212)
        for ax in [self.ax1, self.ax2]:
            ax.set_facecolor("#0f172a")
            ax.tick_params(colors='white');
            ax.xaxis.label.set_color('white');
            ax.yaxis.label.set_color('white')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_grafica)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.fig.canvas.mpl_connect("scroll_event", self._zoom_2d)

    def _zoom_2d(self, event) -> None:
        """Zoom bidimensional en X e Y simultáneamente."""
        if event.inaxes != self.ax1: return
        base = 1.5;
        factor = 1 / base if event.button == 'up' else base
        for axis, coord in [(self.ax1.get_xlim(), event.xdata), (self.ax1.get_ylim(), event.ydata)]:
            new_w = (axis[1] - axis[0]) * factor
            rel = (axis[1] - coord) / (axis[1] - axis[0])
            if axis == self.ax1.get_xlim():
                self.ax1.set_xlim([coord - new_w * (1 - rel), coord + new_w * rel])
            else:
                self.ax1.set_ylim([coord - new_w * (1 - rel), coord + new_w * rel])
        self.canvas.draw()

    def calcular(self) -> None:
        """Ejecuta los algoritmos y actualiza el cronómetro en pantalla."""
        try:
            # 1. Obtención de parámetros de la interfaz
            a = float(self.ent_a.get())
            b = float(self.ent_b.get())
            tol = float(self.ent_tol.get())

            met = self.metodo_actual  # "Ex1", "Ex2", etc.
            t_proceso = 0.0

            # 2. Lógica de ejecución por ejercicio
            if met == "Ex1":
                res = metodo_biseccion(funcion_hash_table, a, b, tol, 100)
                self.historial["Ex1"]["data"][f"[{a},{b}]"] = res
                t_proceso = res["tiempo"]

            elif met == "Ex2":
                # Suma de Bisección + Falsa Posición
                res_f = metodo_falsa_posicion(funcion_balanceo_carga, a, b, tol, 100)
                res_b = metodo_biseccion(funcion_balanceo_carga, a, b, tol, 100)
                self.historial["Ex2"]["Falsa"] = res_f
                self.historial["Ex2"]["Bisec"] = res_b
                t_proceso = res_f["tiempo"] + res_b["tiempo"]

            elif met == "Ex3":
                res = metodo_punto_fijo(g_crecimiento_db, a, tol, 100)
                self.historial["Ex3"]["data"][f"x0={a}"] = res
                t_proceso = res["tiempo"]

            elif met == "Ex4":
                # Newton-Raphson: Valida derivada nula
                res = metodo_newton_raphson(funcion_newton_threads, derivada_newton_threads, a, tol, 100)
                self.historial["Ex4"]["data"][f"n0={a}"] = res
                t_proceso = res["tiempo"]

            elif met == "Ex5":
                # Comparativa Secante vs Newton
                res_s = metodo_secante(funcion_escalabilidad_cloud, a, b, tol, 100)
                res_n = metodo_newton_raphson(funcion_escalabilidad_cloud, derivada_escalabilidad_newton, a, tol, 100)
                self.historial["Ex5"]["data"][f"[{a},{b}]"] = {"Sec": res_s, "New": res_n}
                t_proceso = res_s["tiempo"] + res_n["tiempo"]

            # --- ACTUALIZACIÓN FÍSICA DEL RECUADRO ---
            # Guardamos el tiempo en el historial para persistencia
            self.historial[met]["last_time"] = t_proceso

            # Cambiamos el texto de la etiqueta con 8 decimales de precisión
            self.lbl_status.config(text=f"⏱ Tiempo de ejecución: {t_proceso:.8f} s")

            # Refrescar gráficas y tablas
            self._recuperar_estado_persistente()

        except Exception as e:
            messagebox.showerror("Error de Cálculo", f"El proceso se detuvo: {str(e)}")

    def _recuperar_estado_persistente(self) -> None:
        """Restaura las gráficas, tablas y el tiempo guardado."""
        # Limpieza de los ejes de la gráfica y la tabla de datos
        self.ax1.clear()
        self.ax2.clear()
        for i in self.tree.get_children():
            self.tree.delete(i)

        met = self.metodo_actual

        # 1. RECUPERAR EL TIEMPO GUARDADO DEL HISTORIAL
        # Si no hay tiempo guardado, por defecto es 0.0
        t_guardado = self.historial[met].get("last_time", 0.0)
        self.lbl_status.config(text=f"⏱ Tiempo de ejecución: {t_guardado:.8f} s")

        # 2. Redibujar gráficas correspondientes al ejercicio
        if met == "Ex1":
            self._dibujar_ex1()
        elif met == "Ex2":
            self._dibujar_ex2()
        elif met == "Ex3":
            self._dibujar_ex3()
        elif met == "Ex4":
            self._dibujar_ex4()
        elif met == "Ex5":
            self._dibujar_ex5()

        # Actualizar el lienzo de Matplotlib
        self.canvas.draw()

    def _dibujar_ex1(self) -> None:
        hist = self.historial["Ex1"]["data"]
        x = np.linspace(-0.999, 4.5, 500);
        self.ax1.plot(x, funcion_hash_table(x), color="#38bdf8", label="T(λ)")
        self.ax1.axhline(0, color="white", lw=0.8);
        self.ax1.axvline(-1.0, color="#ef4444", ls="--", label="Asíntota")
        if hist:
            last = list(hist.values())[-1]
            for it in last["iteraciones"]: self.tree.insert("", "end", values=(it["n"], f"{it.get('a', 0):.4f}",
                                                                               f"{it.get('b', 0):.4f}",
                                                                               f"{it['x_n']:.8f}", f"{it['f_xn']:.4e}",
                                                                               f"{it['error_abs']:.4e}",
                                                                               f"{it.get('error_rel', 0):.4f}%"))
            self._marcar_raiz(last["raiz"])
            for i, (lab, r) in enumerate(hist.items()):
                self.ax2.semilogy(range(1, len(r["iteraciones"]) + 1), [it["error_abs"] for it in r["iteraciones"]],
                                  'o-', color=self.paleta[i % len(self.paleta)], label=lab)
        self._set_legends()

    def _dibujar_ex2(self) -> None:
        """
        Restaura la comparativa del Ejercicio 2.
        Soluciona los ceros en 'a' y 'b' y sincroniza el cronómetro.
        """
        hist = self.historial["Ex2"]

        # 1. Configuración de la función en el gráfico superior
        x = np.linspace(0.5, 4.5, 500)
        y = funcion_balanceo_carga(x)
        self.ax1.plot(x, y, color="#38bdf8", label="E(x)")
        self.ax1.axhline(0, color="white", lw=0.8)
        self.ax1.set_title("Comportamiento de la Función E(x)", color="white", fontsize=10)

        if hist["Falsa"]:
            res_f = hist["Falsa"]

            for it in res_f["iteraciones"]:
                self.tree.insert("", "end", values=(
                    it["n"],
                    f"{it['a']:.4f}",
                    f"{it['b']:.4f}",
                    f"{it['x_n']:.8f}",
                    f"{it['f_xn']:.4e}",
                    f"{it['error_abs']:.4e}",
                    f"{it['error_rel']:.4f}%"
                ))

            raiz_f = res_f["raiz"]
            self._marcar_raiz(raiz_f)

            err_f = [it["error_abs"] for it in res_f["iteraciones"]]
            self.ax2.semilogy(range(1, len(err_f) + 1), err_f, 'o-',
                              color=self.paleta[1], label="Falsa Posición")

            # Graficamos Bisección para la comparativa
            if hist["Bisec"]:
                err_b = [it["error_abs"] for it in hist["Bisec"]["iteraciones"]]
                self.ax2.semilogy(range(1, len(err_b) + 1), err_b, 's-',
                                  color=self.paleta[2], label="Bisección")

        self.ax2.set_ylabel("Error Absoluto (log)", color="white")
        self.ax2.set_xlabel("Iteración (n)", color="white")
        self._set_legends()

    def _dibujar_ex3(self) -> None:
        """Diagrama de telaraña sincronizado para ejercicio 3."""

        hist = self.historial["Ex3"]["data"]
        x = np.linspace(0.5, 2.5, 500);
        self.ax1.plot(x, g_crecimiento_db(x), color="#38bdf8", label="g(x)")
        self.ax1.plot(x, x, 'w--', alpha=0.5, label="y=x")
        if hist:
            last = list(hist.values())[-1]
            for it in last["iteraciones"]: self.tree.insert("", "end", values=(it["n"], f"{it['x_n']:.8f}",
                                                                               f"{it.get('g_xn', 0):.8f}",
                                                                               f"{it['error_abs']:.4e}",
                                                                               f"{it.get('error_rel', 0):.4f}%"))
            self._marcar_raiz(last["raiz"], last["raiz"])
            for i, (lab, res) in enumerate(hist.items()):
                color = self.paleta[i % len(self.paleta)]
                for it in res["iteraciones"][:10]:
                    xn, g_xn = it["x_n"], it.get("g_xn", 0)
                    self.ax1.plot([xn, xn], [xn, g_xn], color=color, alpha=0.4)
                    self.ax1.plot([xn, g_xn], [g_xn, g_xn], color=color, alpha=0.4)
                self.ax2.semilogy(range(1, len(res["iteraciones"]) + 1), [it["error_abs"] for it in res["iteraciones"]],
                                  'o-', color=color, label=lab)
        self._set_legends()

    def _dibujar_ex4(self) -> None:
        """Newton con TANGENTES visibles."""

        hist = self.historial["Ex4"]["data"]
        x = np.linspace(0, 6, 500);
        self.ax1.plot(x, funcion_newton_threads(x), color="#38bdf8", label="T(n)")
        self.ax1.axhline(0, color="white", lw=0.8)
        if hist:
            last = list(hist.values())[-1]
            for it in last["iteraciones"]: self.tree.insert("", "end",
                                                            values=(it["n"], f"{it['x_n']:.6f}", f"{it['f_xn']:.4e}",
                                                                    f"{it['df_xn']:.4e}", f"{it['error_abs']:.4e}",
                                                                    f"{it['error_rel']:.4f}%"))
            for it in last["iteraciones"][:4]:
                xn, fxn, dfxn = it["x_n"], it["f_xn"], it["df_xn"]
                xt = np.linspace(xn - 1, xn + 1, 10);
                yt = fxn + dfxn * (xt - xn)
                self.ax1.plot(xt, yt, 'y--', alpha=0.3)
            self._marcar_raiz(last["raiz"])
            for i, (lab, r) in enumerate(hist.items()):
                self.ax2.semilogy(range(1, len(r["iteraciones"]) + 1), [it["error_abs"] for it in r["iteraciones"]],
                                  'o-', color=self.paleta[i % len(self.paleta)], label=lab)
        self._set_legends()

    def _dibujar_ex5(self) -> None:
        """Secante con RECTAS SECANTES amarillas."""

        hist = self.historial["Ex5"]["data"]
        x = np.linspace(0, 10, 500);
        self.ax1.plot(x, funcion_escalabilidad_cloud(x), color="#38bdf8", label="P(x)")
        self.ax1.axhline(0, color="white", lw=0.8)
        if hist:
            last = list(hist.values())[-1];
            sec, new = last["Sec"], last["New"]
            for it in sec["iteraciones"]: self.tree.insert("", "end",
                                                           values=(it["n"], f"{it['xn_1']:.4f}", f"{it['xn']:.4f}",
                                                                   f"{it['fxn_1']:.4e}", f"{it['f_xn']:.4e}",
                                                                   f"{it['x_mas1']:.4f}", f"{it['error_abs']:.4e}"))
            for it in sec["iteraciones"][:4]: self.ax1.plot([it['xn_1'], it['xn']], [it['fxn_1'], it['f_xn']], 'y--',
                                                            alpha=0.4)
            self._marcar_raiz(sec["raiz"])
            self.ax2.semilogy(range(1, len(sec["iteraciones"]) + 1), [it["error_abs"] for it in sec["iteraciones"]],
                              'o-', label="Secante")
            self.ax2.semilogy(range(1, len(new["iteraciones"]) + 1), [it["error_abs"] for it in new["iteraciones"]],
                              's-', label="Newton")
        self._set_legends()

    def _marcar_raiz(self, rx, ry=0):
        self.ax1.plot(rx, ry, 'ro', markersize=8)
        self.ax1.annotate(f"Raiz: {rx:.6f}", (rx, ry), xytext=(0, 10), textcoords="offset points", ha='center',
                          color='white', weight='bold')

    def _set_legends(self) -> None:
        for ax in [self.ax1, self.ax2]:
            h, l = ax.get_legend_handles_labels()
            if l: ax.legend(fontsize=8, facecolor="#1e293b", labelcolor="white")

    def _limpiar_actual(self) -> None:
        met = self.metodo_actual
        if met == "Ex2":
            self.historial[met] = {"Falsa": None, "Bisec": None, "last_time": 0.0}
        else:
            self.historial[met] = {"data": {}, "last_time": 0.0}
        self._recuperar_estado_persistente()

    def _cambiar_metodo(self, n: str) -> None:
        self.metodo_actual = n; self._cargar_componentes()


if __name__ == "__main__": App().mainloop()