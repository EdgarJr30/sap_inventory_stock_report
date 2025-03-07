import os
import json
import sys
from hdbcli import dbapi
from dotenv import load_dotenv
from queries.queries import GET_ARTICLES_NO_STOCK_PENDING_ORDERS, CEODO_VW_DST_ArtSinInv_SalesKit
from services.export_service import export_to_excel
from services.email_service import send_email
from services.file_cleanup_service import delete_file
from services.file_cleanup_service import cleanup_exports_folder
from utils.log_config import setup_logger

# Configurar el logger
logger = setup_logger()
logger.info("=========================================")
logger.info("INCIO DEL SCRIPT")
logger.info("=========================================")

# Función para obtener variables de entorno con validación
def get_env_var(key, default=None, required=True):
    value = os.getenv(key, default)
    if required and value is None:
        logger.error(f"La variable de entorno '{key}' no está definida.")
        sys.exit(1)  # Termina el programa si una variable requerida no está definida
    return value

# def main():

# Determinar la ruta base dependiendo del entorno de ejecución
if getattr(sys, 'frozen', False):
    # Si está ejecutándose como ejecutable .exe, usar la ruta real del ejecutable
    base_path = os.path.dirname(sys.executable)
else:
    # Si está en desarrollo, usar la ruta del script Python
    base_path = os.path.abspath(os.path.dirname(__file__))

# Construir la ruta del archivo .env desde el ejecutable o script
dotenv_path = os.path.join(base_path, 'utils', '.env')
logger.info(f"Intentando cargar el archivo .env desde: {dotenv_path}")

# Cargar las variables de entorno
load_dotenv(dotenv_path)

# Obtener los datos de conexión desde las variables de entorno
host = get_env_var('HOST')
port = int(get_env_var('PORT', '30015'))  # Convertimos a entero después de validar
user = get_env_var('USER')
password = get_env_var('PASSWORD')
company_db = get_env_var('COMPANY_DB')

# Obtener datos de correo desde el archivo .env
email_from = get_env_var('EMAIL_FROM')
email_password = get_env_var('EMAIL_PASSWORD')
smtp_server = get_env_var('SMTP_SERVER')
smtp_port = int(get_env_var('SMTP_PORT'))

# Validar si EMAIL_RECIPIENTS está vacío o mal configurado
email_recipients_env = os.getenv('EMAIL_RECIPIENTS', '')
if not email_recipients_env:
    logger.error("La variable de entorno 'EMAIL_RECIPIENTS' no está definida o está vacía.")
    sys.exit(1)
email_recipients = [email.strip() for email in email_recipients_env.split(',') if email.strip()]
# Validar que al menos haya un destinatario válido
if not email_recipients:
    logger.error("No se encontraron destinatarios válidos en 'EMAIL_RECIPIENTS'.")
    sys.exit(1)
    
admin_email_env = os.getenv('ADMIN_EMAIL', '')
# Validar que el correo sea válido
if not admin_email_env:
    logger.error("La variable de entorno 'ADMIN_EMAIL' no está definida o está vacía.")
    sys.exit(1)
admin_email = [email.strip() for email in admin_email_env.split(',') if email.strip()]
# Validar que al menos haya un destinatario válido
if not admin_email:
    logger.error("No se encontraron destinatarios válidos en 'ADMIN_EMAIL'.")
    sys.exit(1)

logger.info("Archivo .env cargado correctamente.")

