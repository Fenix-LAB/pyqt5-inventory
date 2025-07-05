from connection.conexion import Conexion
from model.cliente import Cliente
from model.proveedor import Proveedor
from model.producto import Producto
import datetime


class ConexionTransacciones(object):

    def __init__(self):
        self.conexion = Conexion()
        self.cliente = Cliente()
        self.proveedor = Proveedor()


    def selectProveedores(self, typeParameter, parameter):
        query = """
                    SELECT prov.idproveedores , prov.descripcion, p.nombre, p.email
                    FROM proveedores prov, personas p
                    WHERE p.idpersonas = prov.personas_idpersonas and prov.estado = 1 and """+ typeParameter +""" LIKE %s
                """
        param = parameter + '%'
        values = param
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        listProveedores = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()
        return listProveedores

    def selectClientes(self, typeParameter, parameter):
        query = """
                    SELECT c.idclientes, c.apellido, p.nombre, p.email
                    FROM clientes c, personas p
                    WHERE p.idpersonas = c.personas_idpersonas and c.estado = 1 and """+ typeParameter +""" LIKE %s
                """
        param = parameter + '%'
        values = param
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        listClientes = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()
        return listClientes

    def selectProductos(self, typeParameter, parameter, parameterTransaccion):
        query = """
                    SELECT p.idproductos, p.nombre, p.descripcion, p.cantidad, p.pCompra, p.pVenta, m.descripcion
                    FROM productos p, marcas m
                    WHERE p.marcas_idmarcas = m.idmarcas and """ +typeParameter+ """ LIKE %s
                """
        if parameterTransaccion == 'VNT':
            query = query + " and p.cantidad > 0 and p.estado = 1"

        param = parameter + '%'
        values = param
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        listProductos = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()
        return listProductos

    def cargarTransaccionCompra(self, listMovimiento, proveedor, estado):
        hoy = datetime.datetime.now().date()
        self.conexion.abrirConexion()

        # 1. Insertar tipo de movimiento
        queryTipoMovimiento = """
                                INSERT INTO tipo_movimiento (tipo_movimiento, proveedores_idproveedores)
                                VALUES ('compra', %s)
                              """
        valuesTipoMovimiento = proveedor.getIdProveedor()
        self.conexion.cursor.execute(queryTipoMovimiento, valuesTipoMovimiento)
        id_tipo_movimiento = self.conexion.lastrowid
        
        # 2. Insertar movimiento
        queryMovimiento = """
                            INSERT INTO movimiento (fecha, tipo_movimiento_idtipo_movimiento)
                            VALUES (%s, %s)
                         """
        valuesMovimiento = (hoy, id_tipo_movimiento)
        self.conexion.cursor.execute(queryMovimiento, valuesMovimiento)
        id_movimiento = self.conexion.lastrowid
        
        # 3. Insertar detalle de movimiento para cada producto
        for movimiento in listMovimiento:
            producto = Producto()
            producto.setIdProducto(movimiento.getProducto().getIdProducto())
            
            queryDetalle = """
                            INSERT INTO detalle_movimiento (cantidad, precio_unitario, productos_idproductos, 
                                                           movimiento_idMovimiento)
                            VALUES (%s, %s, %s, %s)
                           """
            valuesDetalle = (movimiento.getCantidad(), movimiento.getPrecioUnitario(), 
                            movimiento.getProducto().getIdProducto(), id_movimiento)
            self.conexion.cursor.execute(queryDetalle, valuesDetalle)
            
            # Actualizar stock si está confirmada la transacción
            if estado == 1:
                self.modificarStock('CMP', producto)
        
        self.conexion.db.commit()
        self.conexion.cerrarConexion()

    def cargarTransaccionVenta(self, listMovimiento, cliente, estado):
        hoy = datetime.datetime.now().date()
        self.conexion.abrirConexion()
        
        # 1. Insertar tipo de movimiento
        queryTipoMovimiento = """
                                INSERT INTO tipo_movimiento (tipo_movimiento, clientes_idClientes)
                                VALUES ('venta', %s)
                             """
        valuesTipoMovimiento = cliente.getIdCliente()
        self.conexion.cursor.execute(queryTipoMovimiento, valuesTipoMovimiento)
        id_tipo_movimiento = self.conexion.lastrowid
        
        # 2. Insertar movimiento
        queryMovimiento = """
                            INSERT INTO movimiento (fecha, tipo_movimiento_idtipo_movimiento)
                            VALUES (%s, %s)
                         """
        valuesMovimiento = (hoy, id_tipo_movimiento)
        self.conexion.cursor.execute(queryMovimiento, valuesMovimiento)
        id_movimiento = self.conexion.lastrowid
        
        # 3. Insertar detalle de movimiento para cada producto
        for movimiento in listMovimiento:
            producto = Producto()
            producto.setIdProducto(movimiento.getProducto().getIdProducto())
            
            queryDetalle = """
                            INSERT INTO detalle_movimiento (cantidad, precio_unitario, productos_idproductos, 
                                                          movimiento_idMovimiento)
                            VALUES (%s, %s, %s, %s)
                           """
            valuesDetalle = (movimiento.getCantidad(), movimiento.getPrecioUnitario(), 
                            movimiento.getProducto().getIdProducto(), id_movimiento)
            self.conexion.cursor.execute(queryDetalle, valuesDetalle)
            
            # Actualizar stock si está confirmada la transacción
            if estado == 1:
                self.modificarStock('VNT', producto)
                
        self.conexion.db.commit()
        self.conexion.cerrarConexion()

    def modificarStock(self, tipoT, producto):
        self.conexion.abrirConexion()
        
        # Obtener información actual del producto
        queryProducto = "SELECT cantidad FROM productos WHERE idproductos = %s"
        valuesProducto = producto.getIdProducto()
        self.conexion.cursor.execute(queryProducto, valuesProducto)
        result = self.conexion.cursor.fetchone()
        
        if not result:
            self.conexion.cerrarConexion()
            return
            
        cantidad_actual = result[0]
        
        # Obtener cantidad del último movimiento
        if tipoT == 'CMP':
            query = """
                    SELECT dm.cantidad
                    FROM detalle_movimiento dm, movimiento m, tipo_movimiento tm
                    WHERE dm.movimiento_idMovimiento = m.idMovimiento and 
                          m.tipo_movimiento_idtipo_movimiento = tm.idtipo_movimiento and
                          tm.tipo_movimiento = 'compra' and dm.productos_idproductos = %s
                    ORDER BY m.idMovimiento DESC
                    LIMIT 1
                   """
        else:
            query = """
                    SELECT dm.cantidad
                    FROM detalle_movimiento dm, movimiento m, tipo_movimiento tm
                    WHERE dm.movimiento_idMovimiento = m.idMovimiento and 
                          m.tipo_movimiento_idtipo_movimiento = tm.idtipo_movimiento and
                          tm.tipo_movimiento = 'venta' and dm.productos_idproductos = %s
                    ORDER BY m.idMovimiento DESC
                    LIMIT 1
                   """
                   
        values = producto.getIdProducto()
        self.conexion.cursor.execute(query, values)
        result_movimiento = self.conexion.cursor.fetchone()
        
        if not result_movimiento:
            self.conexion.cerrarConexion()
            return
            
        cantidad_movimiento = result_movimiento[0]
        
        # Actualizar stock
        if tipoT == 'CMP':
            nueva_cantidad = int(cantidad_actual) + int(cantidad_movimiento)
        else:
            nueva_cantidad = int(cantidad_actual) - int(cantidad_movimiento)
            
        query_update = "UPDATE productos SET cantidad = %s WHERE idproductos = %s"
        values_update = (nueva_cantidad, producto.getIdProducto())
        self.conexion.cursor.execute(query_update, values_update)
        
        self.conexion.db.commit()
        self.conexion.cerrarConexion()