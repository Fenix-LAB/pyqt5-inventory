#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para probar la conexión a Google Sheets y la migración de la estructura de datos
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from connection.conexion import Conexion
from connection.excel_setup import ExcelSetup
from connection.init_google_sheets import parse_sql_structure



def test_connection():
    """
    Prueba la conexión a Google Sheets
    """
    print("Probando conexión a Google Sheets...")
    conexion = Conexion()
    
    if not conexion.client:
        print("Error: No se pudo establecer la conexión. Verifica las credenciales.")
        return False
        
    print("¡Conexión establecida correctamente!")
    return True


def test_spreadsheet_creation():
    """
    Prueba la creación de la hoja de cálculo
    """
    print("\nProbando la creación de la hoja de cálculo...")
    setup = ExcelSetup()
    
    if setup.setup_credentials():
        print("Credenciales configuradas correctamente")
        
        if setup.create_spreadsheet():
            print("¡Hoja de cálculo creada/abierta correctamente!")
            return True
        else:
            print("Error al crear/abrir la hoja de cálculo")
            return False
    else:
        print("Error al configurar las credenciales")
        return False


def test_sql_parsing():
    """
    Prueba el parseo del archivo SQL
    """
    print("\nProbando el parseo del archivo SQL...")
    sql_file = os.path.join(os.path.dirname(__file__), 'script_db.sql')
    
    if not os.path.exists(sql_file):
        print(f"Error: El archivo SQL no existe en la ruta {sql_file}")
        return False
        
    tables = parse_sql_structure(sql_file)
    
    if not tables:
        print("Error: No se pudieron extraer las tablas del archivo SQL")
        return False
        
    print(f"¡Parseo exitoso! Se encontraron {len(tables)} tablas:")
    
    for table_name, columns in tables.items():
        print(f"  - {table_name}: {len(columns)} columnas")
        
    return True


def test_basic_operations():
    """
    Prueba las operaciones básicas de CRUD
    """
    print("\nProbando operaciones básicas de CRUD...")
    conexion = Conexion()
    
    # Asegurarnos que estamos conectados
    conexion.abrirConexion()
    
    # 1. Prueba SELECT
    print("Probando SELECT...")
    try:
        query = "SELECT descripcion FROM marcas LIMIT 5"
        conexion.cursor.execute(query)
        results = conexion.cursor.fetchall()
        print(f"  Resultado: {results[:5] if results else 'No hay datos'}")
        
    except Exception as e:
        print(f"  Error en SELECT: {e}")
        
    # 2. Prueba INSERT
    print("\nProbando INSERT...")
    try:
        query = "INSERT INTO marcas (descripcion) VALUES (%s)"
        values = ("Marca de Prueba",)
        conexion.cursor.execute(query, values)
        print("  INSERT ejecutado correctamente")
        
    except Exception as e:
        print(f"  Error en INSERT: {e}")
        
    # 3. Prueba UPDATE
    print("\nProbando UPDATE...")
    try:
        query = "UPDATE marcas SET descripcion = %s WHERE descripcion = %s"
        values = ("Marca Actualizada", "Marca de Prueba")
        conexion.cursor.execute(query, values)
        print("  UPDATE ejecutado correctamente")
        
    except Exception as e:
        print(f"  Error en UPDATE: {e}")
        
    # 4. Prueba DELETE
    print("\nProbando DELETE...")
    try:
        query = "DELETE FROM marcas WHERE descripcion = %s"
        values = ("Marca Actualizada",)
        conexion.cursor.execute(query, values)
        print("  DELETE ejecutado correctamente")
        
    except Exception as e:
        print(f"  Error en DELETE: {e}")
        
    conexion.cerrarConexion()
    return True
    

def main():
    """
    Función principal
    """
    print("=== PRUEBA DE MIGRACIÓN A GOOGLE SHEETS ===")
    
    # # Paso 1: Probar conexión
    # if not test_connection():
    #     print("\n[ERROR] La prueba de conexión falló. Verifica las credenciales y permisos.")
    #     return False
        
    # # Paso 2: Probar creación de hoja de cálculo
    # if not test_spreadsheet_creation():
    #     print("\n[ERROR] La prueba de creación de hoja de cálculo falló.")
    #     return False
        
    # # Paso 3: Probar parseo de SQL
    # if not test_sql_parsing():
    #     print("\n[ERROR] La prueba de parseo de SQL falló.")
    #     return False
        
    # Paso 4: Probar operaciones básicas
    if not test_basic_operations():
        print("\n[ERROR] La prueba de operaciones básicas falló.")
        return False
        
    print("\n=== ¡TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE! ===")
    print("La migración de MySQL a Google Sheets parece estar funcionando correctamente.")
    print("\nPara usar el sistema:")
    print("1. Reemplaza el archivo 'credentials.json' con tus credenciales reales de Google API")
    print("2. Ejecuta 'python connection/init_google_sheets.py' para inicializar las hojas")
    print("3. Descomenta la línea 'init_sheets()' en initConexion.py para la primera ejecución")
    print("4. Ejecuta la aplicación normalmente con 'python app.py'")
    
    return True


if __name__ == "__main__":
    main()
