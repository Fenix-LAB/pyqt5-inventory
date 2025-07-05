#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json

class ExcelSetup:
    """
    Clase para configurar y crear las hojas de Google Sheets
    basada en la estructura del script_db.sql
    """
    def __init__(self):
        self.credentials_file = 'credentials.json'
        self.spreadsheet_name = 'inventario_perfumeria'
        self.credentials = None
        self.client = None
        self.spreadsheet = None
        
    def setup_credentials(self, email=None, password=None):
        """
        Configurar las credenciales para Google Sheets
        En un caso real, usarías un archivo de credenciales JSON
        Para este ejemplo usaremos un placeholder
        """
        # PLACEHOLDER: Reemplaza esto con el archivo de credenciales real
        credentials_dict = {
            "type": "service_account",
            "project_id": "your-project-id",
            "private_key_id": "your-private-key-id",
            "private_key": "-----BEGIN PRIVATE KEY-----\nYour Private Key Here\n-----END PRIVATE KEY-----\n",
            "client_email": email if email else "your-service-account@your-project-id.iam.gserviceaccount.com",
            "client_id": "your-client-id",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project-id.iam.gserviceaccount.com"
        }
        
        # En un entorno real, esto se cargaría desde un archivo de credenciales
        if not os.path.exists(self.credentials_file):
            with open(self.credentials_file, 'w') as f:
                json.dump(credentials_dict, f)
            print(f"Se ha creado un archivo placeholder de credenciales en {self.credentials_file}")
            print("Por favor, reemplaza este archivo con tus credenciales reales de Google API")
        
        scope = ['https://spreadsheets.google.com/feeds', 
                'https://www.googleapis.com/auth/drive']
        
        try:
            self.credentials = ServiceAccountCredentials.from_json_keyfile_name(
                self.credentials_file, scope)
            self.client = gspread.authorize(self.credentials)
            return True
        except Exception as e:
            print(f"Error al configurar credenciales: {e}")
            return False
            
    def create_spreadsheet(self):
        """
        Crear la hoja de cálculo si no existe
        """
        try:
            # Intenta abrir una hoja existente
            try:
                self.spreadsheet = self.client.open(self.spreadsheet_name)
                print(f"Hoja de cálculo '{self.spreadsheet_name}' abierta correctamente")
            except gspread.SpreadsheetNotFound:
                # Si no existe, crea una nueva
                self.spreadsheet = self.client.create(self.spreadsheet_name)
                print(f"Hoja de cálculo '{self.spreadsheet_name}' creada correctamente")
                
            # Compartir la hoja (opcional)
            # self.spreadsheet.share('alguien@example.com', perm_type='user', role='writer')
                
            return True
        except Exception as e:
            print(f"Error al crear/abrir hoja de cálculo: {e}")
            return False
            
    def parse_sql_file(self, sql_file):
        """
        Analizar el archivo SQL para extraer la estructura de las tablas
        """
        table_structures = {}
        
        try:
            with open(sql_file, 'r') as f:
                sql_content = f.read()
                
            # Buscar todas las definiciones de tablas
            table_pattern = r"CREATE TABLE IF NOT EXISTS `db_perfumeria`\.`(.*?)`\s*\((.*?)(?:\n\)[^;]*;)"
            table_matches = re.findall(table_pattern, sql_content, re.DOTALL)
            
            for table_name, columns_text in table_matches:
                # Extraer las columnas y sus tipos
                column_pattern = r"`([^`]*)`\s+([^,\n]*)"
                column_matches = re.findall(column_pattern, columns_text)
                
                columns = []
                for col_name, col_type in column_matches:
                    # Ignorar líneas que no son definiciones de columnas
                    if not col_name.startswith('CONSTRAINT') and not col_name.startswith('PRIMARY KEY') and not col_name.startswith('INDEX'):
                        columns.append(col_name)
                
                table_structures[table_name] = columns
                
            return table_structures
            
        except Exception as e:
            print(f"Error al analizar el archivo SQL: {e}")
            return {}
            
    def create_sheets_from_sql(self, sql_file):
        """
        Crear hojas en Google Sheets basadas en la estructura SQL
        """
        table_structures = self.parse_sql_file(sql_file)
        
        if not table_structures:
            print("No se pudieron extraer estructuras de tablas del archivo SQL")
            return False
            
        for table_name, columns in table_structures.items():
            try:
                # Intentar abrir la hoja si existe
                try:
                    worksheet = self.spreadsheet.worksheet(table_name)
                    print(f"Hoja '{table_name}' ya existe, actualizando encabezados")
                    # Actualizar encabezados si es necesario
                    worksheet.update('A1', [columns])
                except gspread.exceptions.WorksheetNotFound:
                    # Crear nueva hoja si no existe
                    worksheet = self.spreadsheet.add_worksheet(title=table_name, rows=100, cols=len(columns))
                    print(f"Hoja '{table_name}' creada correctamente")
                    # Añadir encabezados
                    worksheet.update('A1', [columns])
                    
            except Exception as e:
                print(f"Error al crear/actualizar hoja '{table_name}': {e}")
                
        return True

def main():
    """
    Función principal para ejecutar la configuración
    """
    print("Configurando conexión a Google Sheets...")
    setup = ExcelSetup()
    
    # Solicitar credenciales (en un entorno real)
    # email = input("Ingrese su correo electrónico de Google: ")
    # password = input("Ingrese su contraseña: ")
    
    # Para este ejemplo, usamos valores predeterminados
    if setup.setup_credentials():
        print("Credenciales configuradas correctamente")
        
        if setup.create_spreadsheet():
            print("Hoja de cálculo configurada correctamente")
            
            sql_file = os.path.join(os.path.dirname(__file__), 'script_db.sql')
            if os.path.exists(sql_file):
                print(f"Creando hojas basadas en la estructura de {sql_file}")
                if setup.create_sheets_from_sql(sql_file):
                    print("¡Todas las hojas se han creado correctamente!")
                else:
                    print("Error al crear las hojas en Google Sheets")
            else:
                print(f"El archivo {sql_file} no existe")
        else:
            print("Error al configurar la hoja de cálculo")
    else:
        print("Error al configurar las credenciales")

if __name__ == "__main__":
    main()
