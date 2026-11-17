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
Se ejecutaron las 2 corridas de codigo (funciones `gauss_sin_pivoteo` y `gauss_pivoteo_escalado` de `gauss.py`) ambas con doble precision y 53 bits de mantisa.

| Indicador | Sin pivoteo | Pivoteo parcial escalado |
|---|---:|---:|
| Multiplicador máximo | $2,75259\times10^{13}$ | $2,46556\times10^9$ |
| Factor de crecimiento | 2641,22425 | 1,78320 |
| Error relativo al finalizar la eliminación y sustitución regresiva, antes del refinamiento | $2,38018\times10^{-10}$ | $2,70171\times10^{-13}$ |
| Precisión global equivalente en bits | 31,97 | 41,75 |
| Pérdida equivalente respecto de 53 bits | 21,03 | 11,25 |

Los valores provienen de `resultados/residuo.txt`.
La precisión global equivalente se calcula como $-\log_2(E_{\mathrm{rel}})$ y la pérdida equivalente como $53-b_{\mathrm{efectivos}}$.

### T2 - Pivoteo y mantisa
| **Indicador** | **Sin pivoteo** | **Pivoteo parcial escalado** |
|:---:|:---|:---|
| **Observacion** | El algoritmo sin pivoteo utiliza un pivote inicial, que genera multiplicadores de hasta $2,75259\times10^{13}$. Los productos y actualizaciones de filas dan valores grandes con un factor de crecimiento de $2641,22425$, al operar con 53 bits de mantisa estos productos se redondean. El error relativo final es de $31,97$ bits equivalentes de precision ($21.03$ respecto de $53$) | El algoritmo con pivoteo parcial selecciona pivotes considerando magnitudes relativas de cada fila, aqui el factor de crecimiento disminuye respecto a sin pivoteo a $1,78320$, Esto reduce los errores de redondeo y permite conservar la informacion mas precisa durante la eliminación. El error relativo final es de $41,75$ bits equivalentes de precision ($11,25$ respecto de $53$) |

En resumen, las estrategias difieren debido a un error que a medida que se realizan pasos crece de manera mayor si no existiera un pivoteo, esto provoca que pueda mantenerse dentro de margenes mas precisos y confiables respecto a no utilizar pivoteo alguno.

## 5.- Condicionamiento
Datos extraidos de [resultados/residuo.txt](resultados/residuo.txt).

| Indicador | Valor |
|---|---:|
| Número de condición estimado $\kappa_2(A)$ | $3.08474\times10^{13}$ |
| Épsilon de doble precisión $\varepsilon$ | $2.22045\times10^{-16}$ |
| Cota orientativa $\kappa_2(A)\varepsilon$ | $6.84951\times10^{-3}$ |

El alto valor de condición nos dice que cambios pequeños en los datos pueden amplificarse de manera exponencial en una solución.
El épsilon de doble precisión nos da una referencia de precision, aprox 15 cifras decimales significativas.
La cota orientativa representa una estimación en el peor caso, por lo que el sistema resulta pesimista frente a los errores, ya que las perturbaciones en los valores no siguen las direcciones de maxima sensibilidad. Debido a esto el pivoteo mejora el comportamiento del cálculo.

## 6.- Resultados
Los datos proceden de [solucion.csv](resultados/solucion.csv).
Se utilizaron los registros de estrategia `escalado` y etapa `refinada`, tomando las columnas `valor_reportado` y `digitos_afirmados`.

| Incógnita | Valor reportado | Cifras significativas verificadas |
|:---:|---:|:---:|
| $x_1$ | $7.384915627000000\times10^{-1}$ | 16 |
| $x_2$ | $-1.205937416800000\times10^{0}$ | 16 |
| $x_3$ | $4.387195200000000\times10^{-3}$ | 16 |
| $x_4$ | $-9.172645380000000\times10^{-2}$ | 16 |
| $x_5$ | $2.8461093725000000\times10^{0}$ | 17 |
| $x_6$ | $-6.281540900000000\times10^{-3}$ | 16 |
| $x_7$ | $1.4738205916000000\times10^{0}$ | 17 |
| $x_8$ | $-3.849271640000000\times10^{-2}$ | 16 |
| $x_9$ | $9.152648037000000\times10^{-1}$ | 16 |
| $x_{10}$ | $-2.607139485200000\times10^{0}$ | 16 |
| $x_{11}$ | $5.187362940000000\times10^{-2}$ | 16 |
| $x_{12}$ | $-1.084937162500000\times10^{0}$ | 16 |
## 7.- Verificación

## 8.- Conclusiones

## 9.- Reproducibilidad

## 10.- Uso de asistentes de IA

La utilización y asistencia de los agentes de ia en este trabajo fue el siguiente:
- Asistencia en la creación del codigo en la carpeta ./src/, con posterior revision humana y cambios para ajustarlo a los requisitos (uso de NumPy) solicitados en la evaluacion.
- Generacion de texto en formato .md para mejor legibilidad (arbol de estructura de carpetas del repo, que simbologia se utiliza para generar tablas, etc.).
- Como llegar a la precision global equivalente y perdida equivalente de bits.
- Asistencia en la seccion de 5.- Condicionamiento a traves de explicaciones.

## 11.- Referencias
- Thevapalan, A. (2025, 18 de abril). Eliminación gaussiana: Un método para resolver sistemas de ecuaciones. DataCamp. https://www.datacamp.com/es/tutorial/gaussian-elimination

Formato: tablas en Markdown, fórmulas legibles, figuras opcionales en resultados/. Se exige citar cualquier fuente usada.