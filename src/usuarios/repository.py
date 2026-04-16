import mysql.connector
from config import DB_CONFIG


def crear_usuario(nombre, email):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO usuarios (nombre, email) VALUES (%s, %s)", (nombre, email)
        )
        conn.commit()
        nuevo_id = cursor.lastrowid
        return nuevo_id
    # manejamos el error del email duplicado
    except mysql.connector.errors.IntegrityError:
        return "conflict"
    finally:
        cursor.close()
        conn.close()


def get_usuarios(limit, offset):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) as total FROM usuarios")
    total = cursor.fetchone()["total"]

    cursor.execute(
        "SELECT id, nombre FROM usuarios LIMIT %s OFFSET %s", (limit, offset)
    )
    usuarios = cursor.fetchall()

    cursor.close()
    conn.close()
    return usuarios, total


def get_usuario_id(id):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    return usuario


def actualizar_usuario(id, nombre, email):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE usuarios SET nombre = %s, email = %s WHERE id = %s",
            (nombre, email, id),
        )
        conn.commit()
        return cursor.rowcount

    # manejamos el error del email duplicado
    except mysql.connector.errors.IntegrityError:
        return "conflict"
    finally:
        cursor.close()
        conn.close()


def eliminar_usuario(id):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
    conn.commit()
    afectadas = cursor.rowcount
    cursor.close()
    conn.close()
