from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from models import db, Usuario, Heladeria

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///heladeria.db'
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Usuario.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Nombre de usuario o contraseña incorrectos')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/index')
@login_required
def index():
    return f'¡Bienvenido, {current_user.username}!'


@app.route('/no_autorizado')
def no_autorizado():
    return 'No autorizado', 403


@app.before_request
def verificar_autorizacion():
    if request.endpoint in ['get_rentabilidad_producto', 'get_costo_producto', 'reabastecer_ingrediente',
                            'renovar_ingrediente']:
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        if request.endpoint == 'get_rentabilidad_producto' or request.endpoint == 'get_costo_producto':
            if not current_user.es_admin and not current_user.es_empleado:
                return redirect(url_for('no_autorizado'))
        elif request.endpoint == 'reabastecer_ingrediente' or request.endpoint == 'renovar_ingrediente':
            if not current_user.es_admin:
                return redirect(url_for('no_autorizado'))


def init_db():
    db.create_all()
    heladeria = Heladeria()
    heladeria.cargar_datos()


@app.route('/')
def home():
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
