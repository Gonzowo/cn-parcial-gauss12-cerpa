# El Pivote
### Identificación:
- Nombre: Gonzalo Cerpa Salas
- Asignatura: Computación Numérica
- Fecha de entrega: 19 de Noviembre, 2026
- Repositorio de Github: [text](https://github.com/Gonzowo/cn-parcial-gauss12-cerpa)

## 1.- Planteamiento
Se busca resolver un sistema `Ax=b`, siendo `A` una matriz densa de `12x12` y tanto `x` como `b` tienen 12 componentes, aproximadamente entre `10^{-5}` y `10^{5}`. 
Al no haber elementos nulos, la eliminación requiere un costo de orden `O(n^3)`. Además, el pivote inicial diminuto y la casi dependencia entre filas dificultan conservar la precisión numérica.

El objetivo principal de esta resolucion es encontrar una solucion manteniendo la cantidad de operaciones (flops) al minimo y maximizando la precisión del resultado.

## 2.- Estrategia de eliminación
Se utilizó e implementó la eliminacion gaussiana, el cual es un algoritmo para resolver sistemas de ecuaciones lineales transformando sistemáticamente la matriz aumentada del sistema en forma escalonada (REF). Esta transformación preserva el conjunto de soluciones a la vez que facilita la búsqueda de los valores de las variables. (Thevapalan, 2025, sección “¿Qué es la eliminación gaussiana?”, párr. 1).

### Para `T1 - Triangularización inferior nula`
- El primer paso fue la eliminacion hacia delante, en 11 pasos se anulan los 66 elementos bajo la diagonal, obteniendo la matriz triangular superior del sistema. Los elementos anulados se asignan directamente a cero y las incognitas se calculan mediante sustitucion regresiva, desde la ultima ecuacion hasta la primera.

- Cada multiplicador se calculó una vez y se reutiliza para actualizar la fila y el término independiente, sin modificar las columnas eliminadas.

## 3.- Conteo de operaciones
La tabla se elaboró a partir del [reporte generado por el contador de operaciones](resultados/conteo_flops.md). Para cada uno de los 11 pasos se sumaron los registros de `eliminacion` y `actualizacion_b`, obteniendo la cantidad total de flops por paso.

Convencion: Se cuenta un flop por cada suma, resta, multiplicación o división ejecutada. Incluye la eliminación de la matriz, la actualización de \(b\) y la sustitución regresiva.

| Paso | Multiplicaciones/divisiones | Sumas/restas | Total de flops |
|---|---:|---:|---:|
| 1 | 143 | 132 | 275 |
| 2 | 120 | 110 | 230 |
| 3 | 99 | 90 | 189 |
| 4 | 80 | 72 | 152 |
| 5 | 63 | 56 | 119 |
| 6 | 48 | 42 | 90 |
| 7 | 35 | 30 | 65 |
| 8 | 24 | 20 | 44 |
| 9 | 15 | 12 | 27 |
| 10 | 8 | 6 | 14 |
| 11 | 3 | 2 | 5 |
| Subtotal: eliminación y actualización de b | 638 | 572 | 1210 |
| Sustitución regresiva | 78 | 66 | 144 |
| **Total principal** | **716** | **638** | **1354** |

El total principal es igual en ambas estrategias.
Frente a las 1486 flops de referencia, se ejecutan 132 operaciones menos lo que es una diferencia de −8,88 %, dentro de la tolerancia del ±10 %.
Esta reducción corresponde a asignar directamente a cero los 66 elementos eliminados, evitando una multiplicación y una resta por elemento.

## 4.- Análisis de mantisa y pivote


## 5.- Condicionamiento

## 6.- Resultados

## 7.- Verificación

## 8.- Conclusiones

## 9.- Reproducibilidad

## 10.- Uso de asistentes de IA

La utilización y asistencia de los agentes de ia en este trabajo fue el siguiente:
- Asistencia en la creación del codigo en la carpeta ./src/, con posterior revision humana y cambios para ajustarlo a los requisitos (uso de NumPy) solicitados en la evaluacion.
- Generacion de texto en formato .md para mejor legibilidad (arbol de estructura de carpetas del repo, que simbologia se utiliza para generar tablas, etc.).

## 11.- Referencias
- Thevapalan, A. (2025, 18 de abril). Eliminación gaussiana: Un método para resolver sistemas de ecuaciones. DataCamp. https://www.datacamp.com/es/tutorial/gaussian-elimination

Formato: tablas en Markdown, fórmulas legibles, figuras opcionales en resultados/. Se exige citar cualquier fuente usada.