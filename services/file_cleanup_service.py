import os
from utils.log_config import setup_logger

logger = setup_logger()

def delete_file(file_path):
    """
    Elimina un archivo si existe.
    
    :param file_path: Ruta completa del archivo a eliminar.
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Archivo eliminado: {file_path}")
        else:
            logger.warning(f"El archivo no existe: {file_path}")
    except Exception as e:
        logger.error(f"Error al eliminar el archivo {file_path}: {e}")

def cleanup_exports_folder(export_folder='exports'):
    """
    Elimina todos los archivos en la carpeta de exportación.
    
    :param export_folder: Carpeta donde se encuentran los archivos exportados.
    """
    try:
        if os.path.exists(export_folder):
            for file_name in os.listdir(export_folder):
                file_path = os.path.join(export_folder, file_name)
                delete_file(file_path)
            logger.info(f"Carpeta '{export_folder}' limpiada exitosamente.")
        else:
            logger.warning(f"La carpeta '{export_folder}' no existe.")
    except Exception as e:
        logger.error(f"Error al limpiar la carpeta '{export_folder}': {e}")
