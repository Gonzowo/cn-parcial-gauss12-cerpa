# Costo de las dos estrategias

Para n=12: aproximadamente 1486 flops, tolerancia ±10 %.
La asignación directa de los 66 ceros evita 132 flops: 1486 - 132 = 1354.
Se compara con la referencia el costo principal; el pivoteo se informa aparte.
No se incluyen en él diagnósticos, residuo exacto, referencia racional ni control NumPy.

## Estrategia: ninguno

### Conteo principal

Convención: 1 flop por suma, resta, multiplicación o división.
Comparaciones, valores absolutos e intercambios no son flops.
Se excluyen validaciones, copias, asignaciones y diagnósticos.

| Fase | Paso | Mult./div. | Sumas/restas | Flops | Comparaciones | Abs. | Intercambios |
|---|---:|---:|---:|---:|---:|---:|---:|
| eliminacion | 1 | 132 | 121 | 253 | 0 | 0 | 0 |
| actualizacion_b | 1 | 11 | 11 | 22 | 0 | 0 | 0 |
| eliminacion | 2 | 110 | 100 | 210 | 0 | 0 | 0 |
| actualizacion_b | 2 | 10 | 10 | 20 | 0 | 0 | 0 |
| eliminacion | 3 | 90 | 81 | 171 | 0 | 0 | 0 |
| actualizacion_b | 3 | 9 | 9 | 18 | 0 | 0 | 0 |
| eliminacion | 4 | 72 | 64 | 136 | 0 | 0 | 0 |
| actualizacion_b | 4 | 8 | 8 | 16 | 0 | 0 | 0 |
| eliminacion | 5 | 56 | 49 | 105 | 0 | 0 | 0 |
| actualizacion_b | 5 | 7 | 7 | 14 | 0 | 0 | 0 |
| eliminacion | 6 | 42 | 36 | 78 | 0 | 0 | 0 |
| actualizacion_b | 6 | 6 | 6 | 12 | 0 | 0 | 0 |
| eliminacion | 7 | 30 | 25 | 55 | 0 | 0 | 0 |
| actualizacion_b | 7 | 5 | 5 | 10 | 0 | 0 | 0 |
| eliminacion | 8 | 20 | 16 | 36 | 0 | 0 | 0 |
| actualizacion_b | 8 | 4 | 4 | 8 | 0 | 0 | 0 |
| eliminacion | 9 | 12 | 9 | 21 | 0 | 0 | 0 |
| actualizacion_b | 9 | 3 | 3 | 6 | 0 | 0 | 0 |
| eliminacion | 10 | 6 | 4 | 10 | 0 | 0 | 0 |
| actualizacion_b | 10 | 2 | 2 | 4 | 0 | 0 | 0 |
| eliminacion | 11 | 2 | 1 | 3 | 0 | 0 | 0 |
| actualizacion_b | 11 | 1 | 1 | 2 | 0 | 0 | 0 |
| sustitucion_regresiva | 12 | 1 | 0 | 1 | 0 | 0 | 0 |
| sustitucion_regresiva | 11 | 2 | 1 | 3 | 0 | 0 | 0 |
| sustitucion_regresiva | 10 | 3 | 2 | 5 | 0 | 0 | 0 |
| sustitucion_regresiva | 9 | 4 | 3 | 7 | 0 | 0 | 0 |
| sustitucion_regresiva | 8 | 5 | 4 | 9 | 0 | 0 | 0 |
| sustitucion_regresiva | 7 | 6 | 5 | 11 | 0 | 0 | 0 |
| sustitucion_regresiva | 6 | 7 | 6 | 13 | 0 | 0 | 0 |
| sustitucion_regresiva | 5 | 8 | 7 | 15 | 0 | 0 | 0 |
| sustitucion_regresiva | 4 | 9 | 8 | 17 | 0 | 0 | 0 |
| sustitucion_regresiva | 3 | 10 | 9 | 19 | 0 | 0 | 0 |
| sustitucion_regresiva | 2 | 11 | 10 | 21 | 0 | 0 | 0 |
| sustitucion_regresiva | 1 | 12 | 11 | 23 | 0 | 0 | 0 |

Flops principales: 1354.
Flops adicionales de pivoteo: 0.
Flops totales: 1354.

La subdiagonal se asigna a cero sin multiplicar ni restar; no se actualizan columnas ya eliminadas.

Diferencia frente a 1486: -8.882907 %.
Sobrecosto del refinamiento (incluye sumar la corrección):

### Conteo del refinamiento

