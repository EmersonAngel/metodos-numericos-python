# 📊 Métodos Numéricos Aplicados a Ingeniería de Software

Aplicación desarrollada en Python con interfaz gráfica moderna y oscura para la implementación y visualización de métodos numéricos aplicados a problemas reales de Ingeniería de Software.

---

## 🚀 Características

- Interfaz gráfica moderna (tema oscuro con tonos azulados)
- Arquitectura modular organizada por carpetas
- Implementación de métodos numéricos:
  - Método de Bisección
  - Método de Secante
  - Método de Newton-Raphson
- Visualización gráfica en tiempo real
- Tabla de iteraciones
- Cálculo de:
  - Error absoluto
  - Error relativo
- Soporte para zoom interactivo con el mouse
- Representación matemática visible en la interfaz
- Gráfica completa de la función (incluye asíntotas cuando aplica)

---

## 🧠 Ejercicio 1 – Optimización de Hash Table

Se implementa el método de bisección para resolver:

T(λ) = 2.5 + 0.8λ² − 3.2λ + ln(λ + 1)

### 📌 Objetivo

Encontrar el valor óptimo del factor de carga λ que minimiza el tiempo promedio de búsqueda en una hash table.

### 🔎 Consideraciones Matemáticas

- Dominio: λ > -1
- Existe una asíntota vertical en λ = -1
- La función presenta comportamiento no lineal debido al término logarítmico
- Se requiere cambio de signo para aplicar bisección

---

## 🏗️ Estructura del Proyecto
metodos_numericos/
│
├── main.py
│
├── metodos/
│ ├── biseccion.py
│ ├── secante.py
│ ├── falsa_posicion.py
│ ├── punto_fijo.py
│ ├── funciones.py
│ └── newton.py
│
├── funciones/
│ └── definiciones.py
│
├── utils/
│ ├── evaluador.py
│ └── validaciones.py
│
├── interfaz/
│ └── gui_principal.py
│  
├── tests/
│ └── test_metodos.py
│
└── requirements.txt


---

## ⚙️ Requisitos

Instalar dependencias:

```bash
pip install -r requirements.txt
````

## requirements.txt
- numpy
- matplotlib

## ▶️ Ejecución

Desde la raíz del proyecto:
```bash
python main.py
````

## 📈 Funcionalidades de Visualización

- Gráfica completa de la función

- Línea horizontal en y = 0

- Asíntota vertical cuando corresponde

- Zoom con rueda del mouse

- Visualización de iteraciones sobre la curva

- Gráfica de convergencia del error

## 📚 Métodos Implementados
- Método de Bisección

- Requiere cambio de signo

- Tolerancia configurable

- Máximo de iteraciones configurable

- Registro completo de cada iteración

- Método de Secante

- No requiere derivada

- Aproximación iterativa basada en dos puntos

- Método de Newton

- Usa derivada analítica

- Convergencia cuadrática cuando aplica
