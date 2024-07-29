from flask import Flask, jsonify, abort
from flask_login import login_required, current_user
from models import db, Producto, Ingrediente, Heladeria

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///heladeria.db'
db.init_app(app)

heladeria = Heladeria()  # Asegúrate de instanciar la heladería


@app.route('/api/productos', methods=['GET'])
def get_productos():
    productos = Producto.query.all()
    return jsonify([producto.to_dict() for producto in productos])


@app.route('/api/producto/<int:producto_id>', methods=['GET'])
def get_producto(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    return jsonify(producto.to_dict())


@app.route('/api/producto/nombre/<string:nombre>', methods=['GET'])
def get_producto_por_nombre(nombre):
    producto = Producto.query.filter_by(nombre=nombre).first_or_404()
    return jsonify(producto.to_dict())


@app.route('/api/producto/<int:producto_id>/calorias', methods=['GET'])
def get_calorias_producto(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    return jsonify({'calorias': producto.calcular_calorias()})


@app.route('/api/producto/<int:producto_id>/rentabilidad', methods=['GET'])
@login_required
def get_rentabilidad_producto(producto_id):
    if not current_user.es_admin and not current_user.es_empleado:
        return abort(403)
    producto = Producto.query.get_or_404(producto_id)
    return jsonify({'rentabilidad': producto.calcular_rentabilidad()})


@app.route('/api/producto/<int:producto_id>/costo', methods=['GET'])
@login_required
def get_costo_producto(producto_id):
    if not current_user.es_admin and not current_user.es_empleado:
        return abort(403)
    producto = Producto.query.get_or_404(producto_id)
    return jsonify({'costo': producto.calcular_costo()})


@app.route('/api/producto/<int:producto_id>/vender', methods=['POST'])
def vender_producto(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    try:
        heladeria.vender(producto.nombre)
        return jsonify({'message': '¡Vendido!'})
    except ValueError as e:
        return abort(400, description=f"¡Oh no! Nos hemos quedado sin {e.args[0]}")


@app.route('/api/ingredientes', methods=['GET'])
def get_ingredientes():
    ingredientes = Ingrediente.query.all()
    return jsonify([ingrediente.to_dict() for ingrediente in ingredientes])


@app.route('/api/ingrediente/<int:ingrediente_id>', methods=['GET'])
def get_ingrediente(ingrediente_id):
    ingrediente = Ingrediente.query.get_or_404(ingrediente_id)
    return jsonify(ingrediente.to_dict())


@app.route('/api/ingrediente/nombre/<string:nombre>', methods=['GET'])
def get_ingrediente_por_nombre(nombre):
    ingrediente = Ingrediente.query.filter_by(nombre=nombre).first_or_404()
    return jsonify(ingrediente.to_dict())


@app.route('/api/ingrediente/<int:ingrediente_id>/es_sano', methods=['GET'])
def get_es_sano_ingrediente(ingrediente_id):
    ingrediente = Ingrediente.query.get_or_404(ingrediente_id)
    return jsonify({'es_sano': ingrediente.es_sano()})


@app.route('/api/ingrediente/<int:ingrediente_id>/reabastecer', methods=['POST'])
@login_required
def reabastecer_ingrediente(ingrediente_id):
    if not current_user.es_admin and not current_user.es_empleado:
        return abort(403)
    ingrediente = Ingrediente.query.get_or_404(ingrediente_id)
    ingrediente.abastecer()
    db.session.commit()
    return jsonify({'message': 'Reabastecido'})


@app.route('/api/ingrediente/<int:ingrediente_id>/renovar', methods=['POST'])
@login_required
def renovar_ingrediente(ingrediente_id):
    if not current_user.es_admin and not current_user.es_empleado:
        return abort(403)
    ingrediente = Ingrediente.query.get_or_404(ingrediente_id)
    if hasattr(ingrediente, 'renovar_inventario'):
        ingrediente.renovar_inventario()
        db.session.commit()
        return jsonify({'message': 'Inventario renovado'})
    else:
        return abort(400, description="Sólo los complementos pueden renovar inventario")


if __name__ == '__main__':
    app.run(debug=True)
