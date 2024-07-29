from abc import ABC, abstractmethod


class Ingrediente(ABC):
    def __init__(self, nombre, precio, calorias, inventario, es_vegetariano):
        self._nombre = nombre
        self._precio = precio
        self._calorias = calorias
        self._inventario = inventario
        self._es_vegetariano = es_vegetariano

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, value):
        self._nombre = value

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, value):
        self._precio = value

    @property
    def calorias(self):
        return self._calorias

    @calorias.setter
    def calorias(self, value):
        self._calorias = value

    @property
    def inventario(self):
        return self._inventario

    @inventario.setter
    def inventario(self, value):
        self._inventario = value

    @property
    def es_vegetariano(self):
        return self._es_vegetariano

    @es_vegetariano.setter
    def es_vegetariano(self, value):
        self._es_vegetariano = value

    def es_sano(self):
        return self._calorias < 100 or self._es_vegetariano

    @abstractmethod
    def abastecer(self):
        pass
