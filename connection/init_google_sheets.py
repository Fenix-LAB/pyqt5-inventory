#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def parse_sql_structure(sql_file):
    """
    Parse el archivo SQL para extraer la estructura de tablas y crear hojas de Excel
    """
    tables = {}
    
    try:
        with open(sql_file, 'r') as f:
            sql_content = f.read()

        print("Analizando el archivo SQL para extraer la estructura de tablas...")
            
        # Buscar todas las definiciones de tablas
        table_pattern = r"CREATE TABLE IF NOT EXISTS `db_perfumeria`\.`(\w+)`\s*\(([\s\S]*?)(?:PRIMARY KEY|CONSTRAINT|ENGINE)"
        table_matches = re.findall(table_pattern, sql_content, re.DOTALL)

        print(f"Se encontraron {len(table_matches)} tablas en el archivo SQL.")
        
        for table_name, columns_text in table_matches:
            print(f"Procesando tabla: {table_name}")
            # Extraer las columnas y sus tipos
            column_pattern = r"`([^`]*)`\s+([^,\n]*)"
            column_matches = re.findall(column_pattern, columns_text)
            
            columns = []
            for col_name, col_type in column_matches:
                print(f"  Columna: {col_name} - Tipo: {col_type.strip()}")
                # Ignorar líneas que no son definiciones de columnas
                if not col_name.startswith('CONSTRAINT') and not col_name.startswith('PRIMARY KEY') and not col_name.startswith('INDEX'):
                    columns.append({
                        'name': col_name,
                        'type': col_type.strip()
                    })
            
            tables[table_name] = columns

        print("Estructura de tablas extraída correctamente.")
        return tables

    except Exception as e:
        print(f"Error al analizar el archivo SQL: {e}")
        return {}

def main():
    """
    Función principal para inicializar las hojas de cálculo
    """
    # from connection.conexion import Conexions
    from connection.excel_setup import ExcelSetup
    
    # Ruta al archivo SQL
    sql_file = os.path.join(os.path.dirname(__file__), 'script_db.sql')
    
    if not os.path.exists(sql_file):
        print(f"El archivo SQL no existe en la ruta: {sql_file}")
        return False
    
    print("Archivo SQL encontrado, procediendo a analizar la estructura de tablas...")
        
    # Parsear la estructura de tablas
    tables = parse_sql_structure(sql_file)
    
    if not tables:
        print("No se pudieron extraer las tablas del archivo SQL")
        return False
        
    # Configurar la conexión a Google Sheets
    print("Inicializando la conexión a Google Sheets...")
    setup = ExcelSetup()
    
    # Solicitar credenciales (esto usaría valores predeterminados en un entorno real)
    if setup.setup_credentials():
        print("Credenciales configuradas correctamente")
        
        if setup.create_spreadsheet():
            print("Hoja de cálculo configurada correctamente")
            
            print("Creando hojas basadas en la estructura SQL...")
            if setup.create_sheets_from_sql(sql_file):
                print("¡Todas las hojas se han creado correctamente!")

                # Obtener y mostrar la URL de la hoja de cálculo
                # url = setup.get_spreadsheet_url()
                # print("\n============================================================")
                # print(f"ACCESO A LA HOJA DE CÁLCULO: {url}")
                # print("============================================================\n")
                
                # Mostrar resumen de las tablas creadas
                print("\nResumen de la estructura de la base de datos:")
                for table_name, columns in tables.items():
                    print(f"\nTabla: {table_name}")
                    print("-" * (len(table_name) + 7))
                    for column in columns:
                        print(f"  {column['name']} ({column['type']})")
                
                return True
            else:
                print("Error al crear las hojas en Google Sheets")
                return False
        else:
            print("Error al configurar la hoja de cálculo")
            return False
    else:
        print("Error al configurar las credenciales")
        return False

if __name__ == "__main__":
    main()
