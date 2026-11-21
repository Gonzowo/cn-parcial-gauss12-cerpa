# Evaluación 3: El Pivote
Universidad Católica del Maule - Lab evaluado 3

Este repositorio resuelve un sistema lineal denso de 12 incógnitas mediante eliminación gaussiana, comparando el costo operacional y la precisión numérica con y sin pivoteo parcial escalado.

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
Para ejecutar el codigo principal del trabajo (desde la raiz del repositorio):
`python src/main.py`
El codigo generará cuatro archivos en `resultados/`.

## Estructura de carpetas
La estructura del repositorio se divide entre src (codigos python), resultados (archivos generados), datos (matriz 12x12 y vector de 12 componentes) y por ultimo en la carpeta raiz se encuentran los archivos de requerimientos para ejecutar el codigo, el informe, el readme del repositorio y el archivo .gitignore

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
Solución con pivoteo parcial escalado y una pasada de refinamiento.
Datos de la tabla extraidos de [solucion.csv](resultados/solucion.csv), [conteo_flops.md](resultados/conteo_flops.md) y [residuo.txt](resultados/residuo.txt).

| Incógnita | Valor (10 cifras significativas) |
|:---:|---:|
| $x_1$ | $7.384915627\times10^{-1}$ |
| $x_2$ | $-1.205937417\times10^{0}$ |
| $x_3$ | $4.387195200\times10^{-3}$ |
| $x_4$ | $-9.172645380\times10^{-2}$ |
| $x_5$ | $2.846109372\times10^{0}$ |
| $x_6$ | $-6.281540900\times10^{-3}$ |
| $x_7$ | $1.473820592\times10^{0}$ |
| $x_8$ | $-3.849271640\times10^{-2}$ |
| $x_9$ | $9.152648037\times10^{-1}$ |
| $x_{10}$ | $-2.607139485\times10^{0}$ |
| $x_{11}$ | $5.187362940\times10^{-2}$ |
| $x_{12}$ | $-1.084937162\times10^{0}$ |

| Indicador | Resultado |
|---|---:|
| Flops de resolución, incluido el pivoteo | 1431 |
| Flops adicionales del refinamiento | 288 |
| Total de resolución y refinamiento | 1719 |
| Norma infinito del residuo de la solución refinada, antes del redondeo de presentación | $2.60318737\times10^{-10}$ |

## Enlace al informe.md
Mas detalles del problema, como se llegó al resultado, el metodo utilizado y el analisis del error en el archivo [informe](informe.md)

## Licencia
Proyecto desarrollado con fines académicos utilizando Python y NumPy, herramientas de código abierto que no requieren licencias de pago para su uso. Hecho por Gonzalo Cerpa Salas para la asignatura Computación Numérica (INF-321) de la Universidad Católica del Maule