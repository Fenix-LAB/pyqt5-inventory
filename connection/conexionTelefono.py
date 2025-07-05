#!/usr/bin/env python
# -*- coding: utf-8 -*-

from model.telefono import Telefono
from connection.conexion import Conexion
class conexionTelefono(object):


    def __init__(self):
        self.conexion = Conexion()
        self.telefono = Telefono()

    def selectTelefono(self, telefono):
        query ="""
                    SELECT t.idTelefono, t.tipo, t.numero
                    FROM telefonos t, personas p
                    WHERE t.personas_idpersonas = p.idpersonas and p.idpersonas = %s
                """
        values = telefono.getIdPersona()
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        listTelefono = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()
        return listTelefono

    def modificarTelefono(self, telefono):
        query = """
                    UPDATE telefonos
                    SET numero = %s , tipo = %s
                    WHERE idtelefono= %s;
                """
        values = (telefono.getTelefono(), telefono.getTipo(), telefono.getIdTelefono())
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        self.conexion.db.commit()
        self.conexion.cerrarConexion()

    def insertarTelefono(self, telefono):
        query = "INSERT INTO telefonos (numero, tipo, personas_idpersonas) VALUES (%s , %s, %s)"
        values = (telefono.getTelefono(), telefono.getTipo(), telefono.getIdPersona())
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        self.conexion.db.commit()
        self.conexion.cerrarConexion()


    def insertTelefonoInit(self, telefonos):
        self.conexion.abrirConexion()

        # Obtener el ID de la última persona insertada
        queryIdPersona = "select MAX(idpersonas) from personas"
        self.conexion.cursor.execute(queryIdPersona)
        result = self.conexion.cursor.fetchall()

        # Asegurarse de que hay resultados antes de intentar acceder a ellos
        if result and result[0] and len(result[0]) > 0:
            idPersona = int(result[0][0])
            
            for telefono in telefonos:
                # Verificar que el número de teléfono no está vacío
                if telefono[2] != '':
                    query = "INSERT INTO telefonos (numero, tipo, personas_idpersonas) VALUES (%s , %s, %s)"
                    values = (telefono[2], telefono[1], idPersona)
                    self.conexion.cursor.execute(query, values)
                    self.conexion.db.commit()
        else:
            print("No se pudo obtener el ID de la última persona insertada")

        self.conexion.cerrarConexion()


    def borrarTelefono(self, telefono):
        query = """
                    DELETE FROM telefonos
                    WHERE idtelefono= %s
                """
        values = telefono.getIdTelefono()
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        self.conexion.db.commit()
        self.conexion.cerrarConexion()

