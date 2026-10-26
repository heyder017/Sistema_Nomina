# Sistema de Nómina (CIPA)

Sistema de nómina orientado a objetos para una empresa que maneja cuatro tipos
de empleados, cada uno con su propia forma de calcular salario, beneficios y
deducciones.

## Tipos de empleado

| Tipo | Salario | Beneficios | Deducciones |
|------|---------|------------|-------------|
| **Asalariado** | Fijo mensual | Bono antigüedad 10% si > 5 años; alimentación $1.000.000 | SS+Pensión 4%, ARL 1% |
| **Por horas** | Horas × tarifa; extras > 40 h a 1.5× | Fondo de ahorro 2% si > 1 año y acepta | SS+Pensión 4%, ARL 1% |
| **Por comisión** | Base + % sobre ventas; bono 3% sobre ventas si > $20.000.000 | Alimentación $1.000.000 | SS+Pensión 4%, ARL 1% |
| **Temporal** | Fijo mensual (contrato a término fijo) | Ninguno | SS+Pensión 4%, ARL 1% |

**Validaciones:** salario neto nunca negativo, horas trabajadas no negativas,
ventas no menores a $0.

## Estructura del proyecto

```
sistema-nomina/
├── src/nomina/
│   ├── config.py                  # Parámetros/tasas de la nómina
│   ├── exceptions.py              # Excepciones de dominio
│   ├── __main__.py                # Demo: python -m nomina
│   ├── models/                    # Empleado (ABC) + 4 tipos concretos
│   └── services/                  # Deducciones, beneficios y procesador
├── tests/                         # Pruebas unitarias (pytest)
├── docs/METODOLOGIA.md            # Metodología de desarrollo
└── pyproject.toml
```

## Ejecución

```bash
# Requiere Python 3.10+ y pytest
python -m pip install --user pytest

# Demostración
PYTHONPATH=src python -m nomina

# Pruebas unitarias
python -m pytest
```

## Principios SOLID aplicados

- **S (Responsabilidad única):** cada modelo solo calcula su salario bruto;
  `CalculadoraDeducciones` solo deduce, `CalculadoraBeneficios` solo bonifica
  y `ProcesadorNomina` solo orquesta.
- **O (Abierto/cerrado):** los beneficios y el fondo de ahorro se resuelven
  por polimorfismo (`es_permanente`, `accede_fondo_ahorro`); añadir un quinto
  tipo de empleado no exige modificar servicios existentes.
- **L (Sustitución de Liskov):** cualquier subclase de `Empleado` es usable en
  `ProcesadorNomina` sin comprobar tipos (`isinstance`).
- **I (Segregación de interfaces):** interfaces pequeñas; los métodos de
  capacidad solo existen donde aportan.
- **D (Inversión de dependencias):** `ProcesadorNomina` recibe las calculadoras
  por inyección en el constructor, lo que permite sustituirlas en pruebas.

## Decisiones de diseño documentadas

- Dinero modelado con `decimal.Decimal` (no `float`) para evitar errores
  de redondeo en montos monetarios.
- Constantes de negocio centralizadas en `ParametrosNomina` (configurables
  por inyección, no escritas a mano en la lógica).
- Clases de dominio inmutables (`@dataclass(frozen=True)`).
- Modelo con estructura `src/` + `pyproject.toml` (buenas prácticas modernas
  de empaquetado Python).

## Metodología

Ver [docs/METODOLOGIA.md](docs/METODOLOGIA.md).
