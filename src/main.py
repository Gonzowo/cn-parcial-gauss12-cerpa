"""Reproduce las dos corridas y todos los archivos de resultados.
"""

import csv
from io import StringIO
from pathlib import Path
import platform

import numpy as np

try:
    from .gauss import gauss
    from .verificacion import (cifras_defendibles, decimal_texto, diagnostico,
                               errores_relativos, referencia_racional,
                               refinar, residuo_exacto)
except ImportError:
    from gauss import gauss
    from verificacion import (cifras_defendibles, decimal_texto, diagnostico,
                              errores_relativos, referencia_racional,
                              refinar, residuo_exacto)


RAIZ = Path(__file__).resolve().parents[1]


def cargar_datos():
    # Leer textos antes de convertir evita truncar los datos de la verificación.
    with (RAIZ / 'datos/matriz_a.csv').open(encoding='utf-8-sig', newline='') as archivo:
        a_texto = list(csv.reader(archivo))
    with (RAIZ / 'datos/vector_b.csv').open(encoding='utf-8-sig', newline='') as archivo:
        filas_b = list(csv.reader(archivo))
    if len(a_texto) != 12 or any(len(fila) != 12 for fila in a_texto):
        raise ValueError('matriz_a.csv debe contener exactamente 12 filas y 12 columnas.')
    if len(filas_b) != 12 or any(len(fila) != 1 for fila in filas_b):
        raise ValueError('vector_b.csv debe contener exactamente 12 filas de una columna.')
    b_texto = [fila[0] for fila in filas_b]
    a = np.array(a_texto, dtype=np.float64)
    b = np.array(b_texto, dtype=np.float64)
    if not np.isfinite(a).all() or not np.isfinite(b).all() or np.any(a == 0):
        raise ValueError('El caso requiere datos finitos y una matriz densa sin ceros.')
    return a_texto, b_texto, a, b


def matriz_texto(a) -> str:
    return '\n'.join(' '.join(f'{v:.17e}' for v in fila) for fila in a)