Convención: 1 flop por suma, resta, multiplicación o división.
Comparaciones, valores absolutos e intercambios no son flops.
Se excluyen validaciones, copias, asignaciones y diagnósticos.

| Fase | Paso | Mult./div. | Sumas/restas | Flops | Comparaciones | Abs. | Intercambios |
|---|---:|---:|---:|---:|---:|---:|---:|
| sustitucion_directa | 2 | 1 | 1 | 2 | 0 | 0 | 0 |
| sustitucion_directa | 3 | 2 | 2 | 4 | 0 | 0 | 0 |
| sustitucion_directa | 4 | 3 | 3 | 6 | 0 | 0 | 0 |
| sustitucion_directa | 5 | 4 | 4 | 8 | 0 | 0 | 0 |
| sustitucion_directa | 6 | 5 | 5 | 10 | 0 | 0 | 0 |
| sustitucion_directa | 7 | 6 | 6 | 12 | 0 | 0 | 0 |
| sustitucion_directa | 8 | 7 | 7 | 14 | 0 | 0 | 0 |
| sustitucion_directa | 9 | 8 | 8 | 16 | 0 | 0 | 0 |
| sustitucion_directa | 10 | 9 | 9 | 18 | 0 | 0 | 0 |
| sustitucion_directa | 11 | 10 | 10 | 20 | 0 | 0 | 0 |
| sustitucion_directa | 12 | 11 | 11 | 22 | 0 | 0 | 0 |
| sustitucion_regresiva | 12 | 1 | 0 | 1 | 0 | 0 | 0 |
| sustitucion_regresiva | 11 | 2 | 1 | 3 | 0 | 0 | 0 |
| sustitucion_regresiva | 10 | 3 | 2 | 5 | 0 | 0 | 0 |
| sustitucion_regresiva | 9 | 4 | 3 | 7 | 0 | 0 | 0 |
| sustitucion_regresiva | 8 | 5 | 4 | 9 | 0 | 0 | 0 |
| sustitucion_regresiva | 7 | 6 | 5 | 11 | 0 | 0 | 0 |
| sustitucion_regresiva | 6 | 7 | 6 | 13 | 0 | 0 | 0 |
| sustitucion_regresiva | 5 | 8 | 7 | 15 | 0 | 0 | 0 |
| sustitucion_regresiva | 4 | 9 | 8 | 17 | 0 | 0 | 0 |
| sustitucion_regresiva | 3 | 10 | 9 | 19 | 0 | 0 | 0 |
| sustitucion_regresiva | 2 | 11 | 10 | 21 | 0 | 0 | 0 |
| sustitucion_regresiva | 1 | 12 | 11 | 23 | 0 | 0 | 0 |
| actualizacion_refinamiento | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| actualizacion_refinamiento | 2 | 0 | 1 | 1 | 0 | 0 | 0 |
| actualizacion_refinamiento | 3 | 0 | 1 | 1 | 0 | 0 | 0 |
| actualizacion_refinamiento | 4 | 0 | 1 | 1 | 0 | 0 | 0 |
| actualizacion_refinamiento | 5 | 0 | 1 | 1 | 0 | 0 | 0 |
| actualizacion_refinamiento | 6 | 0 | 1 | 1 | 0 | 0 | 0 |
| actualizacion_refinamiento | 7 | 0 | 1 | 1 | 0 | 0 | 0 |
| actualizacion_refinamiento | 8 | 0 | 1 | 1 | 0 | 0 | 0 |
| actualizacion_refinamiento | 9 | 0 | 1 | 1 | 0 | 0 | 0 |
| actualizacion_refinamiento | 10 | 0 | 1 | 1 | 0 | 0 | 0 |
| actualizacion_refinamiento | 11 | 0 | 1 | 1 | 0 | 0 | 0 |
| actualizacion_refinamiento | 12 | 0 | 1 | 1 | 0 | 0 | 0 |

Flops principales: 288.
Flops adicionales de pivoteo: 0.
Flops totales: 288.

La subdiagonal se asigna a cero sin multiplicar ni restar; no se actualizan columnas ya eliminadas.


## Estrategia: escalado

### Conteo principal

Convención: 1 flop por suma, resta, multiplicación o división.
Comparaciones, valores absolutos e intercambios no son flops.
Se excluyen validaciones, copias, asignaciones y diagnósticos.

