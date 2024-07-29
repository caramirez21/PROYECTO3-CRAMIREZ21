from ingrediente import *


class Base(Ingrediente):
    def __init__(self, nombre, precio, calorias, inventario, es_vegetariano, sabor):
        super().__init__(nombre, precio, calorias, inventario, es_vegetariano)
        self._sabor = sabor

    @property
    def sabor(self):
        return self._sabor

    @sabor.setter
    def sabor(self, value):
        self._sabor = value

    def abastecer(self):
        self._inventario += 5


class Complemento(Ingrediente):
    def abastecer(self):
        self._inventario += 10

    def renovar_inventario(self):
        self._inventario = 0
