from flask import Flask, render_template
from models import db, Heladeria

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///heladeria.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


def init_db():
    db.create_all()
    heladeria = Heladeria()
    heladeria.cargar_datos()


@app.route('/')
def index():
    heladeria = Heladeria()
    productos = heladeria.productos
    return render_template('index.html', productos=productos)


@app.route('/vender/<nombre>')
def vender_producto(nombre):
    heladeria = Heladeria()
    try:
        mensaje = heladeria.vender(nombre)
        return mensaje
    except ValueError as e:
        return f"¡Oh no! Nos hemos quedado sin {e.args[0]}"


if __name__ == '__main__':
    app.run(debug=True)
