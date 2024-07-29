def es_sano(calorias, es_vegetariano):

    # función para determinar si un ingrediente es sano"

    return calorias < 100 or es_vegetariano


def contar_calorias(ingredientes_calorias):

    # función para realizar el conteo de calorias de un producto"

    total_calorias = sum(ingredientes_calorias)
    return round(total_calorias * 0.95, 2)


def calcular_costo(ingrediente1, ingrediente2, ingrediente3):

    # función para calcular el costo de producir un producto"

    return ingrediente1['precio'] + ingrediente2['precio'] + ingrediente3['precio']


def calcular_rentabilidad(precio_venta, ingrediente1, ingrediente2, ingrediente3):

    # función para calcular la rentabilidad un producto"

    costo = calcular_costo(ingrediente1, ingrediente2, ingrediente3)
    return precio_venta - costo


def mejor_producto(producto1, producto2, producto3, producto4):

    # función para encontrar el mejor producto"
    productos = [producto1, producto2, producto3, producto4]
    return max(productos, key=lambda p: p['rentabilidad'])['nombre']


# calorias_ingredientes_1 = [200, 150, 100]
# print(contar_calorias(calorias_ingredientes_1))
