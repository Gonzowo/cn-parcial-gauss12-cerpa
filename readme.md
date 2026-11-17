# Evaluación 3: El Pivote
Universidad Católica del Maule - Lab evaluado 3

Este repositorio resuelve un sistema lineal denso de 12 incógnitas mediante eliminación gaussiana, comparando el costo operacional y la precisión numérica con y sin pivoteo parcial.

### Autor:
Gonzalo Cerpa Salas
### Asignatura:
Computación Numérica

## Requisitos
- Python 3.12 o superior
- NumPy 2.5.0

Para instalar las dependencias desde la carpeta del repositorio:
`python -m pip install -r requirements.txt`

Para instalar NumPy directamente:
`python -m pip install numpy==2.5.0`

## Ejecución
Para ejecutar el codigo principal del trabajo:
`python src/main.py`

## Estructura de carpetas
La estructura del repositorio se divide entre src (codigos python), resultados (archivos generados), datos (matriz 12x12 y vector 1x12) y por ultimo en la carpeta raiz se encuentran los archivos de requerimientos para ejecutar el codigo, el informe, el readme del repositorio y el archivo .gitignore

La estructura del repositorio se divide entre src (codigos python), resultados (archivos generados), datos (matriz 12x12 y vector 1x12) y por ultimo en la carpeta raiz se encuentran los archivos de requerimientos para ejecutar el codigo, el informe, el readme del repositorio y el archivo .gitignore


```text
cn-parcial-gauss12-cerpa/
├── readme.md
├── informe.md
├── requirements.txt
├── .gitignore
├── datos/
│   ├── matriz_a.csv
│   └── vector_b.csv
├── src/
│   ├── conteo.py
│   ├── gauss.py
│   ├── verificacion.py
│   └── main.py
└── resultados/
    ├── solucion.csv
    ├── traza_eliminacion.txt
    ├── conteo_flops.md
    └── residuo.txt
```

## Resultado resumido

## Enlace al informe.md
Mas detalles del problema, como se llegó al resultado, el metodo utilizado y el analisis del error en el archivo [informe](informe.md)

## Licencia
Proyecto desarrollado con fines académicos utilizando Python y NumPy, herramientas de código abierto que no requieren licencias de pago para su uso. Hecho por Gonzalo Cerpa Salas para la asignatura Computación Numérica (INF-321) de la Universidad Católica del Maule