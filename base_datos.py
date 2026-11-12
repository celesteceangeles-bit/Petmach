
import sqlite3


NOMBRE_BASE = "petmatch.db"


def conectar():
    conexion = sqlite3.connect(NOMBRE_BASE)

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS solicitudes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_adoptante TEXT NOT NULL,
            mascota TEXT NOT NULL,
            motivo TEXT NOT NULL,
            estado TEXT NOT NULL DEFAULT 'Pendiente'
        )
    """)

    columnas = conexion.execute(
        "PRAGMA table_info(solicitudes)"
    ).fetchall()

    nombres_columnas = [columna[1] for columna in columnas]

    if "email_adoptante" not in nombres_columnas:
        conexion.execute(
            "ALTER TABLE solicitudes ADD COLUMN email_adoptante TEXT"
        )

    conexion.commit()
    return conexion


def crear_tabla_mensajes():
    conexion = conectar()

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS mensajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_solicitud INTEGER NOT NULL,
            mensaje TEXT NOT NULL,
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
            enviado_email INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (id_solicitud)
                REFERENCES solicitudes(id)
        )
    """)

    conexion.commit()
    conexion.close()


def guardar_solicitud(
    nombre_adoptante,
    mascota,
    motivo,
    email_adoptante=None
):
    conexion = conectar()

    cursor = conexion.execute(
        """
        INSERT INTO solicitudes (
            nombre_adoptante,
            mascota,
            motivo,
            email_adoptante
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            nombre_adoptante.strip(),
            mascota,
            motivo.strip(),
            email_adoptante.strip() if email_adoptante else None
        )
    )

    id_solicitud = cursor.lastrowid

    conexion.commit()
    conexion.close()

    return id_solicitud


def obtener_solicitudes():
    conexion = conectar()

    cursor = conexion.execute("""
        SELECT
            id,
            nombre_adoptante,
            mascota,
            motivo,
            estado,
            email_adoptante
        FROM solicitudes
        ORDER BY id DESC
    """)

    solicitudes = cursor.fetchall()
    conexion.close()

    return solicitudes


def obtener_solicitud_por_id(id_solicitud):
    conexion = conectar()

    cursor = conexion.execute(
        """
        SELECT
            id,
            nombre_adoptante,
            mascota,
            motivo,
            estado,
            email_adoptante
        FROM solicitudes
        WHERE id = ?
        """,
        (id_solicitud,)
    )

    solicitud = cursor.fetchone()
    conexion.close()

    return solicitud


def consultar_estado_solicitud(id_solicitud, email):
    conexion = conectar()

    cursor = conexion.execute(
        """
        SELECT id, mascota, estado
        FROM solicitudes
        WHERE id = ?
          AND LOWER(TRIM(email_adoptante)) = LOWER(TRIM(?))
        """,
        (id_solicitud, email)
    )

    solicitud = cursor.fetchone()
    conexion.close()

    return solicitud


def actualizar_estado(id_solicitud, nuevo_estado):
    estados_validos = [
        "Pendiente",
        "Aprobada",
        "Rechazada"
    ]

    if nuevo_estado not in estados_validos:
        return False

    conexion = conectar()

    cursor = conexion.execute(
        """
        UPDATE solicitudes
        SET estado = ?
        WHERE id = ?
        """,
        (nuevo_estado, id_solicitud)
    )

    conexion.commit()
    actualizado = cursor.rowcount > 0
    conexion.close()

    return actualizado


def guardar_mensaje(id_solicitud, mensaje):
    conexion = conectar()

    cursor = conexion.execute(
        """
        INSERT INTO mensajes (id_solicitud, mensaje)
        SELECT id, ?
        FROM solicitudes
        WHERE id = ?
        """,
        (mensaje.strip(), id_solicitud)
    )

    conexion.commit()
    guardado = cursor.rowcount > 0
    conexion.close()

    return guardado


def obtener_mensajes(id_solicitud):
    conexion = conectar()

    cursor = conexion.execute(
        """
        SELECT id, mensaje, fecha, enviado_email
        FROM mensajes
        WHERE id_solicitud = ?
        ORDER BY id DESC
        """,
        (id_solicitud,)
    )

    mensajes = cursor.fetchall()
    conexion.close()

    return mensajes


def marcar_mensaje_enviado(id_mensaje):
    conexion = conectar()

    cursor = conexion.execute(
        """
        UPDATE mensajes
        SET enviado_email = 1
        WHERE id = ?
        """,
        (id_mensaje,)
    )

    conexion.commit()
    actualizado = cursor.rowcount > 0
    conexion.close()

    return actualizado
