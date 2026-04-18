from src.partidos import repository


def crear_partido(data):
    campos_requeridos = ["equipo_local", "equipo_visitante", "fecha", "fase"]
    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            raise ValueError(f"El campo '{campo}' es requerido")

    nuevo_id = repository.crear_partido(
        equipo_local=data["equipo_local"],
        equipo_visitante=data["equipo_visitante"],
        estadio=data.get("estadio"),
        ciudad=data.get("ciudad"),
        fecha=data["fecha"],
        fase=data["fase"]
    )

    return nuevo_id


def get_partidos(equipo=None, fecha=None, fase=None, limit=10, offset=0):
    return repository.get_partidos(equipo=equipo, fecha=fecha, fase=fase, limit=limit, offset=offset)


def actualizar_resultado(partido_id, data):
    if data is None:
        raise ValueError("No se enviaron los datos para actualizar el resultado")

    for campo in ["local", "visitante"]:
        if campo not in data:
            raise ValueError(f"El campo '{campo}' es requerido")

    goles_local = data["local"]
    goles_visitante = data["visitante"]

    if not isinstance(goles_local, int) or not isinstance(goles_visitante, int):
        raise ValueError("Los goles deben ser valores enteros")
    if goles_local < 0 or goles_visitante < 0:
        raise ValueError("Los goles no pueden ser negativos")

    actualizar_resultado = repository.actualizar_resultado(partido_id, goles_local, goles_visitante)
    if not actualizar_resultado:
        raise LookupError("Partido no encontrado")


def eliminar_partido(partido_id):
    eliminado = repository.eliminar_partido(partido_id)
    if not eliminado:
        raise ValueError("Partido no encontrado")

def actualizar_partido_parcial(id_partido, datos):
    exito = repository.actualizar_partido_parcial(id_partido, datos)
    if exito:
        return {"mensaje": "Partido actualizado con éxito"}, 200
    else:
        return {"error": "No se pudo actualizar. El partido no existe o hubo un problema en la base de datos"}, 404

def predecir_partido(id_partido, datos):
    
    goles_local = datos["local"]
    goles_visitante = datos["visitante"]
    id_usuario = datos["id_usuario"]

    if not isinstance(goles_local, int) or not isinstance(goles_visitante, int):
        raise ValueError("Los goles deben ser valores enteros")
    if goles_local < 0 or goles_visitante < 0:
        raise ValueError("Los goles no pueden ser negativos")
    if not isinstance(id_usuario, int):
        raise ValueError("La id de usuario es un entero positivo")
    
    prediccion = repository.guardar_prediccion(id_partido, id_usuario, goles_local, goles_visitante)
    if prediccion == 1:
        raise LookupError("Partido inexistente")
    elif prediccion == 2:
        raise LookupError("Usuario inexistente")
    
    return True 
