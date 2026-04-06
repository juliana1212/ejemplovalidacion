from .exceptions import (
    ClienteNoEncontradoError,
    ClienteYaExisteError,
    ValidacionClienteError,
)
from .models import Cliente
from .repository import ClienteRepository


class ClienteService:
    def __init__(self, repository: ClienteRepository) -> None:
        self.repository = repository
        self._ultimo_id = 0

    def crear_cliente(self, nombre: str, email: str) -> Cliente:
        self._validar_nombre(nombre)
        self._validar_email(email)

        if self.repository.obtener_por_email(email) is not None:
            raise ClienteYaExisteError(f"Ya existe un cliente con email {email}")

        self._ultimo_id += 1
        cliente = Cliente(
            id=self._ultimo_id,
            nombre=nombre.strip(),
            email=email.strip(),
        )
        return self.repository.guardar(cliente)

    def obtener_cliente(self, cliente_id: int) -> Cliente:
        cliente = self.repository.obtener_por_id(cliente_id)
        if cliente is None:
            raise ClienteNoEncontradoError(f"No existe cliente con id {cliente_id}")
        return cliente

    def listar_clientes(self) -> list[Cliente]:
        return self.repository.listar()

    def actualizar_cliente(self, cliente_id: int, nombre: str, email: str) -> Cliente:
        cliente = self.obtener_cliente(cliente_id)

        self._validar_nombre(nombre)
        self._validar_email(email)

        existente = self.repository.obtener_por_email(email)
        if existente is not None and existente.id != cliente_id:
            raise ClienteYaExisteError(f"Ya existe un cliente con email {email}")

        cliente.nombre = nombre.strip()
        cliente.email = email.strip()
        return self.repository.guardar(cliente)

    def eliminar_cliente(self, cliente_id: int) -> bool:
        eliminado = self.repository.eliminar(cliente_id)
        if not eliminado:
            raise ClienteNoEncontradoError(f"No existe cliente con id {cliente_id}")
        return True

    @staticmethod
    def _validar_nombre(nombre: str) -> None:
        if not nombre or not nombre.strip():
            raise ValidacionClienteError("El nombre es obligatorio")

    @staticmethod
    def _validar_email(email: str) -> None:
        if not email or not email.strip():
            raise ValidacionClienteError("El email es obligatorio")
        if "@" not in email or "." not in email:
            raise ValidacionClienteError("El email no tiene un formato válido")
