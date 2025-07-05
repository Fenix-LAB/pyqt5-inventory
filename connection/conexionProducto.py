#!/usr/bin/env python
# -*- coding: utf-8 -*-
from connection.conexion import Conexion
from model.proveedor import Proveedor
from model.producto import Producto
from model.rubro import Rubro
from model.marca import Marca


class conexionProducto(object):

    def __init__(self):
        self.conexion = Conexion()
        self.producto = Producto()
        self.proveedor = Proveedor()
        self.rubro = Rubro()
        self.marca = Marca()

    def selectProducto(self, typeParameter, parameter, parameterState, parameterStock):
        query = """
                    SELECT p.idproductos, p.nombre, p.descripcion, TRUNCATE(p.pCompra, 2), TRUNCATE(p.pVenta, 2),
                            p.genero, p.estado, p.cantidad, p.cant_minima, m.idmarcas, m.descripcion, r.idrubros,
                            r.descripcion, prov.idproveedores, prov.descripcion
                    FROM productos p, marcas m , rubros r, proveedores prov
                    WHERE p.rubros_idrubros = r.idrubros and p.marcas_idmarcas = m.idmarcas and
                        p.proveedores_idproveedores = prov.idproveedores and """+ typeParameter + """ LIKE %s and
                        p.estado LIKE %s
                """
        param = parameter + '%'

        paramState = '1'
        if parameterState == 0:
            paramState = '%'  # En Google Sheets usamos % como comodín para incluir todos

        # Modificar la consulta si estamos buscando productos con stock bajo
        if parameterStock == 1:
            query = query + " and p.cantidad BETWEEN 0 and p.cant_minima"

        values = (param, paramState)
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        listProducto = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()
        return listProducto

    def modificarProducto(self, producto):
        query = """
                    UPDATE productos
                    SET nombre= %s, cantidad= %s, descripcion= %s, rubros_idrubros= %s, proveedores_idproveedores=%s,
                        marcas_idmarcas= %s, pCompra= %s, pVenta= %s, estado= %s, cant_minima= %s, genero= %s
                    WHERE idproductos= %s
                """
        idRubro = self.getIdRubro(producto.getRubro().getRubro())
        idMarca = self.getIdMarca(producto.getMarca().getMarca())
        idProveedor = self.getIdProveedor(producto.getProveedor().getDescripcion())
        values = (producto.getNombre(), producto.getCantidad(), producto.getDescripcion(), idRubro, idProveedor,
                  idMarca, producto.getPrecioCompra(), producto.getPrecioVenta(), producto.getEstado(),
                  producto.getCantidadMinima(), producto.getGenero(), producto.getIdProducto()
                 )
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        self.conexion.db.commit()
        self.conexion.cerrarConexion()

    def insertarProducto(self, producto):
        query = """
                    INSERT INTO productos (nombre, cantidad, descripcion, rubros_idrubros, 
                                         proveedores_idproveedores, marcas_idmarcas, pCompra, 
                                         pVenta, estado, cant_minima, genero)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
        idRubro = self.getIdRubro(producto.getRubro().getRubro())
        idMarca = self.getIdMarca(producto.getMarca().getMarca())
        idProveedor = self.getIdProveedor(producto.getProveedor().getDescripcion())
        
        values = (producto.getNombre(), producto.getCantidad(), producto.getDescripcion(), idRubro, idProveedor,
                  idMarca, producto.getPrecioCompra(), producto.getPrecioVenta(), producto.getEstado(),
                  producto.getCantidadMinima(), producto.getGenero())
        
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        self.conexion.db.commit()
        self.conexion.cerrarConexion()

    def borrarProducto(self, producto):
        query = """
                    UPDATE productos
                    SET estado = 0
                    WHERE idproductos = %s
                """
        values = producto.getIdProducto()
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        self.conexion.db.commit()
        self.conexion.cerrarConexion()

    def listMarcas(self):
        query = "SELECT idmarcas, descripcion FROM marcas"
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query)
        listMarcas = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()
        return listMarcas

    def listRubro(self):
        query = "SELECT idrubros, descripcion FROM rubros"
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query)
        listRubro = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()
        return listRubro

    def listProveedor(self):
        query = """
                    SELECT prov.idproveedores, prov.descripcion, p.nombre
                    FROM proveedores prov, personas p
                    WHERE p.idpersonas = prov.personas_idpersonas and prov.estado = 1
                """
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query)
        listProveedor = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()
        return listProveedor

    def getIdProveedor(self, proveedor):
        query = "SELECT idproveedores FROM proveedores WHERE descripcion = %s"
        values = proveedor
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        result = self.conexion.cursor.fetchone()
        self.conexion.cerrarConexion()
        
        if result:
            return result[0]
        return None

    def getIdMarca(self, marca):
        query = "SELECT idmarcas FROM marcas WHERE descripcion = %s"
        values = marca
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        result = self.conexion.cursor.fetchone()
        self.conexion.cerrarConexion()
        
        if result:
            return result[0]
        return None

    def getIdRubro(self, rubro):
        query = "SELECT idrubros FROM rubros WHERE descripcion = %s"
        values = rubro
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        result = self.conexion.cursor.fetchone()
        self.conexion.cerrarConexion()
        
        if result:
            return result[0]
        return None