| Fase | Paso | Mult./div. | Sumas/restas | Flops | Comparaciones | Abs. | Intercambios |
|---|---:|---:|---:|---:|---:|---:|---:|
| pivoteo_escalas | 0 | 0 | 0 | 0 | 132 | 144 | 0 |
| pivoteo_busqueda | 1 | 12 | 0 | 12 | 11 | 12 | 1 |
| eliminacion | 1 | 132 | 121 | 253 | 0 | 0 | 0 |
| actualizacion_b | 1 | 11 | 11 | 22 | 0 | 0 | 0 |
| pivoteo_busqueda | 2 | 11 | 0 | 11 | 10 | 11 | 0 |
| eliminacion | 2 | 110 | 100 | 210 | 0 | 0 | 0 |
| actualizacion_b | 2 | 10 | 10 | 20 | 0 | 0 | 0 |
| pivoteo_busqueda | 3 | 10 | 0 | 10 | 9 | 10 | 1 |
| eliminacion | 3 | 90 | 81 | 171 | 0 | 0 | 0 |
| actualizacion_b | 3 | 9 | 9 | 18 | 0 | 0 | 0 |
| pivoteo_busqueda | 4 | 9 | 0 | 9 | 8 | 9 | 1 |
| eliminacion | 4 | 72 | 64 | 136 | 0 | 0 | 0 |
| actualizacion_b | 4 | 8 | 8 | 16 | 0 | 0 | 0 |
| pivoteo_busqueda | 5 | 8 | 0 | 8 | 7 | 8 | 1 |
| eliminacion | 5 | 56 | 49 | 105 | 0 | 0 | 0 |
| actualizacion_b | 5 | 7 | 7 | 14 | 0 | 0 | 0 |
| pivoteo_busqueda | 6 | 7 | 0 | 7 | 6 | 7 | 1 |
| eliminacion | 6 | 42 | 36 | 78 | 0 | 0 | 0 |
| actualizacion_b | 6 | 6 | 6 | 12 | 0 | 0 | 0 |
| pivoteo_busqueda | 7 | 6 | 0 | 6 | 5 | 6 | 1 |
| eliminacion | 7 | 30 | 25 | 55 | 0 | 0 | 0 |
| actualizacion_b | 7 | 5 | 5 | 10 | 0 | 0 | 0 |
| pivoteo_busqueda | 8 | 5 | 0 | 5 | 4 | 5 | 1 |
| eliminacion | 8 | 20 | 16 | 36 | 0 | 0 | 0 |
| actualizacion_b | 8 | 4 | 4 | 8 | 0 | 0 | 0 |
| pivoteo_busqueda | 9 | 4 | 0 | 4 | 3 | 4 | 1 |
| eliminacion | 9 | 12 | 9 | 21 | 0 | 0 | 0 |
| actualizacion_b | 9 | 3 | 3 | 6 | 0 | 0 | 0 |
| pivoteo_busqueda | 10 | 3 | 0 | 3 | 2 | 3 | 0 |
| eliminacion | 10 | 6 | 4 | 10 | 0 | 0 | 0 |
| actualizacion_b | 10 | 2 | 2 | 4 | 0 | 0 | 0 |
| pivoteo_busqueda | 11 | 2 | 0 | 2 | 1 | 2 | 0 |
| eliminacion | 11 | 2 | 1 | 3 | 0 | 0 | 0 |
| actualizacion_b | 11 | 1 | 1 | 2 | 0 | 0 | 0 |
| sustitucion_regresiva | 12 | 1 | 0 | 1 | 0 | 0 | 0 |
| sustitucion_regresiva | 11 | 2 | 1 | 3 | 0 | 0 | 0 |
| sustitucion_regresiva | 10 | 3 | 2 | 5 | 0 | 0 | 0 |
| sustitucion_regresiva | 9 | 4 | 3 | 7 | 0 | 0 | 0 |
| sustitucion_regresiva | 8 | 5 | 4 | 9 | 0 | 0 | 0 |
| sustitucion_regresiva | 7 | 6 | 5 | 11 | 0 | 0 | 0 |
| sustitucion_regresiva | 6 | 7 | 6 | 13 | 0 | 0 | 0 |
| sustitucion_regresiva | 5 | 8 | 7 | 15 | 0 | 0 | 0 |
| sustitucion_regresiva | 4 | 9 | 8 | 17 | 0 | 0 | 0 |
| sustitucion_regresiva | 3 | 10 | 9 | 19 | 0 | 0 | 0 |
| sustitucion_regresiva | 2 | 11 | 10 | 21 | 0 | 0 | 0 |
| sustitucion_regresiva | 1 | 12 | 11 | 23 | 0 | 0 | 0 |