def main() -> None:
    a_texto, b_texto, a, b = cargar_datos()
    referencia = referencia_racional(a_texto, b_texto)
    condicion = diagnostico(a)
    # Control de biblioteca exclusivamente para contraste; no produce la entrega.
    biblioteca = np.linalg.solve(a, b)
    error_biblioteca = errores_relativos(biblioteca, referencia)[1]
    corridas = {nombre: gauss(a, b, nombre) for nombre in ('ninguno', 'escalado')}
    refinamientos = {nombre: refinar(a_texto, b_texto, corrida)
                     for nombre, corrida in corridas.items()}

    traza = ['TRAZAS DE ELIMINACIÓN', 'Valores float64 mostrados con 17 cifras decimales.', '']
    conteo = ['# Costo de las dos estrategias', '',
              'Para n=12: aproximadamente 1486 flops, tolerancia ±10 %.',
              'La asignación directa de los 66 ceros evita 132 flops: 1486 - 132 = 1354.',
              'Se compara con la referencia el costo principal; el pivoteo se informa aparte.',
              'No se incluyen en él diagnósticos, residuo exacto, referencia racional ni control NumPy.', '']
    verificacion = [
        'VERIFICACIÓN NUMÉRICA',
        f'Python {platform.python_version()}; NumPy {np.__version__}',
        'Datos originales leídos como texto; residuos calculados con Fraction, sin redondeo.',
        'Los residuos exactos se muestran redondeados a 25 cifras significativas.',
        'Referencia: eliminación racional propia adicional, solo para validación; residuo exacto cero.',
        'El error relativo global usa norma 2 y se mide contra esa referencia.',
        'El costo racional y los controles no se equiparan a flops de doble precisión.',
        f"kappa_2 estimado por SVD: {condicion['kappa_2']:.17e}",
        f"epsilon float64: {condicion['epsilon']:.17e}",
        f"kappa*epsilon: {condicion['kappa_epsilon']:.17e}",
        f"-log10(kappa*epsilon): {condicion['digitos_orientativos']:.6f}",
        'Esta estimación de peor caso no certifica dígitos por componente; se contrastan con la referencia exacta.',
        f'Error relativo del control numpy.linalg.solve: {error_biblioteca:.17e}', '',
    ]
    salida_csv = StringIO(newline='')
    escritor = csv.writer(salida_csv, lineterminator='\n')
    escritor.writerow(['estrategia', 'etapa', 'incognita', 'valor_float64_17_cifras',
                       'valor_reportado', 'digitos_afirmados', 'error_relativo_float64',
                       'error_relativo_reportado'])
    valores_publicados = None
    for nombre, corrida in corridas.items():
        refinamiento = refinamientos[nombre]
        error_inicial = errores_relativos(corrida.solucion, referencia)[1]
        error_refinado = errores_relativos(refinamiento.solucion, referencia)[1]
        traza.extend([f'ESTRATEGIA: {nombre}', ''])
        for paso in corrida.traza:
            traza.extend([
                f'Paso {paso.paso}; fila elegida antes del intercambio: {paso.fila_elegida}; pivote: {paso.pivote:.17e}',
                'Multiplicadores: ' + ' '.join(f'{v:.17e}' for v in paso.multiplicadores),
                'Matriz aumentada [A^(k) | b^(k)]:',
                matriz_texto(np.column_stack((paso.matriz, paso.vector_b))), '',
            ])
        conteo.extend([f'## Estrategia: {nombre}', '',
                       corrida.contador.reporte_markdown().replace('# Conteo de operaciones', '### Conteo principal', 1),
                       f'Diferencia frente a 1486: {(corrida.contador.flops_principales / 1486 - 1) * 100:.6f} %.',
                       'Sobrecosto del refinamiento (incluye sumar la corrección):', '',
                       refinamiento.contador.reporte_markdown().replace('# Conteo de operaciones', '### Conteo del refinamiento', 1), ''])
        bits = max(0.0, float(np.log2(corrida.multiplicador_maximo))) if corrida.multiplicador_maximo else 0.0
        verificacion.extend([
            f'ESTRATEGIA: {nombre}',
            f'Multiplicador máximo: {corrida.multiplicador_maximo:.17e}',
            f'Factor de crecimiento durante toda la eliminación: {corrida.factor_crecimiento:.17e}',
            f'Indicador log2(max(1,|m|max)): {bits:.6f} bits; es una escala de amplificación, no una medición exacta de bits perdidos.',
            f'Error relativo inicial: {error_inicial:.17e}',
            f'Error relativo tras una pasada de refinamiento: {error_refinado:.17e}',
            f'Norma infinito antes: {decimal_texto(refinamiento.norma_antes)}',
            f'Norma infinito después: {decimal_texto(refinamiento.norma_despues)}',
            f'Mejora estricta de la norma del residuo: {refinamiento.norma_despues < refinamiento.norma_antes}',
            'Corrección calculada usando los mismos L, U y permutación:',
            ' '.join(f'{v:.17e}' for v in refinamiento.correccion),
            'i; residuo inicial; residuo después del refinamiento',
        ])
        for i, (antes, despues) in enumerate(zip(refinamiento.residuo_antes, refinamiento.residuo_despues), 1):
            verificacion.append(f'{i}; {decimal_texto(antes)}; {decimal_texto(despues)}')
        for etapa, x in [('inicial', corrida.solucion), ('refinada', refinamiento.solucion)]:
            errores = errores_relativos(x, referencia)[0]
            publicados = []
            for i, valor in enumerate(x):
                cifras = cifras_defendibles(valor, referencia[i])
                publicado = format(float(valor), f'.{max(1, cifras)}g')
                publicados.append(publicado)
                error_publicado = errores_relativos([publicado], [referencia[i]])[0][0]
                escritor.writerow([nombre, etapa, i + 1, f'{valor:.17g}', publicado,
                                    cifras, f'{errores[i]:.17e}', f'{error_publicado:.17e}'])
            if nombre == 'escalado' and etapa == 'refinada':
                valores_publicados = publicados
        verificacion.append('')

    # Verificar también los números decimales que efectivamente se publican.
    residuo_publicado, norma_publicada = residuo_exacto(a_texto, b_texto, valores_publicados)
    verificacion.extend([
        'SOLUCIÓN PRINCIPAL: pivoteo escalado con una pasada de refinamiento.',
        'valor_reportado contiene solo las cifras defendibles; la columna de 17 cifras permite reproducir el float64.',
        'Los dígitos afirmados exigen cota relativa y coincidencia con el redondeo de la referencia.',
        f'Norma infinito de los valores decimales reportados: {decimal_texto(norma_publicada)}',
        'Residuo de los valores decimales reportados:',
        *[f'{i}: {decimal_texto(v)}' for i, v in enumerate(residuo_publicado, 1)], '',
    ])
    destino = RAIZ / 'resultados'
    destino.mkdir(exist_ok=True)
    contenidos = {
        'solucion.csv': salida_csv.getvalue(),
        'traza_eliminacion.txt': '\n'.join(traza),
        'conteo_flops.md': '\n'.join(conteo),
        'residuo.txt': '\n'.join(verificacion),
    }
    for nombre, contenido in contenidos.items():
        (destino / nombre).write_text(contenido.rstrip() + '\n', encoding='utf-8')
    print('Generados los cuatro archivos de resultados/.')
    print(f"kappa_2 estimado: {condicion['kappa_2']:.6e}")
    for nombre in corridas:
        r = refinamientos[nombre]
        digitos = min(cifras_defendibles(v, ref) for v, ref in zip(r.solucion, referencia))
        print(f'{nombre}: {corridas[nombre].contador.flops_principales} flops principales; '
              f'{corridas[nombre].contador.flops_pivoteo} flops de pivoteo; '
              f'mínimo {digitos} cifras defendibles después de refinar.')


if __name__ == '__main__':
    main()
