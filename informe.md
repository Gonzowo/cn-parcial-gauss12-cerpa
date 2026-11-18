# El Pivote
### Identificación:
- Nombre: Gonzalo Cerpa Salas
- Asignatura: Computación Numérica
- Fecha de entrega: 18 de Noviembre, 2026
- Repositorio de Github: [Github/Gonzowo](https://github.com/Gonzowo/cn-parcial-gauss12-cerpa)

## 1.- Planteamiento
Se busca resolver un sistema $Ax=b$, siendo $A$ una matriz densa de $12\times12$ y tanto $x$ como $b$ vectores de 12 componentes. Las escalas de fila de $A$, definidas como $s_i=\max_j|a_{ij}|$, varían aproximadamente entre $8,05\times10^{-5}$ y $9,67\times10^5$.
Al no haber elementos nulos, la eliminación requiere un costo de orden `O(n^3)`. Además, el pivote inicial diminuto y la casi dependencia entre filas dificultan conservar la precisión numérica.

El objetivo principal de esta resolucion es encontrar una solucion manteniendo la cantidad de operaciones (flops) al minimo y maximizando la precisión del resultado.

## 2.- Estrategia de eliminación
Se utilizó e implementó la eliminacion gaussiana, el cual es un algoritmo para resolver sistemas de ecuaciones lineales transformando sistemáticamente la matriz aumentada del sistema en forma escalonada (REF). Esta transformación preserva el conjunto de soluciones a la vez que facilita la búsqueda de los valores de las variables. (Thevapalan, 2025, sección “¿Qué es la eliminación gaussiana?”, párr. 1).

### Para `T1 - Triangularización inferior nula`
- El primer paso fue la eliminacion hacia delante, en 11 pasos se anulan los 66 elementos bajo la diagonal, obteniendo la matriz triangular superior del sistema. Los elementos anulados se asignan directamente a cero y las incognitas se calculan mediante sustitucion regresiva, desde la ultima ecuacion hasta la primera.

- Cada multiplicador se calculó una vez y se reutiliza para actualizar la fila y el término independiente, sin modificar las columnas eliminadas.

## 3.- Conteo de operaciones
La tabla se elaboró a partir del [resultados/conteo_flops.md](resultados/conteo_flops.md). Para cada uno de los 11 pasos se sumaron los registros de `eliminacion` y `actualizacion_b`, obteniendo la cantidad total de flops por paso.

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

## 4.- Análisis de mantisa y pivoteo.
Se ejecutaron dos corridas de la función `gauss()` de `gauss.py`, llamadas desde `main.py` con las opciones `ninguno` y `escalado`. Ambas utilizaron doble precisión y 53 bits de mantisa.

| Indicador | Sin pivoteo | Pivoteo parcial escalado |
|---|---:|---:|
| Multiplicador máximo | $2,75259\times10^{13}$ | $2,46556\times10^9$ |
| Factor de crecimiento | 2641,22425 | 1,78320 |
| Error relativo al finalizar la eliminación y sustitución regresiva, antes del refinamiento | $2,38018\times10^{-10}$ | $2,70171\times10^{-13}$ |
| Precisión global equivalente en bits | 31,97 | 41,75 |
| Pérdida equivalente respecto de 53 bits | 21,03 | 11,25 |

Los valores provienen de `resultados/residuo.txt`.
La precisión global equivalente se calcula como $-\log_2(E_{\mathrm{rel}})$ y la pérdida equivalente como $53-b_{\mathrm{efectivos}}$. Estos indicadores expresan la precisión global observada a partir del error relativo, no un conteo literal.

### T2 - Pivoteo y mantisa
| **Indicador** | **Sin pivoteo** | **Pivoteo parcial escalado** |
|:---:|:---|:---|
| **Observacion** | El algoritmo sin pivoteo utiliza un pivote inicial, que genera multiplicadores de hasta $2,75259\times10^{13}$. Los productos y actualizaciones de filas dan valores grandes con un factor de crecimiento de $2641,22425$, al operar con 53 bits de mantisa estos productos se redondean. La precisión global equivalente es de $31,97$ bits, lo que representa una perdida equivalentes a $21.03$ bits respecto de $53$ bits de mantisa disponibles. | El algoritmo con pivoteo parcial selecciona pivotes considerando magnitudes relativas de cada fila, aqui el factor de crecimiento disminuye respecto a sin pivoteo a $1,78320$, Esto reduce los errores de redondeo y permite conservar la informacion mas precisa durante la eliminación. La precisión global equivalente es de $41,75$ bits, lo que representa una perdida equivalentes a $11.25$ bits respecto de $53$ bits de mantisa disponibles. |

En resumen, las estrategias difieren debido a un error que a medida que se realizan pasos crece de manera mayor si no existiera un pivoteo, esto provoca que pueda mantenerse dentro de margenes mas precisos y confiables respecto a no utilizar pivoteo alguno.

## 5.- Condicionamiento
Datos extraidos de [resultados/residuo.txt](resultados/residuo.txt).

| Indicador | Valor |
|---|---:|
| Número de condición estimado $\kappa_2(A)$ | $3.08474\times10^{13}$ |
| Épsilon de doble precisión $\varepsilon$ | $2.22045\times10^{-16}$ |
| Cota orientativa $\kappa_2(A)\varepsilon$ | $6.84951\times10^{-3}$ |

El alto valor de condición nos dice que cambios pequeños en los datos pueden amplificarse en una solución.
El épsilon de doble precisión nos da una referencia de precision, aprox 15 cifras decimales significativas.
La cota orientativa representa una estimación en el peor caso, por lo que la cota resulta pesimista frente a los errores, ya que las perturbaciones en los valores no siguen las direcciones de maxima sensibilidad. Debido a esto el pivoteo mejora el comportamiento del cálculo.

El producto $\kappa_2(A)\varepsilon\approx6,85\times10^{-3}$ representa un error relativo orientativo del $0,685\%$. Su escala corresponde aproximadamente a $-\log_{10}(\kappa_2(A)\varepsilon)\approx2,16$ dígitos decimales, pero no garantiza esa cantidad para cada incógnita. Esta estimación de peor caso no permite asegurar por sí sola ocho cifras correctas, la mayor precisión obtenida se respalda mediante la comparación individual con la referencia racional exacta.

## 6.- Resultados
Los datos proceden de [resultados/solucion.csv](resultados/solucion.csv).
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
Para validar las soluciones se obtuvo una referencia usando los decimales originales de los CSV. Esta referencia satisface exactamente el sistema y se utiliza para calcular errores y verificar cifras significativas. No se usa para obtener la solución principal ni para calcular su corrección durante el refinamiento, su costo se considera separado del algoritmo evaluado.

El resultado se verificó calculando el residuo $r=b-Ax$ mediante `Fraction`, obteniendo los valores desde el archivo[resultados/residuo.txt](resultados/residuo.txt) utilizando los decimales originales de la matriz `12x12` y del vector. Esto permite evaluar el residuo sin introducir errores de redondeo adicionales.
$$
\|r\|_\infty=\max_i|r_i|.
$$

Se ejecutó una pasada de refinamiento iterativo para cada estrategia.
- El primer paso fue el calculó del residuo en aritmética exacta.
- Después se convirtió a doble precisión para resolver $A\delta x=r$, reutilizando los factores $L$, $U$ y la permutación existentes. 
- Finalmente, se actualizó la solución mediante $x_{\mathrm{nuevo}}=x+\delta x$ y se recalculó el residuo.

| Indicador | Sin pivoteo | Pivoteo parcial escalado |
|---|---:|---:|
| Norma infinito antes del refinamiento | $1.77175\times10^{-7}$ | $2.29088\times10^{-10}$ |
| Norma infinito después del refinamiento | $2.60319\times10^{-10}$ | $2.60319\times10^{-10}$ |
| Error relativo antes del refinamiento | $2.38018\times10^{-10}$ | $2.70171\times10^{-13}$ |
| Error relativo después del refinamiento | $4.85536\times10^{-17}$ | $4.85536\times10^{-17}$ |

El refinamiento redujo el error relativo de la solución en ambas corridas. La norma infinito del residuo disminuyó en la corrida sin pivoteo, mientras que en la corrida con pivoteo parcial escalado aumentó ligeramente.

Como control independiente se utilizó `numpy.linalg.solve(A, b)` (solicitado en `T4`), cuyo error relativo frente a esa referencia fue de $2.92693\times10^{-13}$.
## 8.- Conclusiones

El algoritmo de eliminación gaussiana permitió resolver el sistema denso de 12x12 utilizando 1354 flops principales, dentro de la tolerancia del ±10 % respecto de las 1486 flops de referencia. El cálculo único de cada multiplicador, su reutilización y la actualización de las columnas pendientes evitaron operaciones innecesarias.

El pivoteo parcial escalado permitió obtener una mejor relacion entre costo y exactitud, agregando 77 flops, además de comparaciones e intercambios, y reduciendo el factor de crecimiento de 2641 a 1,78.

Una pasada de refinamiento, reutilizando los factores existentes, redujo el error relativo en ambas corridas. Esta pasada agregó 288 flops, por lo que la resolución escalada con refinamiento alcanzó 1719 flops, sin incluir los controles independientes. La comprobación respaldó un mínimo de 16 cifras significativas por incógnita. También se observó que mejorar la solución no implica necesariamente disminuir la norma del residuo.

Para un sistema denso de tamaño n=1000, mantendría el pivoteo para mejorar la estabilidad, la reutilización de factores para evitar repetir operaciones y evitaría almacenar todas las matrices intermedias.
## 9.- Reproducibilidad
- **Python utilizado:** 3.14.3.
- **Biblioteca externa:** NumPy 2.5.0.
- **Versión mínima de Python requerida:** 3.12.
- **Módulos de la biblioteca estándar:** `csv`, `io`, `pathlib`, `platform`, `dataclasses`, `decimal` y `fractions`, incluidos en Python.

### Ejecución(Desde la raiz del proyecto)
- `python src/main.py`

## 10.- Uso de asistentes de IA

La utilización y asistencia de los agentes de ia en este trabajo fue el siguiente:
- Asistencia en los pasos a seguir para la realización de la evaluacion, por donde comenzar, como comprobar y finalizar el informe.
- Asistencia en la creación del codigo en la carpeta ./src/, con posterior revision humana y cambios para ajustarlo a los requisitos (uso de NumPy) solicitados en la evaluacion.
- Generacion de texto en formato .md para mejor legibilidad (arbol de estructura de carpetas del repo, que simbologia se utiliza para generar tablas, etc.).
- Generacion de formulas en formato .md para representación de formulas.
- Como llegar a la precision global equivalente y perdida equivalente de bits.
- Asistencia en la seccion de 5.- Condicionamiento a traves de explicaciones.

## 11.- Referencias
- Thevapalan, A. (2025, 18 de abril). Eliminación gaussiana: Un método para resolver sistemas de ecuaciones. DataCamp. https://www.datacamp.com/es/tutorial/gaussian-elimination
