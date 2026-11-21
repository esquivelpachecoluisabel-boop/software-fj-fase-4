
"""
PROYECTO: SOFTWARE FJ
Sistema Integral de Gestión de Clientes, Servicios y Reservas
UNAD - Programación
"""

from abc import ABC, abstractmethod
import logging

# ARCHIVO DE REGISTRO
logging.basicConfig(
    filename="software_fj.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)


# EXCEPCIONES PERSONALIZADAS
class ErrorSistema(Exception):
    pass


class DatosInvalidosError(ErrorSistema):
    pass


class ServicioNoDisponibleError(ErrorSistema):
    pass


class ReservaError(ErrorSistema):
    pass


# CLASE ABSTRACTA ENTIDAD
class Entidad(ABC):

    def __init__(self, identificador):
        if not isinstance(identificador, str) or not identificador.strip():
            raise DatosInvalidosError("El identificador no puede estar vacío.")

        self._identificador = identificador.strip()

    @property
    def identificador(self):
        return self._identificador

    @abstractmethod
    def describir(self):
        pass


# CLASE CLIENTE
class Cliente(Entidad):

    def __init__(self, identificador, nombre, correo, telefono):
        super().__init__(identificador)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or len(valor.strip()) < 2:
            raise DatosInvalidosError(
                "El nombre debe tener al menos 2 caracteres."
            )
        self.__nombre = valor.strip().title()

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if not isinstance(valor, str) or "@" not in valor or "." not in valor.split("@")[-1]:
            raise DatosInvalidosError("El correo no es válido.")
        self.__correo = valor.strip().lower()

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        texto = str(valor).strip()
        if not texto.isdigit() or len(texto) < 7:
            raise DatosInvalidosError("El teléfono debe tener al menos 7 dígitos.")
        self.__telefono = texto

    def describir(self):
        return (
            f"Cliente: {self.nombre} | "
            f"Correo: {self.correo} | Teléfono: {self.telefono}"
        )


# CLASE ABSTRACTA SERVICIO
class Servicio(Entidad, ABC):

    def __init__(self, identificador, nombre, tarifa, disponible=True):
        super().__init__(identificador)

        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidosError("El nombre del servicio es obligatorio.")

        if not isinstance(tarifa, (int, float)) or tarifa <= 0:
            raise DatosInvalidosError("La tarifa debe ser mayor que cero.")

        self.nombre = nombre.strip()
        self.tarifa = float(tarifa)
        self.disponible = bool(disponible)

    def validar_disponibilidad(self):
        if not self.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio {self.nombre} no está disponible."
            )

    def calcular_costo(self, unidades=1, descuento=0, impuesto=0):
        self.validar_disponibilidad()

        if not isinstance(unidades, (int, float)) or unidades <= 0:
            raise DatosInvalidosError("La cantidad debe ser mayor que cero.")

        if not 0 <= descuento <= 100:
            raise DatosInvalidosError("Descuento inválido.")

        if not 0 <= impuesto <= 100:
            raise DatosInvalidosError("Impuesto inválido.")

        subtotal = self.tarifa * unidades
        valor_descuento = subtotal * descuento / 100
        base = subtotal - valor_descuento
        total = base + (base * impuesto / 100)

        return round(total, 2)

    @abstractmethod
    def describir(self):
        pass

    @abstractmethod
    def validar_parametros(self, unidades):
        pass


# SERVICIO DE SALAS
class ServicioSala(Servicio):

    def validar_parametros(self, unidades):
        if not isinstance(unidades, (int, float)) or unidades <= 0 or unidades > 12:
            raise DatosInvalidosError("La sala debe reservarse entre 1 y 12 horas.")

    def describir(self):
        return f"Sala: {self.nombre} - ${self.tarifa} por hora"


# SERVICIO DE EQUIPOS
class ServicioEquipo(Servicio):

    def validar_parametros(self, unidades):
        if not isinstance(unidades, int) or unidades <= 0 or unidades > 30:
            raise DatosInvalidosError("El alquiler debe ser de 1 a 30 días.")

    def describir(self):
        return f"Equipo: {self.nombre} - ${self.tarifa} por día"


