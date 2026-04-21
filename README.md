# Metodos Numericos Aplicados a Ingenieria de Software

Aplicacion de escritorio en Python para visualizar y comparar metodos numericos con una interfaz grafica tipo dashboard.

## Metodos incluidos

- Biseccion
- Falsa posicion
- Punto fijo
- Newton-Raphson
- Secante
- Interpolacion polinomica de Lagrange

## Novedades

- Se agrego un nuevo ejercicio de interpolacion polinomica.
- La GUI ahora permite ingresar listas de puntos en formato CSV para interpolar.
- Se reforzaron validaciones comunes en tolerancia, iteraciones y consistencia de datos.
- Se corrigieron y ampliaron las pruebas unitarias.

## Uso

1. Instala dependencias:

```bash
pip install -r requirements.txt
```

2. Ejecuta la aplicacion:

```bash
python main.py
```

## Interpolacion polinomica

En el Ejercicio 6:

- Campo 1: valores de `x` separados por comas. Ejemplo: `0,1,2,3`
- Campo 2: valores de `y` separados por comas. Ejemplo: `1,3,2,5`
- Campo 3: valor `x` donde se desea evaluar el polinomio. Ejemplo: `1.5`

La tabla muestra los terminos de la base de Lagrange y su contribucion, y la grafica muestra:

- El polinomio interpolante
- Los puntos originales
- El punto evaluado

## Estructura

```text
metodos_numericos/
|-- main.py
|-- funciones/
|-- interfaz/
|-- metodos/
|-- tests/
`-- utils/
```
