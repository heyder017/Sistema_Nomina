"""Punto de entrada de demostración: ``python -m nomina``.

Muestra el cálculo de nómina de un empleado de cada tipo.
"""
from __future__ import annotations

from datetime import date
from decimal import Decimal

from nomina.models import Asalariado, PorComision, PorHoras, Temporal
from nomina.services import ProcesadorNomina


def _formatear(monto: Decimal) -> str:
    """Formatea un monto en pesos colombianos sin decimales."""
    return f"${monto:,.0f}"


def main() -> None:
    """Calcula y muestra las nóminas de ejemplo de los cuatro tipos."""
    hoy = date.today()

    empleados = [
        Asalariado(
            nombre="Ana Asalariada",
            identificacion="1000001",
            fecha_ingreso=date(hoy.year - 6, 1, 1),
            salario_mensual=Decimal("4000000"),
        ),
        PorHoras(
            nombre="Bruno PorHoras",
            identificacion="1000002",
            fecha_ingreso=date(hoy.year - 2, 3, 15),
            tarifa_por_hora=Decimal("20000"),
            horas_trabajadas=Decimal("45"),
            acepta_fondo_ahorro=True,
        ),
        PorComision(
            nombre="Carla PorComisión",
            identificacion="1000003",
            fecha_ingreso=date(hoy.year - 3, 7, 1),
            salario_base=Decimal("1500000"),
            porcentaje_comision=Decimal("0.05"),
            ventas=Decimal("25000000"),
        ),
        Temporal(
            nombre="Diego Temporal",
            identificacion="1000004",
            fecha_ingreso=date(hoy.year, 1, 1),
            salario_mensual=Decimal("2000000"),
            fecha_fin_contrato=date(hoy.year, 12, 31),
        ),
    ]

    procesador = ProcesadorNomina()
    for empleado in empleados:
        recibo = procesador.procesar(empleado)
        print(f"--- {recibo.empleado.nombre} ({type(empleado).__name__}) ---")
        print(f"  Salario bruto:        {_formatear(recibo.salario_bruto)}")
        print(f"  Deducciones:         -{_formatear(recibo.deducciones.total)}")
        print(f"  Bono alimentación:    {_formatear(recibo.beneficios.bono_alimentacion)}")
        print(f"  Fondo de ahorro:      {_formatear(recibo.beneficios.fondo_ahorro)}")
        print(f"  Salario neto:         {_formatear(recibo.salario_neto)}")
        print()


if __name__ == "__main__":
    main()
