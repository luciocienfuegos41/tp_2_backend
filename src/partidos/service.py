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


def get_partidos(equipo=None, fecha=None, fase=None):
    return repository.get_partidos(equipo=equipo, fecha=fecha, fase=fase)
