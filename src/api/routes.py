"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, TokenBlocklist
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt

api = Blueprint('api', __name__)
app = Flask(__name__)
bcrypt = Bcrypt(app)

# Allow CORS requests to this API
CORS(api)

# Esto es para el registro


@api.route('/register', methods=['POST'])
def register_user():
    # Tomar el cuerpo de la petición
    body = request.get_json()
    # Creamos el usuario sin clave
    new_user = User(email=body["email"], fullname=body["fullname"])
    # Primero se encripta la clave
    hashed_password = bcrypt.generate_password_hash(
        body["password"]).decode("utf-8")
    # Se agrega la clave encriptada al usuario que se va a crear
    new_user.password = hashed_password
    # Se guarda el nuevo usuario en la base de datos
    db.session.add(new_user)
    db.session.commit()
    # Se responde con los datos del uaurio creado
    return jsonify(new_user.serialize()), 201

# Esto es para el login


@api.route('/login', methods=['POST'])
def login_user():
    # Tomar el cuerpo de la petición
    body = request.get_json()
    # Usar el email del body para buscar el usuario de la base de datos
    user = User.query.filter_by(email=body["email"]).first()
    # Si no se consigue, retornamos un error
    if user is None:
        return jsonify({"msg": "Correo no encontrado"}), 401
    # Si se consigue el usuario, se valida la clave
    is_valid_password = bcrypt.check_password_hash(
        user.password, body["password"])
    # Si la clave no es valida, se retorna un error
    if not is_valid_password:
        return jsonify({"msg": "Clave inválida "}), 401
    # Si la clave es válida, se genera el token, pudiendo agregar campos personalizados en el payload
    payload = {
        "admin": False,
        "permisions": "123123"
    }
    token = create_access_token(identity=str(
        user.id), additional_claims=payload)
    # Retornamos el toekn recién creado
    return jsonify({"token": token}), 200


@api.route('/userinfo', methods=["GET"])
@jwt_required()  # Se agrega el decorador para que la ruta sea protegida por la libreria
def user_info():
    # Como es una ruta que solo se puede acceder con un token válido,
    # Se tiene acceso a las funciones para obtener informaciondl token
    user_id = get_jwt_identity()  # Obtiene el subjet del token (el identity)
    user = User.query.get(user_id)
    payload = get_jwt()  # Obtiene todos los campos del payload del token
    # Retornando la información del token y del usuario
    return jsonify({
        "user": user.serialize(),
        "payload": payload
    })


@api.route('/logout', methods=["POST"])
@jwt_required()
def user_logout():
    # Se obtiene el payload del token
    payload = get_jwt()
    # Se crea un registro de token bloqueado con el jti del token
    token_blocked = TokenBlocklist(jti=payload["jti"])
    # Se guarda en la base de datos
    db.session.add(token_blocked)
    db.session.commit()
    return jsonify({"msg": "User logged out"})


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200
