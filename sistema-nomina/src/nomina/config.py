"""Parámetros (reglas de negocio) del sistema de nómina.

Centralizar las constantes en un único lugar facilita su mantenimiento y su
inyección en las calculadoras (Principio SOLID de Responsabilidad Única y de
Inversión de Dependencias): cambiar una tasa no requiere tocar la lógica.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class ParametrosNomina:
    """Parámetros configurables de la nómina (todas las tasas son decimales)."""

    # --- Deducciones obligatorias -----------------------------------------
    tasa_seguro_social_pension: Decimal = Decimal("0.04")  # 4% SS + Pensión
    tasa_arl: Decimal = Decimal("0.01")  # ARL (1%)

    # --- Empleado asalariado ----------------------------------------------
    tasa_bono_antiguedad: Decimal = Decimal("0.10")  # 10% si > 5 años
    anios_minimos_bono_antiguedad: int = 5

    # --- Empleado por horas ------------------------------------------------
    horas_regulares: int = 40  # semanales; lo que supere son extras
    multiplicador_horas_extras: Decimal = Decimal("1.5")
    tasa_fondo_ahorro: Decimal = Decimal("0.02")  # 2% del salario
    anios_minimos_fondo_ahorro: int = 1

    # --- Empleado por comisión ---------------------------------------------
    umbral_ventas_bono_comision: Decimal = Decimal("20000000")
    tasa_bono_comision: Decimal = Decimal("0.03")  # 3% sobre ventas

    # --- Beneficios adicionales ---------------------------------------------
    bono_alimentacion: Decimal = Decimal("1000000")  # $1.000.000/mes


# Instancia por defecto usada por las calculadoras.
PARAMETROS_POR_DEFECTO = ParametrosNomina()
