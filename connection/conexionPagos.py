from connection.conexion import Conexion
from model.cliente import Cliente
from model.proveedor import Proveedor
import datetime


class ConexionPagos(object):

    def __init__(self):
        self.conexion = Conexion()
        self.cliente = Cliente()
        self.proveedor = Proveedor()


    def selectProveedores(self, tipoParametro, parametro):
        query = """
                    SELECT prov.idproveedores , prov.descripcion, p.nombre, p.email
                    FROM proveedores prov, personas p
                    WHERE p.idpersonas = prov.personas_idpersonas and prov.estado = 1 and
                    """ + tipoParametro + """ LIKE %s
                """
        parametro = parametro + '%'
        values = parametro
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        listProveedores = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()
        return listProveedores


    def selectClientes(self, tipoParametro, parametro):
        query = """
                    SELECT c.idclientes, c.apellido, p.nombre, p.email
                    FROM clientes c, personas p
                    WHERE p.idpersonas = c.personas_idpersonas and c.estado = 1 and
                    """+ tipoParametro + """ LIKE %s
                """
        parametro = parametro + '%'
        values = parametro
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        listClientes = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()
        return listClientes


    def selectListPagosProveedor(self, proveedor):
        query = """
                    SELECT p.fecha, p.monto, tm.tipo_movimiento
                    FROM proveedores prov, pagos p, tipo_movimiento tm
                    WHERE tm.proveedores_idproveedores = prov.idproveedores and
                        p.tipo_movimiento_idtipo_movimiento = tm.idtipo_movimiento and
                        prov.idproveedores = %s
                """
        values = proveedor.getIdProveedor()
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        listPagos = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()
        return listPagos

    def selectListTransaccionProveedor(self, proveedor):
        query = """
                    SELECT m.fecha, tm.tipo_movimiento, p.nombre, p.email
                    FROM movimiento m, tipo_movimiento tm, proveedores prov, personas p
                    WHERE m.tipo_movimiento_idtipo_movimiento = tm.idtipo_movimiento and
                        tm.proveedores_idproveedores = prov.idproveedores and
                        prov.personas_idpersonas = p.idpersonas and
                        prov.idproveedores = %s
                """
        values = proveedor.getIdProveedor()
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        listTransacciones = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()
        return listTransacciones

    def selectListPagosCliente(self, cliente):
        query = """
                    SELECT p.fecha, p.monto, tm.tipo_movimiento
                    FROM clientes c, pagos p, tipo_movimiento tm
                    WHERE tm.clientes_idClientes = c.idClientes and
                        p.tipo_movimiento_idtipo_movimiento = tm.idtipo_movimiento and
                        c.idClientes = %s
                """
        values = cliente.getIdCliente()
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        listPagos = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()
        return listPagos

    def selectListTransaccionCliente(self, cliente):
        query = """
                    SELECT m.fecha, tm.tipo_movimiento, p.nombre, p.email
                    FROM movimiento m, tipo_movimiento tm, clientes c, personas p
                    WHERE m.tipo_movimiento_idtipo_movimiento = tm.idtipo_movimiento and
                        tm.clientes_idClientes = c.idClientes and
                        c.personas_idpersonas = p.idpersonas and
                        c.idClientes = %s
                """
        values = cliente.getIdCliente()
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        listTransacciones = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()
        return listTransacciones

    def cargarCobranza(self, cliente, monto):
        hoy = datetime.datetime.now().date()
        
        self.conexion.abrirConexion()
        
        # 1. Insertar tipo de movimiento
        queryTipoMovimiento = """
                                INSERT INTO tipo_movimiento (tipo_movimiento, clientes_idClientes)
                                VALUES ('cobranza', %s)
                             """
        valuesTipoMovimiento = cliente.getIdCliente()
        self.conexion.cursor.execute(queryTipoMovimiento, valuesTipoMovimiento)
        id_tipo_movimiento = self.conexion.lastrowid
        
        # 2. Insertar pago
        queryPago = """
                        INSERT INTO pagos (fecha, monto, tipo_movimiento_idtipo_movimiento)
                        VALUES (%s, %s, %s)
                    """
        valuesPago = (hoy, monto, id_tipo_movimiento)
        self.conexion.cursor.execute(queryPago, valuesPago)
        
        self.conexion.db.commit()
        self.conexion.cerrarConexion()

    def cargarPago(self, proveedor, monto):
        hoy = datetime.datetime.now().date()
        
        self.conexion.abrirConexion()
        
        # 1. Insertar tipo de movimiento
        queryTipoMovimiento = """
                                INSERT INTO tipo_movimiento (tipo_movimiento, proveedores_idproveedores)
                                VALUES ('pago', %s)
                             """
        valuesTipoMovimiento = proveedor.getIdProveedor()
        self.conexion.cursor.execute(queryTipoMovimiento, valuesTipoMovimiento)
        id_tipo_movimiento = self.conexion.lastrowid
        
        # 2. Insertar pago
        queryPago = """
                        INSERT INTO pagos (fecha, monto, tipo_movimiento_idtipo_movimiento)
                        VALUES (%s, %s, %s)
                    """
        valuesPago = (hoy, monto, id_tipo_movimiento)
        self.conexion.cursor.execute(queryPago, valuesPago)
        
        self.conexion.db.commit()
        self.conexion.cerrarConexion()