from flask import Blueprint, request, jsonify
from src.usuarios import service

ranking_bp = Blueprint("ranking", __name__)


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


@ranking_bp.route("/ranking", methods=["GET"])
def get_ranking():
    limit = request.args.get("_limit", 10, type=int)
    offset = request.args.get("_offset", 0, type=int)

    ranking, total = service.get_ranking(limit, offset)

    if not ranking:
        return "", 204

    base_url = "/ranking"
    return (
        jsonify(
            {
                "ranking": ranking,
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
