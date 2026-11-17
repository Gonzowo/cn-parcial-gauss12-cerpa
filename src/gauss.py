"""Eliminación gaussiana propia en doble precisión con factores reutilizables.
"""

from dataclasses import dataclass

import numpy as np

try:
    from .conteo import Contador
except ImportError:
    from conteo import Contador


@dataclass
class PasoEliminacion:
    paso: int
    fila_elegida: int  # Posición antes del intercambio, numerada desde 1.
    pivote: float
    multiplicadores: np.ndarray
    matriz: np.ndarray
    vector_b: np.ndarray


@dataclass
class ResultadoGauss:
    solucion: np.ndarray
    l: np.ndarray
    u: np.ndarray
    permutacion: np.ndarray  # PA = LU; (Pb)[i] = b[permutacion[i]].
    traza: list[PasoEliminacion]
    contador: Contador
    multiplicador_maximo: float
    factor_crecimiento: float
    estrategia: str


def _copiar_sistema(a, b) -> tuple[np.ndarray, np.ndarray]:
    matriz = np.array(a, dtype=np.float64, copy=True)
    vector = np.array(b, dtype=np.float64, copy=True)
    if (matriz.ndim != 2 or matriz.shape[0] == 0
            or matriz.shape[0] != matriz.shape[1]
            or vector.ndim != 1 or vector.size != matriz.shape[0]):
        raise ValueError("Se requiere una matriz cuadrada no vacía y un vector compatible.")
    if not np.isfinite(matriz).all():
        raise ValueError("La matriz debe contener valores finitos.")
    if not np.isfinite(vector).all():
        raise ValueError("El vector debe contener valores finitos.")
    return matriz, vector


def _sustitucion_regresiva(u, b, contador: Contador) -> np.ndarray:
    n = len(u)
    x = np.zeros(n, dtype=np.float64)
    for i in range(n - 1, -1, -1):
        if u[i][i] == 0.0:
            raise ValueError(f"Pivote nulo en la fila {i + 1}.")
        acumulado = b[i]
        for j in range(i + 1, n):
            producto = u[i][j] * x[j]
            contador.registrar("sustitucion_regresiva", i + 1, "multiplicaciones")
            acumulado -= producto
            contador.registrar("sustitucion_regresiva", i + 1, "restas")
        x[i] = acumulado / u[i][i]
        contador.registrar("sustitucion_regresiva", i + 1, "divisiones")
        if not np.isfinite(x[i]):
            raise ArithmeticError("Resultado no finito durante la sustitución regresiva.")
    return x


