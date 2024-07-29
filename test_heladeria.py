import unittest
from models import db, Ingrediente, Producto, ProductoIngrediente, Heladeria
from app import app


class TestHeladeria(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        cls.app = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()
            heladeria = Heladeria()
            heladeria.cargar_datos()

    def setUp(self):
        self.app = TestHeladeria.app

    def test_ingrediente_sano(self):
        with app.app_context():
            ingrediente = Ingrediente.query.first()
            self.assertTrue(ingrediente.es_sano())

    def test_abastecer_ingrediente(self):
        with app.app_context():
            ingrediente = Ingrediente.query.first()
            inventario_inicial = ingrediente.inventario
            ingrediente.abastecer()
            db.session.commit()
            self.assertEqual(ingrediente.inventario, inventario_inicial + 10)

    def test_calcular_costo(self):
        with app.app_context():
            producto = Producto.query.first()
            costo = producto.calcular_costo()
            self.assertIsInstance(costo, float)

    def test_calcular_rentabilidad(self):
        with app.app_context():
            producto = Producto.query.first()
            rentabilidad = producto.calcular_rentabilidad()
            self.assertIsInstance(rentabilidad, float)

    def test_vender_producto(self):
        with app.app_context():
            heladeria = Heladeria()
            resultado = heladeria.vender('Copa de Chocolate')
            self.assertEqual(resultado, '¡Vendido!')

    def test_vender_producto_fallido(self):
        with app.app_context():
            heladeria = Heladeria()
            with self.assertRaises(ValueError) as context:
                heladeria.vender('Producto Inexistente')
            self.assertTrue('Producto Producto Inexistente no encontrado' in str(context.exception))


if __name__ == '__main__':
    unittest.main()
