from flask import Blueprint, request, jsonify
from src.partidos import service

partidos_bp = Blueprint("partidos", __name__)


@partidos_bp.route("/partidos", methods=["POST"])
def crear_partido():
    data = request.get_json()

    try:
        nuevo_id = service.crear_partido(data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({"id": nuevo_id}), 201


@partidos_bp.route("/partidos", methods=["GET"])
def get_partidos():
    equipo = request.args.get("equipo")
    fecha = request.args.get("fecha")
    fase = request.args.get("fase")
    limit = int(request.args.get("limit", 10))
    offset = int(request.args.get("offset", 0))

    partidos, total = service.get_partidos(equipo=equipo, fecha=fecha, fase=fase, limit=limit, offset=offset)

    base = "/partidos?"
    filtros = ""
    if equipo:
        filtros += f"equipo={equipo}&"
    if fecha:
        filtros += f"fecha={fecha}&"
    if fase:
        filtros += f"fase={fase}&"

    last_offset = max(0, total - limit)

    return jsonify({
        "partidos": partidos,
        "total": total,
        "_first": f"{base}{filtros}limit={limit}&offset=0",
        "_prev":  f"{base}{filtros}limit={limit}&offset={max(0, offset - limit)}",
        "_next":  f"{base}{filtros}limit={limit}&offset={min(offset + limit, last_offset)}",
        "_last":  f"{base}{filtros}limit={limit}&offset={last_offset}"
    }), 200


@partidos_bp.route("/partidos/<int:partido_id>", methods=["GET"])
def detalle_partido(partido_id):
    partido = service.get_partido_by_id(partido_id)
    
    if partido is None:
        return jsonify({"error": "Partido no encontrado"}), 404
    
    return jsonify(partido), 200

@partidos_bp.route("/partidos/<int:partido_id>", methods=["DELETE"])
def eliminar_partido(partido_id):
    try:
        service.eliminar_partido(partido_id)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

    return jsonify({"mensaje": "Partido eliminado exitosamente"}), 200


@partidos_bp.route('/partidos/<int:partido_id>/resultado', methods=['PUT'])
def actualizar_resultado(partido_id):
    datos_resultado = request.get_json()

    if datos_resultado is None or not datos_resultado:
        return jsonify({"Bad Request": "No se enviaron los datos para actualizar el resultado"}), 400
    if "local" not in datos_resultado or "visitante" not in datos_resultado:
        return jsonify({"Bad Request": "Los campos 'local' y 'visitante' son requeridos"}), 400
    
    try:
        service.actualizar_resultado(partido_id, datos_resultado)
    except ValueError as e:
        return jsonify({"Bad Request": str(e)}), 400
    except LookupError as e:
        return jsonify({"Not Found": str(e)}), 404
    except Exception:
        return jsonify({"Internal Server Error": "Error interno del servidor"}), 500

    return "", 204


@partidos_bp.route('/partidos/<int:partido_id>', methods=['PUT'])
def reemplazar_partido(partido_id):
    data = request.get_json()

    try:
        service.reemplazar_partido(partido_id, data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except LookupError as e:
        return jsonify({"error": str(e)}), 404

    return jsonify({"mensaje": "Partido actualizado exitosamente"}), 200


@partidos_bp.route('/partidos/<int:id_partido>', methods=['PATCH'])
def actualizar_datos(id_partido):
    datos_a_actualizar = request.get_json()

    if not datos_a_actualizar:
        return jsonify({"error": "No se enviaron los datos para actualizar"}), 400
    
    resultado, status_code = service.actualizar_partido_parcial(id_partido, datos_a_actualizar)

    return jsonify(resultado), status_code


@partidos_bp.route('/partidos/<int:partido_id>/prediccion', methods=['POST'])
def predeccion_partido(partido_id):
    datos = request.get_json()

    if not datos or datos is None:
        return jsonify({"error": "No se enviaron datos"}), 400
    if "local" not in datos or "visitante" not in datos or "id_usuario" not in datos:
        return jsonify({"Bad Request": "Los campos 'local', 'visitante' y 'partido_id' son requeridos"}), 400

    try:
        service.predecir_partido(partido_id, datos)
    except ValueError as e:
        return jsonify({"Bad Request": str(e)}), 400
    except LookupError as e:
        return jsonify({"Not Found": str(e)}), 404
    except NotImplementedError:
        return jsonify({"Conflict":"No se puede predecir el mismo partido 2 veces"}), 409
    except Exception:
        return jsonify({"Internal Server Error": "Error interno del servidor"}), 500
    
    return jsonify({"Created": "La prediccion ha sido creada... Mucha Suerte!!"}), 201
