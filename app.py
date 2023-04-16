from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from read import readfile
from monitor import Monitor

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userdb.db'
db = SQLAlchemy(app)
getdata = Monitor()
#getdata.get_statistics()
data = readfile()

# Secret key for JWT
app.config['SECRET_KEY'] = 'secret_key'

## Class for the users database
class User(db.Model):
    # Create the table and columns.
    __tablename__ = 'login-users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    password = db.Column(db.String(200), primary_key=False, unique=False, nullable=False)

    # Create password for the user
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    # Check the hashed password in the db
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

with app.app_context():
    # Delete any previous users
    try:
        db.session.query(User).delete()
        db.session.commit()
    # Handle if the db doesn't exist
    except:
        db.create_all()
    # Finally create our admin user
    finally:
        user = User(
        name="admin" # Default username
        )

        user.set_password("password") # Default password

        db.session.add(user)
        db.session.commit()

## Route for login page
@app.route('/login', methods=['GET'])
def client():
    return render_template('login.html')

## Route for dashboard page
@app.route('/dashboard', methods=['GET'])
def dash():
    return render_template('dashboard.html')

## Route for index page and redirect to login page
@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('client'))

## Get the content from the json file.
## Calls read.py
@app.route('/result', methods=['GET'])
def result():
    data.__init__()
    return data.measurements

## Get new data from the linux server as a POST request
## Calls monitor.py
@app.route('/result/refresh', methods=['POST'])
def refresh():
    getdata.get_statistics()
    return "OK", 200


# Login route and token
@app.route('/login', methods=['POST'])
def login():
    # Get the username and password from the request
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    # Find the user with the matching credentials
    user = User.query.filter_by(name=username).first()

    # If user is not found or wrong password, return a 401 response
    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid credentials'}), 401

    # Create a JWT token with the user ID as the payload
    token = jwt.encode({'id': user.id}, app.config['SECRET_KEY'], algorithm='HS256')

    # Return the JWT token to the client
    return jsonify({'token': token.encode().decode('UTF-8')}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)