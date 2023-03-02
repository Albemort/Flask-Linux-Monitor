from flask import Flask, jsonify, request, render_template
import jwt
from read import readfile
from monitor import Monitor

app = Flask(__name__)
data = readfile()
getdata = Monitor()

# Secret key for JWT
app.config['SECRET_KEY'] = 'secret_key'


users = [
    {
        'id': 1,
        'username': 'john',
        'password': 'password1'
    },
    {
        'id': 2,
        'username': 'jane',
        'password': 'password2'
    }
]


@app.route('/login', methods=['GET'])
def client():
    return render_template('client.html')

@app.route('/dashboard', methods=['GET'])
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
    user = next((user for user in users if user['username'] == username and user['password'] == password), None)

    # If user is not found, return a 401 response
    if not user:
        return jsonify({'message': 'Invalid credentials'}), 401

    # Create a JWT token with the user ID as the payload
    token = jwt.encode({'id': user['id']}, app.config['SECRET_KEY'], algorithm='HS256')

    # Return the JWT token to the client
    return jsonify({'token': token.encode().decode('UTF-8')}), 200


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)