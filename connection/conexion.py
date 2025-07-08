#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os
import json
import re

class Conexion(object):
    '''
    Clase para manejar la conexión a Google Sheets
    '''

    def __init__(self):
        self.credentials_file = 'credentials.json'
        self.spreadsheet_name = 'inventario_perfumeria'
        self.client = None
        self.spreadsheet = None
        self.worksheet = None
        self.cursor = None
        self.db = self  # Para compatibilidad con el código existente
        self.current_data = None
        self.current_headers = None
        self.setup_credentials()

    def get_spreadsheet_url(self):
        """
        Devuelve la URL de la hoja de cálculo actual.
        """
        try:
            # Si no hay una conexión activa, intentamos conectar primero
            if not self.spreadsheet:
                self.conectar()
                
            # Si después de conectar aún no tenemos spreadsheet, algo falló
            if not self.spreadsheet:
                print("No se pudo obtener la hoja de cálculo")
                return None
                
            # En Google Sheets, la URL de la hoja se construye con el ID
            spreadsheet_id = self.spreadsheet.id
            url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}"
            return url
        except Exception as e:
            print(f"Error al obtener URL de la hoja de cálculo: {e}")
            return None
        
    def share_spreadsheet(self, email):
        """
        Comparte la hoja de cálculo con el email especificado
        """
        try:
            if not self.spreadsheet:
                self.conectar()
                
            if not self.spreadsheet:
                print("No se pudo obtener la hoja de cálculo")
                return False
                
            self.spreadsheet.share(email, perm_type='user', role='writer')
            print(f"Hoja compartida con {email}")
            return True
        except Exception as e:
            print(f"Error al compartir la hoja: {e}")
            return False

    def setup_credentials(self, email=None, password=None):
        """
        Configura las credenciales para acceder a Google Sheets.
        """
        # PLACEHOLDER: En un entorno real, el usuario proporcionaría credenciales válidas
        if not os.path.exists(self.credentials_file):
            print(f"AVISO: No se encontró el archivo de credenciales {self.credentials_file}")
            print("Necesitas crear un archivo de credenciales desde Google Cloud Console.")
            print("Visita: https://console.cloud.google.com/apis/credentials")
            
            # Crear un archivo placeholder (solo para este ejemplo)
            credentials_dict = {
                "type": "service_account",
                "project_id": "PLACEHOLDER-PROJECT-ID",
                "private_key_id": "PLACEHOLDER-KEY-ID",
                "private_key": "-----BEGIN PRIVATE KEY-----\nPLACEHOLDER-KEY\n-----END PRIVATE KEY-----\n",
                "client_email": email if email else "PLACEHOLDER@example.com",
                "client_id": "PLACEHOLDER-CLIENT-ID"
            }
            
            with open(self.credentials_file, 'w') as f:
                json.dump(credentials_dict, f)
                
            print(f"Se ha creado un archivo placeholder en {self.credentials_file}")
            print("Reemplázalo con tus credenciales reales para usar esta aplicación.")
        
        try:
            scope = ['https://spreadsheets.google.com/feeds', 
                    'https://www.googleapis.com/auth/drive']
            
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                self.credentials_file, scope)
                
            self.client = gspread.authorize(credentials)
        except Exception as e:
            print(f"Error al configurar credenciales: {e}")

    def conectar(self):
        """
        Conecta con la hoja de cálculo de Google Sheets
        """
        try:
            if not self.client:
                self.setup_credentials()
                
            # Intenta abrir la hoja de cálculo existente
            try:
                self.spreadsheet = self.client.open(self.spreadsheet_name)
            except gspread.SpreadsheetNotFound:
                # Si no existe, intenta crearla
                self.spreadsheet = self.client.create(self.spreadsheet_name)
                print(f"Hoja de cálculo '{self.spreadsheet_name}' creada.")
                
                # Opcional: Compartir la hoja con un usuario específico
                # self.spreadsheet.share('usuario@example.com', perm_type='user', role='writer')
        except Exception as e:
            print(f"Error al conectar con Google Sheets: {e}")

    def abrir_cursor(self):
        """
        Método de compatibilidad (no hace nada específico en Google Sheets)
        """
        self.cursor = self  # Para mantener compatibilidad con el código existente

    def cerrar_cursor(self):
        """
        Método de compatibilidad (no hace nada específico en Google Sheets)
        """
        self.cursor = None
        self.current_data = None
        self.current_headers = None

    def cerrar_conexion(self):
        """
        Método de compatibilidad (no hace nada específico en Google Sheets)
        """
        self.spreadsheet = None
        
    def abrirConexion(self):
        """
        Método para abrir la conexión a Google Sheets (mantiene la compatibilidad)
        """
        self.conectar()
        self.abrir_cursor()
    
    def cerrarConexion(self):
        """
        Método para cerrar la conexión a Google Sheets (mantiene la compatibilidad)
        """
        self.cerrar_cursor()
        self.cerrar_conexion()
    
    def select_worksheet(self, table_name):
        """
        Selecciona una hoja de trabajo específica (equivalente a una tabla en MySQL)
        """
        try:
            if not self.spreadsheet:
                self.conectar()
                
            try:
                self.worksheet = self.spreadsheet.worksheet(table_name)
                # Cargar los datos y encabezados
                self.current_headers = self.worksheet.row_values(1)
                return True
            except gspread.WorksheetNotFound:
                print(f"La hoja '{table_name}' no existe en el documento.")
                return False
        except Exception as e:
            print(f"Error al seleccionar hoja: {e}")
            return False
            
    def execute(self, query, values=None):
        """
        Método para simular la ejecución de consultas SQL en Google Sheets
        query: consulta SQL (se analiza para determinar la acción a realizar)
        values: valores a utilizar en la consulta
        """
        try:
            # Analizar la consulta para determinar qué operación realizar
            query = query.strip().lower()
            
            # Operación SELECT
            if query.startswith("select"):
                return self._handle_select(query, values)
            
            # Operación INSERT
            elif query.startswith("insert"):
                return self._handle_insert(query, values)
                
            # Operación UPDATE
            elif query.startswith("update"):
                return self._handle_update(query, values)
                
            # Operación DELETE
            elif query.startswith("delete"):
                return self._handle_delete(query, values)
                
            else:
                print(f"Operación no soportada: {query}")
                return None
                
        except Exception as e:
            print(f"Error al ejecutar consulta: {e}")
            return None
            
    def _handle_select(self, query, values):
        """
        Maneja consultas SELECT
        """
        try:
            # Extraer nombre de tabla de la consulta
            table_pattern = r"from\s+([a-zA-Z0-9_]+)"
            table_match = re.search(table_pattern, query)
            
            if not table_match:
                print("No se pudo determinar la tabla en la consulta SELECT")
                return None
                
            table_name = table_match.group(1)
            
            # Seleccionar la hoja correspondiente
            if not self.select_worksheet(table_name):
                # Si no existe, intentar buscar otras hojas relacionadas
                all_sheets = [sheet.title for sheet in self.spreadsheet.worksheets()]
                possible_sheets = [s for s in all_sheets if table_name in s]
                
                if not possible_sheets:
                    print(f"No se encontró ninguna hoja para la tabla '{table_name}'")
                    return None
                    
                table_name = possible_sheets[0]
                if not self.select_worksheet(table_name):
                    return None
            
            # Obtener todos los datos de la hoja
            all_data = self.worksheet.get_all_records()
            
            # Extraer condiciones de la consulta WHERE
            where_pattern = r"where\s+(.*?)(?:$|order\s+by|group\s+by|limit)"
            where_match = re.search(where_pattern, query)
            
            filtered_data = all_data
            
            if where_match:
                conditions = where_match.group(1).strip()
                
                # Convertir valores del parámetro si es necesario
                if values:
                    if isinstance(values, tuple) and len(values) == 1:
                        values = values[0]
                    
                    # Reemplazar comodines %s en las condiciones
                    if isinstance(values, tuple) or isinstance(values, list):
                        for value in values:
                            conditions = conditions.replace("%s", str(value), 1)
                    else:
                        conditions = conditions.replace("%s", str(values))
                
                # Filtrar datos según condiciones
                # Esta es una implementación simplificada, solo maneja condiciones básicas
                # Para consultas complejas, se necesitaría un analizador SQL más robusto
                filtered_data = self._filter_data_by_conditions(all_data, conditions)
            
            self.current_data = filtered_data
            return filtered_data
            
        except Exception as e:
            print(f"Error en consulta SELECT: {e}")
            return None
    
    def _filter_data_by_conditions(self, data, conditions):
        """
        Filtra los datos según las condiciones WHERE (simplificado)
        """
        filtered = []
        
        # Simplificación: solo maneja condiciones básicas como "campo = valor"
        # En un caso real, se requeriría un analizador de condiciones más complejo
        try:
            # Manejo básico para LIKE
            like_pattern = r"([a-zA-Z0-9_\.]+)\s+like\s+['\"]([^'\"]*)['\"]"
            like_match = re.search(like_pattern, conditions)
            
            if like_match:
                field = like_match.group(1).split('.')[-1]  # Eliminar prefijo de tabla si existe
                value_pattern = like_match.group(2).replace('%', '.*')
                
                for row in data:
                    if field in row and re.match(f"^{value_pattern}$", str(row[field]), re.IGNORECASE):
                        filtered.append(row)
                return filtered
                
            # Manejo básico para =, <, >
            condition_pattern = r"([a-zA-Z0-9_\.]+)\s*([=<>])\s*['\"]?([^'\")]*)['\"]?"
            condition_match = re.search(condition_pattern, conditions)
            
            if condition_match:
                field = condition_match.group(1).split('.')[-1]  # Eliminar prefijo de tabla si existe
                operator = condition_match.group(2)
                value = condition_match.group(3)
                
                for row in data:
                    if field in row:
                        if operator == '=' and str(row[field]) == value:
                            filtered.append(row)
                        elif operator == '>' and str(row[field]) > value:
                            filtered.append(row)
                        elif operator == '<' and str(row[field]) < value:
                            filtered.append(row)
                return filtered
                
            # Si no se pudo analizar la condición, devolver todos los datos
            return data
            
        except Exception as e:
            print(f"Error al filtrar datos: {e}")
            return data
    
    def _handle_insert(self, query, values):
        """
        Maneja consultas INSERT
        """
        try:
            # Extraer nombre de tabla y columnas de la consulta
            table_pattern = r"insert\s+into\s+([a-zA-Z0-9_\.]+)\s*\(([^)]+)\)"
            table_match = re.search(table_pattern, query)
            
            if not table_match:
                print("No se pudo determinar la tabla/columnas en la consulta INSERT")
                return None
                
            table_name = table_match.group(1).split('.')[-1]  # Eliminar prefijo de base de datos si existe
            columns = [col.strip() for col in table_match.group(2).split(',')]
            
            # Seleccionar la hoja correspondiente
            if not self.select_worksheet(table_name):
                print(f"No se encontró la hoja '{table_name}'")
                return None
            
            # Verificar que tenemos valores para insertar
            if not values:
                print("No se proporcionaron valores para INSERT")
                return None
                
            # Preparar la nueva fila
            new_row = []
            all_headers = self.current_headers
            
            # Crear una fila con todos los valores en NULL/vacíos
            new_row = [""] * len(all_headers)
            
            # Colocar los valores en las columnas correspondientes
            for i, col in enumerate(columns):
                if i < len(values):
                    col_index = all_headers.index(col)
                    if col_index >= 0:
                        new_row[col_index] = values[i]
            
            # Añadir la nueva fila a la hoja
            self.worksheet.append_row(new_row)
            
            # Simular la funcionalidad de lastrowid para compatibilidad
            total_rows = len(self.worksheet.get_all_values())
            self.lastrowid = total_rows - 1  # -1 para excluir la fila de encabezados
            
            return True
            
        except Exception as e:
            print(f"Error en consulta INSERT: {e}")
            return None
    
    def _handle_update(self, query, values):
        """
        Maneja consultas UPDATE
        """
        try:
            # Extraer nombre de tabla de la consulta
            table_pattern = r"update\s+([a-zA-Z0-9_\.]+)\s+set"
            table_match = re.search(table_pattern, query)
            
            if not table_match:
                print("No se pudo determinar la tabla en la consulta UPDATE")
                return None
                
            table_name = table_match.group(1).split('.')[-1]  # Eliminar prefijo de base de datos si existe
            
            # Extraer condiciones WHERE
            where_pattern = r"where\s+(.*?)(?:$|order\s+by|group\s+by|limit)"
            where_match = re.search(where_pattern, query)
            
            if not where_match:
                print("No se encontró cláusula WHERE en UPDATE (requerida)")
                return None
                
            conditions = where_match.group(1).strip()
            
            # Extraer campos a actualizar
            set_pattern = r"set\s+(.*?)\s+where"
            set_match = re.search(set_pattern, query)
            
            if not set_match:
                print("No se pudieron determinar los campos a actualizar")
                return None
                
            set_clause = set_match.group(1).strip()
            
            # Seleccionar la hoja correspondiente
            if not self.select_worksheet(table_name):
                print(f"No se encontró la hoja '{table_name}'")
                return None
            
            # Obtener todos los datos de la hoja
            all_data = self.worksheet.get_all_records()
            all_values = self.worksheet.get_all_values()
            headers = all_values[0]
            
            # Aplicar condición WHERE
            if values:
                if isinstance(values, tuple):
                    # Preparar los valores para el SET y WHERE
                    num_set_values = set_clause.count('%s')
                    set_values = values[:num_set_values]
                    where_values = values[num_set_values:]
                    
                    # Reemplazar los comodines en WHERE
                    for value in where_values:
                        conditions = conditions.replace("%s", str(value), 1)
                        
                    # Procesar cláusula SET (simplificado)
                    # En un caso real, se necesitaría un parser más complejo
                    set_pairs = set_clause.split(',')
                    set_fields = []
                    for i, pair in enumerate(set_pairs):
                        if '%s' in pair and i < len(set_values):
                            field = pair.split('=')[0].strip()
                            set_fields.append((field, set_values[i]))
                        
                    # Actualizar las filas que cumplan con las condiciones
                    filtered_rows = self._filter_data_by_conditions(all_data, conditions)
                    for row in filtered_rows:
                        # Encontrar el índice de esta fila en la hoja
                        row_idx = None
                        for i, data_row in enumerate(all_data):
                            match = True
                            for key, value in data_row.items():
                                if key in row and row[key] != value:
                                    match = False
                                    break
                            if match:
                                row_idx = i + 2  # +2 porque los índices comienzan en 1 y hay encabezados
                                break
                        
                        if row_idx is not None:
                            # Actualizar cada campo
                            for field, value in set_fields:
                                col_idx = headers.index(field) + 1  # +1 porque los índices comienzan en 1
                                self.worksheet.update_cell(row_idx, col_idx, value)
                
                return True
                
        except Exception as e:
            print(f"Error en consulta UPDATE: {e}")
            return None
    
    def _handle_delete(self, query, values):
        """
        Maneja consultas DELETE
        """
        try:
            # Extraer nombre de tabla de la consulta
            table_pattern = r"delete\s+from\s+([a-zA-Z0-9_\.]+)"
            table_match = re.search(table_pattern, query)
            
            if not table_match:
                print("No se pudo determinar la tabla en la consulta DELETE")
                return None
                
            table_name = table_match.group(1).split('.')[-1]  # Eliminar prefijo de base de datos si existe
            
            # Extraer condiciones WHERE
            where_pattern = r"where\s+(.*?)(?:$|order\s+by|group\s+by|limit)"
            where_match = re.search(where_pattern, query)
            
            if not where_match:
                print("No se encontró cláusula WHERE en DELETE (requerida)")
                return None
                
            conditions = where_match.group(1).strip()
            
            # Seleccionar la hoja correspondiente
            if not self.select_worksheet(table_name):
                print(f"No se encontró la hoja '{table_name}'")
                return None
            
            # Obtener todos los datos de la hoja
            all_data = self.worksheet.get_all_records()
            
            # Aplicar condición WHERE
            if values:
                if isinstance(values, (str, int, float)):
                    # Único valor
                    conditions = conditions.replace("%s", str(values))
                elif isinstance(values, tuple):
                    # Múltiples valores
                    for value in values:
                        conditions = conditions.replace("%s", str(value), 1)
                        
            # Identificar las filas a eliminar
            filtered_rows = self._filter_data_by_conditions(all_data, conditions)
            rows_to_delete = []
            
            for i, row in enumerate(all_data):
                for filtered_row in filtered_rows:
                    if all(row.get(k) == filtered_row.get(k) for k in row.keys()):
                        rows_to_delete.append(i + 2)  # +2 porque los índices comienzan en 1 y hay encabezados
                        break
            
            # Eliminar filas (comenzando desde la última para no afectar los índices)
            for row_idx in sorted(rows_to_delete, reverse=True):
                self.worksheet.delete_rows(row_idx)
                
            return True
                
        except Exception as e:
            print(f"Error en consulta DELETE: {e}")
            return None
            
    def fetchall(self):
        """
        Devuelve todos los registros de la última consulta
        """
        if self.current_data is not None:
            # Convertir los diccionarios en listas de valores
            result = []
            for row in self.current_data:
                result.append(tuple(row.values()))
            return result
        return []
        
    def fetchone(self):
        """
        Devuelve el primer registro de la última consulta
        """
        if self.current_data and len(self.current_data) > 0:
            return tuple(self.current_data[0].values())
        return None
        
    def commit(self):
        """
        Método de compatibilidad (no es necesario en Google Sheets)
        """
        pass  # Google Sheets se guarda automáticamente
