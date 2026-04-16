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


@partidos_bp.route("/partidos/<int:partido_id>", methods=["DELETE"])
def eliminar_partido(partido_id):
    try:
        service.eliminar_partido(partido_id)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

    return jsonify({"mensaje": "Partido eliminado exitosamente"}), 200
