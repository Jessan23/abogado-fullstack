import jwt
import datetime
from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
from werkzeug.security import check_password_hash
from api.models import db, User, Cliente
from api.utils import APIException

SECRET_KEY = "tu_secreto_super_seguro"

api = Blueprint('api', __name__)

# Permitir solicitudes CORS
CORS(api)

# Ruta para Login
@api.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        # Verificar que los datos estén presentes
        if not data or not data.get("email") or not data.get("password"):
            return jsonify({"message": "Email y contraseña son requeridos"}), 400

        # Buscar el usuario en la base de datos
        user = User.query.filter_by(email=data["email"]).first()

        if not user or not check_password_hash(user.password, data["password"]):
            return jsonify({"message": "Credenciales inválidas"}), 401

        # Generar el Token JWT
        token = jwt.encode(
            {"user_id": user.id, "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)},
            SECRET_KEY,
            algorithm="HS256"
        )

        return jsonify({"message": "Login exitoso", "token": token}), 200

    except Exception as e:
        return jsonify({"message": "Error al hacer login", "error": str(e)}), 500

# Decorador para verificar el token
def token_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({"message": "Token es requerido"}), 401

        try:
            token = token.split(" ")[1]  # Extract the "Bearer" part
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = User.query.get(data["user_id"])
            if not current_user:
                return jsonify({"message": "Usuario no encontrado"}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token inválido"}), 401

        return f(current_user, *args, **kwargs)

    return decorated

# Obtener todos los usuarios
@api.route('/users', methods=['GET'])
@token_required
def get_users(current_user):
    try:
        users = User.query.all()
        users_data = [user.serialize() for user in users]
        return jsonify(users_data), 200
    except Exception as e:
        return jsonify({"message": "Error al obtener los usuarios", "error": str(e)}), 501

# Crear un nuevo usuario
@api.route('/users', methods=['POST'])
@token_required
def create_user(current_user):
    try:
        data = request.get_json()

        # Verificar que los campos requeridos están presentes
        if not data or not data.get("email") or not data.get("password"):
            return jsonify({"message": "Email y contraseña son obligatorios"}), 400

        # Crear el nuevo usuario
        new_user = User(
            email=data["email"],
            password=data["password"],  # ¡IMPORTANTE! Aquí deberías encriptar la contraseña antes de guardarla
            is_active=data.get("is_active", True)  # Si no se envía, se asume activo por defecto
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "Usuario creado exitosamente", "user": new_user.serialize()}), 201
    except Exception as e:
        return jsonify({"message": "Error al crear el usuario", "error": str(e)}), 501

# Ruta para obtener todos los clientes (Leer)
@api.route('/clientes', methods=['GET'])
@token_required
def get_clientes(current_user):
    try:
        clientes = Cliente.query.all()
        # Serializando la respuesta
        clientes_data = [cliente.serialize() for cliente in clientes]
        return jsonify(clientes_data), 200
    except Exception as e:
        return jsonify({"message": "Error al obtener los clientes", "error": str(e)}), 501

# Ruta para agregar un cliente (Crear)
@api.route('/clientes', methods=['POST'])
@token_required
def add_cliente(current_user):
    try:
        data = request.get_json()

        # Verificar que los datos necesarios estén presentes
        if not data or not data.get("nombre") or not data.get("correo"):
            return jsonify({"message": "Nombre y correo son requeridos"}), 400  # Bad Request

        # Crear una nueva instancia de Cliente con los datos proporcionados
        nuevo_cliente = Cliente(
            nombre=data.get("nombre"),
            correo=data.get("correo"),
            telefono=data.get("telefono", "")
        )

        # Agregar el nuevo cliente a la base de datos
        db.session.add(nuevo_cliente)
        db.session.commit()

        return jsonify({"message": "Cliente creado exitosamente", "cliente": nuevo_cliente.serialize()}), 201

    except Exception as e:
        return jsonify({"message": "Error al agregar el cliente", "error": str(e)}), 501

# Ruta para obtener un cliente por su ID (Leer)
@api.route('/clientes/<int:id>', methods=['GET'])
@token_required
def get_cliente(current_user, id):
    try:
        cliente = Cliente.query.get(id)
        if cliente is None:
            return jsonify({"message": "Cliente no encontrado"}), 404  # No encontrado
        return jsonify(cliente.serialize()), 200
    except Exception as e:
        return jsonify({"message": "Error al obtener el cliente", "error": str(e)}), 501

# Ruta para actualizar un cliente (Actualizar)
@api.route('/clientes/<int:id>', methods=['PUT'])
@token_required
def update_cliente(current_user, id):
    try:
        cliente = Cliente.query.get(id)
        if cliente is None:
            return jsonify({"message": "Cliente no encontrado"}), 404  # No encontrado

        data = request.get_json()

        # Actualizar los campos del cliente
        if data.get("nombre"):
            cliente.nombre = data.get("nombre")
        if data.get("correo"):
            cliente.correo = data.get("correo")
        if data.get("telefono"):
            cliente.telefono = data.get("telefono")

        db.session.commit()

        return jsonify({"message": "Cliente actualizado exitosamente", "cliente": cliente.serialize()}), 200

    except Exception as e:
        return jsonify({"message": "Error al actualizar el cliente", "error": str(e)}), 501

# Ruta para eliminar un cliente (Eliminar)
@api.route('/clientes/<int:id>', methods=['DELETE'])
@token_required
def delete_cliente(current_user, id):
    try:
        cliente = Cliente.query.get(id)
        if cliente is None:
            return jsonify({"message": "Cliente no encontrado"}), 404  # No encontrado

        db.session.delete(cliente)
        db.session.commit()

        return jsonify({"message": "Cliente eliminado exitosamente"}), 200

    except Exception as e:
        return jsonify({"message": "Error al eliminar el cliente", "error": str(e)}), 501
