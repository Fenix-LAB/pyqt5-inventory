# Migración de MySQL a Google Sheets

Este documento explica el proceso de migración del sistema de inventario desde MySQL a Google Sheets.

## Descripción

La aplicación originalmente utilizaba MySQL como base de datos. Se ha migrado a Google Sheets para facilitar el acceso y la colaboración en la nube, eliminando la necesidad de un servidor de base de datos.

## Estructura

Cada tabla de la base de datos MySQL se ha convertido en una hoja dentro de un documento de Google Sheets:
- Cada tabla = 1 hoja de cálculo
- Primera fila = nombres de columnas
- Filas siguientes = registros

## Requisitos

- Python 3.7 o superior
- PyQt5
- gspread
- oauth2client
- pandas

Puedes instalar las dependencias con:
```
pip install -r requirements.txt
```

## Configuración

### 1. Credenciales de Google API

Para usar Google Sheets, necesitas credenciales de Google API:

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto
3. Habilita las APIs de Google Sheets y Google Drive
4. Crea una cuenta de servicio y descarga el archivo de credenciales JSON
5. Renombra el archivo a `credentials.json` y colócalo en la carpeta `connection/`

### 2. Inicializar las hojas de cálculo

Para crear la estructura de hojas basada en la base de datos original:

```
python connection/init_google_sheets.py
```

Este script creará un documento de Google Sheets llamado "inventario_perfumeria" con una hoja para cada tabla.

## Cambios realizados

- `conexion.py`: Reemplazado completamente para conectar con Google Sheets en lugar de MySQL
- Todas las clases de conexión: Actualizadas para usar la nueva implementación de Google Sheets
- Nuevo archivo `excel_setup.py`: Proporciona funcionalidades para configurar las hojas de cálculo
- Nuevo archivo `init_google_sheets.py`: Crea la estructura de hojas basada en script_db.sql
- Nuevo archivo `test_sheets_migration.py`: Prueba la conexión y las operaciones básicas

## Uso

1. Asegúrate de tener el archivo `credentials.json` correctamente configurado
2. Ejecuta `python connection/init_google_sheets.py` para inicializar la estructura
3. Ejecuta la aplicación normalmente con `python app.py`

## Consideraciones

- El rendimiento puede ser más lento que con MySQL para grandes conjuntos de datos
- Las consultas complejas se han simplificado para adaptarse a las limitaciones de Google Sheets
- Se mantiene la misma interfaz de la aplicación y los mismos métodos en las clases de conexión

## Solución de problemas

- Si hay problemas de conexión, verifica que el archivo `credentials.json` sea válido
- Si hay problemas de permisos, asegúrate de que la cuenta de servicio tenga acceso al documento
- Para depurar, ejecuta `python connection/test_sheets_migration.py`
