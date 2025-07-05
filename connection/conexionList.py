from connection.conexion import Conexion


class ConexionList():

    def __init__(self):
        self.conexion = Conexion()

    def selectClientes(self):
        """
        Devuelve una lista de todos los clientes activos
        """
        query = """
                    SELECT c.idclientes, c.apellido, p.nombre, p.email
                    FROM clientes c, personas p
                    WHERE p.idpersonas = c.personas_idpersonas and c.estado = 1
                """
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query)
        listClientes = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()
        return listClientes

    def selectProveedores(self):
        """
        Devuelve una lista de todos los proveedores activos
        """
        query = """
                    SELECT prov.idproveedores, prov.descripcion, p.nombre, p.email
                    FROM proveedores prov, personas p
                    WHERE p.idpersonas = prov.personas_idpersonas and prov.estado = 1
                """
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query)
        listProveedores = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()
        return listProveedores





