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
