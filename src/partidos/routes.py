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

    partidos = service.get_partidos(equipo=equipo, fecha=fecha, fase=fase)
    return jsonify(partidos), 200


@partidos_bp.route("/partidos/<int:partido_id>", methods=["DELETE"])
def eliminar_partido(partido_id):
    try:
        service.eliminar_partido(partido_id)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

    return jsonify({"mensaje": "Partido eliminado exitosamente"}), 200

@partidos_bp.route('/partidos/<int:partido_id>/resultado', methods=['PUT']) 
def actualizar_resultado(partido_id): datos_resultado = request.get_json() 
if datos_resultado is None or not datos_resultado: 
    return jsonify({"No Content": "No se enviaron los datos para actualizar el resultado"}), 400 
if "local" not in datos_resultado or "visitante" not in datos_resultado: 
    return jsonify({"Bad Request": "Los campos 'local' y 'visitante' son requeridos"}), 400 
try: service.actualizar_resultado(partido_id, datos_resultado) 
except ValueError as e: 
    return jsonify({"error": str(e)}), 400 
except LookupError as e: 
    return jsonify({"error": str(e)}), 404 
except Exception: 
    return jsonify({"error": "Error interno del servidor"}), 500 
return "", 204

@partidos_bp.route('/partidos/<int:id_partido>', methods=['PATCH'])
def actualizar_datos(id_partido):
    datos_a_actualizar = request.get_json()

    if not datos_a_actualizar:
        return jsonify({"error": "No se enviaron los datos para actualizar"}), 400
    
    resultado, status_code = actualizar_partido_parcial(id_partidon datos_a_actualizar)

    return jsonify(resultado), status_code