def gauss(a, b, pivoteo: str = "escalado") -> ResultadoGauss:
    """Resuelve Ax=b sin modificar las entradas.
    """
    if pivoteo not in ("ninguno", "escalado"):
        raise ValueError("El pivoteo debe ser 'ninguno' o 'escalado'.")
    u, rhs = _copiar_sistema(a, b)
    n = len(u)
    l = np.eye(n, dtype=np.float64)
    permutacion = np.arange(n)
    contador = Contador()
    traza = []
    max_inicial = float(np.max(np.abs(u)))
    if max_inicial == 0.0:
        raise ValueError("La matriz nula es singular.")
    max_observado = max_inicial
    max_multiplicador = 0.0
    escalas = np.zeros(n, dtype=np.float64)
    if pivoteo == "escalado":
        for indice, fila in enumerate(u):
            escala = abs(fila[0])
            contador.registrar("pivoteo_escalas", 0, "valores_absolutos")
            for valor in fila[1:]:
                candidato = abs(valor)
                contador.registrar("pivoteo_escalas", 0, "valores_absolutos")
                contador.registrar("pivoteo_escalas", 0, "comparaciones")
                if candidato > escala:
                    escala = candidato
            if escala == 0.0:
                raise ValueError("Una fila nula hace singular la matriz.")
            escalas[indice] = escala

    for k in range(n - 1):
        paso = k + 1
        elegida = k
        if pivoteo == "escalado":
            mejor = -1.0
            for i in range(k, n):
                numerador = abs(u[i][k])
                contador.registrar("pivoteo_busqueda", paso, "valores_absolutos")
                cociente = numerador / escalas[i]
                contador.registrar("pivoteo_busqueda", paso, "divisiones")
                if i == k:
                    mejor = cociente
                else:
                    contador.registrar("pivoteo_busqueda", paso, "comparaciones")
                    if cociente > mejor:
                        mejor, elegida = cociente, i
            if elegida != k:
                # La indexación avanzada crea una copia antes de asignar las filas.
                u[[k, elegida]] = u[[elegida, k]]
                rhs[k], rhs[elegida] = rhs[elegida], rhs[k]
                escalas[k], escalas[elegida] = escalas[elegida], escalas[k]
                permutacion[k], permutacion[elegida] = permutacion[elegida], permutacion[k]
                # Los multiplicadores de columnas anteriores también cambian de fila.
                for j in range(k):
                    l[k][j], l[elegida][j] = l[elegida][j], l[k][j]
                contador.registrar("pivoteo_busqueda", paso, "intercambios")
        pivote = u[k][k]
        if pivote == 0.0:
            raise ValueError(f"Pivote nulo en el paso {paso}; estrategia: {pivoteo}.")
        multiplicadores = []
        for i in range(k + 1, n):
            m = u[i][k] / pivote
            contador.registrar("eliminacion", paso, "divisiones")
            l[i][k] = m
            multiplicadores.append(m)
            max_multiplicador = max(max_multiplicador, abs(m))
            u[i][k] = 0.0
            for j in range(k + 1, n):
                producto = m * u[k][j]
                contador.registrar("eliminacion", paso, "multiplicaciones")
                u[i][j] -= producto
                contador.registrar("eliminacion", paso, "restas")
                if not np.isfinite(u[i][j]):
                    raise ArithmeticError("Resultado no finito durante la eliminación.")
                max_observado = max(max_observado, abs(u[i][j]))
            producto_b = m * rhs[k]
            contador.registrar("actualizacion_b", paso, "multiplicaciones")
            rhs[i] -= producto_b
            contador.registrar("actualizacion_b", paso, "restas")
            if not np.isfinite(rhs[i]):
                raise ArithmeticError("Lado derecho no finito durante la eliminación.")
        traza.append(PasoEliminacion(
            paso, elegida + 1, float(pivote),
            np.array(multiplicadores, dtype=np.float64), u.copy(), rhs.copy(),
        ))

    solucion = _sustitucion_regresiva(u, rhs, contador)
    return ResultadoGauss(
        solucion, l, u, permutacion, traza, contador,
        float(max_multiplicador), float(max_observado / max_inicial), pivoteo,
    )


def gauss_sin_pivoteo(a, b) -> ResultadoGauss:
    return gauss(a, b, pivoteo="ninguno")


def gauss_pivoteo_escalado(a, b) -> ResultadoGauss:
    return gauss(a, b, pivoteo="escalado")


def resolver_con_factores(resultado: ResultadoGauss, b,
                          contador: Contador | None = None) -> np.ndarray:
    """Resuelve otro lado derecho con los factores existentes (sin refactorizar).

    Un contador nuevo evita mezclar el refinamiento con la corrida principal.
    Para consultar su costo, el llamador puede proporcionar su propio contador.
    """
    n = len(resultado.u)
    rhs = np.array(b, dtype=np.float64, copy=True)
    if rhs.ndim != 1 or rhs.size != n or not np.isfinite(rhs).all():
        raise ValueError("El lado derecho debe tener dimensión compatible y valores finitos.")
    if contador is None:
        contador = Contador()
    elif contador is resultado.contador:
        raise ValueError("Utilice otro contador para separar el costo de la corrección.")
    y = rhs[resultado.permutacion].copy()
    for i in range(n):
        for j in range(i):
            producto = resultado.l[i][j] * y[j]
            contador.registrar("sustitucion_directa", i + 1, "multiplicaciones")
            y[i] -= producto
            contador.registrar("sustitucion_directa", i + 1, "restas")
        if not np.isfinite(y[i]):
            raise ArithmeticError("Resultado no finito durante la sustitución directa.")
    return _sustitucion_regresiva(resultado.u, y, contador)
