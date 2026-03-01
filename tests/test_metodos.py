import unittest
import math

from metodos.biseccion import metodo_biseccion
from metodos.falsa_posicion import metodo_falsa_posicion
from metodos.punto_fijo import metodo_punto_fijo
from metodos.newton import metodo_newton
from metodos.secante import metodo_secante


# Función de prueba simple
def f(x):
    return x**2 - 4  # raíz en 2


def df(x):
    return 2*x


def g(x):
    return math.sqrt(4)  # punto fijo trivial hacia 2


class TestMetodosNumericos(unittest.TestCase):

    def test_biseccion(self):
        resultado = metodo_biseccion(f, 0, 3, 1e-6)
        self.assertAlmostEqual(resultado["raiz"], 2, places=4)

    def test_falsa_posicion(self):
        resultado = metodo_falsa_posicion(f, 0, 3, 1e-6)
        self.assertAlmostEqual(resultado["raiz"], 2, places=4)

    def test_newton(self):
        resultado = metodo_newton(f, df, 3, 1e-6)
        self.assertAlmostEqual(resultado["raiz"], 2, places=4)

    def test_secante(self):
        resultado = metodo_secante(f, 1, 3, 1e-6)
        self.assertAlmostEqual(resultado["raiz"], 2, places=4)

    def test_punto_fijo(self):
        resultado = metodo_punto_fijo(g, 1, 1e-6)
        self.assertAlmostEqual(resultado["raiz"], 2, places=4)


if __name__ == "__main__":
    unittest.main()