# SERVICIO DE ASESORÍAS
class ServicioAsesoria(Servicio):

    def validar_parametros(self, unidades):
        if not isinstance(unidades, int) or unidades <= 0 or unidades > 20:
            raise DatosInvalidosError("La asesoría debe tener entre 1 y 20 sesiones.")

    def describir(self):
        return f"Asesoría: {self.nombre} - ${self.tarifa} por sesión"


# CLASE RESERVA
class Reserva(Entidad):

    def __init__(self, identificador, cliente, servicio, duracion):
        super().__init__(identificador)

        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("Se requiere un cliente válido.")

        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("Se requiere un servicio válido.")

        try:
            servicio.validar_disponibilidad()
            servicio.validar_parametros(duracion)

        except (DatosInvalidosError, ServicioNoDisponibleError) as error:
            raise ReservaError(
                "No fue posible crear la reserva."
            ) from error

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"
        self.costo = None

    def describir(self):
        return (
            f"Reserva {self.identificador} | "
            f"Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | "
            f"Estado: {self.estado}"
        )

    def confirmar(self):
        if self.estado != "Pendiente":
            raise ReservaError("Solo se confirman reservas pendientes.")

        self.servicio.validar_disponibilidad()
        self.estado = "Confirmada"
        logging.info("Reserva %s confirmada.", self.identificador)

    def cancelar(self):
        if self.estado not in ("Pendiente", "Confirmada"):
            raise ReservaError("No se puede cancelar una reserva procesada.")

        self.estado = "Cancelada"
        logging.info("Reserva %s cancelada.", self.identificador)

    def procesar(self, descuento=0, impuesto=0):
        if self.estado != "Confirmada":
            raise ReservaError(
                "La reserva debe estar confirmada antes de procesarse."
            )

        self.costo = self.servicio.calcular_costo(
            self.duracion,
            descuento=descuento,
            impuesto=impuesto
        )

        self.estado = "Procesada"

        logging.info(
            "Reserva %s procesada. Total: $%.2f",
            self.identificador,
            self.costo
        )

        return self.costo


# SISTEMA DE GESTIÓN
class SistemaSoftwareFJ:

    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrar_cliente(self, cliente):
        if any(c.identificador == cliente.identificador for c in self.clientes):
            raise DatosInvalidosError("El cliente ya existe.")

        self.clientes.append(cliente)
        logging.info("Cliente registrado: %s", cliente.nombre)
        return cliente

    def registrar_servicio(self, servicio):
        if any(s.identificador == servicio.identificador for s in self.servicios):
            raise DatosInvalidosError("El servicio ya existe.")

        self.servicios.append(servicio)
        logging.info("Servicio registrado: %s", servicio.nombre)
        return servicio

    def crear_reserva(self, reserva):
        if any(r.identificador == reserva.identificador for r in self.reservas):
            raise ReservaError("La reserva ya existe.")

        self.reservas.append(reserva)
        logging.info("Reserva creada: %s", reserva.identificador)
        return reserva


# FUNCIÓN PARA EJECUTAR Y CONTROLAR LAS PRUEBAS
def ejecutar_operacion(numero, descripcion, funcion):

    print(f"\nPRUEBA {numero}: {descripcion}")

    try:
        resultado = funcion()

    except Exception as error:
        print(f"ERROR CONTROLADO: {error}")
        logging.exception("Error en prueba %s", numero)

    else:
        if resultado is not None:
            print(resultado)

        print("Resultado: operación ejecutada correctamente.")

    finally:
        print("Fin de la operación.")
        logging.info("Finalizó la prueba %s", numero)


