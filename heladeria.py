from base import *


class Heladeria:
    def __init__(self):
        self._productos = []
        self._ingredientes = []
        self._ventas_del_dia = 0

    @property
    def productos(self):
        return self._productos

    @productos.setter
    def productos(self, value):
        self._productos = value

    @property
    def ingredientes(self):
        return self._ingredientes

    @ingredientes.setter
    def ingredientes(self, value):
        self._ingredientes = value

    @property
    def ventas_del_dia(self):
        return self._ventas_del_dia

    @ventas_del_dia.setter
    def ventas_del_dia(self, value):
        self._ventas_del_dia = value

    def producto_mas_rentable(self):
        if not self._productos:
            return None
        return max(self._productos, key=lambda p: p.calcular_rentabilidad()).nombre

    def vender(self, nombre_producto):
        for producto in self._productos:
            if producto.nombre == nombre_producto:
                for ingrediente in producto._ingredientes:
                    if ingrediente.inventario < 1:
                        return False
                for ingrediente in producto._ingredientes:
                    if isinstance(ingrediente, Base):
                        ingrediente.inventario -= 0.2
                    else:
                        ingrediente.inventario -= 1
                self._ventas_del_dia += producto.precio_publico
                return True
        return False
