import os
import smtplib
import ssl
from email.message import EmailMessage

from dotenv import load_dotenv

# Carga las credenciales desde el archivo .env del proyecto.
load_dotenv()


def enviar_correo(destinatario, asunto, mensaje):
    """
    Envía un correo mediante Gmail.
    Devuelve (True, mensaje) si se envía correctamente,
    o (False, mensaje de error) si falla.
    """
    correo_emisor = os.getenv("PETMATCH_GMAIL")
    contrasena = os.getenv("PETMATCH_APP_PASSWORD")

    if not correo_emisor or not contrasena:
        return False, (
            "Faltan las credenciales de Gmail. "
            "Revisa el archivo .env."
        )

    if not destinatario or not destinatario.strip():
        return False, "Esta solicitud no tiene un correo de destino."

    email = EmailMessage()
    email["From"] = correo_emisor
    email["To"] = destinatario.strip()
    email["Subject"] = asunto
    email.set_content(mensaje)

    contexto = ssl.create_default_context()

    try:
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as servidor:
            servidor.ehlo()
            servidor.starttls(context=contexto)
            servidor.ehlo()
            servidor.login(correo_emisor, contrasena)
            servidor.send_message(email)

        return True, "Correo enviado correctamente."

    except smtplib.SMTPAuthenticationError:
        return False, (
            "Gmail rechazó la autenticación. Revisa que el correo "
            "y la contraseña de aplicación estén bien escritos."
        )
    except (smtplib.SMTPException, OSError):
        return False, (
            "No se pudo conectar con Gmail o completar el envío. "
            "Revisa tu conexión y la configuración de la cuenta."
        )
