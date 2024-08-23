from flask import Flask, jsonify, request, abort, Blueprint
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from .models import db, User  # Assuming models.py is in the same directory
from .rate_limiting import limiter  # Assuming you have a rate_limiting module
from .throttling import throttle  # Assuming you have a throttling module

api = Blueprint('api', __name__)

# JWT setup
jwt = JWTManager()

@api.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not all(k in data for k in ('email', 'password', 'name', 'age')):
        abort(400, description="Missing required parameters")
    
    hashed_password = generate_password_hash(data['password'], method='sha256')
    
    new_user = User(
        name=data['name'],
        age=data['age'],
        email=data['email'],
        password_hash=hashed_password
    )
    
    try:
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(409, description="User with this email already exists.")
    
    return jsonify({"message": "User registered successfully"}), 201

@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not all(k in data for k in ('email', 'password')):
        abort(400, description="Missing required parameters")
    
    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password_hash, data['password']):
        abort(401, description="Invalid credentials")
    
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200

@api.route('/user', methods=['GET'])
@jwt_required()
@limiter.limit("5 per minute")  # Rate limiting example
@throttle(max_calls=10, period=60)  # Throttling example
def get_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        abort(404, description="User not found")
    
    return jsonify({
        "id": user.id,
        "name": user.name,
        "age": user.age,
        "email": user.email
    }), 200

@api.route('/health', methods=['GET'])
def health_check():
    # Simple health check route
    return jsonify({"status": "healthy"}), 200

@api.route('/update_profile', methods=['PUT'])
@jwt_required()
def update_profile():
    data = request.get_json()
    user_id = get_jwt_identity()
    
    user = User.query.get(user_id)
    if not user:
        abort(404, description="User not found")
    
    if 'name' in data:
        user.name = data['name']
    if 'age' in data:
        user.age = data['age']
    if 'password' in data:
        user.password_hash = generate_password_hash(data['password'], method='sha256')
    
    db.session.commit()
    return jsonify({"message": "Profile updated successfully"}), 200

# Register the routes with the Flask app
def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)
    
    # Register the Blueprint
    app.register_blueprint(api, url_prefix='/api')

    @app.before_first_request
    def create_tables():
        db.create_all()

    return app
