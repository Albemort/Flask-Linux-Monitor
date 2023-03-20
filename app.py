from flask import Flask, jsonify, request, render_template
import jwt
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from read import readfile
from monitor import Monitor

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userdb.db'
db = SQLAlchemy(app)
data = readfile()
getdata = Monitor()

# Secret key for JWT
app.config['SECRET_KEY'] = 'secret_key'

class User(db.Model):
    __tablename__ = 'login-users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), primary_key=False, unique=False, nullable=False)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    
    def __init__(self, name):
        self.name = name

with app.app_context():
    db.create_all() 

    user = User(
    name="admin"
    )

    user.set_password("password")

    db.session.add(user)
    db.session.commit()

@app.route('/login', methods=['GET'])
def client():
    return render_template('login.html')

@app.route('/dashboard' and '/', methods=['GET'])
def dash():
    return render_template('dashboard.html')

@app.route('/result', methods=['GET'])
def result():
    data.__init__()
    return data.measurements

@app.route('/result/refresh', methods=['POST'])
def refresh():
    getdata.get_statistics()
    return "OK", 200


# Example login route
@app.route('/login', methods=['POST'])
def login():
    # Get the username and password from the request
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    # Find the user with the matching credentials
    user = User.query.filter_by(name=username).first()

    # If user is not found, return a 401 response
    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid credentials'}), 401

    # Create a JWT token with the user ID as the payload
    token = jwt.encode({'id': user.id}, app.config['SECRET_KEY'], algorithm='HS256')

    # Return the JWT token to the client
    return jsonify({'token': token.encode().decode('UTF-8')}), 200


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)