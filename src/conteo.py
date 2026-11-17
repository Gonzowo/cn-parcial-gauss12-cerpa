"""Conteo de operaciones ejecutadas.
"""

from dataclasses import dataclass


@dataclass
class Operaciones:
    sumas: int = 0
    restas: int = 0
    multiplicaciones: int = 0
    divisiones: int = 0
    comparaciones: int = 0
    valores_absolutos: int = 0
    intercambios: int = 0

    @property
    def flops(self) -> int:
        return self.sumas + self.restas + self.multiplicaciones + self.divisiones


class Contador:
    """Acumula registros por fase y paso (numerados desde 1).

    El paso 0 se reserva para la preparación de las escalas. Las fases cuyo
    nombre empieza por 'pivoteo' son sobrecosto de estabilidad.
    """

    def __init__(self) -> None:
        self.registros: dict[tuple[str, int], Operaciones] = {}

    def registrar(self, fase: str, paso: int, operacion: str,
                  cantidad: int = 1) -> None:
        if operacion not in Operaciones.__dataclass_fields__:
            raise ValueError(f"Operación desconocida: {operacion}")
        if not isinstance(cantidad, int) or cantidad < 0:
            raise ValueError("La cantidad debe ser un entero no negativo.")
        if not isinstance(paso, int) or paso < 0:
            raise ValueError("El paso debe ser un entero no negativo.")
        registro = self.registros.setdefault((fase, paso), Operaciones())
        setattr(registro, operacion, getattr(registro, operacion) + cantidad)

    def total(self, fase: str | None = None) -> Operaciones:
        resultado = Operaciones()
        for (nombre, _), registro in self.registros.items():
            if fase is None or nombre == fase:
                for campo in Operaciones.__dataclass_fields__:
                    setattr(resultado, campo,
                            getattr(resultado, campo) + getattr(registro, campo))
        return resultado

    @property
    def flops_pivoteo(self) -> int:
        return sum(registro.flops for (fase, _), registro in self.registros.items()
                   if fase.startswith("pivoteo"))

    @property
    def flops_principales(self) -> int:
        return self.total().flops - self.flops_pivoteo

    def reporte_markdown(self) -> str:
        lineas = [
            "# Conteo de operaciones", "",
            "Convención: 1 flop por suma, resta, multiplicación o división.",
            "Comparaciones, valores absolutos e intercambios no son flops.",
            "Se excluyen validaciones, copias, asignaciones y diagnósticos.", "",
            "| Fase | Paso | Mult./div. | Sumas/restas | Flops | Comparaciones | Abs. | Intercambios |",
            "|---|---:|---:|---:|---:|---:|---:|---:|",
        ]
        for (fase, paso), op in self.registros.items():
            lineas.append(
                f"| {fase} | {paso} | {op.multiplicaciones + op.divisiones} | "
                f"{op.sumas + op.restas} | {op.flops} | {op.comparaciones} | "
                f"{op.valores_absolutos} | {op.intercambios} |"
            )
        lineas.extend([
            "", f"Flops principales: {self.flops_principales}.",
            f"Flops adicionales de pivoteo: {self.flops_pivoteo}.",
            f"Flops totales: {self.total().flops}.", "",
            "La subdiagonal se asigna a cero sin multiplicar ni restar; "
            "no se actualizan columnas ya eliminadas.",
        ])
        return "\n".join(lineas) + "\n"
