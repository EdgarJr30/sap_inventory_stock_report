import logging
import os
from datetime import datetime

# Configuración del logger
def setup_logger(log_file='application.log', log_folder='logs'):
    # Crear la carpeta de logs si no existe
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    # Generar un nombre de archivo con timestamp
    timestamp = datetime.now().strftime('%Y%m%d')
    full_log_path = os.path.join(log_folder, f"{timestamp}_{log_file}")

    # Configurar el logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(full_log_path),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)