# PROGRAMA PRINCIPAL
def main():

    sistema = SistemaSoftwareFJ()

    print("=" * 60)
    print("SISTEMA INTEGRAL DE GESTIÓN - SOFTWARE FJ")
    print("=" * 60)

    cliente_1 = None
    cliente_2 = None
    reserva_1 = None
    reserva_2 = None

    # PRUEBA 1: REGISTRO DE CLIENTE
    def prueba_1():
        nonlocal cliente_1

        cliente_1 = Cliente(
            "C001", "Ana Pérez", "ana@gmail.com", "3001234567"
        )

        sistema.registrar_cliente(cliente_1)
        return cliente_1.describir()

    ejecutar_operacion(1, "Registrar cliente válido", prueba_1)

    # PRUEBA 2: CLIENTE INVÁLIDO
    ejecutar_operacion(
        2,
        "Registrar cliente con nombre vacío",
        lambda: Cliente("C002", "", "invalido@gmail.com", "3001234567")
    )

    # PRUEBA 3: OTRO CLIENTE
    def prueba_3():
        nonlocal cliente_2

        cliente_2 = Cliente(
            "C003", "Carlos Gómez", "carlos@gmail.com", "3107654321"
        )

        sistema.registrar_cliente(cliente_2)
        return cliente_2.describir()

    ejecutar_operacion(3, "Registrar segundo cliente", prueba_3)

    # PRUEBA 4: CREAR SALA
    sala = ServicioSala("S001", "Sala de reuniones", 50000)

    ejecutar_operacion(
        4,
        "Registrar servicio de sala",
        lambda: sistema.registrar_servicio(sala).describir()
    )

    # PRUEBA 5: CREAR EQUIPO
    equipo = ServicioEquipo("E001", "Proyector", 35000)

    ejecutar_operacion(
        5,
        "Registrar servicio de equipo",
        lambda: sistema.registrar_servicio(equipo).describir()
    )

    # PRUEBA 6: CREAR ASESORÍA
    asesoria = ServicioAsesoria(
        "A001", "Asesoría en programación", 80000
    )

    ejecutar_operacion(
        6,
        "Registrar servicio de asesoría",
        lambda: sistema.registrar_servicio(asesoria).describir()
    )

    # PRUEBA 7: SERVICIO INVÁLIDO
    ejecutar_operacion(
        7,
        "Crear servicio con tarifa cero",
        lambda: ServicioSala("S002", "Sala inválida", 0)
    )

    # PRUEBA 8: CREAR RESERVA
    def prueba_8():
        nonlocal reserva_1

        reserva_1 = Reserva("R001", cliente_1, sala, 2)
        sistema.crear_reserva(reserva_1)

        return reserva_1.describir()

    ejecutar_operacion(8, "Crear reserva válida", prueba_8)

    # PRUEBA 9: CONFIRMAR RESERVA
    ejecutar_operacion(
        9,
        "Confirmar reserva R001",
        lambda: (reserva_1.confirmar(), reserva_1.describir())[1]
    )

    # PRUEBA 10: PROCESAR RESERVA
    ejecutar_operacion(
        10,
        "Procesar reserva con descuento e impuesto",
        lambda: (
            f"Costo final: ${reserva_1.procesar(descuento=10, impuesto=19):.2f}"
        )
    )

    # PRUEBA 11: RESERVA CON DURACIÓN CERO
    ejecutar_operacion(
        11,
        "Crear reserva con duración cero",
        lambda: Reserva("R002", cliente_2, sala, 0)
    )

    # PRUEBA 12: CREAR Y CANCELAR RESERVA
    def prueba_12():
        nonlocal reserva_2

        reserva_2 = Reserva("R003", cliente_2, asesoria, 2)
        sistema.crear_reserva(reserva_2)
        reserva_2.confirmar()
        reserva_2.cancelar()

        return reserva_2.describir()

    ejecutar_operacion(12, "Crear y cancelar reserva", prueba_12)

    # PRUEBA 13: PROCESAR RESERVA CANCELADA
    ejecutar_operacion(
        13,
        "Procesar reserva cancelada",
        lambda: reserva_2.procesar()
    )

    # PRUEBA 14: SERVICIO NO DISPONIBLE
    servicio_no_disponible = ServicioEquipo(
        "E002", "Computador portátil", 60000, disponible=False
    )

    ejecutar_operacion(
        14,
        "Reservar servicio no disponible",
        lambda: Reserva("R004", cliente_1, servicio_no_disponible, 1)
    )

    # PRUEBA 15: CALCULAR COSTO DE EQUIPO
    ejecutar_operacion(
        15,
        "Calcular alquiler de equipo por tres días",
        lambda: f"Costo: ${equipo.calcular_costo(3):.2f}"
    )

    # RESUMEN FINAL
    print("\n" + "=" * 60)
    print("RESUMEN DEL SISTEMA")
    print(f"Clientes registrados: {len(sistema.clientes)}")
    print(f"Servicios registrados: {len(sistema.servicios)}")
    print(f"Reservas registradas: {len(sistema.reservas)}")
    print("Se ejecutaron 15 pruebas.")
    print("Consulte el archivo software_fj.log.")
    print("=" * 60)


if __name__ == "__main__":
    main()
