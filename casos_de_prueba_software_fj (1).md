# Casos de prueba – Software FJ
**Proyecto:** Sistema Integral de Gestión de Clientes, Servicios y Reservas  
**Repositorio:** https://github.com/esquivelpachecoluisabel-boop/software-fj-fase-4  
**Archivo revisado:** `main.py`  
**Responsable de documentación:** Samuel Gallego  
**Estado:** Casos documentados; resultados pendientes de ejecución y verificación.

> Importante: los resultados esperados se derivan de la lectura del código actual. Deben ejecutarse en Python y completar la columna “Resultado observado” antes de afirmar que las pruebas fueron aprobadas.

## Casos de prueba

| N.º | Operación / datos de entrada | Resultado esperado | Resultado observado |
|---:|---|---|---|
| 1 | Crear cliente `C001`, Ana Pérez, `ana@gmail.com`, teléfono `3001234567`, y registrarlo. | Cliente creado y agregado a la lista del sistema. | Pendiente de ejecutar. |
| 2 | Crear cliente `C002` con nombre vacío. | Se genera `DatosInvalidosError` porque el nombre debe tener al menos 2 caracteres. | Pendiente de ejecutar. |
| 3 | Crear y registrar cliente `C003`, Carlos Gómez, `carlos@gmail.com`, teléfono `3107654321`. | Cliente creado y agregado correctamente. | Pendiente de ejecutar. |
| 4 | Crear y registrar sala `S001`, “Sala de reuniones”, tarifa de $50.000 por hora. | Servicio registrado y descripción de la sala mostrada. | Pendiente de ejecutar. |
| 5 | Crear y registrar equipo `E001`, “Proyector”, tarifa de $35.000 por día. | Servicio registrado y descripción del equipo mostrada. | Pendiente de ejecutar. |
| 6 | Crear y registrar asesoría `A001`, “Asesoría en programación”, tarifa de $80.000 por sesión. | Servicio registrado y descripción de la asesoría mostrada. | Pendiente de ejecutar. |
| 7 | Intentar crear sala `S002`, “Sala inválida”, con tarifa cero. | Se genera `DatosInvalidosError` porque la tarifa debe ser mayor que cero. | Pendiente de ejecutar. |
| 8 | Crear reserva `R001` para Ana Pérez, sala `S001`, duración de 2 horas. | Reserva creada con estado “Pendiente”. | Pendiente de ejecutar. |
| 9 | Confirmar la reserva `R001`. | El estado cambia a “Confirmada” y el evento se registra en el log. | Pendiente de ejecutar. |
| 10 | Procesar `R001` con descuento del 10 % e impuesto del 19 %. | Cálculo: $100.000 − $10.000 = $90.000; impuesto de $17.100; total esperado $107.100. Estado “Procesada”. | Pendiente de ejecutar. |
| 11 | Intentar crear reserva `R002` con duración cero. | Se genera `ReservaError`, conservando como causa el error de validación de duración. | Pendiente de ejecutar. |
| 12 | Crear reserva `R003` para Carlos con dos sesiones de asesoría, confirmarla y cancelarla. | La reserva termina con estado “Cancelada”. | Pendiente de ejecutar. |
| 13 | Intentar procesar la reserva cancelada `R003`. | Se genera `ReservaError` porque solo se procesan reservas confirmadas. | Pendiente de ejecutar. |
| 14 | Intentar reservar el equipo `E002` configurado como no disponible. | Se genera `ReservaError` y su causa es `ServicioNoDisponibleError`. | Pendiente de ejecutar. |
| 15 | Calcular el alquiler del equipo `E001` durante 3 días. | Con tarifa de $35.000 por día, el costo esperado es $105.000. | Pendiente de ejecutar. |

## Observaciones de revisión del código

1. El archivo `main.py` ya contiene 15 operaciones de prueba mediante la función `ejecutar_operacion()`.
2. La función utiliza `try`, `except`, `else` y `finally`; además, registra los errores y la finalización de las pruebas en `software_fj.log`.
3. La clase `Reserva` valida la disponibilidad y los parámetros específicos del servicio al crear una reserva.
4. **Ajuste técnico recomendado:** el método `Servicio.calcular_costo()` valida que las unidades sean mayores que cero, pero no llama a `self.validar_parametros(unidades)`. Por eso, al calcular directamente un servicio, podrían omitirse límites específicos como máximo de 12 horas para salas, 30 días para equipos o 20 sesiones para asesorías. Se recomienda incorporar esa validación y probar los límites.
5. En el código actual, las tarifas de ejemplo son: sala $50.000 por hora, equipo $35.000 por día y asesoría $80.000 por sesión. No se deben cambiar sin acuerdo del equipo.

## Conclusión

Se identificaron y documentaron 15 casos de prueba basados en las operaciones incluidas en `main.py`. Estos casos cubren registros válidos e inválidos, creación de servicios, reservas, confirmación, cancelación, procesamiento de costos y manejo de errores. La aprobación de cada caso debe establecerse después de ejecutar el programa y comparar el resultado real con el esperado.
