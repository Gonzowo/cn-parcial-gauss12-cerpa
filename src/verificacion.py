"""Validación independiente de los datos decimales originales.
"""

from dataclasses import dataclass
from decimal import Decimal, localcontext
from fractions import Fraction

import numpy as np

try:
    from .conteo import Contador
    from .gauss import ResultadoGauss, resolver_con_factores
except ImportError:
    from conteo import Contador
    from gauss import ResultadoGauss, resolver_con_factores


def racional(valor) -> Fraction:
    """Un texto conserva el decimal original; un float conserva su valor binario."""
    if isinstance(valor, (float, np.floating)):
        return Fraction.from_float(float(valor))
    return Fraction(valor)


def decimal_texto(valor: Fraction, cifras: int = 25) -> str:
    with localcontext() as contexto:
        contexto.prec = max(80, cifras + 20)
        return format(Decimal(valor.numerator) / Decimal(valor.denominator), f'.{cifras}g')


def residuo_exacto(a, b, x) -> tuple[list[Fraction], Fraction]:
    """Calcula b-Ax y su norma infinito en aritmética racional exacta."""
    n = len(a)
    if n == 0 or len(b) != n or len(x) != n or any(len(fila) != n for fila in a):
        raise ValueError("Dimensiones incompatibles para calcular el residuo.")
    xq = [racional(valor) for valor in x]
    residuo = [racional(b[i]) - sum(
        (racional(a[i][j]) * xq[j] for j in range(n)), Fraction(0)
    ) for i in range(n)]
    return residuo, max(abs(valor) for valor in residuo)


def referencia_racional(a, b) -> list[Fraction]:
    """Gauss auxiliar exacto, independiente del algoritmo float64 evaluado.

    Esta factorización adicional no produce la solución entregada ni se usa para
    refinarla. Su costo de aritmética racional queda fuera del conteo principal.
    """
    n = len(a)
    if n == 0 or len(b) != n or any(len(fila) != n for fila in a):
        raise ValueError("La referencia requiere un sistema cuadrado compatible.")
    aumentada = [[racional(v) for v in fila] + [racional(rhs)]
                 for fila, rhs in zip(a, b)]
    for k in range(n - 1):
        p = max(range(k, n), key=lambda i: abs(aumentada[i][k]))
        aumentada[k], aumentada[p] = aumentada[p], aumentada[k]
        if aumentada[k][k] == 0:
            raise ValueError("El sistema de referencia es singular.")
        for i in range(k + 1, n):
            m = aumentada[i][k] / aumentada[k][k]
            for j in range(k + 1, n + 1):
                aumentada[i][j] -= m * aumentada[k][j]
            aumentada[i][k] = Fraction(0)
    x = [Fraction(0)] * n
    for i in range(n - 1, -1, -1):
        if aumentada[i][i] == 0:
            raise ValueError("El sistema de referencia es singular.")
        x[i] = (aumentada[i][n] - sum(
            (aumentada[i][j] * x[j] for j in range(i + 1, n)), Fraction(0)
        )) / aumentada[i][i]
    # La referencia debe satisfacer exactamente los decimales suministrados.
    if residuo_exacto(a, b, x)[1] != 0:
        raise ArithmeticError("La referencia racional no satisface el sistema.")
    return x


def errores_relativos(x, referencia) -> tuple[np.ndarray, float]:
    """Resta exacta antes de convertir a float para evaluar la norma 2."""
    if len(x) != len(referencia):
        raise ValueError("Solución y referencia de dimensiones incompatibles.")
    diferencias = [racional(v) - racional(r) for v, r in zip(x, referencia)]
    por_componente = np.array([
        float(abs(d / racional(r))) if r != 0 else (0.0 if d == 0 else np.inf)
        for d, r in zip(diferencias, referencia)
    ])
    denominador = np.linalg.norm(np.array([float(r) for r in referencia]))
    numerador = np.linalg.norm(np.array([float(d) for d in diferencias]))
    relativo = numerador / denominador if denominador else (0.0 if numerador == 0 else np.inf)
    return por_componente, float(relativo)


def cifras_defendibles(valor, referencia: Fraction, maximo: int = 17) -> int:
    """Criterio conservador: cota relativa y coincidencia de redondeo decimal.

    Para d cifras se exige error relativo <= 0.5*10**(1-d), y que el valor
    publicado redondee igual que la referencia a esas d cifras. Se devuelve la
    mayor precisión que satisface ambas condiciones. Un desacuerdo de redondeo
    no descarta precisiones posteriores; solo la cota relativa permite detener
    la búsqueda, porque se vuelve más estricta al aumentar d.
    """
    if referencia == 0:
        return maximo if racional(valor) == 0 else 0
    error = abs((racional(valor) - referencia) / referencia)
    correctas = 0
    for d in range(1, maximo + 1):
        cota = Fraction(1, 2) * Fraction(10) ** (1 - d)
        if error > cota:
            break
        publicado = format(float(valor), f'.{d}g')
        esperado = decimal_texto(referencia, d)
        if Fraction(publicado) == Fraction(esperado):
            correctas = d
    return correctas


@dataclass
class Refinamiento:
    solucion: np.ndarray
    correccion: np.ndarray
    residuo_antes: list[Fraction]
    norma_antes: Fraction
    residuo_despues: list[Fraction]
    norma_despues: Fraction
    contador: Contador


def refinar(a, b, resultado: ResultadoGauss) -> Refinamiento:
    """Una pasada: residuo exacto, corrección con LU existente, suma float64."""
    antes, norma_antes = residuo_exacto(a, b, resultado.solucion)
    contador = Contador()
    rhs = np.array([float(valor) for valor in antes], dtype=np.float64)
    correccion = resolver_con_factores(resultado, rhs, contador)
    solucion = resultado.solucion.copy()
    for i in range(len(solucion)):
        solucion[i] += correccion[i]
        contador.registrar('actualizacion_refinamiento', i + 1, 'sumas')
    despues, norma_despues = residuo_exacto(a, b, solucion)
    return Refinamiento(solucion, correccion, antes, norma_antes,
                        despues, norma_despues, contador)


def diagnostico(a) -> dict:
    matriz = np.asarray(a, dtype=np.float64)
    kappa = float(np.linalg.cond(matriz, p=2))  # SVD; no calcula la inversa.
    epsilon = float(np.finfo(np.float64).eps)
    producto = kappa * epsilon
    return {
        'kappa_2': kappa,
        'epsilon': epsilon,
        'kappa_epsilon': producto,
        'digitos_orientativos': max(0.0, -float(np.log10(producto))),
    }
