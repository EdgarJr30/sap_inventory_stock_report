import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from utils.log_config import setup_logger

logger = setup_logger()

def send_email(subject, body, to_emails, from_email, smtp_server, smtp_port, email_password, attachment_paths=None):
    """
     Envía un correo con uno o más archivos adjuntos a uno o varios destinatarios.

    :param subject: Asunto del correo.
    :param body: Cuerpo del mensaje.
    :param to_emails: Lista de direcciones de correo del destinatario.
    :param from_email: Dirección de correo del remitente.
    :param smtp_server: Servidor SMTP.
    :param smtp_port: Puerto SMTP.
    :param email_password: Contraseña del correo del remitente.
    :param attachment_paths: Lista de rutas de archivos adjuntos (puede ser una sola ruta o una lista).
    """
    try:
        # Crear el mensaje de correo
        message = MIMEMultipart()
        message['From'] = from_email
        message['To'] = ", ".join(to_emails)  # Combinar múltiples destinatarios
        message['Subject'] = subject

        # Adjuntar el cuerpo del mensaje
        message.attach(MIMEText(body, 'plain'))
        
        # Si attachment_paths es una cadena, convertirlo a una lista
        if isinstance(attachment_paths, str):
            attachment_paths = [attachment_paths]

        # Adjuntar múltiples archivos
        if attachment_paths:
            for attachment_path in attachment_paths:
                if os.path.exists(attachment_path):
                    with open(attachment_path, 'rb') as attachment_file:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment_file.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename={os.path.basename(attachment_path)}'
                        )
                        message.attach(part)
                else:
                    logger.warning(f"Archivo adjunto no encontrado: {attachment_path}")

        # Configurar el servidor SMTP y enviar el correo
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, email_password)
        server.sendmail(from_email, to_emails, message.as_string())  # Enviar a varios destinatarios
        server.quit()

        logger.info(f"Correo enviado exitosamente a {', '.join(to_emails)}.")

    except Exception as e:
        logger.error(f"Error al enviar el correo: {e}")
        raise