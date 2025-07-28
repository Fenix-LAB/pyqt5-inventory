# Migración de Google Sheets a Excel

Este documento explica los cambios realizados para migrar el proyecto de Google Sheets a Excel tradicional.

## Cambios Realizados

### 1. Dependencias Actualizadas

Se actualizó el archivo `requirements.txt`:
- ❌ Eliminado: `gspread`, `oauth2client` (Google Sheets)
- ✅ Agregado: `openpyxl` (manejo de archivos Excel)
- ✅ Mantenido: `pandas`, `PyQt5`, `reportlab`

### 2. Clase Conexion Migrada

La clase `Conexion` en `/connection/conexion.py` fue completamente reescrita:

#### Antes (Google Sheets):
- Conexión a Google Sheets API
- Autenticación con credenciales JSON
- Manejo de hojas online

#### Ahora (Excel):
- Manejo de archivos Excel locales (.xlsx)
- Sin necesidad de autenticación
- Operaciones offline completas

### 3. Funcionalidades Mantenidas

✅ **Compatibilidad**: Todos los métodos existentes mantienen la misma interfaz
✅ **Consultas SQL**: Simulación de SELECT, INSERT, UPDATE, DELETE
✅ **Métodos de conexión**: `abrirConexion()`, `cerrarConexion()`, etc.
✅ **Resultados**: `fetchall()`, `fetchone()`, `commit()`

### 4. Nuevas Características

🆕 **Archivo local**: `inventario.xlsx` se crea automáticamente
🆕 **Múltiples hojas**: Soporte para todas las tablas del sistema
🆕 **Cache DataFrame**: Mejor rendimiento con pandas
🆕 **Backup automático**: Se guarda automáticamente después de cada operación

## Estructura del Archivo Excel

El archivo `inventario.xlsx` contiene las siguientes hojas:

- **productos**: id, nombre, marca, categoria, precio, stock, descripcion
- **categorias**: id, nombre, descripcion  
- **clientes**: id, nombre, apellido, email, telefono, direccion
- **proveedores**: id, nombre, contacto, telefono, email, direccion
- **usuarios**: id, username, password, email, rol, activo
- **marcas**: id, nombre, descripcion
- **rubros**: id, nombre, descripcion
- **ventas**: id, producto_id, cantidad, fecha, total
- **transacciones**: id, tipo, cliente_id, producto_id, cantidad, precio, fecha, total
- **pagos**: id, transaccion_id, monto, metodo_pago, fecha, estado

## Instalación y Uso

### 1. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 2. Ejecutar Migración (Opcional)
```bash
python migrate_to_excel.py
```

### 3. Ejecutar la Aplicación
```bash
python app.py
```

El archivo Excel se creará automáticamente la primera vez que ejecutes la aplicación.

## Migración de Datos Existentes

Si tienes datos en Google Sheets y quieres migrarlos:

### Opción 1: Manual
1. Abre tu Google Sheet
2. Descarga cada hoja como CSV (Archivo > Descargar > CSV)
3. Usa el script `convert_csv_to_excel.py`:
   ```python
   from convert_csv_to_excel import convert_csv_to_excel_sheet
   convert_csv_to_excel_sheet('productos.csv', 'productos')
   convert_csv_to_excel_sheet('clientes.csv', 'clientes')
   # etc...
   ```

### Opción 2: Automática
Si necesitas una migración automática desde Google Sheets, puedes:
1. Temporalmente instalar las dependencias antiguas
2. Ejecutar un script que lea de Google Sheets y escriba a Excel
3. Luego desinstalar las dependencias de Google Sheets

## Ventajas de la Migración

✅ **Sin dependencias externas**: No necesitas credenciales de Google
✅ **Trabajo offline**: Funciona sin conexión a internet
✅ **Mejor rendimiento**: Operaciones más rápidas en archivos locales
✅ **Fácil backup**: Solo necesitas respaldar un archivo .xlsx
✅ **Interoperabilidad**: Excel es universalmente compatible
✅ **Sin límites de API**: No hay restricciones de cuota o velocidad

## Archivos de Respaldo

- `conexion_backup.py`: Respaldo de la implementación original con Google Sheets
- `credentials.json`: Ya no es necesario (puedes eliminarlo)

## Troubleshooting

### Error: "Import openpyxl could not be resolved"
```bash
pip install openpyxl
```

### Error: "No such file or directory: inventario.xlsx"
El archivo se crea automáticamente. Si hay problemas, ejecuta:
```bash
python migrate_to_excel.py
```

### Los datos no se guardan
Verifica que tienes permisos de escritura en el directorio del proyecto.

### Performance lento
Para grandes cantidades de datos, considera usar chunks o procesar por lotes.

## Próximos Pasos Sugeridos

1. **Indexación**: Agregar índices en columnas frecuentemente consultadas
2. **Validación**: Implementar validación de datos en las hojas
3. **Sincronización**: Si necesitas colaboración, considera usar SharePoint o OneDrive
4. **Backup automático**: Implementar backup automático periódico
5. **Compresión**: Para archivos grandes, considerar compresión

## Soporte

Si encuentras algún problema con la migración:
1. Revisa este README
2. Verifica que todas las dependencias estén instaladas
3. Comprueba los permisos de archivo
4. Consulta los logs de error en la aplicación
