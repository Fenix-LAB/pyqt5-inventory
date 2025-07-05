#!/usr/bin/env python
# -*- coding: utf-8 -*-
from connection.conexion import Conexion
from connection.conexionProducto import conexionProducto
from connection.conexionProveedor import conexionProveedor
from connection.conexionCliente import conexionCliente
from connection.conexionUsuario import conexionUsuario
from connection.conexionMarca import conexionMarca
from connection.conexionRubro import conexionRubro
from connection.init_google_sheets import main as init_sheets

class ControllerConnection(object):

    def __init__(self):
        self.connection = Conexion()
        self.connectionCliente = conexionCliente()
        
        # Inicializar Google Sheets si es necesario
        # Comentar esta línea después de la primera ejecución
        # init_sheets()

    def getConnectionRubro(self):
        self.__connectionRubro = conexionRubro()
        return self.__connectionRubro

    def getConnectionMarca(self):
        self.__connectioMarca = conexionMarca()
        return self.__connectioMarca

    def getConnectionUsuario(self):
        self.__connectionUsuario = conexionUsuario()
        return self.__connectionUsuario

    def getConnectionCliente(self):
        return self.connectionCliente

    def getConnectionProveedor(self):
        self.__connectionProveedor = conexionProveedor()
        return self.__connectionProveedor

    def getConnectionProducto(self):
        self.__connectionProducto = conexionProducto()
        return self.__connectionProducto

