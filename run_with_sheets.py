#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para ejecutar la aplicación con la conexión a Google Sheets
"""

import os
import sys
import subprocess

def check_prerequisites():
    """
    Verifica que todos los requisitos están instalados y configurados
    """
    print("Verificando requisitos...")
    
    # Verificar que el archivo de credenciales existe
    if not os.path.exists("connection/credentials.json"):
        print("\n[ERROR] No se encontró el archivo 'credentials.json' en la carpeta 'connection/'")
        print("Este archivo es necesario para conectar con Google Sheets.")
        print("\nPor favor, sigue estos pasos:")
        print("1. Ve a https://console.cloud.google.com/")
        print("2. Crea un proyecto y habilita las APIs de Google Sheets y Drive")
        print("3. Crea una cuenta de servicio y descarga el archivo JSON")
        print("4. Renombra el archivo a 'credentials.json'")
        print("5. Colócalo en la carpeta 'connection/'")
        return False
    
    # Verificar dependencias
    try:
        import gspread
        import oauth2client
        import pandas
    except ImportError as e:
        print(f"\n[ERROR] Faltan dependencias: {e}")
        print("Por favor, instala las dependencias requeridas:")
        print("pip install -r requirements.txt")
        return False
        
    print("Requisitos verificados correctamente.")
    return True


def initialize_sheets():
    """
    Inicializa las hojas de Google Sheets si es necesario
    """
    print("\nVerificando hojas de Google Sheets...")
    
    # Preguntar al usuario si desea inicializar las hojas
    response = input("¿Deseas inicializar/reinicializar las hojas de Google Sheets? (s/N): ")
    
    if response.lower() == 's':
        print("\nInicializando hojas de Google Sheets...")
        
        try:
            from connection.init_google_sheets import main as init_sheets
            result = init_sheets()
            
            if not result:
                print("[ERROR] No se pudieron inicializar las hojas de Google Sheets.")
                return False
                
            print("Hojas de Google Sheets inicializadas correctamente.")
            return True
            
        except Exception as e:
            print(f"[ERROR] Error al inicializar las hojas de Google Sheets: {e}")
            return False
    else:
        print("Omitiendo la inicialización de hojas.")
        return True


def run_application():
    """
    Ejecuta la aplicación
    """
    print("\nEjecutando la aplicación...")
    
    try:
        # Ejecutar la aplicación
        subprocess.run([sys.executable, "app.py"])
        return True
    except Exception as e:
        print(f"[ERROR] Error al ejecutar la aplicación: {e}")
        return False


def main():
    """
    Función principal
    """
    print("=== SISTEMA DE INVENTARIO CON GOOGLE SHEETS ===")
    
    # Verificar requisitos
    if not check_prerequisites():
        print("\n[ERROR] Faltan requisitos. Por favor, configúralos e intenta de nuevo.")
        return False
        
    # Inicializar hojas si es necesario
    if not initialize_sheets():
        print("\n[ADVERTENCIA] No se inicializaron las hojas de Google Sheets.")
        continue_anyway = input("¿Deseas continuar de todos modos? (s/N): ")
        
        if continue_anyway.lower() != 's':
            print("Abortando la ejecución.")
            return False
    
    # Ejecutar la aplicación
    run_application()
    
    return True


if __name__ == "__main__":
    main()
