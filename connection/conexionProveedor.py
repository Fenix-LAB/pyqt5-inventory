#!/usr/bin/env python
# -*- coding: utf-8 -*-


from model.proveedor import Proveedor
from connection.conexion import Conexion
class conexionProveedor(object):


    def __init__(self):
        self.conexion = Conexion()
        self.proveedor = Proveedor()

    def selectProveedor(self, typeParameter, parameter, parameterState):
        query ="""
                    SELECT prov.idproveedores, prov.descripcion, p.nombre, p.email, prov.web, d.direccion, d.numero,
                        d.piso, dpto, p.idpersonas, d.iddirecciones, prov.estado
                    FROM proveedores prov, personas p, direcciones d
                    WHERE p.direcciones_iddirecciones = d.iddirecciones and p.idpersonas = prov.personas_idpersonas and
                    """ + typeParameter + """ LIKE %s and prov.estado LIKE %s
               """
        param = parameter + '%'

        paramState = '1'
        if parameterState == 0:
            paramState = '%'  # En Google Sheets usamos % como comodín para incluir todos

        values = (param, paramState)
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        listProveedor = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()
        return listProveedor

    def selectTelefonoProveedor(self, proveedor):
        query = """SELECT t.idtelefono, t.numero, t.tipo
                    FROM telefonos t, personas p, proveedores prov
                    WHERE p.idpersonas = prov.personas_idpersonas and p.idpersonas = t.personas_idpersonas
                    and prov.idproveedores = %s"""
        value = proveedor.getIdProveedor()
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, value)
        listTelefono = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()
        return listTelefono

    def modificarProveedor(self, proveedor):
        query = """
                    UPDATE personas p, proveedores prov, direcciones d
                    SET p.nombre = %s , p.email= %s , prov.descripcion = %s, prov.web = %s, d.direccion= %s,
                            d.numero = %s, d.piso = %s, dpto = %s, prov.estado = %s
                    WHERE p.idpersonas = prov.personas_idpersonas and p.direcciones_iddirecciones = d.iddirecciones
                            and prov.idproveedores = %s
                """
        values = (proveedor.getNombre(), proveedor.getEmail(), proveedor.getDescripcion(),
                    proveedor.getWeb(), proveedor.getDireccion().getDireccion(), proveedor.getDireccion().getNumero(),
                    proveedor.getDireccion().getPiso(), proveedor.getDireccion().getDpto(), proveedor.getEstado(),
                    proveedor.getIdProveedor()
        )
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        self.conexion.db.commit()
        self.conexion.cerrarConexion()

    def insertarProveedor(self, proveedor):
        self.conexion.abrirConexion()
        
        # 1. Insertar dirección
        queryDireccion = "INSERT INTO direcciones (direccion, numero, piso, dpto) VALUES (%s, %s, %s, %s)"
        valuesDireccion = (proveedor.getDireccion().getDireccion(), proveedor.getDireccion().getNumero(),
                           proveedor.getDireccion().getPiso(), proveedor.getDireccion().getDpto())
        self.conexion.cursor.execute(queryDireccion, valuesDireccion)
        id_direccion = self.conexion.lastrowid
        
        # 2. Insertar persona
        queryPersona = "INSERT INTO personas (nombre, email, direcciones_iddirecciones) VALUES (%s, %s, %s)"
        valuesPersona = (proveedor.getNombre(), proveedor.getEmail(), id_direccion)
        self.conexion.cursor.execute(queryPersona, valuesPersona)
        id_persona = self.conexion.lastrowid
        
        # 3. Insertar proveedor
        queryProveedor = "INSERT INTO proveedores (descripcion, personas_idpersonas, web, estado) VALUES (%s, %s, %s, %s)"
        valuesProveedor = (proveedor.getDescripcion(), id_persona, proveedor.getWeb(), proveedor.getEstado())
        self.conexion.cursor.execute(queryProveedor, valuesProveedor)
        
        self.conexion.db.commit()
        self.conexion.cerrarConexion()

    def borrarProveedor(self, proveedor):
        queryProveedor = """
                            UPDATE proveedores
                            SET estado = 0
                            WHERE idproveedores = %s
                        """
        valueProveedor = proveedor.getIdProveedor()
        
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(queryProveedor, valueProveedor)
        self.conexion.db.commit()
        self.conexion.cerrarConexion()