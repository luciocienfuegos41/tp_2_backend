from flask import Blueprint, request, jsonify
from src.usuarios import service

usuarios_bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")


def error(codigo, mensaje, descipcion, codigo_estatus):
    return (
        jsonify(
            {
                "errors": [
                    {
                        "code": codigo,
                        "message": mensaje,
                        "level": "error",
                        "description": descipcion,
                    }
                ]
            }
        ),
        codigo_estatus,
    )


@usuarios_bp.route("", methods=["POST"])
def post_usuario():
    data = request.get_json()
    nombre = data.get("nombre")
    email = data.get("email")

    if not nombre or not email:
        return error("400", "bad request", "nombre y email son requeridos", 400)

    resultado = service.crear_usuario(nombre, email)
    if resultado == "conflict":
        return error("409", "Conflict", "El email ya está registrado", 409)

    return "", 201


@usuarios_bp.route("", methods=["GET"])
def get_usuarios():
    limit = request.args.get("_limit", 10, type=int)
    offset = request.args.get("_offset", 0, type=int)

    usuarios, total = service.get_usuarios(limit, offset)

    if not usuarios:
        return "", 204

    base_url = "/usuarios"
    return (
        jsonify(
            {
                "usuarios": usuarios,
                "_links": {
                    "_first": {"href": f"{base_url}?_limit={limit}&_offset=0"},
                    "_prev": (
                        {
                            "href": f"{base_url}?_limit={limit}&_offset={max(0, offset - limit)}"
                        }
                        if offset > 0
                        else None
                    ),
                    "_next": (
                        {"href": f"{base_url}?_limit={limit}&_offset={offset + limit}"}
                        if offset + limit < total
                        else None
                    ),
                    "_last": {
                        "href": f"{base_url}?_limit={limit}&_offset={max(0, total - limit)}"
                    },
                },
            }
        ),
        200,
    )


@usuarios_bp.route("/<int:id>", methods=["GET"])
def get_usuario(id):
    usuario = service.get_usuario_id(id)
    if not usuario:
        return error("404", "Not Found", f"Usuario {id} no encontrado", 404)
    return jsonify(usuario), 200


@usuarios_bp.route("/<int:id>", methods=["PUT"])
def put_usuario(id):
    data = request.get_json()
    nombre = data.get("nombre")
    email = data.get("email")

    if not nombre or not email:
        return error("400", "Bad Request", "nombre y email son requeridos", 400)

    resultado = service.actualizar_usuario(id, nombre, email)
    if resultado == "conflict":
        return error("409", "Conflict", "El email ya está registrado", 409)

    return "", 204


@usuarios_bp.route("/<int:id>", methods=["DELETE"])
def delete_usuario(id):
    usuario = service.get_usuario_id(id)
    if not usuario:
        return error("404", "Not Found", f"Usuario {id} no encontrado", 404)

    service.eliminar_usuario(id)
    return "", 204