try:
    logger.info("Iniciando conexión a SAP HANA...")
    connection = dbapi.connect(
        address=host,
        port=port,
        user=user,
        password=password
    )
    logger.info("Conexión exitosa a SAP HANA.")

    # Cambiar al esquema o base de datos que necesitas
    cursor = connection.cursor()
    cursor.execute(f'SET SCHEMA "{company_db}"')
    logger.info(f"Conectado al esquema '{company_db}'.")

    # Ejecutar el query
    logger.info("Ejecutando el query para obtener articulos sin stock y ordenes pendientes...")
    cursor.execute(GET_ARTICLES_NO_STOCK_PENDING_ORDERS)
    results = cursor.fetchall()
    
    logger.info("Ejecutando el query para obtener datos del SalesKit sin inventario...")
    cursor.execute(CEODO_VW_DST_ArtSinInv_SalesKit)
    saleskit_results = cursor.fetchall()

    # Mostrar los resultados
    for row in results:
        print(row)
        logger.info(row)
        
    for row in saleskit_results:
        print(row)
        logger.info(row)

    if results or saleskit_results:
        logger.info("Query's ejecutado con exito.")
        logger.info(f"Exportando {len(results)} registros a Excel, del query GET_ARTICLES_NO_STOCK_PENDING_ORDERS")
        logger.info(f"Exportando {len(saleskit_results)} registros a Excel, del query CEODO_VW_DST_ArtSinInv_SalesKit")
        export_file_path_1, filtered_file_path_1 = export_to_excel(results, base_file_name='articles_no_stock_pending_orders.xlsx')
        export_file_path_2, filtered_file_path_2 = export_to_excel(saleskit_results, base_file_name='saleskit_no_stock.xlsx')

        # Enviar el archivo por correo
        logger.info("Enviando los archivos por correo...")
        send_email(
            subject="Reporte automatizado DST Artículos sin inventario y órdenes pendientes",
            body="Se adjunta el reporte automatizado de DST Artículos sin inventario y órdenes pendientes.",
            to_emails=email_recipients,
            attachment_paths=[export_file_path_1, filtered_file_path_1, export_file_path_2, filtered_file_path_2],
            from_email=email_from,
            smtp_server=smtp_server,
            smtp_port=smtp_port,
            email_password=email_password
        )

        # Eliminar el archivo exportado
        logger.info("Eliminando los archivos exportados...")
        delete_file(export_file_path_1)
        delete_file(filtered_file_path_1)
        delete_file(export_file_path_2)
        delete_file(filtered_file_path_2)
        
        # Limpiar todos los archivos del folder completo
        cleanup_exports_folder()
    else:
        logger.warning("No se encontraron resultados para exportar.")
        # Enviar notificación de contingencia al administrador
        logger.info("Enviando notificación de contingencia al administrador y usuarios.")
        logger.info(f"Enviando correo al administrador: {admin_email}")
        logger.info(f"Enviando correo a los usuarios: {email_recipients}")
        
        try:
            contingency_message = (
                "No se encontraron resultados en el reporte automatizado de DST Artículos sin inventario y órdenes pendientes. "
                "Esto podría indicar una posible contingencia en la base de datos. Se requiere una revisión."
            )

            # Correo al administrador
            send_email(
                subject="Alerta de contingencia en el reporte de artículos sin inventario",
                body=contingency_message,
                to_emails=admin_email,
                from_email=email_from,
                smtp_server=smtp_server,
                smtp_port=smtp_port,
                email_password=email_password
            )
        except Exception as e:
            logger.error(f"Error al enviar el correo al administrador: {e}", exc_info=True)
            
        try:
            # Correo de notificación a los usuarios
            send_email(
                subject="Error en el reporte DST Artículos sin inventario y órdenes pendientes",
                body="Se ha presentando una contingencia en el reporte DST Artículos sin inventario y órdenes pendientes, por lo que no se encontraron resultados en el reporte. Nuestro equipo está revisando el problema.",
                to_emails=email_recipients,
                from_email=email_from,
                smtp_server=smtp_server,
                smtp_port=smtp_port,
                email_password=email_password
            )
        except Exception as e:
            logger.error(f"Error al enviar el correo a los usuarios: {e}", exc_info=True)
                
    # Cerrar la conexión
    cursor.close()
    connection.close()
    logger.info("Conexión cerrada correctamente.")
    logger.info("=========================================")

except dbapi.Error as e:
    logger.error(f"Error al conectar o ejecutar la consulta: {e}", exc_info=True)
except Exception as e:
    logger.error(f"Ocurrió un error inesperado: {e}", exc_info=True)
    
logger.info("=========================================")
logger.info("FIN DEL SCRIPT")
logger.info("=========================================")

# if __name__ == "__main__":
#     try:
#         main()
#     except Exception as e:
#         logger.critical(f"Error crítico: {e}", exc_info=True)
#     finally:
#         input("Presione Enter para salir...")

