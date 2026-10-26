# Metodología de Desarrollo de Software

## Enfoque general

Se aplicó un proceso **iterativo e incremental** inspirado en Scrum, adaptado
a un ejercicio de una sola iteración (sprint):

1. **Requisitos y análisis:** desglose del enunciado en reglas de negocio
   verificables (4 tipos de empleado, deducciones, beneficios, validaciones).
2. **Diseño:** modelado OOP con patrón **Strategy implícito** (cada tipo de
   empleado implementa su propio `calcular_salario_bruto()`) y separación en
   capas *modelo* / *servicios*.
3. **Implementación:** código limpio con Python moderno, tipado estático
   (`type hints`), docstrings y comentarios de intención (no de transcripción).
4. **Pruebas:** suite de pruebas unitarias con **pytest** antes de considerar
   la historia terminada (aproximación a TDD en los casos de reglas de negocio).
5. **Control de versiones:** repositorio Git con commits atómicos y
   convencionalistas (feat/test/docs/chaf) para evidenciar la evolución.

## Principios de código limpio aplicados

- Nombres descriptivos en español del dominio (`salario_bruto`,
  `bono_antiguedad`, `accede_fondo_ahorro`).
- Funciones y métodos cortos, con una sola razón para cambiar.
- Docstrings en cada módulo, clase y método público.
- Excepciones de dominio propias (`NominaError` y subtipos) en lugar de
  errores genéricos, para que el llamador distinga fallos de negocio.
- Clases inmutables (`frozen=True`) y ausencia de estado compartido.

## Pruebas unitarias

- Framework: **pytest** (31 pruebas).
- Cubren: cada tipo de empleado, cada regla de bono/beneficio, cada
  validación, las calculadoras de deducciones/beneficios y la orquestación
  del procesador (incluida la red de seguridad del neto negativo).
- Uso de *doubles* (doble `CalculadoraDeducciones` excesiva) para forzar
  caminos de error inalcanzables con las tasas reales.

```bash
python -m pytest
```

## Control de versiones (Git)

Commits atómicos que cuentan la historia del proyecto:

| Commit | Propósito |
|--------|-----------|
| `chore: ...` | Estructura, configuración y `.gitignore` |
| `feat(models): ...` | Modelo de dominio de empleados |
| `feat(services): ...` | Deducciones, beneficios y procesador |
| `test: ...` | Suite de pruebas unitarias |
| `docs: ...` | Metodología y README |

## Posibles mejoras futuras (backlog)

- Persistencia de empleados y periodos de pago (repositorios + BD).
- Reportes en PDF/XML y exportación a planilla.
- Múltiples periodos (quincenal, semanal) parametrizados.
- Interfaz web o CLI interactiva para el área de talento humano.
