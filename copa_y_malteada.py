from iproducto import *


class Copa(IProducto):
    def __init__(self, nombre, precio_publico, ingredientes, tipo_vaso):
        self._nombre = nombre
        self._precio_publico = precio_publico
        self._ingredientes = ingredientes
        self._tipo_vaso = tipo_vaso

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, value):
        self._nombre = value

    @property
    def precio_publico(self):
        return self._precio_publico

    @precio_publico.setter
    def precio_publico(self, value):
        self._precio_publico = value

    @property
    def tipo_vaso(self):
        return self._tipo_vaso

    @tipo_vaso.setter
    def tipo_vaso(self, value):
        self._tipo_vaso = value

    def calcular_costo(self):
        return sum(ingrediente.precio for ingrediente in self._ingredientes)

    def calcular_rentabilidad(self):
        return self._precio_publico - self.calcular_costo()

    def calcular_calorias(self):
        return round(sum(ingrediente.calorias for ingrediente in self._ingredientes) * 0.95, 2)


class Malteada(IProducto):
    def __init__(self, nombre, precio_publico, ingredientes, volumen):
        self._nombre = nombre
        self._precio_publico = precio_publico
        self._ingredientes = ingredientes
        self._volumen = volumen

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, value):
        self._nombre = value

    @property
    def precio_publico(self):
        return self._precio_publico

    @precio_publico.setter
    def precio_publico(self, value):
        self._precio_publico = value

    @property
    def volumen(self):
        return self._volumen

    @volumen.setter
    def volumen(self, value):
        self._volumen = value

    def calcular_costo(self):
        return sum(ingrediente.precio for ingrediente in self._ingredientes) + 500

    def calcular_rentabilidad(self):
        return self._precio_publico - self.calcular_costo()

    def calcular_calorias(self):
        return sum(ingrediente.calorias for ingrediente in self._ingredientes) + 200
