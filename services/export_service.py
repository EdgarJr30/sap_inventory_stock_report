import pandas as pd
import os
from datetime import datetime
from utils.log_config import setup_logger

logger = setup_logger()

def export_to_excel(data, base_file_name, export_folder='exports'):
    """
    Exporta los resultados del query a dos archivos Excel.
    
    1. El primer archivo contiene los datos completos sin modificaciones.
    2. El segundo archivo contiene los datos agrupados, filtrados y calculados con una columna de cantidad ordenada al inicio,
       una columna vacía titulada "Total", y el almacén al final.

    :param data: Lista de resultados del query.
    :param file_name: Nombre del archivo de salida.
    :param export_folder: Carpeta donde se guardará el archivo.
    :return: Ruta completa de ambos archivos exportados.
    """
    
    try:
        # Crear la carpeta de exportación si no existe
        if not os.path.exists(export_folder):
            os.makedirs(export_folder)

        # Generar un nombre de archivo con timestamp para evitar duplicados
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        full_file_path = os.path.join(export_folder, f"{timestamp}_{base_file_name}")
        filtered_file_path = os.path.join(export_folder, f"{timestamp}_filtered_{base_file_name}")
        
        # Definir los nombres de las columnas
        column_names = [
            "Fecha de la orden", "ID interno de la orden", "Ticket", "Artículo padre",
            "Artículo hijo", "Descripción", "Cantidad Ordenada", "En stock",
            "Comprometido", "Pedido", "Disponible", "Almacén", "Error"
        ]
        
        # # Verificar que haya datos antes de crear el DataFrame
        # if not data:
        #     logger.warning(f"No hay datos para exportar en '{base_file_name}'. Se omite la exportacion.")
        #     return None, None

        # Convertir los resultados a un DataFrame de pandas
        df = pd.DataFrame(data, columns=column_names)

        # Exportar el primer archivo con los datos sin modificar
        df.to_excel(full_file_path, index=False)
        logger.info(f"Archivo completo exportado exitosamente a '{full_file_path}'.")

        # Agrupar los datos por "Artículo hijo", "Descripción" y "Almacén"
        df_grouped = (
            df.groupby(["Artículo hijo", "Descripción", "Almacén"], as_index=False)
            .agg({"Cantidad Ordenada": "sum"})
        )
        
        # Renombrar columnas
        df_grouped.rename(columns={"Artículo hijo": "Número de Artículo"}, inplace=True)
        df_grouped.rename(columns={"Descripción": "Descripción del artículo"}, inplace=True)
        df_grouped.rename(columns={"Cantidad Ordenada": "Cantidad"}, inplace=True)

        # Crear columnas vacías para el archivo filtrado
        df_grouped["Precio por unidad"] = ""
        df_grouped["Total"] = ""

        # Reordenar las columnas: "Cantidad Ordenada", "Total" (vacía), "Almacén"
        df_filtered = df_grouped[["Número de Artículo", "Descripción del artículo", "Cantidad", "Precio por unidad", "Total", "Almacén"]]

        # Exportar el archivo filtrado
        df_filtered.to_excel(filtered_file_path, index=False)
        logger.info(f"Archivo filtrado exportado exitosamente a '{filtered_file_path}'.")

        # Retornar las rutas completas de ambos archivos generados
        return full_file_path, filtered_file_path

    except Exception as e:
        logger.error(f"Error al exportar los resultados a Excel: {e}")
        raise