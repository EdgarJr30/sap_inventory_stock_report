# SAP Inventory Stock Report

Este proyecto es una aplicación de consola desarrollada en Python para conectarse a SAP HANA mediante el Service Layer, ejecutar una consulta SQL específica, exportar los resultados a un archivo Excel, enviar dicho archivo por correo electrónico y limpiar automáticamente los archivos generados.

El reporte que genera la aplicación se basa en **artículos sin inventario** y **órdenes pendientes**, utilizando datos almacenados en SAP HANA.

---

## **Objetivo del Proyecto**
Automatizar la generación, exportación y distribución de reportes relacionados con inventario y órdenes pendientes en SAP HANA, mejorando la eficiencia operativa y reduciendo errores manuales en la distribución de información.

---

## **Requisitos Previos**
Asegúrate de tener instalados los siguientes componentes antes de ejecutar el proyecto:

- **Python 3.11** o superior
- **Pip** (gestor de paquetes de Python)
- Dependencias del proyecto instaladas (ver `requirements.txt`)
- Acceso a una base de datos SAP HANA
- Configuración SMTP válida para el envío de correos
- Archivo `.env` con las variables de configuración necesarias

---

## **Configuración del Proyecto**

### **1. Clonar el Repositorio**
Clona el repositorio del proyecto desde tu fuente de control:

```bash
git clone https://github.com/edgarjr30/sap_inventory_stock_report.git
cd sap_inventory_stock_report
```

### **2. Crear y Configurar el Archivo .env**
En el directorio utils, crea un archivo .env con el siguiente contenido:

# Configuración de conexión a SAP HANA
HOST=tu_servidor_sap
PORT=30015
USER=tu_usuario_sap
PASSWORD=tu_contraseña_sap
COMPANY_DB=nombre_base_datos

# Configuración de correo electrónico
EMAIL_FROM=tu_correo@ejemplo.com
EMAIL_PASSWORD=tu_contraseña_correo
SMTP_SERVER=smtp.office365.com
SMTP_PORT=587
EMAIL_RECIPIENTS=destinatario1@example.com,destinatario2@example.com

HOST: Dirección del servidor de SAP HANA.
PORT: Puerto de conexión (predeterminado: 30015).
EMAIL_RECIPIENTS: Lista de destinatarios separados por comas.

### **3. Instalar Dependencias**
Ejecuta el siguiente comando para instalar las dependencias del proyecto:

```bash
pip install -r requirements.txt
```

### **4. Ejecutar el Proyecto**
Para ejecutar el proyecto en modo desarrollo, utiliza el siguiente comando:

```bash
python main.py
```

Para ejecutar en MAC
```bash
python3 main.py
```

El proyecto generará un archivo Excel con los resultados del reporte y lo enviará a los destinatarios configurados en el .env.



📜 Aviso de Copyright y Confidencialidad
© CILM, 2025. Todos los derechos reservados.

Este proyecto es propiedad exclusiva de CILM. Está estrictamente prohibido copiar, reproducir, distribuir o modificar este proyecto sin autorización previa por escrito.

Contacto
Para consultas o soporte relacionado con este proyecto, por favor comunícate con:

📧 eperez@cilm.do
📞 809-467-4032