Flops principales: 1354.
Flops adicionales de pivoteo: 77.
Flops totales: 1431.

La subdiagonal se asigna a cero sin multiplicar ni restar; no se actualizan columnas ya eliminadas.

Diferencia frente a 1486: -8.882907 %.
Sobrecosto del refinamiento (incluye sumar la corrección):

### Conteo del refinamiento

Convención: 1 flop por suma, resta, multiplicación o división.
Comparaciones, valores absolutos e intercambios no son flops.
Se excluyen validaciones, copias, asignaciones y diagnósticos.

| Fase | Paso | Mult./div. | Sumas/restas | Flops | Comparaciones | Abs. | Intercambios |
|---|---:|---:|---:|---:|---:|---:|---:|
| sustitucion_directa | 2 | 1 | 1 | 2 | 0 | 0 | 0 |
| sustitucion_directa | 3 | 2 | 2 | 4 | 0 | 0 | 0 |
| sustitucion_directa | 4 | 3 | 3 | 6 | 0 | 0 | 0 |
| sustitucion_directa | 5 | 4 | 4 | 8 | 0 | 0 | 0 |
| sustitucion_directa | 6 | 5 | 5 | 10 | 0 | 0 | 0 |
| sustitucion_directa | 7 | 6 | 6 | 12 | 0 | 0 | 0 |
| sustitucion_directa | 8 | 7 | 7 | 14 | 0 | 0 | 0 |
| sustitucion_directa | 9 | 8 | 8 | 16 | 0 | 0 | 0 |
| sustitucion_directa | 10 | 9 | 9 | 18 | 0 | 0 | 0 |
| sustitucion_directa | 11 | 10 | 10 | 20 | 0 | 0 | 0 |
| sustitucion_directa | 12 | 11 | 11 | 22 | 0 | 0 | 0 |
| sustitucion_regresiva | 12 | 1 | 0 | 1 | 0 | 0 | 0 |
| sustitucion_regresiva | 11 | 2 | 1 | 3 | 0 | 0 | 0 |
| sustitucion_regresiva | 10 | 3 | 2 | 5 | 0 | 0 | 0 |
| sustitucion_regresiva | 9 | 4 | 3 | 7 | 0 | 0 | 0 |
| sustitucion_regresiva | 8 | 5 | 4 | 9 | 0 | 0 | 0 |
| sustitucion_regresiva | 7 | 6 | 5 | 11 | 0 | 0 | 0 |
| sustitucion_regresiva | 6 | 7 | 6 | 13 | 0 | 0 | 0 |
| sustitucion_regresiva | 5 | 8 | 7 | 15 | 0 | 0 | 0 |
| sustitucion_regresiva | 4 | 9 | 8 | 17 | 0 | 0 | 0 |
| sustitucion_regresiva | 3 | 10 | 9 | 19 | 0 | 0 | 0 |
| sustitucion_regresiva | 2 | 11 | 10 | 21 | 0 | 0 | 0 |
| sustitucion_regresiva | 1 | 12 | 11 | 23 | 0 | 0 | 0 |
| actualizacion_refinamiento | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| actualizacion_refinamiento | 2 | 0 | 1 | 1 | 0 | 0 | 0 |
| actualizacion_refinamiento | 3 | 0 | 1 | 1 | 0 | 0 | 0 |
| actualizacion_refinamiento | 4 | 0 | 1 | 1 | 0 | 0 | 0 |
| actualizacion_refinamiento | 5 | 0 | 1 | 1 | 0 | 0 | 0 |
| actualizacion_refinamiento | 6 | 0 | 1 | 1 | 0 | 0 | 0 |
| actualizacion_refinamiento | 7 | 0 | 1 | 1 | 0 | 0 | 0 |
| actualizacion_refinamiento | 8 | 0 | 1 | 1 | 0 | 0 | 0 |
| actualizacion_refinamiento | 9 | 0 | 1 | 1 | 0 | 0 | 0 |
| actualizacion_refinamiento | 10 | 0 | 1 | 1 | 0 | 0 | 0 |
| actualizacion_refinamiento | 11 | 0 | 1 | 1 | 0 | 0 | 0 |
| actualizacion_refinamiento | 12 | 0 | 1 | 1 | 0 | 0 | 0 |

Flops principales: 288.
Flops adicionales de pivoteo: 0.
Flops totales: 288.

La subdiagonal se asigna a cero sin multiplicar ni restar; no se actualizan columnas ya eliminadas.
