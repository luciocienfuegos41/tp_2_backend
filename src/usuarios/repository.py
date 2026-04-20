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


def get_ranking(limit, offset):
    """
    Calcula el ranking de usuarios basado en sus predicciones correctas.
    - 3 puntos: resultado exacto
    - 1 punto: ganador correcto
    - 0 puntos: falló
    """
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)

    # SQL que calcula los puntos de cada usuario
    sql = """
    SELECT 
        u.id as id_usuario,
        u.nombre,
        SUM(
            CASE 
                WHEN p.goles_local = pa.goles_local AND p.goles_visitante = pa.goles_visitante THEN 3
                WHEN (
                    (p.goles_local > p.goles_visitante AND pa.goles_local > pa.goles_visitante) OR
                    (p.goles_local < p.goles_visitante AND pa.goles_local < pa.goles_visitante) OR
                    (p.goles_local = p.goles_visitante AND pa.goles_local = pa.goles_visitante)
                ) THEN 1
                ELSE 0
            END
        ) as puntos
    FROM usuarios u
    LEFT JOIN prediccion p ON u.id = p.id_usuario
    LEFT JOIN partidos pa ON p.id_partido = pa.id
    WHERE pa.goles_local IS NOT NULL AND pa.goles_visitante IS NOT NULL
    GROUP BY u.id, u.nombre
    ORDER BY puntos DESC
    """

    cursor.execute(sql)
    ranking = cursor.fetchall()

    # Contar total de usuarios para links
    cursor.execute("SELECT COUNT(*) as total FROM usuarios")
    total = cursor.fetchone()["total"]

    cursor.close()
    conn.close()

    return ranking, total
