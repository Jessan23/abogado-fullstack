"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Cliente
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

from flask import Flask, request, jsonify, Blueprint
from api.models import db, User
from api.utils import APIException
from flask_cors import CORS

api = Blueprint('api', __name__)

# Permitir solicitudes CORS
CORS(api)

# Obtener todos los usuarios
@api.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        users_data = [user.serialize() for user in users]
        return jsonify(users_data), 200
    except Exception as e:
        return jsonify({"message": "Error al obtener los usuarios", "error": str(e)}), 501


# Crear un nuevo usuario
@api.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()

        # Verificar que los campos requeridos están presentes
        if not data or not data.get("email") or not data.get("password"):
            return jsonify({"message": "Email y contraseña son obligatorios"}), 400

        # Crear el nuevo usuario
        new_user = User(
            email=data["email"],
            password=data["password"],  # *¡IMPORTANTE! Aquí deberías encriptar la contraseña antes de guardarla*
            is_active=data.get("is_active", True)  # Si no se envía, se asume activo por defecto
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "Usuario creado exitosamente", "user": new_user.serialize()}), 201
    except Exception as e:
        return jsonify({"message": "Error al crear el usuario", "error": str(e)}), 501

# Actualizar un usuario
@api.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        user = User.query.get(id)
        if user is None:
            return jsonify({"message": "Usuario no encontrado"}), 404

        data = request.get_json()

        # Actualizar los campos proporcionados
        if "email" in data:
            user.email = data["email"]
        if "password" in data:
            user.password = data["password"]  # *¡IMPORTANTE! Deberías encriptar la nueva contraseña*
        if "is_active" in data:
            user.is_active = data["is_active"]

        db.session.commit()

        return jsonify({"message": "Usuario actualizado exitosamente", "user": user.serialize()}), 200
    except Exception as e:
        return jsonify({"message": "Error al actualizar el usuario", "error": str(e)}), 501

# Eliminar un usuario
@api.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.get(id)
        if user is None:
            return jsonify({"message": "Usuario no encontrado"}), 404

        db.session.delete(user)
        db.session.commit()

        return jsonify({"message": "Usuario eliminado exitosamente"}), 200
    except Exception as e:
        return jsonify({"message": "Error al eliminar el usuario", "error": str(e)}), 501




@api.route('/clientes', methods=['GET'])
def get_clientes():
    try:
        clientes = Cliente.query.all()
        # Serializando la respuesta
        clientes_data = [cliente.serialize() for cliente in clientes]
        return jsonify(clientes_data), 200
    except Exception as e:
        return jsonify({"message": "Error al obtener los clientes", "error": str(e)}), 501

# Ruta para agregar un cliente (Crear)
@api.route('/clientes', methods=['POST'])
def add_cliente():
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
def get_cliente(id):
    try:
        cliente = Cliente.query.get(id)
        if cliente is None:
            return jsonify({"message": "Cliente no encontrado"}), 404  # No encontrado
        return jsonify(cliente.serialize()), 200
    except Exception as e:
        return jsonify({"message": "Error al obtener el cliente", "error": str(e)}), 501

# Ruta para actualizar un cliente (Actualizar)
@api.route('/clientes/<int:id>', methods=['PUT'])
def update_cliente(id):
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
def delete_cliente(id):
    try:
        cliente = Cliente.query.get(id)
        if cliente is None:
            return jsonify({"message": "Cliente no encontrado"}), 404  # No encontrado

        db.session.delete(cliente)
        db.session.commit()

        return jsonify({"message": "Cliente eliminado exitosamente"}), 200

    except Exception as e:
        return jsonify({"message": "Error al eliminar el cliente", "error": str(e)}), 501