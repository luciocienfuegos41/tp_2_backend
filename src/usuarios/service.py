from src.usuarios import repository


def crear_usuario(nombre, email):
    return repository.crear_usuario(nombre, email)


def get_usuarios(limit, offset):
    return repository.get_usuarios(limit, offset)


def get_usuario_id(id):
    return repository.get_usuario_id(id)


def actualizar_usuario(id, nombre, email):
    return repository.actualizar_usuario(id, nombre, email)


def eliminar_usuario(id):
    return repository.eliminar_usuario(id)
