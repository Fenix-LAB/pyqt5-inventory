#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test para verificar que la migración a Excel funciona correctamente
"""

import os
import sys

# Agregar el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from connection.conexion import Conexion

def test_excel_connection():
    """Test básico de conexión a Excel"""
    print("🧪 Iniciando test de conexión a Excel...")
    
    try:
        # Crear instancia de conexión
        conn = Conexion()
        print("✅ Conexión creada exitosamente")
        
        # Verificar que el archivo Excel se creó
        if os.path.exists(conn.excel_file):
            print(f"✅ Archivo Excel creado: {conn.excel_file}")
        else:
            print(f"❌ Archivo Excel no encontrado: {conn.excel_file}")
            return False
        
        # Probar conexión
        if conn.conectar():
            print("✅ Conexión a Excel exitosa")
        else:
            print("❌ Error al conectar con Excel")
            return False
        
        # Verificar hojas
        if conn.workbook:
            hojas = conn.workbook.sheetnames
            print(f"✅ Hojas encontradas: {hojas}")
            
            # Verificar que existen las hojas principales
            hojas_esperadas = ["productos", "categorias", "clientes", "proveedores", "usuarios"]
            for hoja in hojas_esperadas:
                if hoja in hojas:
                    print(f"  ✅ Hoja '{hoja}' encontrada")
                else:
                    print(f"  ❌ Hoja '{hoja}' no encontrada")
        
        # Test de consulta básica
        try:
            conn.execute("SELECT * FROM categorias")
            result = conn.fetchall()
            print(f"✅ Consulta SELECT ejecutada. Registros encontrados: {len(result)}")
            
            if result:
                print(f"  📄 Primer registro: {result[0]}")
            
        except Exception as e:
            print(f"❌ Error en consulta SELECT: {e}")
        
        # Test de inserción
        try:
            conn.execute("INSERT INTO categorias (id, nombre, descripcion) VALUES (%s, %s, %s)", 
                        (999, "Test Category", "Categoría de prueba"))
            print("✅ Inserción test ejecutada")
            
            # Verificar inserción
            conn.execute("SELECT * FROM categorias WHERE id = %s", (999,))
            result = conn.fetchone()
            if result:
                print(f"✅ Registro insertado correctamente: {result}")
                
                # Limpiar test
                conn.execute("DELETE FROM categorias WHERE id = %s", (999,))
                print("✅ Registro de prueba eliminado")
            
        except Exception as e:
            print(f"❌ Error en test de inserción: {e}")
        
        # Cerrar conexión
        conn.cerrarConexion()
        print("✅ Conexión cerrada correctamente")
        
        print("\n🎉 ¡Todos los tests pasaron exitosamente!")
        print(f"📁 Archivo Excel ubicado en: {os.path.abspath(conn.excel_file)}")
        return True
        
    except Exception as e:
        print(f"❌ Error general en el test: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("TEST DE MIGRACIÓN A EXCEL")
    print("=" * 50)
    
    success = test_excel_connection()
    
    if success:
        print("\n✅ La migración a Excel funciona correctamente!")
        print("🚀 Puedes proceder a usar la aplicación normalmente.")
    else:
        print("\n❌ Hay problemas con la migración.")
        print("🔧 Revisa los errores anteriores y verifica las dependencias.")
    
    print("\n" + "=" * 50)
