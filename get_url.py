#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from connection.conexion import Conexion

def main():
    """
    Script simple para obtener la URL de la hoja de cálculo de Google Sheets
    """
    print("Obteniendo URL de la hoja de cálculo...")
    conexion = Conexion()
    
    # Pregunta por el correo electrónico
    email = input("Ingresa tu correo electrónico para obtener acceso: ")
    
    # Compartir la hoja
    if email:
        print(f"Compartiendo la hoja con {email}...")
        conexion.share_spreadsheet(email)
    
    # Intentar conectar y obtener la URL
    url = conexion.get_spreadsheet_url()

    if url:
        print("\n=============================================================")
        print(f"URL DE LA HOJA DE CÁLCULO: {url}")
        print("=============================================================\n")
        print("Abre este enlace en tu navegador para ver y editar los datos.")
    else:
        print("\nERROR: No se pudo obtener la URL.")
        print("Verifica que las credenciales sean correctas y que tengas conexión a internet.")

if __name__ == "__main__":
    main()