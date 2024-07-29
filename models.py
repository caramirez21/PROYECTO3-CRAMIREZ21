from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Ingrediente(db.Model):
    __tablename__ = 'ingredientes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    calorias = db.Column(db.Integer, nullable=False)
    inventario = db.Column(db.Integer, nullable=False)
    es_vegetariano = db.Column(db.Boolean, nullable=False)

    def es_sano(self):
        return self.calorias < 100 or self.es_vegetariano

    def abastecer(self):
        self.inventario += 10


class ProductoIngrediente(db.Model):
    __tablename__ = 'producto_ingrediente'
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    ingrediente_id = db.Column(db.Integer, db.ForeignKey('ingredientes.id'), nullable=False)
    cantidad = db.Column(db.Float, nullable=False, default=1.0)
    ingrediente = db.relationship('Ingrediente', backref='productos_asociados')


class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    precio_publico = db.Column(db.Float, nullable=False)
    tipo_vaso = db.Column(db.String(50), nullable=True)
    volumen = db.Column(db.Float, nullable=True)
    ingredientes = db.relationship('ProductoIngrediente', backref='producto', lazy=True)

    def calcular_costo(self):
        return sum(pi.ingrediente.precio * pi.cantidad for pi in self.ingredientes)

    def calcular_rentabilidad(self):
        return self.precio_publico - self.calcular_costo()

    def calcular_calorias(self):
        return round(sum(pi.ingrediente.calorias * pi.cantidad for pi in self.ingredientes) * 0.95, 2)


class Heladeria:
    def __init__(self):
        self.productos = Producto.query.all()
        self.ingredientes = Ingrediente.query.all()
        self.ventas_del_dia = 0

    def producto_mas_rentable(self):
        if not self.productos:
            return None
        return max(self.productos, key=lambda p: p.calcular_rentabilidad()).nombre

    def vender(self, nombre_producto):
        for producto in self.productos:
            if producto.nombre == nombre_producto:
                for pi in producto.ingredientes:
                    ingrediente = pi.ingrediente
                    if ingrediente.inventario < pi.cantidad:
                        raise ValueError(ingrediente.nombre)
                for pi in producto.ingredientes:
                    ingrediente = pi.ingrediente
                    ingrediente.inventario -= pi.cantidad
                self.ventas_del_dia += producto.precio_publico
                return "¡Vendido!"
        raise ValueError(f"Producto {nombre_producto} no encontrado")

    def cargar_datos(self):
        ingredientes = [
            Ingrediente(nombre='Leche', precio=2.5, calorias=150, inventario=100, es_vegetariano=True),
            Ingrediente(nombre='Chocolate', precio=1.5, calorias=200, inventario=50, es_vegetariano=True),
            Ingrediente(nombre='Fresa', precio=1.0, calorias=50, inventario=80, es_vegetariano=True),
            Ingrediente(nombre='Azúcar', precio=0.5, calorias=50, inventario=200, es_vegetariano=True),
            Ingrediente(nombre='Vainilla', precio=1.0, calorias=50, inventario=60, es_vegetariano=True),
        ]

        productos = [
            Producto(nombre='Copa de Chocolate', precio_publico=8.0, tipo_vaso='Vaso Grande', ingredientes=[
                ProductoIngrediente(ingrediente=ingredientes[0], cantidad=1),
                ProductoIngrediente(ingrediente=ingredientes[1], cantidad=2)
            ]),
            Producto(nombre='Malteada de Fresa', precio_publico=7.0, volumen=400, ingredientes=[
                ProductoIngrediente(ingrediente=ingredientes[0], cantidad=1),
                ProductoIngrediente(ingrediente=ingredientes[2], cantidad=2)
            ]),
        ]

        db.session.add_all(ingredientes + productos)
        db.session.commit()

        self.ingredientes = Ingrediente.query.all()
        self.productos = Producto.query.all()


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    es_admin = db.Column(db.Boolean, default=False)
    es_empleado = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
